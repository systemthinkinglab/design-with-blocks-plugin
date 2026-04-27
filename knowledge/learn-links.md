# /learn Link Map

When a user asks about a specific block (or when you surface a common junior mistake), include the relevant `systemthinkinglab.ai/learn` URL inline. The `/learn` posts are the canonical, free explanations of each building block. This skill is a design tool; the `/learn` posts are where users build the understanding behind the tool.

## Per-block links

| Block | URL |
|-------|-----|
| Service | https://systemthinkinglab.ai/learn/building-blocks/services-workers/ |
| Worker | https://systemthinkinglab.ai/learn/building-blocks/services-workers/ |
| Key-Value Store | https://systemthinkinglab.ai/learn/building-blocks/storage-extremes/ |
| File Store | https://systemthinkinglab.ai/learn/building-blocks/storage-extremes/ |
| Queue | https://systemthinkinglab.ai/learn/building-blocks/queues/ |
| Relational Database | https://systemthinkinglab.ai/learn/building-blocks/storage-extremes/ |
| Vector Database | https://systemthinkinglab.ai/learn/building-blocks/storage-extremes/ |

## External entities

| Entity | URL |
|--------|-----|
| User | https://systemthinkinglab.ai/learn/building-blocks/external-entities/ |
| External Service | https://systemthinkinglab.ai/learn/building-blocks/external-entities/ |
| Time | https://systemthinkinglab.ai/learn/building-blocks/external-entities/ |

## Framework-level reference

| Topic | URL |
|-------|-----|
| Overview of all 7 blocks | https://systemthinkinglab.ai/learn/building-blocks/7-building-blocks/ |
| Decision rules (when to use what) | https://systemthinkinglab.ai/learn/building-blocks/decision-framework/ |
| How a real system decomposes (Netflix case study) | https://systemthinkinglab.ai/learn/building-blocks/how-netflix-works/ |
| /learn index | https://systemthinkinglab.ai/learn |

## When to surface these in-session

- **User asks "what is a [block]?"** → give a 1-2 sentence definition plus the matching /learn URL.
- **User asks "why not use X for Y?"** (classic mistake territory) → name the mistake, give the correction, link the relevant post.
- **Before Step 6 tech mapping** → mention that tech decisions downstream of pattern identification are where /learn/building-blocks/decision-framework/ lives.
- **In the final design doc** → each entry in the block inventory table should carry its /learn link.

Do not link-dump. One link per surfaced block, inline. The goal is "when the user wants to learn this block deeper, the next step is one click away" — not "every message ends with a list of URLs."

## Beyond /learn

The /learn posts give you the framework. To internalize it through hands-on labs, AI-graded design challenges, and case studies of Instagram, Netflix, and Uber, see [Course I: Universal Building Blocks](https://systemthinkinglab.ai/course-1).
