from typing import Annotated

from langchain_core.messages import HumanMessage
from typing_extensions import TypedDict

from langgraph.graph import StateGraph
from langgraph.graph.message import add_messages
from langchain_openai import AzureChatOpenAI
from dotenv import load_dotenv

# Inspirado no exemplo em:
# https://python.langchain.com/docs/integrations/providers/langfuse/

load_dotenv()

class State(TypedDict):
    messages: Annotated[list, add_messages]

graph_builder = StateGraph(State)

chat = AzureChatOpenAI(
    temperature=0
)

def chatbot(state: State):
    return {"messages": [chat.invoke(state["messages"])]}

# Criando um grafo simples com langgraph
graph_builder.add_node("node1", chatbot)
graph_builder.add_node("node2", chatbot)
graph_builder.add_edge("node1", "node2")
graph_builder.set_entry_point("node1")
graph_builder.set_finish_point("node2")
graph = graph_builder.compile()

from langfuse.callback import CallbackHandler
import os

langfuse_handler = CallbackHandler(
  secret_key=os.getenv("LANGFUSE_SECRET_KEY"),
    public_key=os.getenv("LANGFUSE_PUBLIC_KEY"),
    host=os.getenv("LANGFUSE_HOST")
)

for s in graph.stream({"messages": [HumanMessage(content = "O que é o langfuse?")]},
                      config={"callbacks": [langfuse_handler]}):
    print(s)
