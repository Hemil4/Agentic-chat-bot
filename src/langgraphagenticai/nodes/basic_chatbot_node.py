from src.langgraphagenticai.state.state import State
from langchain_core.messages import HumanMessage

class BasicChatbotNode:
    """
    Basic Chatbot logic implementation
    """

    def __init__(self, model):
        self.llm = model

    def process(self, state: State) -> dict:
        """
        Processes the input state and generates a chatbot response.
        """
        messages = state.get('messages', [])
        
        # Generate response using the LLM
        response = self.llm.invoke(messages)
        
        # Return the response to be added to the messages
        return {"messages": [response]}