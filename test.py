from uagents import Agent, Context, Model
import ast
from openai import OpenAI
OPENAI_KEY = open(".env", "r").read().strip()


client = OpenAI(api_key=OPENAI_KEY)


class UserRequest(Model):
   message: str


class Agent_Response(Model):
    response: str



QuestionnaireAgent = Agent(
    name="questionnaireAgent",
    port=6145,
    seed="questionnaire-Agent-Seed",
    endpoint=["http://localhost:6145/input"],
)


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


@QuestionnaireAgent.on_event("startup")
async def startup(ctx: Context):
    ctx.logger.info(f"Starting up {QuestionnaireAgent.name}")
    ctx.logger.info(f"With address: {QuestionnaireAgent.address}")
    ctx.logger.info(f"And wallet address: {QuestionnaireAgent.wallet.address()}")


@QuestionnaireAgent.on_query(model=UserRequest, replies={Agent_Response})
async def query_handler(ctx: Context, _query: UserRequest, sender: str):
    ctx.logger.info(f"UserRequest: {_query.message}")
    try:
        # do something here
        await ctx.send(sender, Agent_Response(response="success"))
    except Exception:
        await ctx.send(sender, Agent_Response(response="fail"))

    # output_struct = {"questions":["list of questions about the 3D model to be built, along with sample options"]}

    # chat_msgs = []

    # SYSTEM_PROMPT = f"""You're a 3D graphic designer & planner who specializes in creating 3D models schema based on descriptions of objects. Do not assume anything, you have to ask questions about the model, like how it has to be, its approx dimensions, texture, features and other user customizations too. return the response in this json format: {output_struct} only!, don't include any introductory/ending text."""

    # chat_msgs.append(message("system", SYSTEM_PROMPT))
    # chat_msgs.append(message("user", _query.message))

    # ctx.logger.info(f"chat_msgs: {chat_msgs}")

    # try:
    #     # response = chat(chat_msgs)
    #     response = '{"questions":["list of questions about the 3D model to be built, along with sample options"]}'
    #     questions = ast.literal_eval(response)
    #     ctx.logger.log(questions)

    #     questions = [q for q in questions["questions"]]
    #     await ctx.send("success", Agent_Response(response="success"))
    # except Exception as e:
    #     ctx.logger.error(e)
    #     await ctx.send("fail", Agent_Response(response="fail"))


if __name__ == "__main__":
    QuestionnaireAgent.run()