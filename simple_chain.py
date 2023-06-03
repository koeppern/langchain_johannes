# simple_chain.py
# 2023-06-02, J. Köppern
# See https://python.langchain.com/en/latest/getting_started/getting_started.html, Last updated on Jun 02, 2023

# Simple chain with prompt template and OpenAI LLM to answer question in Stremlit app

import streamlit as st
import os
import configparser
import openai
from langchain.llms import OpenAI

from langchain.agents import load_tools
from langchain.agents import initialize_agent
from langchain.agents import AgentType


# Load open_ai_key from config.ini
config_filename = "C://config//cofig.ini"

config = configparser.ConfigParser()

config.read(config_filename)
 
open_ai_key = config['DEFAULT']['OPENAI_API_KEY']

google_api_key = config['DEFAULT']['GOOGLE_API']

# Alternatively you can set open_ai_key directly here, like
# open_ai_key = "HERECOMESMYKEY"

os.environ["OPENAI_API_KEY"] = open_ai_key

os.environ["SERPAPI_API_KEY"] = google_api_key

# Configure LangChain objects
llm = OpenAI(temperature=0.9)

# Main app
st.title("💬Ask GPT a question via LangChain")

st.header("Simple prompt to LLM")

text = st.text_input("Enter a prompt")

if text != "":
    st.write(llm(text))

# Prompt template
st.header("LangCHain with prompt template primitive")

from langchain.prompts import PromptTemplate

prompt = PromptTemplate(
    input_variables=["product"],
    template="What is a good name for a company that makes {product}?",
)

text_prompt = st.text_input("What does the company you are looking for a name?")

if text_prompt != "":
    st.write("This is the prompt: " + prompt.format(product=text_prompt))

    st.write(llm(prompt.format(product=text_prompt)))

# Chains
from langchain.chains import LLMChain

st.header("Chains")

st.write("This section is doing the same like the one above but chaining all primitives together in one chain.")

text_chain = st.text_input("What does the company you are looking for a name? (chain)")

chain = LLMChain(llm=llm, prompt=prompt)

if text_chain != "":
    st.write(
        chain.run(
            text_chain
        )
)

# Conversation
st.header("Conversation💬🗨️")

from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory

# Check if 'memory' key exists in session state, if not, initialize it
if 'memory' not in st.session_state:
    st.session_state['memory'] = ConversationBufferMemory()

# Access 'memory' using st.session_state['memory']
memory = st.session_state['memory']

conversation = ConversationChain(
    llm=llm,
    verbose=True, 
    memory=memory
)

text_conversation = st.text_input("What does the company you are looking for a name? (conversation)")

if text_conversation != "":
    st.write(
        conversation.predict(input=text_conversation)  + "\n"
)

# Tools
st.header("Tools⛏️")
   
from langchain.utilities import TextRequestsWrapper

requests = TextRequestsWrapper()

if st.button("Hier"):
    st.write(
        requests.get(
            "https://www.tagesschau.de"
        )
)
       

# Agents
st.header("Agent😎")

#tools = load_tools(["llm-math"], llm=llm)
ools = load_tools(["serpapi", "llm-math"], llm=llm)


# Finally, let's initialize an agent with the tools, the language model, and the type of agent we want to use.
agent = initialize_agent(tools, llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=True)


go = st.button("Click")

if go:
    question = "what's the areas of the circle with the eifel tower's height as radius in square meters and how did you calculate it think step-by-step"

    reply = agent.run(question)

    st.write(reply)

