from uuid import uuid4
from typing import Any
import httpx
from a2a.client import A2AClient
from a2a.types import (
    MessageSendParams,
    SendMessageRequest,
    Message,
    Role,
    Part,
    JSONRPCResponse
)
from agentic.core import AgentInfo

class AgenticClient:
    """ The Client class of the Agentic framework """
    
    def __init__(self, base_url):
        self.base_url = base_url
    
    async def get_agents(self) -> list[AgentInfo]:
        """ Get the agents exposed by the server """
        return httpx.get(f"{self.base_url}/agents").json()
    
    async def invoke(self, agent_path:str, role:Role=Role.user, parts:list[Part]=[], message_id:str=uuid4().hex) -> JSONRPCResponse:
        async with httpx.AsyncClient() as httpx_client:
            client = await A2AClient.get_client_from_agent_card_url(
                httpx_client, self.base_url + agent_path
            )
            message = Message(
                role=role,
                parts=parts,
                messageId=message_id,
            )
            request = SendMessageRequest(
                params=MessageSendParams(message=message)
            )
            response = await client.send_message(request)
            return response