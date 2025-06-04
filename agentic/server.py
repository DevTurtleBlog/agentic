import importlib, pkgutil
from a2a.server.agent_execution import AgentExecutor, RequestContext
from a2a.server.events import EventQueue, Event
from a2a.types import AgentCard, AgentSkill, AgentCapabilities
from a2a.server.tasks import InMemoryTaskStore
from a2a.server.apps import A2AStarletteApplication
from a2a.server.request_handlers import DefaultRequestHandler
from fastapi import FastAPI
import uvicorn
from agentic.core import registered_agents, registered_skills

class AgenticServer:
    """ The main App class of the Agentic framework """

    def __init__(self, base_url:str, scan_root:str=None):
        """ Initialize the AgenticApp """
        if scan_root:
            self.__scan_imports(scan_root)
        if base_url.endswith('/'):
            base_url = base_url[:-1]
        self.base_url = base_url
        self.__run_server()
        self.__merge_skills_in_agents()
        self.__init_agent()
        self.__setup_a2a_server()

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

    def __merge_skills_in_agents(self):
        """ Merge skills in agents """
        for skill in registered_skills.values():
            agent_name = skill["agent"]
            if agent_name in registered_agents:
                registered_agents[agent_name].get("skills")[skill['id']]=skill

    def __setup_a2a_server(self):
        """ Setup the agent-to-agent server """
        agent_cards = self.__generate_agents_cards()
        app_builders = self.__generate_app_builders(agent_cards)
        fastapi = FastAPI()
        for builder in app_builders:
            url = builder.agent_card.url.replace(self.base_url, '')
            fastapi.mount(url, builder.build()) 
        uvicorn.run(fastapi, host='0.0.0.0', port=9999)
        
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
    
    def __generate_app_builders(self, agent_cards):
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
    
    def __run_server(self):
        """ Run the server """
        print("Server running...")
        
