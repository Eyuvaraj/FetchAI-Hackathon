from uagents import Agent, Context
import ast

Questionnaire_agent = Agent(name="questionnaire_agent", seed="questionnaire_agent_seed")

from openai import OpenAI
OPENAI_KEY = "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"

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
#   messages.append(message("assistant", response))
  return response


@Questionnaire_agent.on_event("startup")
async def questionnaire_agent(ctx: Context):
    ctx.logger.info("Questionnaire agent is kicking off")

    output_struct = {"questions":["list of questions about the 3D model to be built, along with sample options"]}

    chat_msgs = []

    SYSTEM_PROMPT = f"""You're a 3D graphic designer & planner who specializes in creating 3D models schema based on descriptions of objects. Do not assume anything, you have to ask questions about the model, like how it has to be, its approx dimensions, texture, features and other user customizations too. return the response in this json format: {output_struct} only!, don't include any introductory/ending text."""

    chat_msgs.append(message("system", SYSTEM_PROMPT))
    chat_msgs.append(message("user", "I want a house"))

    print(ctx.logger.info(chat(chat_msgs)))

    # try:
    #     questions = ast.literal_eval(chat(chat_msgs))
    #     print(questions)

    #     questions = [q for q in questions["questions"]]
    # except Exception as e:
    #     ctx.logger.error(e)
    #     print(e)
    #     questions = []

    # ctx.logger.info(chat(chat_msgs))


if __name__ == "__main__":
    Questionnaire_agent.run()