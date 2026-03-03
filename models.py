from datetime import datetime

from pydantic import BaseModel, Field


class AgentCard(BaseModel):
    id: str
    name: str
    capabilities: list[str]
    endpoint: str
    input: str
    output: str
    status: str = "available"
    owner: str
    registered_at: datetime = Field(default_factory=datetime.now)
