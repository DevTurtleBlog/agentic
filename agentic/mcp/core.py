import types

registered_tools = {}

def mcp(methods:list[str]=["GET"], name:str=None, tags:list[str]=None, path:str=None):
    """Define an MCP tool function"""
    def decorator(func):
        nonlocal name, path
        if not isinstance(func, types.FunctionType):
            raise TypeError("@tool should be used on a function")  
        if name is None:
            name = func.__qualname__
        if path and path.startswith('/'):
            path = path[1:]
        registered_tools[name] = {
            "name": name,
            "path": path if path else name,
            "methods": methods,
            "tags": tags,
            "func": func
        }
        return func
    return decorator

