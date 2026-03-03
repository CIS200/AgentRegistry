import asyncio
import os

import httpx
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .database import delete_agent, get_all_agents, init_db, insert_agent, update_agent_status
from .models import AgentCard

app = FastAPI(title="AgentBoard Registry")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])


async def health_check_loop():
    while True:
        await asyncio.sleep(30)
        agents = get_all_agents()
        async with httpx.AsyncClient(timeout=5) as client:
            for agent in agents:
                try:
                    resp = await client.get(agent.endpoint)
                    status = "available" if resp.status_code < 500 else "offline"
                except Exception:
                    status = "offline"
                update_agent_status(agent.id, status)


@app.on_event("startup")
async def startup():
    init_db()
    asyncio.create_task(health_check_loop())


@app.post("/agents/register")
def register_agent(agent: AgentCard):
    insert_agent(agent)
    return {"status": "success", "agent_id": agent.id}


@app.delete("/agents/{agent_id}")
def remove_agent(agent_id: str):
    delete_agent(agent_id)
    return {"status": "success", "agent_id": agent_id}


@app.get("/agents")
def list_agents(capability: str | None = None):
    agents = get_all_agents()
    if capability:
        agents = [a for a in agents if capability in a.capabilities]
    return agents
