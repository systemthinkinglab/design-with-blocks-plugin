# Vector Database

A storage primitive for similarity search via high-dimensional embeddings.

## Shape
Cube. Pink.

## Definition
A Vector Database stores vectors (numeric arrays representing embeddings of text, images, audio, or other data) and answers the question "which stored items are most similar to this query?" by computing distance in vector space. Typical distance metrics: cosine, dot product, Euclidean.

The vectors are produced by an embedding model: a separate system that turns text or images into numbers, where semantically similar inputs produce numerically similar vectors.

## Mental model
**Smart librarian.** Ask for books about dogs and they bring you books about pets, animals, veterinary care, even books that do not contain the word "dog." They are matching by meaning, not by keyword. A Vector Database does the same thing: it finds things that are *like* your query, not things that exactly match it.

## When to use
- Semantic search (users type concepts; you want results by meaning)
- Retrieval-Augmented Generation (RAG): find docs similar to a user's question, feed them to an LLM for an answer
- Recommendations based on similarity (products, videos, articles)
- Clustering and deduplication (find near-duplicates)

## Common examples
- ChatGPT "chat with your docs": embed docs into a Vector Database, fetch relevant ones per query, send to LLM
- Spotify, YouTube: part of the recommendation stack at some layer
- E-commerce: "show me products similar to this one"
- Support search: find past tickets similar to the current one

## Common junior mistakes
- **Using Vector Database for exact matches.** Similarity is for *approximate* "like this" queries. If you want exact keywords, dates, or IDs, use Relational Database with an index.
- **Replacing your Relational Database.** Vector Database is narrow-purpose. Most product data still needs structured storage and joins. Use both.
- **Skipping the embedding step.** A Vector Database is only useful with good embeddings. Bad embeddings → bad retrieval. The embedding model is part of the design.
- **Ignoring metadata filtering.** "Find similar items owned by this user" needs metadata filtering plus vector similarity. Not all Vector Databases support this well.
- **Assuming embeddings are stable.** If you change the embedding model, all stored vectors are in a different space. You must re-embed.

## Common combinations
- Service + Vector Database + External Service — the RAG pattern: Service receives query, Vector Database finds similar docs, External Service (LLM) writes the answer
- File Store + Worker + Vector Database — async ingestion: file lands in File Store, Worker embeds it, writes to Vector Database
- Relational Database + Vector Database — hybrid search: Relational for structured filters, Vector for similarity, results joined in Service
- Queue + Worker + Vector Database — async embedding pipeline for large corpora

## Technologies that implement it
- **Dedicated:** Pinecone, Weaviate, Qdrant, Chroma, Milvus
- **Postgres extension:** pgvector (often the simplest if you already have Postgres)
- **Cloud-managed:** AWS OpenSearch kNN, GCP Vertex AI Vector Search
- **Embedded:** Chroma (in-process), LanceDB, FAISS (library)

## Related blocks
- Almost always paired with External Service (embedding model API) and often with File Store (the source corpus) and Relational Database (metadata).
