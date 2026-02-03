import os
import sys
import warnings
import yaml
from dotenv import load_dotenv

from crewai import Agent, Task, Crew, Process
from crewai_tools import SerperDevTool, ScrapeWebsiteTool

import schemas


schemas.venue_details

def main () -> None:

    print ("info # crewAI environment start, Event Planner")

    # warning control
    warnings.filterwarnings ('ignore')

    # script info
    pyScriptFullPath: str = os.path.abspath(sys.argv[0])
    print ("info # absolute path of python script =", pyScriptFullPath)

    # environment variables
    envFileFullPath: str = os.path.join (os.path.dirname (pyScriptFullPath), ".env")
    print (f"info # load environment variables from '{envFileFullPath}'")
    load_dotenv (dotenv_path=envFileFullPath)
    print (f"info # agent API key = {os.getenv ('GEMINI_API_KEY')[:10]}...")

    # agents config
    agentsConfigFileFullPath : str = os.path.join (os.path.dirname (pyScriptFullPath), "config", "agents.yaml")
    print (f"info # read agents config from '{agentsConfigFileFullPath}'")
    agentsConfig = None
    with open (agentsConfigFileFullPath, "r") as file:
        agentsConfig = yaml.safe_load (file)
    
    # tasks config
    tasksConfigFileFullPath : str = os.path.join (os.path.dirname (pyScriptFullPath), "config", "tasks.yaml")
    print (f"info # read tasks config from '{tasksConfigFileFullPath}'")
    tasksConfig = None
    with open (tasksConfigFileFullPath, "r") as file:
        tasksConfig = yaml.safe_load (file)

    #####

    # tools
    #search_tool = SerperDevTool ()
    scrape_tool = ScrapeWebsiteTool ()

    # agents
    print ("info # create agent, name = venue_coordinator")
    venue_coordinator = Agent (
        config=agentsConfig["venue_coordinator"],
        verbose=True,
        allow_delegation=False,
        tools=[scrape_tool]
    )

    print ("info # create agent, name = logistics_manager")
    logistics_manager = Agent (
        config=agentsConfig["logistics_manager"],
        verbose=True,
        allow_delegation=False,
        tools=[scrape_tool]
    )

    print ("info # create agent, name = marketing_communications_agent")
    marketing_communications_agent = Agent (
        config=agentsConfig["marketing_communications_agent"],
        verbose=True,
        allow_delegation=False,
        tools=[scrape_tool]
    )

    # tasks
    print ("info # create task, name = venue_task")
    venue_task = Task (
        config=tasksConfig["venue_task"],
        agent=venue_coordinator,
        human_input=True,
        output_json=schemas.MODEL_MAP['VenueDetails'],
        output_file=os.path.join (os.path.dirname (pyScriptFullPath), 'output', 'venue_details.json')
    )

    print ("info # create task, name = logistics_task")
    logistics_task = Task (
        config=tasksConfig["logistics_task"],
        agent=logistics_manager,
        human_input=True
    )

    print ("info # create task, name = marketing_task")
    marketing_task = Task (
        config=tasksConfig["marketing_task"],
        agent=marketing_communications_agent,
        output_file=os.path.join (os.path.dirname (pyScriptFullPath), 'output', 'marketing_report.md')
    )
    

    # crew
    print ("info # create crew, name = projekt_crew")
    projekt_crew = Crew (
        agents=[venue_coordinator, logistics_manager, marketing_communications_agent],
        tasks=[venue_task, logistics_task, marketing_task],
        verbose=True
    )

    print ("info # start crew")
    event_details = {
        'event_city' : 'san francisco',
        'event_topic' : 'tech innovation conference',
        'expected_participants' : 500,
        'tentative_date' : '2026-09-25',
        'budget' : 20000, # additional, ndef in any task or agent
        'venue_type' : 'conference hall'  # additional, ndef in any task or agent 
    }
    result = projekt_crew.kickoff (inputs=event_details)
    print (result)


    print ("info # CrewAI environment end")



if __name__ == "__main__":
    main ()
