Day 6: Integrate real university catalog data into ask-uni index

- Created new Pinecone index (ask-uni) for university data
- Refactored code into modular files (load_data, chunking, embeddings, upserting, history)
- Loaded, chunked, embedded, and upserted university catalog (200 vectors)
- Fixed bug: upsert() parameter name (vector -> vectors)
- Fixed bug: reformulated query wasn't being embedded before Pinecone query