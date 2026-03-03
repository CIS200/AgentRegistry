# AgentBoard

AgentBoard is a universal registry for AI agents that lets you register, discover, and orchestrate agents through a single API. It includes automatic health checking, natural language agent search, and a web UI for managing your agent fleet.

## Run locally

```bash
git clone <your-repo-url> && cd AgentRegistry
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env  # add your ANTHROPIC_API_KEY
uvicorn agentboard.registry.main:app --reload
```

The registry runs at http://127.0.0.1:8000. Open `agentboard/ui/index.html` in a browser for the web UI.

## Register an agent

```bash
curl -X POST http://127.0.0.1:8000/agents/register \
  -H "Content-Type: application/json" \
  -d '{
    "id": "agent-001",
    "name": "My Agent",
    "capabilities": ["summarize"],
    "endpoint": "http://127.0.0.1:9001/run",
    "input": "text",
    "output": "summary",
    "owner": "you"
  }'
```
