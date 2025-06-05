from a2a.server.agent_execution import RequestContext
from a2a.types import Part, JSONRPCResponse, SendMessageSuccessResponse, Message

class RquestParser:
    """ The OutputParser class of the Agentic framework """

    def __init__(self, request:RequestContext):
        """ Initialize the OutputParser """
        self.req = request

    def get_parts(self) -> list[Part]:
        """ Get the parts of the message """
        parts = []
        for part in self.req.message.parts:
            parts.append(part.root)
        return parts
    
    def get_first_part(self) -> Part:
        """ Get the first part of the message """
        return self.get_parts()[0]
    
    def get_part(self, index:int) -> Part:
        """ Get the part at the given index """
        return self.get_parts()[index]
    
    def get_part_message(self, index:int) -> str:
        """ Get the message of the part at the given index """
        part:Part = self.get_part(index)
        match part.kind:
            case 'text':
                return part.text
            case 'data':
                return part.data
            case _:
                raise Exception('The part is not a TextPart or DataPart')
    
    def get_part_message_data(self, part_index:int) -> dict:
        """ Get the data of the part at the given index """
        part:Part = self.get_part(part_index)
        if part.kind == 'data':
            return part.data
        else:
            raise Exception('The part is not a DataPart')
        
    def get_part_message_text(self, part_index:int) -> str:
        """ Get the text of the part at the given index """
        part:Part = self.get_part(part_index)
        if part.kind == 'text':
            return part.text
        else:
            raise Exception('The part is not a TextPart')
        
class ResponseParser:
    """ The ResponseParser class of the Agentic framework """

    def  __init__(self, response:JSONRPCResponse):
        """ Initialize the ResponseParser """
        self.response = response

    def get_parts(self) -> list[Part]:
        """ Get the parts of the message """
        if isinstance(self.response.root, SendMessageSuccessResponse):
            if self.response.root.result.kind == 'message':
                return self.response.root.result.parts
        raise Exception('The response has no parts')
