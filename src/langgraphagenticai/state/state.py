from email import message
from numpy import add
from typing_extensions import TypedDict
from langgraph.graph.message import add_messages

class State(TypedDict):
    """
    Represent the structure of the state used in graph
    """
    message: Annotated[list,add_messages]