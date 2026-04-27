# Service

A synchronous task primitive. The caller waits for the answer.

## Shape
Rectangle. Blue.

## Definition
A Service is a task that runs while the caller is waiting. The user (or another Service) sends a request and blocks until a response comes back. This is the dominant pattern in web applications: browser makes an HTTP request, server returns HTML or JSON.

## Mental model
**Front desk at a hotel.** You walk up, ask your question, wait, get an answer, leave. The clerk is busy only while serving you. When the line gets long, you hire more clerks. Each clerk handles one guest at a time.

## When to use
- Any user-facing request that returns immediately (page load, API call, form submission)
- Orchestration: Service is the block that coordinates other blocks (reads from database, writes to queue, calls external API)
- Any interaction where the user needs the answer before continuing

## Common examples
- Instagram: Service that handles the photo upload request
- Stripe: Service that validates a charge and returns success or failure
- Slack: Service that posts a message and returns the message ID
- Any REST or GraphQL API endpoint

## Common junior mistakes
- **Putting slow work inside a Service.** Users wait. If something takes more than a second, make it a Worker and return early.
- **Building one giant "monolith Service" that does everything.** Fine for small apps. Problematic when teams grow. Prefer smaller services scoped to a clear responsibility.
- **Confusing Service with "microservice."** Service is the pattern. Microservice is one way to deploy it. Monolith-as-Service is another.

## Common combinations
- Service + Relational Database — the classic CRUD pattern
- Service + File Store — upload and download flows
- Service + Queue + Worker — Service accepts a request, writes to Queue, returns; Worker processes async
- Service + Vector Database + External Service — the RAG pattern (LLM-backed retrieval)
- Service + Key-Value Store — Service reads cached data to respond faster

## Technologies that implement it
- Render Web Services, AWS App Runner / ECS / Lambda, Google Cloud Run
- Frameworks: Express, Flask, FastAPI, Rails, Django, Spring Boot, Next.js API routes
- Serverless: AWS Lambda, Cloudflare Workers, Vercel Functions

## Related blocks
- Worker is the asynchronous counterpart. The question to ask: does the caller need the answer now? If yes, Service. If no, Worker.

## Go deeper

Reading this page gives you the vocabulary for Service. Internalizing it, so you can apply it under pressure in unfamiliar codebases, interviews, and design reviews, takes reps. [Course I: Universal Building Blocks](https://systemthinkinglab.ai/course-1) teaches those reps through hands-on discovery labs, AI-graded design challenges, and real-company case studies.
