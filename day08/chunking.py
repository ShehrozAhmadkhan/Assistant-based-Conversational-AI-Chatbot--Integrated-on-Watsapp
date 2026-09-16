def word_based_chunking(data,chunk_size,overlap):
    start = 0
    end = chunk_size
    step = chunk_size - overlap
    temp = data.split(" ")
    chunks = []

    while start < len(temp):
        chunk = temp[start:end]
        updated_chunk = " ".join(chunk)
        chunks.append(updated_chunk)

        start += step
        end += step

    return chunks


