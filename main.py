import json

from openai import chat
from fastapi import FastAPI
from uagents import Model
from uagents.query import query
from pydantic import BaseModel

QUESTIONNAIRE_ADDRESS = "agent1qff6gfj65rz50ae2pjpnhrvqu3a5yypsqcmphuagkmxqdpwf3vwv53vu8xv"
MODELDECRIPTOR_ADDRESS = "agent1qgk2srf2axh35fklj9p5nt7xwvsq2965540t5q7eav8wwfjh59g52m34y2t"


class TestRequest(Model):
    message: str
    
class TestRequest(Model):
    message: list


async def agent_query_QuestionnaireAgent(req):
    response = await query(destination=QUESTIONNAIRE_ADDRESS, message=req, timeout=15.0)
    data = json.loads(response.decode_payload())
    return data["text"]

async def agent_query_ModelDescriptorAgent(req):
    response = await query(destination=QUESTIONNAIRE_ADDRESS, message=req, timeout=15.0)
    data = json.loads(response.decode_payload())
    return data["text"]


app = FastAPI()


@app.get("/")
def read_root():
    return "Hello from the Agent controller"


@app.post("/new_request")
async def make_agent_call(req: TestRequest):
    try:
        res = await agent_query_QuestionnaireAgent(req)
        return {"data": res}
    except Exception as e:
        print(e)
        return "unsuccessful agent call"



class messages(BaseModel):
    role: str
    content: str

@app.post("/post_messages")
async def Post_Messages(request: list[messages]):
    for item in request:
        print(item.role, item.content)
    return {"message": "success"}
