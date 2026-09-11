from openai import OpenAI
from pinecone import Pinecone
import os
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
index = pc.Index("ask-uni")

entry = 5
history = []

def save_entry(history,entry,user_question,assistant_answer):
    history.append({"role":"user","content":user_question})
    history.append({"role":"assistant","content":assistant_answer})

    max_chat = entry*2

    if len(history) > max_chat:
        history = history[-max_chat:]

    return history

while True:

    user_question = input("I am your helping Assistant! Ask questions or type 'exit' to quit: ")

    if user_question.lower() == "exit":
        break

    else:
        if len(history) == 0:

            try:
                user_question_embed1 = client.embeddings.create(model = "text-embedding-3-small", input = user_question, dimensions = 1024)
                user_question_vector1 = user_question_embed1.data[0].embedding

            except Exception as e:
                print(f"Error: {e}")
                continue

            try:
                vdb_query1 = index.query(vector=user_question_vector1, top_k=2, include_metadata=True)

                if len(vdb_query1.matches) == 0 or vdb_query1.matches[0].score < 0.5:
                    print("Question out of base knowledge! Ask Fccu 25-26 catalog relevant questions!")
                    continue

                else:
                    context1 = []
                    for i in vdb_query1.matches:
                        context1.append(i.metadata["text"])
                    context1 = "\n".join(context1)

            except Exception as e:
                print(f"Error: {e}")
                continue

            try:
                prompt1 = f""" You are a helpfull assistant. Your task is generate a well structure, clean answer using the question and context. If the question is in english generate in english, if yhe question is in roman urdu generate in roman urdu, dont include hindi words in it!
                question : {user_question}
                context : {context1}"""

                llm1 = client.chat.completions.create(model= "gpt-4o-mini", messages = [{"role" : "user", "content" : prompt1}])
                answer1 = llm1.choices[0].message.content
                history = save_entry(history,entry,user_question,answer1)
                print(answer1)

            except Exception as e:
                print(f"Error: {e}")
                continue

        elif len(history) != 0:

            try:
                prompt2 = f""" You are an helpfull assistant. Your task is generate a reformulated query using question and history. if the question is in english generate in english, if the question is in roman urdu generate in roman urdu dont include hindi words!
                question : {user_question}
                history : {history}"""

                llm2 = client.chat.completions.create(model = "gpt-4o-mini", messages = [{"role" : "user", "content" : prompt2}])
                reformulated_query = llm2.choices[0].message.content

            except Exception as e:
                print(f"Error: {e}")
                continue

            try:
                reformulated_query_embed = client.embeddings.create(model = "text-embedding-3-small", input = reformulated_query, dimensions = 1024)
                reformulated_query_vector = reformulated_query_embed.data[0].embedding

            except Exception as e:
                print(f"Error: {e}")
                continue

            try:
                vdb_query2 = index.query(vector = reformulated_query_vector, top_k = 2, include_metadata = True)

                if len(vdb_query2.matches) == 0 or vdb_query2.matches[0].score < 0.5:
                    print("Question out of base knowledge! Ask Fccu 25-26 catalog relevant questions!")
                    continue

                else:
                    context2 = []
                    for i in vdb_query2.matches:
                        context2.append(i.metadata["text"])
                    context2 = "\n".join(context2)

            except Exception as e:
                print(f"Error: {e}")
                continue

            try:
                prompt3 = f""" You are an helpfull assistant. Your job is to generate a well stuctured, clean answer. If the question is in english generate the answer in english, and if the question is in roman urdu generate the answer in roman urdu and dont include hindi words in it!
                question = {user_question}
                context : {context2}
                history : {history}"""

                llm3 = client.chat.completions.create(model = "gpt-4o-mini", messages = [{"role" : "user", "content" : prompt3}])
                answer2 = llm3.choices[0].message.content
                history = save_entry(history,entry,user_question,answer2)
                print(answer2)

            except Exception as e:
                print(f"Error: {e}")
                continue
