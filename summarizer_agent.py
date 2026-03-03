import os

import anthropic
import httpx
from fastapi import FastAPI
from pydantic import BaseModel

REGISTRY_URL = "http://127.0.0.1:8000"
AGENT_ID = "agent-summarizer"

AGENT_CARD = {
    "id": AGENT_ID,
    "name": "Summarizer Agent",
    "capabilities": ["summarize"],
    "endpoint": "http://127.0.0.1:9001/run",
    "input": "text",
    "output": "summary",
    "owner": "caroline",
}

app = FastAPI(title="Summarizer Agent")
client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))


class Task(BaseModel):
    task: str


@app.on_event("startup")
def register():
    httpx.post(f"{REGISTRY_URL}/agents/register", json=AGENT_CARD)


@app.on_event("shutdown")
def deregister():
    httpx.delete(f"{REGISTRY_URL}/agents/{AGENT_ID}")


@app.post("/run")
def run(task: Task):
    message = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=1024,
        messages=[
            {"role": "user", "content": f"Summarize the following text concisely:\n\n{task.task}"}
        ],
    )
    return {"summary": message.content[0].text}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=9001)
