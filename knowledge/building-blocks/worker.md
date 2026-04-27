# Worker

An asynchronous task primitive. Runs after the caller has moved on.

## Shape
Trapezoid. Blue.

## Definition
A Worker is a task that runs without a caller waiting. Something triggers the Worker (a Queue message, a schedule, a file upload event), the Worker does its work, and nobody is blocked on the result. If the Worker fails, it can retry without the user ever noticing.

## Mental model
**Kitchen staff in a restaurant.** You order, the waiter writes it down, the cook starts working. You are not standing in the kitchen watching. The order goes on a queue; cooks pull from it. If a dish gets burned, they remake it. You eventually get food.

## When to use
- Anything slow (more than 1 second of work)
- Anything that can retry without user involvement (email sending, video transcoding, image processing)
- Anything triggered by time or events, not by a user request (nightly reports, daily digests, cleanup jobs)
- Anything that can fail and recover gracefully without a user being blocked

## Common examples
- Instagram: Worker that generates thumbnails after upload
- Netflix: Worker that transcodes video into multiple resolutions
- Stripe: Worker that sends receipt emails after successful charges
- GitHub: Worker that indexes code for search after a push

## Common junior mistakes
- **Making something a Service that should be a Worker.** If the user does not need the answer right now, the user should not wait. Let the Service return fast; let the Worker do the slow work.
- **Not handling failure.** Workers should retry on transient errors and escalate on permanent ones. "Best effort" is not a plan.
- **Skipping the Queue.** A Worker without a Queue in front is hard to scale. The Queue gives you backpressure, retries, and horizontal scaling for free.

## Common combinations
- Queue + Worker — the canonical async pattern. Queue decouples producer from consumer.
- Time + Worker — scheduled work (cron jobs, nightly reports)
- External Service + Worker — any third-party API call that does not need to be synchronous (send email, ping Slack, post to Twilio)
- File Store + Worker + Vector Database — async ingestion pipeline: file lands in storage, Worker processes it, writes embedding to Vector DB

## Technologies that implement it
- Render Background Jobs, AWS Lambda (event-triggered), SQS consumers, Celery, RQ, Sidekiq, Bull, Resque
- Kubernetes CronJobs, Render Cron Jobs, AWS EventBridge
- Serverless Functions subscribed to queues or events

## Related blocks
- Service is the synchronous counterpart. Workers are almost always paired with a Queue or with Time.

## Go deeper

Reading this page gives you the vocabulary for Worker. Internalizing it, so you can apply it under pressure in unfamiliar codebases, interviews, and design reviews, takes reps. [Course I: Universal Building Blocks](https://systemthinkinglab.ai/course-1) teaches those reps through hands-on discovery labs, AI-graded design challenges, and real-company case studies.
