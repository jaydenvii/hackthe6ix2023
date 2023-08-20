import openai

openai.api_key = open("API_KEY.txt", "r").read()

def get_response(prompt):

    chatLog = [{
        "role": "user",
        "content": prompt
        }]

    GPT = openai.ChatCompletion.create(
        model = "gpt-3.5-turbo",
        messages = chatLog
    )

    response = GPT["choices"][0]["message"]["content"]

    return response.strip("\n").strip()
