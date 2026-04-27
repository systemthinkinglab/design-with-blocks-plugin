# File Store

A storage primitive for blobs — images, videos, PDFs, arbitrary bytes.

## Shape
Pentagon. Pink.

## Definition
A File Store holds files. You put a file in, you get a URL or key out. You fetch the file later by that URL or key. The store does not care what is inside (JPEG, MP4, PDF, CSV). It stores bytes.

## Mental model
**Warehouse.** You drop off a box. They tag it with an aisle and shelf number. You come back later with the tag; they fetch your box. They do not know or care what is inside. Boxes go in, boxes come out.

## When to use
- User-uploaded photos, videos, audio, documents
- Generated files (exported reports, transcoded video variants, resized images)
- Static site assets (bundled JavaScript, CSS, images served over a CDN)
- Any binary blob too large or too unstructured for a database

## Common examples
- Instagram: every photo lives in File Store
- Netflix: every video variant (1080p, 720p, 480p) is a file in File Store, served via CDN
- Dropbox: the entire product is a File Store with a UI on top
- Stripe: invoice PDFs, dispute evidence files

## Common junior mistakes
- **Putting blobs into a database.** Databases can hold binary data but they should not. Storage gets expensive, queries get slow, backups balloon. Put the blob in File Store, put the metadata in the database.
- **Not using a CDN for read-heavy content.** A File Store without a CDN in front is slow for global users. Most managed File Stores offer CDN integration; use it.
- **Skipping access control.** File URLs are often guessable or leakable. Use signed URLs with expiration for private content.
- **Not thinking about cost at scale.** Storage is cheap; egress is expensive. Users streaming a lot of video will cost you bandwidth, not storage.

## Common combinations
- Service + File Store — upload and download flow (Service signs the URL, user uploads direct to File Store)
- File Store + Worker — post-upload processing (Worker picks up the file, transcodes, writes results back)
- File Store + Relational Database — File Store holds the blob, Relational Database holds the metadata (owner, upload time, content type)
- File Store + Vector Database — the RAG corpus pattern (File Store holds documents, Vector Database indexes their embeddings)

## Technologies that implement it
- AWS S3, GCP Cloud Storage, Azure Blob Storage, Cloudflare R2, Backblaze B2
- Render Persistent Disks (for simpler apps)
- MinIO (self-hosted S3-compatible)
- Often paired with CloudFront, Cloudflare, Fastly, or Bunny CDN for global delivery

## Related blocks
- Often paired with Relational Database to separate blob from metadata. Often paired with Worker for async processing of uploaded files.
