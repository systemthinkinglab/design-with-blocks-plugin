# Technology Defaults

For each block, a default technology and the main alternatives. Defaults lead with **open source and widely used** options (PostgreSQL, Redis, S3). Managed platforms (AWS, GCP, Fly, Railway, Render, Supabase) are mentioned as convenience layers *on top* of the same primitives, not as the primitives themselves.

Why this ordering matters. The framework is pattern-first. A Service is not "a Render web service" or "an AWS Lambda"; it is a synchronous task primitive that can be implemented by any HTTP server. Anchoring on the underlying primitive first is what lets you swap the vendor without rethinking the architecture.

## A note on containers, VMs, and orchestration

**Docker, Kubernetes, and VMs are not building blocks.** They are packaging and deployment layers. Any of the 7 building blocks can be delivered as a container, a VM image, or a bare process. Saying "I use Docker for my Service" is like saying "I use a spoon for my soup." True, but it does not tell you what primitive you are implementing.

A Docker container running Express is a **Service**.
A Docker container running a BullMQ consumer is a **Worker**.
A Docker container running Postgres is a **Relational Database**.
A Docker container running Redis can be a **Key-Value Store**, a **Queue**, or both (watch the replacement trap).
A Docker container running MinIO is a **File Store**.

The image determines the block. The container is the wrapper. When this file mentions Docker or Kubernetes, treat them as how-to-ship, not what-to-build.

## Task primitives

### Service

**What it actually is:** an HTTP server (or RPC server) that accepts requests and returns responses. Any language, any framework, any runtime.

**Default:** an HTTP framework in the language your team knows, running as a long-lived process. Packaging (container, VM image, bare process) and deployment target (VM, container orchestrator, managed platform, serverless) are orthogonal choices on top of this primitive.

| Language | Popular framework |
|----------|-------------------|
| Python | FastAPI, Flask, Django |
| JavaScript / TypeScript | Express, Fastify, Next.js API routes, Hono |
| Ruby | Rails, Sinatra |
| Go | net/http, Gin, Echo, Chi |
| Java / Kotlin | Spring Boot, Ktor |
| Rust | Axum, Actix |

**Where to run it:**

- **Self-managed:** a VM (EC2, DigitalOcean Droplet, Hetzner) running Docker or systemd
- **Orchestrated:** Kubernetes (EKS, GKE, self-hosted)
- **Managed container:** AWS ECS / Fargate, Google Cloud Run, AWS App Runner
- **Managed platform (convenience layers):** Fly.io, Railway, Render, Heroku, Vercel (for JS-heavy apps)
- **Serverless functions:** AWS Lambda, Cloudflare Workers, Vercel Functions (when workload is spiky)

**Rule of thumb:** if your team already knows a deployment pattern, use it. The pattern (Service) does not change; the platform is a taste choice.

### Worker

**What it actually is:** a long-running or event-triggered process that pulls work off a queue or schedule and does it. Same runtimes as Service; different lifecycle.

**Default:** a process running a Worker library in your team's language, consuming from a Queue. Same packaging and deployment targets as Service.

**Popular worker libraries:**

| Language | Libraries |
|----------|-----------|
| Python | Celery, RQ, Dramatiq |
| JavaScript / TypeScript | BullMQ, graphile-worker, Bree |
| Ruby | Sidekiq, Resque, GoodJob |
| Go | asynq, River |
| Elixir | Oban |
| Java / Kotlin | Spring Batch, Quartz |

**Where to run it:**

- Same options as Service. Typically you run Worker processes alongside Service processes in the same cluster.
- Serverless-triggered Workers: AWS Lambda behind SQS / SNS / EventBridge; Google Cloud Functions on Pub/Sub.

## Storage primitives

### Key-Value Store

**What it actually is:** fast lookup by one key. In-memory by default, sometimes persisted.

| Option | When |
|--------|------|
| **Redis** *(default — open source, ubiquitous)* | Most common. Supports persistence, TTLs, pub/sub. |
| Memcached | Lighter. Ephemeral-only. Fine when a cache can disappear without consequence. |
| DynamoDB | Managed, durable, scales horizontally. Read the pricing model first. |
| Cloudflare Workers KV | Edge-replicated. Best for globally-distributed reads. |
| etcd | Distributed configuration, service discovery. Not an application cache. |

**Managed Redis (convenience layers):** AWS ElastiCache, GCP Memorystore, Upstash, Redis Cloud, Render Redis. All run the same Redis you could install yourself.

### File Store

**What it actually is:** object storage for blobs. Put a file in, get a URL or key back, fetch later by key.

| Option | When |
|--------|------|
| **S3** *(default — the industry standard; every tool integrates with the S3 API)* | AWS S3 is the reference implementation. |
| S3-compatible, self-hosted | MinIO, Ceph. When you need to own your bytes or run on-prem. |
| S3-compatible, managed | Cloudflare R2 (no egress fees), Backblaze B2, Wasabi, DigitalOcean Spaces. |
| Cloud-native alternatives | GCP Cloud Storage, Azure Blob Storage. Same pattern, different API. |

**Almost always pair with a CDN for read-heavy content:** CloudFront, Cloudflare, Fastly, Bunny CDN.

### Queue

**What it actually is:** a durable pipe between producer and consumer. Producer writes, consumer reads, messages retry on failure.

| Option | When |
|--------|------|
| **RabbitMQ** *(default for classic messaging — open source, mature)* | Rich routing, widely deployed, easy to reason about. |
| **SQS** *(default for AWS shops — managed, simple)* | Zero-ops. Pair with Lambda for serverless Workers. |
| Kafka (or Redpanda) | Event sourcing, high throughput, durable log. Operationally heavier. |
| NATS | Lightweight pub/sub, cloud-native. |
| Postgres-based queues: `graphile-worker`, `pg-boss`, Oban, River | Small-to-medium scale. Uses your existing Relational Database. Transactional enqueue for free. |
| Redis-based queues: BullMQ, RQ, Sidekiq, Celery-on-Redis | Convenient if Redis is already in the stack. **Watch the replacement trap:** do not overload one Redis instance to serve both Key-Value Store and Queue; separate the patterns. |

**Managed flavors:** AWS SQS, GCP Pub/Sub, Azure Service Bus, CloudAMQP (managed RabbitMQ).

### Relational Database

**What it actually is:** structured tables, rows, columns, foreign keys, SQL. ACID transactions.

| Option | When |
|--------|------|
| **PostgreSQL** *(default — the right answer almost always)* | Rich feature set. Handles Vector Database duties via `pgvector`. Open source. |
| MySQL / MariaDB | Legacy or team familiarity. |
| SQLite | Single-node, embedded, or edge. |

**Managed Postgres (convenience layers):** AWS RDS / Aurora, GCP Cloud SQL, Azure Database for Postgres, Supabase, Neon, Crunchy Bridge, Render Postgres, Heroku Postgres. All run the same Postgres you could install yourself.

**Rule of thumb:** use managed unless you have a specific operational reason to self-host.

### Vector Database

**What it actually is:** similarity search over high-dimensional embeddings. Ask "find the N stored items most like this query."

| Option | When |
|--------|------|
| **pgvector on Postgres** *(default — simplest, one fewer system to run)* | Handles up to millions of vectors comfortably. Uses your existing Relational Database. |
| **Qdrant** *(default for dedicated vector needs — open source, Rust)* | Fast, self-hostable, actively maintained. |
| Weaviate | Open source, feature-rich (filtering, hybrid search, built-in vectorizers). |
| Milvus | Open source, handles very large corpora. Operationally heavier. |
| Chroma | Open source, embedded or server mode. Popular for RAG prototypes. |
| Pinecone | Managed, purpose-built, widely used. |
| FAISS, LanceDB | Library-level, embedded, or edge. |
| Cloud-managed: AWS OpenSearch kNN, GCP Vertex AI Vector Search | If you are already on that cloud. |

The embedding model is a separate decision. Open source: sentence-transformers, BGE, nomic-embed. Proprietary APIs: OpenAI, Voyage, Cohere.

## External entities

### User
Not a technology choice; the audience. Web, mobile native, PWA, voice, or AI agent.

### External Service
Pick by category. Open-source-first options where they exist; managed where they do not.

| Category | Managed defaults | Self-host alternatives |
|----------|-----------------|-----------------------|
| Payments | Stripe, Adyen, Paddle | *(few viable self-host options at scale)* |
| Email | Postmark, SendGrid, Resend, AWS SES | Postal, Listmonk |
| SMS / voice | Twilio, Plivo | FreeSWITCH, Asterisk |
| Auth | Auth0, Clerk, WorkOS | Keycloak, Ory, Authentik, Supabase Auth |
| LLM APIs | OpenAI, Anthropic | Ollama, vLLM, Text Generation Inference |
| Analytics | Segment, Mixpanel, PostHog (cloud) | PostHog (self-hosted), Plausible, Umami |
| Search | Algolia, Elastic Cloud | Meilisearch, Typesense, Elasticsearch / OpenSearch |
| Observability | Datadog, New Relic | Prometheus + Grafana, OpenTelemetry collectors |

### Time
- **Default:** a managed scheduler. Kubernetes CronJobs, AWS EventBridge, GCP Cloud Scheduler, Render Cron Jobs, Fly Machines schedules.
- Avoid `setInterval` in the Service process. Cron-in-the-app loses reliability on restart.

## The point of this list

Every row is an implementation of a pattern. The pattern is the durable thing. Tools come and go. When you see a new vector database on Hacker News next year, you will not need to rethink the architecture. You will ask: does this implement the Vector Database pattern better than pgvector or Qdrant? If yes, swap it in. If no, move on.

Defaults are there to get you started, not to constrain you. A framework that tells you "always use X vendor" is the opposite of pattern-first thinking; it is vendor-first thinking wearing a pattern costume. This file leads with primitives (Postgres, Redis, S3, Docker) and names managed flavors as convenience layers, because that is the teaching the framework actually makes.
