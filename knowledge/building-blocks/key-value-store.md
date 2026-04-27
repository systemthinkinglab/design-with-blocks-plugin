# Key-Value Store

A storage primitive for fast lookup by a single key.

## Shape
Diamond. Pink.

## Definition
A Key-Value Store maps a key (a string or bytes) to a value (anything) with O(1) lookup. No queries by the value, no joins, no aggregations. You give it a key, you get the value back, very fast, very simple.

## Mental model
**Coat check.** You give the attendant a coat, they give you a ticket. You come back with the ticket, you get your coat. They do not care what is in your coat or what color it is. The ticket is the key. The coat is the value.

## When to use
- Cache in front of a slower store (database, external API)
- Session storage (session ID → user state)
- Rate limiting (user ID → request count)
- Feature flags (flag name → on/off)
- Any access pattern that is exactly "give me the thing associated with this one key"

## Common examples
- Instagram: caches the user's feed (user_id → feed bytes) so database does not get hit on every scroll
- Stripe: session tokens (token → customer_id)
- Any web app: login sessions (session_id → user_id)

## Common junior mistakes
- **Using it as a primary store.** Key-Value Stores are often in-memory and not durable by default. Treat it as a cache that can disappear.
- **Trying to query by value.** If you need to find "all keys where value is X," you want a Relational Database or a search index, not a Key-Value Store.
- **Caching without an invalidation plan.** If you cannot tell me when this value will change and how the cache will know, you do not need a cache. You need a plan.
- **Overusing it as a Queue or a Database.** Redis can do all three, but mixing patterns in one tool is the replacement trap. Separate the patterns.

## Common combinations
- Service + Key-Value Store + Relational Database — Service checks cache first, falls back to database on miss
- Service + Key-Value Store (session) — Service reads the session at the start of every request
- Worker + Key-Value Store — Worker updates cache after changing the underlying data

## Technologies that implement it
- Redis (the default), Memcached (simpler, lighter), DynamoDB (managed, durable, at scale), etcd (distributed configuration)
- Render Redis, AWS ElastiCache, GCP Memorystore

## Related blocks
- Often sits in front of Relational Database or File Store as a cache. Not a replacement for either.
