import json
from fastapi import FastAPI
from uagents import Model
from uagents.query import query

AGENT_ADDRESS = "agent1qff6gfj65rz50ae2pjpnhrvqu3a5yypsqcmphuagkmxqdpwf3vwv53vu8xv"


class TestRequest(Model):
    message: str


async def agent_query(req):
    response = await query(destination=AGENT_ADDRESS, message=req, timeout=15.0)
    data = json.loads(response.decode_payload())
    return data["text"]


app = FastAPI()


@app.get("/")
def read_root():
    return "Hello from the Agent controller"


@app.post("/new_request")
async def make_agent_call(req: TestRequest):
    try:
        res = await agent_query(req)
        return {"data": res}
    except Exception as e:
        print(e)
        return "unsuccessful agent call"
