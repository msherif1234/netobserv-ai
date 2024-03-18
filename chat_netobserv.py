#!/usr/bin/python3
from secret_key import openapi_key
import os

os.environ['OPENAI_API_KEY'] = openapi_key
from langchain.chat_models import ChatOpenAI
from langchain.chains.conversation.memory import ConversationBufferWindowMemory
from langchain.agents import initialize_agent
from langchain.agents import Tool

import query_flow_db

filters = ["drop", "no drop", "slow rtt", "slow dns"]

fixed_prompt = '''Assistant is a large language model trained by OpenAI.
Assistant is designed to be able to assist with a wide range of tasks, from answering simple questions to providing in-depth explanations and discussions on a wide range of topics. As a language model, Assistant is able to generate human-like text based on the input it receives, allowing it to engage in natural-sounding conversations and provide responses that are coherent and relevant to the topic at hand.
Assistant doesn't know anything about flows with drops or with no drops or flows with slow rtt or slow dns queries and should use a tool for questions about these topics.
Assistant is constantly learning and improving, and its capabilities are constantly evolving. It is able to process and understand large amounts of text, and can use this knowledge to provide accurate and informative responses to a wide range of questions. Additionally, Assistant is able to generate its own text based on the input it receives, allowing it to engage in discussions and provide explanations and descriptions on a wide range of topics.
Overall, Assistant is a powerful system that can help with a wide range of tasks and provide valuable insights and information on a wide range of topics. Whether you need help with a specific question or just want to have a conversation about a particular topic, Assistant is here to assist.'''

def netobserv_ai_setup():
    turbo_llm = ChatOpenAI(
        temperature=0, # using low temperature for more predictable results
        model_name='gpt-3.5-turbo'
    )
    query_flows_with_drops_tool = Tool(
        name='Find all netobserv flows with drop',
        func=query_flow_db.query_flows_with_drop,
        description="Useful for when you need to answer a question about a flow with drop",
    )
    query_flows_with_no_drops_tool = Tool(
        name='Find all netobserv flows with no drop',
        func=query_flow_db.query_flows_without_drop,
        description="Useful for when you need to answer a question about a flow without drop",
    )
    query_flows_with_slow_rtt_tool = Tool(
        name='Find all netobserv flows with slow rtt',
        func=query_flow_db.query_flows_with_slow_rtt,
        description="Useful for when you need to answer a question about a flow with slow rtt",
    )
    query_flows_with_slow_dns_tool = Tool(
        name='Find all netobserv flows with slow dns',
        func=query_flow_db.query_flows_with_slow_dns,
        description="Useful for when you need to answer a question about a flow with slow dns",
    )
    tools = [
            query_flows_with_drops_tool,
            query_flows_with_no_drops_tool,
            query_flows_with_slow_rtt_tool,
            query_flows_with_slow_dns_tool,
            ]
    # conversational agent memory
    memory = ConversationBufferWindowMemory(
        memory_key='chat_history',
        k=3,
        return_messages=True
    )

    # create our agent
    conversational_agent = initialize_agent(
        agent='chat-conversational-react-description',
        tools=tools,
        llm=turbo_llm,
        verbose=False, # set to True for more verbose output
        max_iterations=3,
        early_stopping_method='generate',
        handle_parsing_errors=True,
        memory=memory
    )
    conversational_agent.agent.llm_chain.prompt.messages[0].prompt.template = fixed_prompt
    return conversational_agent


if __name__ == '__main__':
    agent = netobserv_ai_setup()
    # agent.run("show me flows with drop")
    # agent.run("show me flows with no drop")
    # agent.run("show me flows with slow rtt")
    agent.run("show me flows with slow dns")

