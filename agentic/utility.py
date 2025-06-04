from a2a.server.agent_execution import RequestContext
from a2a.types import Part

class RquestParser:
    """ The OutputParser class of the Agentic framework """

    def __init__(self, request:RequestContext):
        self.req = request

    def get_parts(self) -> list[Part]:
        return self.req.message.parts
    
    def get_first_part(self) -> Part:
        return self.get_parts()[0].root
    
    def get_message_data(self) -> dict:
        part = self.get_first_part()
        if part.kind == 'data':
            return self.get_first_part().data
        else:
            raise Exception('The part is not a DataPart')
        
    def get_message_text(self) -> str:
        part = self.get_first_part()
        if part.kind == 'text':
            return self.get_first_part().text
        else:
            raise Exception('The part is not a TextPart')
