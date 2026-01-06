from src.langgraphagenticai.LLMs.groqllm import GroqLLM
from src.langgraphagenticai.state.state import State

class BasicChatbotNode:
    """
    This is basic chatbot implementation
    """
    def __init__(self,model):
        self.llm = model
    def process(self, state:State)-> dict:
        """
            Process the user input and generates a chatbot response.
        """
        return {"messages": self.llm.invoke(state["messages"])}