import importlib, pkgutil
from agentic.a2a.server import AgenticA2AServer
from agentic.mcp.server import AgenticMcpServer
from fastapi import FastAPI
import uvicorn

class AgenticApp(AgenticMcpServer, AgenticA2AServer, FastAPI):
    """ The main App class of the Agentic framework """

    def __init__(
            self, 
            protocol:str='http',
            hostname:str = 'localhost',
            port:int = 8080,
            root_package:str=None, 
            server_name:str=None,
            enable_a2a:bool=True,
            enable_mcp:bool=True,
            enable_discovery_a2a:bool=False,
            **kwargs
        ):
        """ Initialize the AgenticApp """
        self.hostname = hostname
        self.port = port
        if root_package:
            self.__scan_imports(root_package)
        self.base_url = f"{protocol}://{hostname}:{port}"
        self.fastapi= self
        FastAPI.__init__(self, **kwargs)
        if enable_mcp:
            AgenticMcpServer.__init__(self, fastapi=self, server_name=server_name)
        if enable_a2a:
            AgenticA2AServer.__init__(self, fastapi=self, base_url=self.base_url, enable_discovery=enable_discovery_a2a)

    def run(self) -> None:
        """ Run the FastAPI app """
        uvicorn.run(self.fastapi, host=self.hostname, port=self.port)
        
    def __scan_imports(self, package_name):
        """ Import all modules in a package and its subpackages """
        package = importlib.import_module(package_name)
        package_path = package.__path__
        for _, module_name, is_pkg in pkgutil.walk_packages(package_path):
            path = package.__name__ + '.' + module_name
            if is_pkg:
                self.__scan_imports(path)
            else:
                importlib.import_module(path)
    
    def get_fastapi(self) -> FastAPI:
        """ Get the FastAPI instance """
        return self.fastapi