from fastapi import FastAPI
from fastapi_mcp import FastApiMCP
from agentic.mcp.core import registered_tools

class AgenticMcpServer:
    """ The server class for mcp protocol """

    def __init__(self, fastapi:FastAPI, server_name:str=None):
        """ Initialize the AgenticServer """
        self.fastapi = fastapi
        self.mcp:FastApiMCP = FastApiMCP(
            fastapi=self.fastapi,            
            name=server_name,
        )
        self.mcp.mount()
        self.__mount_mcp_tools()

    def __mount_mcp_tools(self):
        """ Mount MCP tools to the FastAPI app """
        for tool in registered_tools.values():
            router = tool['router']
            if router is None:
                router = self.fastapi
            router.add_api_route(
                f"/{tool['path']}",
                tool['func'],
                methods=tool['methods'],
                tags=tool['tags'],
                operation_id=tool['name']
            )
            if tool['router'] is not None:
                self.fastapi.include_router(tool['router'])
            self.mcp.setup_server()