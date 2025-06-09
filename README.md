# Agentic

A Python framework for developing and deploying multi-agent AI applications using the agent-to-agent (a2a) protocol.

> ⚠️ **Beta Version**: This framework is currently in active development and is considered a beta release. Features may change, and some functionality may be unstable.

## Overview

Agentic is a powerful framework that simplifies the creation of multi-agent systems by leveraging the a2a protocol. Built on top of [FastAPI](https://fastapi.tiangolo.com/) and the [a2a-sdk](https://github.com/google-a2a/a2a-python), Agentic enables developers to easily define, deploy, and manage multiple AI agents.

## Key Features

- **Simple Agent Definition**: Use `@agent` and `@skill` decorators to define agents and their capabilities with minimal boilerplate code
- **Multi-Agent Server**: Deploy multiple agents on the same server instance
- **A2A Protocol Support**: Built-in support for agent-to-agent communication using the standardized a2a protocol
- **FastAPI Integration**: Leverages FastAPI's performance and features for robust web service deployment
- **Request Parsing**: Built-in utilities for parsing and handling agent requests
- **Client SDK**: Included client for easy interaction with deployed agents

## Development Status

This project is currently in **beta development**. We are actively working on:
- Stabilizing the core API
- Adding comprehensive documentation
- Implementing additional features

Feedback and contributions are highly appreciated as we work towards a stable release.

## Main Components

### Agent Definition
Use decorators to define agents and their skills:
- `@agent`: Define an agent with metadata like name, description, and capabilities
- `@skill`: Define specific skills/functions that agents can perform

## Getting Started

> **Note**: As this is a beta version, the API may change in future releases.

1. **Define an Agent**:
   ```python
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
   ```

2. **Deploy the Server**:
   ```python
    from agentic.server import AgenticServer
    app = AgenticServer(base_url='http://localhost:9999/', scan_root='agents')
   ```

3. **Use the Client**:
   ```python
    import asyncio
    from agentic.client import AgenticClient
    from agentic.core import AgentInfo
    from agentic.utility import ResponseParser
    from a2a.types import DataPart

    async def main():
        BASE_URL =  'http://localhost:9999'
        client = AgenticClient(base_url=BASE_URL)

        data = { "messages": [
                {'role': 'user', 'content': '...'}
        ]}

        result = await client.invoke("/mathagent", parts=[DataPart(data=data)])
        parser = ResponseParser(result)
        print("RESULT: ", parser.get_parts())

    if __name__ == "__main__":
        asyncio.run(main())
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
