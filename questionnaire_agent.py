from uagents import Agent, Context, Model
import ast
from openai import OpenAI
import re

OPENAI_KEY = open(".env", "r").read().strip()

client = OpenAI(api_key="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")

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

class TestRequest(Model):
    message: str


class Response(Model):
    text: str


QuestionnaireAgent = Agent(
    name="QuestionnaireAgent",
    seed="questionnaire-Agent-Seed",
    port=8001,
    endpoint="http://localhost:8001/submit",
)


@QuestionnaireAgent.on_event("startup")
async def startup(ctx: Context):
    ctx.logger.info(f"Starting up {QuestionnaireAgent.name}")
    ctx.logger.info(f"With address: {QuestionnaireAgent.address}")
    ctx.logger.info(f"And wallet address: {QuestionnaireAgent.wallet.address()}")


@QuestionnaireAgent.on_query(model=TestRequest, replies={Response})
async def query_handler(ctx: Context, sender: str, _query: TestRequest):
    ctx.logger.info("Query received")
    ctx.logger.info(f"Message: {_query.message}")
    ctx.logger.info(f"Sender: {sender}")
    
    output_struct = {"questions":["list of questions about the 3D model to be built, along with sample options"]}
    
    try:
        chat_msgs = []

        SYSTEM_PROMPT = f"""You're a 3D graphic designer & planner who specializes in creating a minimalist and simple 3D models schema based on descriptions of objects. Do not assume anything, you have to ask questions about the model, like how it has to be, its approx dimensions, texture, features and other user customizations too. return the response in this json format: {output_struct} only!, don't include any introductory/ending text."""

        chat_msgs.append(message("system", SYSTEM_PROMPT))
        chat_msgs.append(message("user", _query.message))

        response = chat(chat_msgs)
        print(response)

        try:
            if re.search(r"```json\n", response):
                response = re.sub(r"```json\n", "", response)
            elif re.search("```json", response):
              response = re.sub("```json", "", response)
            if re.search(r"\n```", response):
               response = re.sub(r"\n```", response)
            elif re.search("```", response):
               response = re.sub("```", "", response)

            qu = ast.literal_eval(response)
              
            qu = [q for q in qu["questions"]]

            for q in qu:
              ctx.logger.info(q)
            await ctx.send(sender, Response(text=str(qu)))
        except Exception as e:
            ctx.logger.error(e)
            await ctx.send(sender, Response(text="fail"))

    except Exception as e:
        ctx.logger.error(e)
        await ctx.send(sender, Response(text="fail"))


if __name__ == "__main__":
    QuestionnaireAgent.run()