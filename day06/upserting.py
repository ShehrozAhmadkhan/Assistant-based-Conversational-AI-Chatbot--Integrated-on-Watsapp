def upserting(index,embeds,chunks,batches = 100):
    optimized_vectors = []

    for i in range(len(embeds)):
        optimized_vectors.append({"id" : f"chunk : {i}",
                                "values" : embeds[i],
                                 "metadata" : {"text" : chunks[i]}})

    for i in range(0,len(optimized_vectors),batches):
        batch = optimized_vectors[i:i+batches]
        index.upsert(vectors = batch)