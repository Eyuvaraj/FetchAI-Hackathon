from openai import OpenAI
OPENAI_KEY = open(".env", "r").read().strip()

client = OpenAI(api_key=OPENAI_KEY)

def message(role, content):
  return {
    "role": role,
    "content": content
  }

def chat(messages):
  completion = client.chat.completions.create(
    model="gpt-4o",
    messages=messages
  )
  response =  completion.choices[0].message.content
  return response