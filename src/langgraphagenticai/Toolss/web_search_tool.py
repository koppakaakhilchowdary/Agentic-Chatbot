from langchain_community.tools.tavily_search import TavilySearchResults
from langgraph.prebuilt import ToolNode

class Tools:
    def get_tools():
        tools = [TavilySearchResults(max_results=2)]
        return tools
    def create_tool_node(tools):
        return ToolNode(tools)