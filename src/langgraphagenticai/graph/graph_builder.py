from langgraph.graph import StateGraph, START, END
from src.langgraphagenticai.nodes.basic_chatbot_node import BasicChatbotNode
from src.langgraphagenticai.state.state import State
from src.langgraphagenticai.Toolss.web_search_tool import Tools
from langgraph.prebuilt import tools_condition
from src.langgraphagenticai.nodes.chatbot_with_tool import ChatbotToolNode
from src.langgraphagenticai.nodes.ai_news_node import AINewsNode

class GraphBuilder:
    def __init__(self,model):
        self.llm = model
        self.graph_builder = StateGraph(State)
        
    def basic_chatbot_build_graph(self):
        """
            Builds a basic chatbot graph using LangGraph.
            This method initializes a chatbot node using the BasicChatbotNode class
            and integrates it into the graph. The chatbot node is set as both the
            entry and exit point of the graph.
        """
        self.basic_chatbot_node = BasicChatbotNode(self.llm)
        self.graph_builder.add_node("chatbot",self.basic_chatbot_node.process)
        self.graph_builder.add_edge(START,"chatbot")
        self.graph_builder.add_edge("chatbot",END)
    
    def chatbot_with_tool_graph(self):
        tools = Tools.get_tools()
        tool_node = Tools.create_tool_node(tools)
        
        chatbot_with_tool = ChatbotToolNode(self.llm)
        chatbot_node = chatbot_with_tool.create_chatbot(tools)
        self.graph_builder.add_node("chatbot",chatbot_node)
        self.graph_builder.add_node("tools",tool_node)
        self.graph_builder.add_edge(START,"chatbot")
        self.graph_builder.add_conditional_edges("chatbot", tools_condition)
        self.graph_builder.add_edge("tools","chatbot")
        self.graph_builder.add_edge("chatbot",END)        
        
    def ai_news_graph(self):
        ai_news = AINewsNode(self.llm)
        
        self.graph_builder.add_node("fetch_news",ai_news.fetch_news)
        self.graph_builder.add_node("summarize",ai_news.summarize_news)
        self.graph_builder.add_node("save_result",ai_news.save_result)
        
        self.graph_builder.set_entry_point("fetch_news")
        self.graph_builder.add_edge("fetch_news","summarize")
        self.graph_builder.add_edge("summarize","save_result")
        self.graph_builder.add_edge("save_result",END)
        print("No error")
        
    
    def setup_graph(self, usecase: str):
        """
        sets up the graph for selected use case.
        """
        if usecase=="Basic Chatbot":
            self.basic_chatbot_build_graph()
        if usecase == "Chatbot with Tool":
            self.chatbot_with_tool_graph()
        if usecase == "AI News":
            self.ai_news_graph()
        return self.graph_builder.compile()