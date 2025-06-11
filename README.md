# Agentic

A Python framework for developing and deploying complete AI applications that includes:
- Multi-agent systems according to the Agent2Agent (A2A) protocol
- MCP tools

> ⚠️ **Beta Version**: This framework is currently in active development and is considered a beta release. Features may change, and some functionality may be unstable.

## Overview

Agentic is a powerful framework that simplifies the creation of multi-agent systems by leveraging the a2a protocol. Built on top of [FastAPI](https://fastapi.tiangolo.com/) and the [a2a-sdk](https://github.com/google-a2a/a2a-python), Agentic enables developers to easily define, deploy, and manage multiple AI agents.
Agentic also allows the creation of tools according to the MCP standard. The MCP system is built on top of [FastApiMCP](https://github.com/tadata-org/fastapi_mcp).

## Key Features

- **Simple Agent Definition**: Use `@agent` and `@skill` decorators to define agents and their capabilities with minimal boilerplate code
- **Multi-Agent Server**: Deploy multiple agents on the same server instance
- **A2A Protocol Support**: Built-in support for agent-to-agent communication using the standardized a2a protocol
- **FastAPI Integration**: Leverages FastAPI's performance and features for robust web service deployment
- **A2A Client**: Included client for easy interaction with deployed agents
- **MCP Tools**: Use `@mcp` decorator to expose tools according to the MCP standard

## Development Status

This project is currently in **beta development**. We are actively working on:
- Stabilizing the core API
- Adding comprehensive documentation
- Implementing additional features

Feedback and contributions are highly appreciated as we work towards a stable release.

## Getting Started

> **Note**: As this is a beta version, the API may change in future releases.

1. **Define an Agent**:
   ```python
   from agentic.a2a.core import agent, skill, BaseAgent
   from a2a.server.agent_execution import RequestContext
   from a2a.utils import new_agent_text_message
   from a2a.server.events import Event

   @agent(
    description="Agent for performing arithmetic operations",
    )
    class MathAgent(BaseAgent):

        async def execute(self, input:RequestContext) -> Event:
            ...
            out = new_agent_text_message("The result is: ...")
            return out

        @skill(
            name="Sum operation", 
            description="Retur result of sum of two numbers",
        )
        async def sum(self, input):
            ...
            return "The result is: ..."
   ```

2. **Deploy the Server**:
   ```python
    from agentic.server import AgenticApp
    AgenticApp(scan_root='agents').run()
   ```

3. **Use the A2A Client**:
   ```python
    import asyncio
    from agentic.a2a.client import ClientA2A
    from agentic.a2a.utility import ResponseParser
    from a2a.types import DataPart

    async def main():
        client = ClientA2A(base_url='http://localhost:9999')

        data = { "messages": [
                {'role': 'user', 'content': '...'}
        ]}
        
        result = await client.invoke("/mathAgent", parts=[DataPart(data=data)])
        parser = ResponseParser(result)
        print("RESULT: ", parser.get_parts())

    if __name__ == "__main__":
    asyncio.run(main())
   ```

4. **Define an MCP Tool**:
   ```python
    @mcp(
        name="hello_world",
        methods=["GET"],
        path="/hello/{name}",
    )
    def hello_world(name:str) -> str:
        """ Prenota un concerto."""
        return "Hello, " + name + "!"
    ```

## Architecture

Agentic follows the agent-to-agent (a2a) protocol specification, enabling:
- Standardized communication between agents
- Interoperability with other a2a-compliant systems
- Scalable multi-agent architectures
- Easy integration with existing AI workflows

## Requirements

- Python 3.8+
- FastAPI
- a2a-python SDK
- httpx (for client functionality)

## Contributing

As this is a beta project, contributions are especially welcome! Please feel free to:
- Report bugs and issues
- Suggest new features
- Submit pull requests
- Provide feedback on the API design

## Links

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [A2A Python SDK](https://github.com/google-a2a/a2a-python)
- [Agent-to-Agent Protocol Specification](https://github.com/google-a2a)
