from crewai import Agent, Crew, Process, Task
from crewai_tools import TXTSearchTool, WebsiteSearchTool
from crewai.project import CrewBase, agent, crew, task
import os
from tools import search_tools
from langchain.llms import Ollama


text_search_tool = TXTSearchTool(os.path.join(os.path.dirname(__file__),'sample.txt'))
website_search_tool = WebsiteSearchTool('https://www.avenueblu.com')
yelp_reviews_search_tool = WebsiteSearchTool('https://www.yelp.com/biz/avenue-blu-tampa-bay?osq=avenueblu')

mistral = Ollama(
    model = "crewai_llama3") 

@CrewBase
class RestaurantCrew():
    """RestaurantCrew crew"""
    agents_config = os.path.join(os.path.dirname(__file__), 'config', 'agents.yml')
    tasks_config = os.path.join(os.path.dirname(__file__), 'config', 'tasks.yml')

    def __init__(self) -> None:
        self.groq_llm = mistral

    @agent
    def restaurant_researcher(self) -> Agent:
        return Agent(
            config = self.agents_config['restaurant_researcher']
        )
    @agent
    def restaurant_analyst(self) -> Agent:
        return Agent(
            config = self.agents_config['restaurant_analyst']
        )
    @agent
    def restaurant_lookout(self) -> Agent:
        return Agent(
            config = self.agents_config['restaurant_lookout']
        )
    
    @task
    def data_capture(self) -> Task:
        return Task(
            config=self.tasks_config['data_capture'],
            agent=self.restaurant_researcher(),
            tools=[yelp_reviews_search_tool, 
                   search_tools.SearchTools.search_internet, 
                   search_tools.SearchTools.get_review_and_session_analytics]
        )
    @task
    def business_review(self)-> Task:
        return Task(
            config=self.tasks_config['business_review'],
            agent=self.restaurant_analyst(),
            tools=[text_search_tool, website_search_tool]
        )
    @crew
    def crew(self) -> Crew:
        """Creates the RestaurantCrew crew"""
        return Crew(
            agents = self.agents,
            tasks = self.tasks,
            process = Process.sequential,
            verbose = 0
        )