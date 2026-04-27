# Mental Models

Short analogies that make each block memorable. Use them generously during the decomposition step. A student who remembers "coat check" will remember Key-Value Store a year from now. A student who memorizes a definition will not.

## The 7 building blocks

**Service — Front desk at a hotel.**
You walk up, ask your question, wait, get an answer, leave. The clerk is busy only while serving you. When the line gets long, you hire more clerks. Each clerk handles one guest at a time.

**Worker — Kitchen staff in a restaurant.**
You order. The waiter writes it down. The cook starts working. You are not standing in the kitchen. Your order goes on a queue. Cooks pull from it. If a dish gets burned, they remake it. You eventually get food.

**Key-Value Store — Coat check.**
You give the attendant a coat. They give you a ticket. You come back with the ticket. You get your coat. They do not care what is in it or what color it is. The ticket is the key. The coat is the value.

**File Store — Warehouse.**
You drop off a box. They tag it with an aisle and shelf number. You come back later with the tag. They fetch your box. They do not know or care what is inside. Boxes go in. Boxes come out.

**Queue — Coffee shop line.**
The barista cannot make five drinks at once. You leave your order with the cashier. The order goes on the counter. The barista pulls orders in order. If the barista drops a drink, they remake it. The line smooths out bursts.

**Relational Database — Filing cabinet with an index.**
Drawers are tables. Each folder is a row. Tabs on folders are columns. A master index tells you which folder goes in which drawer and which folders reference each other. You can ask "all invoices from customers in California" and the filing system can answer.

**Vector Database — Smart librarian.**
Ask for books about dogs. They bring you books about pets, animals, veterinary care, even books that do not contain the word "dog." They are matching by meaning, not by keyword. Ask for things like your query; you get similar things.

## The 3 external entities

**User — The guest the hotel exists for.**
Sometimes a human at a browser. Sometimes a human on a phone. In 2026, increasingly an AI agent calling on behalf of a human. The system exists to serve them. They drive everything that happens inside.

**External Service — Specialist vendors you call.**
The hotel does not run its own laundromat. It calls out to the laundry service. Stripe is the laundromat for payments. SendGrid is the laundromat for email. OpenAI is the laundromat for LLMs. You call them. They do the specialist work. They send it back.

**Time — The clock on the wall.**
At 3 AM the housekeeping rounds start. At 9 AM checkout is due. At 11 PM the front desk light dims. Nothing has to call anything; the clock ticks and things happen. Billing runs. Reports generate. Sessions expire. Retries fire.

## Why these analogies matter

Pattern recognition is about seeing the same shape in different places. When a student can say "this is a coat check" about a Redis cache *and* a CDN edge cache *and* a DNS cache, they have internalized the pattern. The tool changes; the pattern does not.

In a design session, use the analogy the moment you introduce a block:

> Your upload flow needs a File Store. That is the warehouse. The photo is the box. Your database stores the tag.

Memorable. Teachable. Hard to confuse with anything else.

## Where these come alive

The analogies above are memorable on the page. They become instinct, not reference, when you have run discovery labs that put each pattern under pressure. [Course I: Universal Building Blocks](https://systemthinkinglab.ai/course-1) builds them into your hands, not just your notes.
