import openai

openai.api_key = open("API_KEY.txt", "r").read()

with open("prompt.txt", "r") as file:
    prompt = file.read()

with open("prompt2.txt", "r") as file:
    prompt2 = file.read()

chatLog = [{
    "role": "user",
    "content": prompt
    }]

response = openai.ChatCompletion.create(
    model = "gpt-3.5-turbo",
    messages = chatLog
)

assistantResponse= response["choices"][0]["message"]["content"]

print(assistantResponse.strip("\n").strip())

chatLog.append({"role": "user", "content": prompt2})
chatLog.append({"role": "assistant", "content": assistantResponse})

newResponse = openai.ChatCompletion.create(
    model = "gpt-3.5-turbo",
    messages = chatLog
)

newAssistantResponse= newResponse["choices"][0]["message"]["content"]

print("--------------------------")
print(newAssistantResponse.strip("\n").strip())
