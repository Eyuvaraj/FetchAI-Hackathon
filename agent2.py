from uagents import Agent, Context, Model
import ast
from openai import OpenAI
import re

OPENAI_KEY = open(".env", "r").read().strip()

client = OpenAI(api_key=OPENAI_KEY)

def message(role, content):
  return {
    "role": role,
    "content": content
  }

def chat(messages):
  completion = client.chat.completions.create(
    model="gpt-3.5-turbo-0125",
    messages=messages
  )
  response =  completion.choices[0].message.content
  return response

class TestRequest(Model):
    message: list


class Response(Model):
    text: str


Model_Descriptor_Agent = Agent(
    name="Model_Descriptor_Agent",
    seed="Model_Descriptor_Agent-Seed",
    port=8002,
    endpoint="http://localhost:8001/sumbit_messages",
)


@Model_Descriptor_Agent.on_event("startup")
async def startup(ctx: Context):
    ctx.logger.info(f"Starting up {Model_Descriptor_Agent.name}")
    ctx.logger.info(f"With address: {Model_Descriptor_Agent.address}")
    ctx.logger.info(f"And wallet address: {Model_Descriptor_Agent.wallet.address()}")


@Model_Descriptor_Agent.on_query(model=TestRequest, replies={Response})
async def query_handler(ctx: Context, sender: str, _query: TestRequest):
    ctx.logger.info("Query received")
    ctx.logger.info(f"Message: {_query.message}")
    ctx.logger.info(f"Sender: {sender}")
    
    output_struct = {"steps":["list of instruction to draw the 3D model"]}
    
    try:
        chat_msgs = []


        SYSTEM_PROMPT = f"""You're a 3D graphic designer & planner who specializes in creating 3D models schema based on descriptions of objects. Take your time, think and solve step by step, and generate a concise and straightforward list of steps to draw the 3D model (Not 2D) from the description, including proper dimensions for each component. return the response in this json format: {output_struct} only!"""

        chat_msgs.append(message("system", SYSTEM_PROMPT))
        print(_query.message)

    #     response = chat(chat_msgs)
    #     print(response)

    #     try:
    #         if re.search(r"```json\n", response):
    #             response = re.sub(r"```json\n", "", response)
    #         elif re.search("```json", response):
    #           response = re.sub("```json", "", response)
    #         if re.search(r"\n```", response):
    #            response = re.sub(r"\n```", response)
    #         elif re.search("```", response):
    #            response = re.sub("```", "", response)

    #         qu = ast.literal_eval(response)
              
    #         qu = [q for q in qu["questions"]]

    #         for q in qu:
    #           ctx.logger.info(q)
    #         await ctx.send(sender, Response(text=str(qu)))
    #     except Exception as e:
    #         ctx.logger.error(e)
    #         await ctx.send(sender, Response(text="fail"))

    except Exception as e:
        ctx.logger.error(e)
        await ctx.send(sender, Response(text="fail"))


if __name__ == "__main__":
    Model_Descriptor_Agent.run()