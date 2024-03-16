#!/usr/bin/python3
from secret_key import openapi_key
import os

os.environ['OPENAI_API_KEY'] = openapi_key
from langchain_openai import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
import query_flow_db

filters = ["drop", "no drop"]

def netobserv_flows_llm(filter):
    llm = OpenAI(temperature=0.7)
    query = llm("show me netobserv flows for specific netobserv flows with {filter}")
    # print(query)

    template_name = PromptTemplate(
        input_variables=[filter],
        template="show me netobserv flows with {filter}",
    )
    template_name.format(filter="specific netobserv flows")

    chain = LLMChain(llm=llm, prompt=template_name)
    switcher = {
        "drop": query_flow_db.query_flows_with_drop(),
        "no drop": query_flow_db.query_flows_without_drop(),
    }
    chain.run(switcher[filter])


if __name__ == '__main__':
    netobserv_flows_llm("drop")
    netobserv_flows_llm("no drop")
