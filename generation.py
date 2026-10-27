from openai import OpenAI
import os
from dotenv import load_dotenv
from retrieval import retrieval_top_5k

system_prompt = """
You are a tutor for an AI master. You receive chunks from scientific articles and answer them using between 200-600 words depending on 
the substance of the prompt and complexity of the question. When you receive the chunks answer the question by outlining the main points
of the chunks relevant to the prompt. Then use the outline to generate the final answer. If the answer isn't in the chunks please answer 
with "I don't know" this is excempt from the length rule. The chunks are separated by "---".
"""
model= "gpt-6.1-sol"
load_dotenv()
client = OpenAI(api_key = os.getenv("OPENAI_API_KEY"))

# History track in main as list
def first_message(client, query, system_prompt, model):
    context_raw = retrieval_top_5k(query)["documents"][0]
    context =" --- ".join(context_raw)
    rag_load = f"Context:{context}, user question:{query}"
    response = client.responses.create(
        model = model,
        reasoning = {"effort": "high"},
        input = [
            {"role": "system", "content": system_prompt},
            {"role":"user", "content": rag_load},
        ],
        store = True
    )
    generated_response = response.output_text
    response_id = response.id
    return context_raw, generated_response, response_id

def multi_turn(client, query, system_prompt, model, previous_response_id, history):
    condensation_turn = client.responses.create(
        model = model,
        previous_response_id = previous_response_id,
        input = f"Based on the conversation history, rephrase this follow up in a standalone search query: {query}"
    )
    rag_load = retrieval_top_5k(query)
    response = client.responses.create(
        model = model,
        reasoning = {"effort": "high"},
        previous_response_id = previous_response_id,
        input = [
            {"role": "system", "content": system_prompt},
            {"role":"user", "content": rag_load},
        ],
        store = True
    )
    generated_response = response.output_text
    new_response_id = response_id
    return generated_response, new_response_id

if __name__ == "__main__":
    prompt = "Give a real-world example that shows that arbitrariness is hard to deal with in machine learning"
    raw, response, _ = first_message(client,prompt, system_prompt, model)
    print(response)
    print (raw)
