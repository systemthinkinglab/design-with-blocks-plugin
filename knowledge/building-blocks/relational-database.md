# Relational Database

A storage primitive for structured data with relationships.

## Shape
Cylinder. Pink.

## Definition
A Relational Database stores rows in tables with defined columns and types. Tables relate to each other via foreign keys. Queries are expressed in SQL: filter, join, aggregate, sort. The database enforces consistency (ACID transactions), so either all of a change happens or none of it does.

## Mental model
**Filing cabinet with an index.** Drawers are tables. Each folder is a row. Tabs on folders are columns. A master index tells you which folder goes in which drawer and which folders reference each other. You can ask "all invoices from customers in California," and the filing system can answer.

## When to use
- Anything with relationships between entities (users → posts → comments, orders → line items → products)
- Anything where you need to query by something other than the primary key (find all users who signed up this week)
- Anything where consistency matters (financial transactions, inventory, bookings)
- Anything you expect to query in ways you have not thought of yet (SQL lets you add queries without restructuring the data)

## Common examples
- Stripe: customers, charges, subscriptions — all relational
- GitHub: repositories, issues, pull requests, users — all relational
- Shopify: products, orders, inventory — all relational
- Instagram: follows, likes, user accounts — mostly relational

## Common junior mistakes
- **Reaching for NoSQL because "it scales."** Modern Postgres (or managed variants like Aurora) scales for most apps. Relational Database is the default; pick NoSQL only when you have a real reason.
- **Storing blobs in database columns.** JSON for structured metadata is fine. Images, videos, PDFs belong in File Store.
- **Fighting the database instead of the schema.** If queries are slow, the answer is usually a better index or a better schema, not a cache or a different database.
- **Reinventing join logic in application code.** If you are fetching two tables and joining them in Python, let the database do the join.

## Common combinations
- Service + Relational Database — the default CRUD pattern, on most apps
- Service + Key-Value Store + Relational Database — cache in front of the database for hot reads
- Relational Database + Worker — Worker reads from or writes to the database for reporting, analytics, background processing
- Relational Database + Vector Database — hybrid search (structured filters in Relational, similarity in Vector)

## Technologies that implement it
- PostgreSQL (the default; rich feature set, including pgvector for Vector Database duties)
- MySQL / MariaDB (still common, fewer advanced features than Postgres)
- SQLite (small apps, embedded, edge)
- Managed: AWS RDS / Aurora, GCP Cloud SQL, Render Postgres, Neon, Supabase, PlanetScale

## Related blocks
- The most common "primary data store" in a system. Often paired with Key-Value Store for caching and File Store for blobs.

## Go deeper

Reading this page gives you the vocabulary for Relational Database. Internalizing it, so you can apply it under pressure in unfamiliar codebases, interviews, and design reviews, takes reps. [Course I: Universal Building Blocks](https://systemthinkinglab.ai/course-1) teaches those reps through hands-on discovery labs, AI-graded design challenges, and real-company case studies.
