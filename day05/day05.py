from dotenv import load_dotenv
from openai import OpenAI
from pinecone import Pinecone
import os
import PyPDF2

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
index = pc.Index("watsapp-bot-learning")

"""

def load_data(file_path):
    file = open(file_path,"rb")
    book = PyPDF2.PdfReader(file)
    pdfinstring = ""
    for page in book.pages:
        text = page.extract_text()
        if text:
            pdfinstring += text
    return pdfinstring

data = load_data("Company-Rules.pdf")
print("done")

def word_based_chunking(chunk_size,overlap,data):
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

chunks = word_based_chunking(100,20,data)
print("done")

def batch_based_embeddings(chunks,batches = 100):
    all_embeddings = []
    for i in range(0,len(chunks),batches):
        batch = chunks[i:i+batches]
        response = client.embeddings.create(model="text-embedding-3-small",input=batch,dimensions=1024)

        for i in response.data:
            all_embeddings.append(i.embedding)
    return all_embeddings

embeds = batch_based_embeddings(chunks)
print("done")

optimized_vectors = []
for i in range(len(embeds)):
    optimized_vectors.append({"id" : f"chunk {i}",
                              "values" : embeds[i],
                              "metadata" : {"text" : chunks[i]}})

def batch_based_upserting(index,optimized_vectors,batches =100):
    for i in range(0,len(optimized_vectors),batches):
        batch = optimized_vectors[i:i+batches]
        index.upsert(vectors = batch)

vd = batch_based_upserting(index,optimized_vectors)
print("done")

"""

history = []
entries = 5

def save_entry(history,user_question,assistant_answer):
        history.append({"role":"user","content":user_question})
        history.append({"role":"assistant","content":assistant_answer})

        chat = entries*2
        if len(history) > chat:
            history = history[-chat:]
        return history

while True:
    
    user_question = input("I am your Helping Assistant! How can i help?  or (exit) to quit: ")
    if user_question.lower() == "exit":
         break
    else:
        user_question_embed = client.embeddings.create(model="text-embedding-3-small",input=user_question,dimensions=1024)
        user_question_vector = user_question_embed.data[0].embedding

        if len(history) == 0:

            db_query = index.query(vector=user_question_vector,top_k=2,include_metadata=True)

            if (len(db_query.matches) == 0) or (db_query.matches[0].score <= 0.3):
                answer = "This question is out of my domain!"
                print(answer)

            else:
                relevant_chunks = []
                for i in db_query.matches:
                    relevant_chunks.append(i.metadata["text"])
                relevant_chunks = "\n".join(relevant_chunks)

                prompt = f""" you are a helpfull assistant. I will share you user question and relevant chunks, just generate answer, nothing more.
                user question : {user_question}
                relevant chunks : {relevant_chunks}
                """

                llm = client.chat.completions.create(model="gpt-4o-mini",messages=[{"role":"user","content":prompt}])
                answer = llm.choices[0].message.content
                history = save_entry(history,user_question,answer)
                print(answer)

        elif (len(history) != 0):
            prompt = f"""You are an helpfull assistant. Create an reformulated query by using user question and history! and just give me reformulated query.
            user question : {user_question}
            history : {history}
            """
            llm = client.chat.completions.create(model="gpt-4o-mini",messages=[{"role":"user","content":prompt}])
            reformulated_query = llm.choices[0].message.content
            response = client.embeddings.create(model="text-embedding-3-small",input=reformulated_query,dimensions=1024)
            reformulated_query_vector = response.data[0].embedding

            relevant_chunks = index.query(vector = reformulated_query_vector,top_k=2,include_metadata=True)

            if (len(relevant_chunks.matches) == 0) or (relevant_chunks.matches[0].score <= 0.3):
                answer = "This question is out of my domain!"
                print(answer)
            else:

                context = []
                for i in relevant_chunks.matches:
                    context.append(i.metadata["text"])

                context = "\n".join(context)

                prompt = f""" You are an helpfull assistant. just generate me an answer using relevant chunks, history and user question.
                history : {history}
                relevant chunks : {context}
                user question : {user_question}
                """

                llm1 = client.chat.completions.create(model="gpt-4o-mini",messages=[{"role":"user","content":prompt}])
                answer = llm1.choices[0].message.content
                history = save_entry(history,user_question,answer)
                print(answer)


