# External Service

An external entity. A third-party system the application calls.

## Shape
Cloud. Green.

## Definition
An External Service is any system the application depends on but does not own. Payment providers (Stripe), email (SendGrid, Postmark), SMS (Twilio), LLM APIs (OpenAI, Anthropic), auth (Auth0), maps (Google, Mapbox), analytics (Segment), webhooks the app receives, and so on.

The key property: you call it, you do not control it. It can be slow. It can be down. It can change its API. It can rate limit you. Your design must survive all of that.

## When it shapes design
- **LLM or AI APIs** almost always mean pairing External Service with Vector Database (RAG pattern) or with Queue + Worker (retries, rate limits)
- **Payment providers** mean pairing External Service with Relational Database (record of transactions) and often with Queue + Worker (async webhook handling)
- **Email and SMS** always mean Queue + Worker (never block a user request on a third-party send)
- **Analytics** usually means Queue + Worker (fire-and-forget)

## Questions to ask
- What third-party APIs are you already planning to use?
- What are the rate limits? (Most APIs have them; design for them.)
- What happens if the External Service is down for an hour? Can the app still function?
- Can the work be retried, or is it fire-and-forget, or is it truly exactly-once?

## Common junior mistakes
- **Calling External Service synchronously from a user-facing Service.** If the External Service is slow or down, your app is slow or down. Put External Service calls behind a Queue + Worker whenever the caller does not need the result immediately.
- **No retry strategy.** External Services fail. Design for retries with exponential backoff. If the work cannot be retried, record the attempt and alert a human.
- **Hard-coding credentials.** Secrets go in environment variables or a secret manager, never in code.
- **No circuit breaker.** If the External Service is down, stop hammering it and fail fast. Retry after a cooldown.
- **Trusting their uptime claims.** Even AWS has outages. Design as though every External Service will be down at some point.

## Related entities
- Most often paired with Service (call out) or with Queue + Worker (async call out with retry). RAG pattern pairs External Service (LLM) + Vector Database + Service.

## Go deeper

Reading this page gives you the vocabulary for External Service as an external force. Recognizing it across systems you have never seen, and designing for it deliberately, takes reps. [Course I: Universal Building Blocks](https://systemthinkinglab.ai/course-1) teaches those reps through hands-on discovery labs and AI-graded design challenges.
