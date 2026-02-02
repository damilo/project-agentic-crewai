import os
from dotenv import load_dotenv

from crewai import Agent, Task, Crew

def run_demo () -> None:

  # load environment variables
  load_dotenv ()
  
  #####
  
  # agents
  print ("info # create agent, name = greeter_agent")
  greeter_agent = Agent (
    role="Showcase Ambassador",
    goal="Greet the audience and explain that crewAI is running perfectly.",
    backstory="You are a professional AI host. You are excited to show how easy it is to use agents.",
    verbose=True,
    allow_delegation=False
  )
  
  # tasks
  print ("info # create task, name = hello_task")
  hello_task = Task (
    description="Write a short, enthusiastic 'Hello World' message for a live demo.",
    expected_output="A 2-sentence greeting confirming the system is online.",
    agent=greeter_agent
  )
  
  # crew
  print ("info # create crew, name = test_crew")
  test_crew = Crew (
    agents=[greeter_agent],
    tasks=[hello_task],
    verbose=True
  )
  
  #####
  
  # execute
  print ("info # start crew")
  result = test_crew.kickoff()
  
  print ("info # result")
  print(result)



if __name__ == "__main__":
    run_demo ()
