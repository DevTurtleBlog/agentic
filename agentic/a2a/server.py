from a2a.server.agent_execution import AgentExecutor, RequestContext
from a2a.server.events import EventQueue, Event
from a2a.types import AgentCard, AgentSkill, AgentCapabilities
from a2a.server.tasks import InMemoryTaskStore
from a2a.server.apps import A2AStarletteApplication
from a2a.server.request_handlers import DefaultRequestHandler
from fastapi import FastAPI
from agentic.a2a.core import registered_agents, registered_skills, AgentInfo

class AgenticA2AServer:
    """ The server class for a2a protocol """

    def __init__(self, fastapi:FastAPI, base_url:str, path:str=None):
        """ Initialize the AgenticServer """
        self.base_url = base_url
        self.fastapi = fastapi
        self.path = path if path is not None else "a2a"
        if self.path.startswith('/'):
            self.path = self.path[1:]
        self.__merge_skills_in_agents()
        self.__init_agent()
        self.__setup_server()

    def __init_agent(self):
        """ Initialize the agent """
        for agent in registered_agents.values():
            cls = agent["class"]
            skills = []
            for skill in agent['skills'].values():
                skills.append(skill['function'])
            def get_skills(self):
                return skills
            cls.get_skills = get_skills

    def __merge_skills_in_agents(self):
        """ Merge skills in agents """
        for skill in registered_skills.values():
            agent_name = skill["agent"]
            if agent_name in registered_agents:
                registered_agents[agent_name].get("skills")[skill['id']]=skill

    def __setup_server(self):
        """ Setup the agent-to-agent server """
        agent_cards = self.__generate_agents_cards()
        app_builders = self.__generate_app_builders(agent_cards)
        for builder in app_builders:
            url = builder.agent_card.url.replace(self.base_url, '')
            self.fastapi.mount(url, builder.build()) 
        @self.fastapi.get("/"+self.path+"/agents", response_model=list[dict])
        def list_agents() -> list[AgentInfo]:
            agent_list:list[AgentInfo]=[]
            for agent in agent_cards:
                agent_url = agent.url.replace(self.base_url, '')
                agent_list.append(AgentInfo(name=agent.name, path=agent_url, description=agent.description, version=agent.version))
            return agent_list
        self.list_agents = list_agents
        
    def __generate_agents_cards(self):
        """ Generate the agents cards """
        agent_cards = []
        for agent in registered_agents.values():
            agent_skills = {}
            for skill in agent["skills"].values():
                agent_skills[skill["id"]]=AgentSkill(
                    id=skill["id"],
                    name=skill["name"],
                    description=skill["description"],
                    tags=skill["tags"],
                    examples=skill["examples"],
                )
            agent_card = AgentCard(
                name=agent["name"],
                description=agent["description"],
                url=self.base_url + '/' + agent["url"],
                version=agent["version"],
                defaultInputModes=agent["defaultInputModes"],
                defaultOutputModes=agent["defaultOutputModes"],
                capabilities=AgentCapabilities(streaming=agent["streaming"]),
                skills=agent_skills.values(),
            )
            agent_cards.append(agent_card)
        return agent_cards
    
    def __generate_app_builders(self, agent_cards) -> list[A2AStarletteApplication]:
        """ Generate the executors """
        app_builders = []
        for agent_card in agent_cards:
            def init(self):
                self.agent = registered_agents[agent_card.name]
            async def execute(context: RequestContext, event_queue: EventQueue,) -> None:
                agent_instance = registered_agents[agent_card.name]['class']()
                result:Event = await agent_instance.execute(context)
                event_queue.enqueue_event(result)
            async def cancel(context: RequestContext, event_queue: EventQueue,) -> None:
                raise Exception('cancel not supported')
            executor = type(agent_card.name + "Executor", (AgentExecutor,), {
                "__init__": init,
                "execute": execute,
                "cancel": cancel,
            })
            request_handler = DefaultRequestHandler(
                agent_executor=executor,
                task_store=InMemoryTaskStore(),
            )
            server_app_builder = A2AStarletteApplication(
                agent_card=agent_card, http_handler=request_handler
            )
            app_builders.append(server_app_builder)
        return app_builders
        
