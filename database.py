import json
import sqlite3

from .models import AgentCard

DB_PATH = "agentboard.db"


def init_db():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS agents (
            id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            capabilities TEXT NOT NULL,
            endpoint TEXT NOT NULL,
            input TEXT NOT NULL,
            output TEXT NOT NULL,
            status TEXT NOT NULL DEFAULT 'available',
            owner TEXT NOT NULL,
            registered_at TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()


def insert_agent(agent: AgentCard):
    conn = sqlite3.connect(DB_PATH)
    conn.execute(
        "INSERT OR REPLACE INTO agents VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
        (
            agent.id,
            agent.name,
            json.dumps(agent.capabilities),
            agent.endpoint,
            agent.input,
            agent.output,
            agent.status,
            agent.owner,
            agent.registered_at.isoformat(),
        ),
    )
    conn.commit()
    conn.close()


def get_all_agents() -> list[AgentCard]:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    rows = conn.execute("SELECT * FROM agents").fetchall()
    conn.close()
    return [
        AgentCard(
            id=row["id"],
            name=row["name"],
            capabilities=json.loads(row["capabilities"]),
            endpoint=row["endpoint"],
            input=row["input"],
            output=row["output"],
            status=row["status"],
            owner=row["owner"],
            registered_at=row["registered_at"],
        )
        for row in rows
    ]


def update_agent_status(agent_id: str, status: str):
    conn = sqlite3.connect(DB_PATH)
    conn.execute("UPDATE agents SET status = ? WHERE id = ?", (status, agent_id))
    conn.commit()
    conn.close()


def delete_agent(agent_id: str):
    conn = sqlite3.connect(DB_PATH)
    conn.execute("DELETE FROM agents WHERE id = ?", (agent_id,))
    conn.commit()
    conn.close()
