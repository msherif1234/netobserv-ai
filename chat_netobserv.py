#!/usr/bin/python3
from secret_key import openapi_key
import os
from typing import Any
from langchain import hub
from langchain.agents import AgentExecutor, create_openai_tools_agent
from langchain_openai import ChatOpenAI
from fastapi import FastAPI
from langchain.pydantic_v1 import BaseModel
from langserve import add_routes
import uvicorn
import query_flow_db

os.environ['OPENAI_API_KEY'] = openapi_key

def netobserv_ai_setup(verbose):
    # Choose the LLM that will drive the agent
    # Only certain models support this
    llm = ChatOpenAI(
        temperature=0, # using low temperature for more predictable results
        model="gpt-3.5-turbo-1106"
    )

    tools = [
            query_flow_db.query_flows_with_drop,
            query_flow_db.query_flows_without_drop,
            query_flow_db.query_flows_with_slow_rtt,
            query_flow_db.query_flows_with_slow_dns,
            query_flow_db.query_flows_with_netpol_drop
            ]

    # Get the prompt to use - you can modify this!
    prompt = hub.pull("hwchase17/openai-tools-agent")

    # Construct the OpenAI Tools agent
    llm_agent = create_openai_tools_agent(llm, tools, prompt)

    # Create an agent executor by passing in the agent and tools
    agent_executor = AgentExecutor(agent=llm_agent, tools=tools, verbose=verbose)

    return agent_executor

def netobserv_ai_server(agent_executor):
    app = FastAPI(
    title="LangChain Server",
    version="1.0",
    description="Spin up a simple api server using LangChain's Runnable interfaces",
    )
    # We need to add these input/output schemas because the current AgentExecutor
    # is lacking in schemas.
    class Input(BaseModel):
        input: str


    class Output(BaseModel):
        output: Any

    # Adds routes to the app for using the chain under:
    # /invoke
    # /batch
    # /stream
    # /stream_events
    add_routes(
        app,
        agent_executor.with_types(input_type=Input, output_type=Output).with_config(
            {"run_name": "agent"}
        ),
    )
    # Run the server
    uvicorn.run(app, host="localhost", port=8000)

if __name__ == '__main__':
    agent_executor = netobserv_ai_setup(verbose=True)
    # agent_executor.run("show me flows with drop")
    # agent_executor.run("show me flows with no drop")
    # agent_executor.run("show me flows with slow rtt")
    # agent_executor.invoke({"input": "show me flows with slow dns queries"})
    agent_executor.invoke({"input": "show me flows with netpol drop"})
    # netobserv_ai_server(agent_executor)

