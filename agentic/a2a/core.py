import types
from abc import ABC, abstractmethod
from a2a.server.agent_execution import RequestContext
from a2a.server.events import Event
from typing import TypedDict

registered_agents = {}
registered_skills = {}

def agent(description, url:str=None, version="1.0.0", defaultInputModes=['text'], defaultOutputModes=['text'], streaming=True):
    """ Register an agent """
    if url is not None:
        if url != None and url.startswith('/'):
                url = url[1:]
        if url.endswith('/'):
            url = url[:-1]
    def decorator(cls):
        if not isinstance(cls, type):
            raise TypeError("@agent should be used on a class")
        if not issubclass(cls, BaseAgent):
            raise TypeError("@agent should be used on a subclass of agentic.core.BaseAgent")
        nonlocal url
        if url is None:
            url = cls.__qualname__.lower()
        agent = {
            "name": cls.__qualname__,
            "description": description,
            "url": url + '/',
            "version": version,
            "defaultInputModes": defaultInputModes,
            "defaultOutputModes": defaultOutputModes,
            "streaming": streaming,
            "class": cls,
            "skills": {}
        }
        registered_agents[cls.__qualname__]=agent
        return cls
    return decorator

def skill(id=None, name=None, description=None, tags=[], examples=[]):
    """Define a skill function"""
    def decorator(func):
        if not isinstance(func, types.FunctionType):
            raise TypeError("@skill should be used on a function")
        
        qualname = func.__qualname__
        if "." not in qualname:
            raise TypeError("@skill should be used on a class method")
        
        class_name = qualname.split(".")[0]
        
        nonlocal id, name
        if id is None:
            id = class_name
        if name is None:
            name = class_name
        
        skill = {
            "id": id,
            "name": name,
            "agent": class_name,
            "description": description,
            "function": func,
            "tags": tags,
            "examples": examples
        }

        registered_skills[id]=skill

        return func
    return decorator

class BaseAgent(ABC):
    """ Base class for all agents """
    def __init__(self):
        pass

    def get_skills(self) -> list[types.FunctionType]:
        """ Get the skill functions of the agent. This method is overrided by the agent decorator. """
        pass

    @abstractmethod
    async def execute(self, input:RequestContext) -> Event:
        """ Execute the agent """
        pass

class AgentInfo(TypedDict):
    """ Info about the agents exposed by the agentic server """
    name: str
    path: str