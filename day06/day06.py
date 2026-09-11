from openai import OpenAI
from pinecone import Pinecone, ServerlessSpec
from dotenv import load_dotenv
import os
import PyPDF2

from load_data import load_pdf_data
from chunking import word_based_chunking
from embeddings import batch_based_embeddings
from upserting import upserting
from history import save_history


load_dotenv()

client = OpenAI(api_key = os.getenv("OPENAI_API_KEY"))

pc = Pinecone(api_key = os.getenv("PINECONE_API_KEY"))

index = pc.Index("ask-uni")
"""
data = load_pdf_data("catalog.pdf")

chunks = word_based_chunking(100,20,data)

embeds = batch_based_embeddings(chunks)

upserting(index,embeds,chunks)
"""

enties = 5
history = []

while True:

    user_question = input("I am your helpfull assistant! Ask about your university catalog or enter 'exit' to quit: ")

    if user_question.lower() == "exit":
        break

    else:

        if len(history) == 0:
            uq_embed = client.embeddings.create(model="text-embedding-3-small",input=user_question,dimensions=1024)
            uq_vector = uq_embed.data[0].embedding

            vdb_query = index.query(vector=uq_vector,top_k=2,include_metadata=True)

            if (len(vdb_query.matches) == 0) or (vdb_query.matches[0].score <0.3):
                answer = "The question is out of my domain knowledge!"
                print(answer)

            else:
                context = []
                for i in vdb_query.matches:
                    context.append(i.metadata["text"])
                context = "\n".join(context)

                prompt = f""" you are an helpfull assistant. Generate an answer using user question and context:
                user question : {user_question}
                context : {context}"""

                llm = client.chat.completions.create(model="gpt-4o-mini",messages=[{"role":"user","content":prompt}])
                answer = llm.choices[0].message.content
                save_history(user_question,answer,enties,history)
                print(answer)

        else:

            prompt = f""" You are an helpfull assistant and your goal is to create a reformulated query. 
            I will share you user question and history, just give me reformulated query and nothing else.
            user question : {user_question}
            history : {history}
            """

            llm = client.chat.completions.create(model="gpt-4o-mini",messages=[{"role":"user","content":prompt}])
            reformulated_query = llm.choices[0].message.content
            response = client.embeddings.create(model="text-embedding-3-small",input=reformulated_query,dimensions=1024)
            reformulated_query_vector = response.data[0].embedding
            vdb_query = index.query(vector=reformulated_query_vector,top_k=2,include_metadata=True)
            context = []
            for i in vdb_query.matches:
                context.append(i.metadata["text"])

            context = "\n".join(context)

            prompt1 = f"""You are an helpfull assistant. I will give you user question, context, and history generate me a well structured and explained answer.
            user question : {user_question}
            context : {context}
            history : {history}"""

            llm1 = client.chat.completions.create(model="gpt-4o-mini",messages=[{"role":"user","content":prompt1}])
            answer = llm1.choices[0].message.content
            save_history(user_question,answer,enties,history)
            print(answer)





            



