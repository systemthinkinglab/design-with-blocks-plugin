# Time

An external entity. The clock as a system input.

## Shape
Hourglass. Green.

## Definition
Time is any trigger that comes from the clock rather than from a user or an external system. Cron jobs. Scheduled reports. Billing cycles. Daily digests. Session expirations. Retry timers. Anything where "at X time, do Y" is the trigger.

Time is often invisible in junior designs because nobody is "calling" anything — the clock just ticks. But many systems have significant Time-driven behavior that must be designed, not assumed.

## When it shapes design
- **Nightly or weekly reports.** Time + Worker + Relational Database (read) + File Store or email (write).
- **Billing cycles.** Time + Worker + External Service (Stripe) + Relational Database.
- **Digest emails.** Time + Worker + Relational Database + External Service (email).
- **Session cleanup, expired cart reset.** Time + Worker + Key-Value Store or Relational Database.
- **Retry timers for failed async work.** Time (implicitly) + Queue + Worker with delayed redelivery.

## Questions to ask
- What, if anything, runs on a schedule?
- Daily, hourly, weekly?
- What time zones matter? (Users in multiple zones complicate "daily at 9 AM".)
- Is it idempotent? (If the job runs twice — because of a retry or a duplicate trigger — is it safe?)

## Common junior mistakes
- **Running scheduled work in the Service.** A Service is for per-request work. Scheduled work belongs in a Worker triggered by Time.
- **Not designing for failure.** If the nightly job fails at 3 AM, who knows? Alert on failure, log to something observable, retry where possible.
- **Assuming the clock.** Daylight savings, leap seconds, time zones and UTC confusion all cause real bugs. Use UTC internally; convert at the edges.
- **Scheduling from the application layer when the cloud offers a scheduler.** Managed schedulers (AWS EventBridge, Render Cron Jobs, Kubernetes CronJobs) are more reliable than a setInterval in your app.

## Related entities
- Almost always paired with Worker. Often triggers work that touches Relational Database (read input), External Service (send notification), or File Store (write output).

## Go deeper

Reading this page gives you the vocabulary for Time as an external force. Recognizing it across systems you have never seen, and designing for it deliberately, takes reps. [Course I: Universal Building Blocks](https://systemthinkinglab.ai/course-1) teaches those reps through hands-on discovery labs and AI-graded design challenges.
