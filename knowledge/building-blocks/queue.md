# Queue

A storage primitive for decoupling producers from consumers.

## Shape
Stacked rectangles. Pink.

## Definition
A Queue is a durable pipe. Producers write messages to it; consumers (Workers) read messages from it. The Queue holds messages until they are processed. If a consumer is slow or down, messages wait. If the consumer fails, the message can be retried.

## Mental model
**Coffee shop line.** The barista cannot make five drinks at once. You leave your order with the cashier. The order goes on the counter. The barista pulls orders in order. If the barista drops a drink, they remake it. The line smooths out bursts.

## When to use
- Async work: producer does not need to wait for consumer
- Rate limiting: consumer can only handle N jobs per second, Queue buffers the excess
- Decoupling services: producer and consumer can be deployed, scaled, and failed independently
- Retry logic: message stays in Queue until acknowledged; failed processing means the message returns for retry
- Fan-out: one message, multiple consumers (pub/sub pattern)

## Common examples
- Instagram: upload arrives → message on Queue → Worker generates thumbnails
- Stripe: charge succeeds → message on Queue → Workers send receipt email, update analytics, notify webhooks
- Slack: message posted → Queue → Workers deliver to each recipient, index for search, run moderation

## Common junior mistakes
- **Using a Queue when a direct Service call would work.** If the caller can wait and the work is fast, you do not need a Queue. Do not over-engineer.
- **No dead letter queue.** Messages that fail repeatedly should go to a dead letter queue for inspection, not loop forever.
- **Out-of-order assumptions.** Most Queues do not guarantee order across partitions. If ordering matters, use a Queue that guarantees it (Kafka with partition key, SQS FIFO).
- **Expecting exactly-once delivery.** Most Queues deliver at-least-once. Design consumers to be idempotent: processing the same message twice should be safe.
- **Using Redis for both caching and queuing.** The replacement trap. Redis can do both, but you end up with a tool that changes for reasons unrelated to the pattern you care about. Separate the tools.

## Common combinations
- Queue + Worker — the canonical async pattern. Almost every Queue is paired with a Worker.
- Service + Queue + Worker — Service accepts request, writes to Queue, returns; Worker processes async and notifies if needed
- Queue + Worker + External Service — async third-party API calls with retry (email, SMS, push notifications)
- File Store + Queue + Worker — file uploaded triggers Queue message, Worker processes the file

## Technologies that implement it
- SQS, Amazon MQ, GCP Pub/Sub, Azure Service Bus (managed)
- RabbitMQ, Kafka, NATS, Redpanda (self-hosted)
- Redis (with rq, Celery, Sidekiq — simple cases only; watch the replacement trap)
- Cloudflare Queues, Render Redis (for small scale)

## Related blocks
- Almost always paired with Worker. Often triggered by Service or File Store events.

## Go deeper

Reading this page gives you the vocabulary for Queue. Internalizing it, so you can apply it under pressure in unfamiliar codebases, interviews, and design reviews, takes reps. [Course I: Universal Building Blocks](https://systemthinkinglab.ai/course-1) teaches those reps through hands-on discovery labs, AI-graded design challenges, and real-company case studies.
