from src.langgraphagenticai.state.state import State
from src.langgraphagenticai.Toolss.web_search_tool import Tools

class ChatbotToolNode:
    def __init__(self,model):
        self.llm = model
        
    def process(self, state: State)->dict:
        user_input = state['messages'][-1] if state['messages'] else ""
        llm_message = self.llm.invoke([{"role":"user","content":user_input}])
        tools_response = f"Tool integration for: {user_input}"
        return {"messages":[llm_message,tools_response]}
    def create_chatbot(self,tools):
        llm_with_tools = self.llm.bind_tools(tools)
        def chatbot_node(state:State):
            return {"messages": [llm_with_tools.invoke(state["messages"])]}
        return chatbot_node