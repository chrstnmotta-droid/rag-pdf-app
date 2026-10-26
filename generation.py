system_prompt = """

"""
client = OpenAI("actualkey needed")
# History track in main as list
def first_message(client, prompt, system_prompt, model):
    content = retrieval_top_5k(prompt)
    rag_load = f"Context:{context}, user question:{prompt}"
    response = client.responses.create(
        model = model,
        reasoning = {"effort": "high"},
        input = [
            {"role": "developer", "content": system_prompt},
            ("role":"user", "content": rag_load ),
        ],
        store = True
    )
    generated_response = response.output_text
    response_id = response.id
    return generated_response, response_id

def multi_turn(client, prompt, system_prompt, model, previous_response_id, history):
    condensation_turn = client.responses.create(
        model = model,
        previous_response_id = previous_response_id,
        input = f"Based on the conversation history, rephrase this follow up in a standalone search query: {prompt}"
    )
    rag_load = retrieval_top_5k(prompt)
    response = client.responses.create(
        model = model,
        reasoning = {"effort": "high"},
        previous_response_id = previous_response_id,
        input = [
            {"role": "developer", "content": system_prompt},
            ("role":"user", "content": rag_load ),
        ],
        store = True
    )
    generated_response = response.output_text
    new_response_id = response_id
    return generated_response, new_response_id
