# Agentic

A Python framework for developing and deploying multi-agent AI applications using the agent-to-agent (a2a) protocol.

> ⚠️ **Beta Version**: This framework is currently in active development and is considered a beta release. Features may change, and some functionality may be unstable. Use with caution in production environments.

## Overview

Agentic is a powerful framework that simplifies the creation of multi-agent systems by leveraging the a2a protocol. Built on top of [FastAPI](https://fastapi.tiangolo.com/) and the [a2a-sdk](https://github.com/google-a2a/a2a-python), Agentic enables developers to easily define, deploy, and manage multiple AI agents on a single server.

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
- Bug fixes and performance improvements

Feedback and contributions are highly appreciated as we work towards a stable release.

## Main Components

### Agent Definition
Use decorators to define agents and their skills:
- `@agent`: Define an agent with metadata like name, description, and capabilities
- `@skill`: Define specific skills/functions that agents can perform

### Server
- Deploy multiple agents on a single server
- Automatic agent card generation
- Built-in request handling and task management

### Client
- Easy-to-use client for interacting with deployed agents
- Support for invoking agent skills remotely
- Agent discovery capabilities

### Utilities
- `RequestParser`: Parse and extract parts from agent requests
- Message handling and part extraction utilities

## Getting Started

> **Note**: As this is a beta version, the API may change in future releases.

1. **Define an Agent**:
   ```python
   @agent(name="MyAgent", description="A sample agent")
   class MyAgent:
       
       @skill(name="process_text", description="Process text input")
       def process_text(self, text: str) -> str:
           return f"Processed: {text}"
   ```

2. **Deploy the Server**:
   ```python
   from agentic.server import AgenticServer
   
   server = AgenticServer()
   server.add_agent(MyAgent)
   server.run()
   ```

3. **Use the Client**:
   ```python
   from agentic.client import AgenticClient
   
   client = AgenticClient("http://localhost:8000")
   agents = await client.get_agents()
   result = await client.invoke("/my-agent", parts=[...])
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

## Installation

```bash
pip install agentic-a2a
```

## Known Limitations (Beta)

- API may change in future versions
- Limited documentation and examples
- Some features may be incomplete or unstable
- Error handling may need improvements

## Contributing

As this is a beta project, contributions are especially welcome! Please feel free to:
- Report bugs and issues
- Suggest new features
- Submit pull requests
- Provide feedback on the API design

## Roadmap

- [ ] Stabilize core API
- [ ] Add comprehensive documentation
- [ ] Implement additional agent capabilities
- [ ] Add more examples and tutorials
- [ ] Performance optimizations
- [ ] Production-ready features

## License

[Add your license information here]

## Links

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [A2A Python SDK](https://github.com/google-a2a/a2a-python)
- [Agent-to-Agent Protocol Specification](https://github.com/google-a2a)
