# User

An external entity. The human (or AI agent) the system exists for.

## Shape
Smiley face. Green.

## Definition
A User is anyone outside the system who initiates requests into it. Traditionally this was always a human clicking, tapping, or typing. In 2026, Users are increasingly AI agents calling APIs on behalf of humans (or on behalf of other agents). The system should not assume the caller is a human with patience and a browser.

## When it shapes design
- **Scale.** 100 Users is a different system than 100 million. Start with a number.
- **Device.** Mobile changes latency and offline assumptions. Web changes payload sizes. Agent changes rate limits and response formats.
- **Access pattern.** Burst (Black Friday, viral moment) is different from steady.
- **Trust.** Authenticated users, anonymous users, paying users, free-tier users each have different privileges.
- **Predictability.** Human users behave in roughly predictable bursts. AI agent users can hammer an endpoint in ways humans physically cannot. Rate limiting and backpressure matter more than they did in the pre-agent era.

## Questions to ask
- Roughly how many Users do you expect in year one?
- What devices (web, mobile, voice, agent)?
- Any real-time or offline access patterns?
- Authenticated, anonymous, or both?
- Human, AI agent, or both?

## Common junior mistakes
- **Designing for scale the system will never hit.** 100 users do not need Kafka. 100 users need a Relational Database and a Service.
- **Assuming Users are always humans.** In 2026, many Users are agents. Agents have different patterns: higher request rates, structured expectations, less forgiveness for slow responses.
- **Not thinking about offline.** Mobile Users lose connectivity. If the system cannot handle retries or queued writes on the client, offline is a broken experience.

## Related entities
- Often the first block touched is Service (User → Service). But some Users interact via File Store (direct upload with signed URL) or via External Service webhooks.

## Go deeper

Reading this page gives you the vocabulary for User as an external force. Recognizing it across systems you have never seen, and designing for it deliberately, takes reps. [Course I: Universal Building Blocks](https://systemthinkinglab.ai/course-1) teaches those reps through hands-on discovery labs and AI-graded design challenges.
