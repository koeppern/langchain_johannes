from langchain.llms import OpenAI
from langchain.chains import ConversationChain
import os


llm = OpenAI(temperature=0)

conversation = ConversationChain(
    llm=llm, 
    verbose=True, 
    memory=ConversationBufferMemory()
)
conversation.predict(input="Hi there!")