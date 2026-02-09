import os
import sys
import warnings
import yaml
from dotenv import load_dotenv

from crewai import Agent, Task, Crew, Process

import schemas
from tools import PDFMRNExtractorTool, PdfToTextTool


def main () -> None:

    print ("info # crewAI environment start, MRN Extractor")

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
    #pdf_mrn_extractor_tool = PDFMRNExtractorTool ()
    pdf_to_text_tool = PdfToTextTool ()

    # agents
    print ("info # create agent, name = zolldokument_analyst")
    zolldokument_analyst = Agent (
        config=agentsConfig["zolldokument_analyst"],
        verbose=True,
        allow_delegation=False,
        tools=[pdf_to_text_tool]
    )

    print ("info # create agent, name = logistik_kommunikator")
    logistik_kommunikator = Agent (
        config=agentsConfig["logistik_kommunikator"],
        verbose=True,
        allow_delegation=False
    )

    # tasks
    print ("info # create task, name = mrn_extraction_task")
    mrn_extraction_task = Task (
        config=tasksConfig["mrn_extraction_task"],
        agent=zolldokument_analyst
    )

    print ("info # create task, name = email_creation_task")
    email_creation_task = Task (
        config=tasksConfig["email_creation_task"],
        agent=logistik_kommunikator,
        context=[mrn_extraction_task],
        output_file=os.path.join (os.path.dirname (pyScriptFullPath), 'output', 'email_body.txt')
    )

    # crew
    print ("info # create crew, name = projekt_crew")
    projekt_crew = Crew (
        agents=[zolldokument_analyst, logistik_kommunikator],
        tasks=[mrn_extraction_task, email_creation_task],
        verbose=True,
        process=Process.sequential
    )

    print ("info # start crew")
    inputs = {
        'pdf_path' : os.path.join (os.path.dirname (pyScriptFullPath), 'input', 'Zalando Polen.pdf'),
        'email_subject' : 'Frachtbrief',
        'email_sender_name' : 'Daniel Hellwig'
    }
    result = projekt_crew.kickoff (inputs=inputs)
    print (result)


    print ("info # CrewAI environment end")



if __name__ == "__main__":
    main ()
