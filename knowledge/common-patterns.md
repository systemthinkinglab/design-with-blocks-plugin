# Common Patterns

Combinations of blocks that show up repeatedly across real systems. Use these to jump-start decomposition when a feature matches a known pattern.

## CRUD (Create, Read, Update, Delete)
**Service + Relational Database**

The default web-app pattern. Service accepts requests. Relational Database stores the entities and their relationships. Covers 60 to 80 percent of most apps.

*Common on:* GitHub issues, Stripe customers, any admin dashboard, any B2B SaaS.

## Cached CRUD
**Service + Key-Value Store + Relational Database**

Hot reads are faster if you cache them. Service checks the Key-Value Store first. On miss, reads from Relational Database and writes the result back to the cache. Invalidate on write.

*Common on:* Instagram feeds, Twitter timelines, any read-heavy product with a database.

## Upload and process
**Service + File Store + Queue + Worker**

User uploads a file. Service signs a URL, user uploads directly to File Store, Service writes a Queue message, Worker processes the file (transcode, resize, OCR, index), writes results back.

*Common on:* Instagram photo uploads (thumbnails), YouTube video uploads (transcoding), Dropbox file processing.

## Send something slow
**Service + Queue + Worker + External Service**

User does something that requires a third-party call that might be slow or unreliable (send email, send SMS, ping webhook, call LLM). Service writes to Queue and returns fast. Worker pulls from Queue and calls External Service with retry.

*Common on:* password reset emails, purchase confirmations, any webhook firing.

## Retrieval-Augmented Generation (RAG)
**Service + Vector Database + External Service (LLM) + File Store**

User asks a question. Service embeds the question. Vector Database returns similar documents. Service sends those documents plus the question to the LLM (External Service). LLM composes the answer. The underlying documents live in File Store; their embeddings live in Vector Database.

Often paired with a Worker-based ingestion pipeline: new documents arrive, Worker embeds them and writes to Vector Database.

*Common on:* ChatGPT-over-your-docs, Notion AI, Perplexity, any "chat with your data" product.

## Scheduled work
**Time + Worker**

At a scheduled time, a Worker runs and does something: generate a report, send a digest, clean up expired sessions, reconcile billing. No user is involved. The clock is the trigger.

*Common on:* nightly analytics, weekly digest emails, monthly billing, session cleanup.

## Real-time updates
**Service + Queue + Worker (fan-out)**

An event happens (new message, price change, live sports update). Service publishes to Queue. One or more Workers pull and fan out to interested users via WebSockets, push notifications, or email.

*Common on:* Slack messages, Discord channels, stock tickers, ride-hailing updates.

## Hybrid search
**Service + Relational Database + Vector Database**

User searches with both structured filters (price range, category, date) and a natural-language phrase. Service queries Relational Database for the filter part and Vector Database for the similarity part, then joins the results in memory.

*Common on:* e-commerce search, support ticket search, document search.

## Data Layer Service
**Service (dedicated) + Relational Database (or External Service)**

A Service whose only job is to mediate access to a single data source, usually a database or an external vendor. The rest of the application does not talk to the underlying store directly. It goes through the Data Layer Service.

Why: business rules, access control, retry logic, and schema evolution all live in one place. Other services become simpler because they stop worrying about the storage layer's quirks.

*Common on:* large companies with multiple apps sharing a database. Also the pattern when wrapping an external API (payments, shipping) so the rest of the system sees a clean internal interface.

## Composition is the point

Most real systems are 3 to 5 of these patterns glued together. Instagram is Upload-and-process plus Cached CRUD plus Real-time updates plus RAG (for "find similar" features). Stripe is CRUD plus Send-something-slow plus Scheduled work (billing).

The patterns above are not exhaustive. They are enough to recognize about 80 percent of what shows up in practice. When you have internalized them, new systems stop feeling new.
