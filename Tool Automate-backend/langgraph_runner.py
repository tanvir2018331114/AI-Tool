from typing_extensions import TypedDict
from langgraph.graph import StateGraph, END
from typing import Annotated, Dict, Any, Callable
from tool_runner import run_tool
from models import Tool
from langgraph.graph.message import add_messages
from langchain_core.runnables import Runnable, RunnableConfig
from langgraph.graph import END, StateGraph, START
from langgraph.prebuilt import tools_condition
from langchain_core.runnables import RunnableLambda
from langchain_core.messages import ToolMessage
from langgraph.prebuilt import ToolNode
from datetime import datetime
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.chat_models import ChatOpenAI
from langchain_core.tools import StructuredTool
from config import settings


class State(TypedDict):
    messages: Annotated[list, add_messages]


class ToolLogger:
    def __init__(self):
        self.called_tools = []

    def log_call(self, tool_name):
        self.called_tools.append(tool_name)
        
def wrap_tool_with_logger(tool, logger: ToolLogger):
    original_func = tool.func

    def wrapped_func(*args, **kwargs):
        logger.log_call(tool.name)
        return original_func(*args, **kwargs)

    tool.func = wrapped_func
    return tool

def convert_tool_to_langchain_tool(tool: Tool):
    
    local_namespace = {}
    exec(tool.code, {}, local_namespace)
    tool_func = local_namespace.get(tool.name.replace(" ", ""))

    if tool_func is None:
        raise ValueError(f"Failed to extract function from code for tool: {tool.name}")

    if not tool_func.__doc__:
        tool_func.__doc__ = tool.description

    return StructuredTool.from_function(tool_func)

class Assistant:
    def __init__(self, runnable: Runnable):
        self.runnable = runnable

    def __call__(self, state: State, config: RunnableConfig):
        while True:
            configuration = config.get("configurable", {})
            result = self.runnable.invoke(state)
            
            
            if not result.tool_calls and (
                not result.content
                or isinstance(result.content, list)
                and not result.content[0].get("text")
            ):
                messages = state["messages"] + [("user", "Respond with a real output.")]
                state = {**state, "messages": messages}
            else:
                break
        return {"messages": result}
    
def create_tool_node_with_fallback(tools: list) -> dict:
    return ToolNode(tools).with_fallbacks(
        [RunnableLambda(handle_tool_error)], exception_key="error"
    )


def handle_tool_error(state) -> dict:
    error = state.get("error")
    tool_calls = state["messages"][-1].tool_calls
    return {
        "messages": [
            ToolMessage(
                content=f"Error: {repr(error)}\n please fix your mistakes.",
                tool_call_id=tc["id"],
            )
            for tc in tool_calls
        ]
    }

def _print_event(event: dict, _printed: set, max_length=1500):
    message = event.get("messages")
    msg_repr=''
    if message:
        if isinstance(message, list):
            message = message[-1]
        if message.id not in _printed:
            msg_repr += message.content
            
            _printed.add(message.id)
    
    return msg_repr

def build_graph(tools: list[Tool]) -> StateGraph:
    builder = StateGraph(State)
    logger = ToolLogger()

    langchain_tools = [wrap_tool_with_logger(convert_tool_to_langchain_tool(tool), logger) for tool in tools]
    
    llm = ChatOpenAI(model="gpt-4-turbo-preview",openai_api_key=settings.openai_api_key)

    primary_assistant_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are a helpful assistant. Use provided tools.Calls these tools and executes them in correct order."
        ),
        ("assistant", "Let me assist you."),
        ("placeholder", "{messages}"),
    ]
    ).partial(time=datetime.now)
    
    runnable = primary_assistant_prompt | llm.bind_tools(langchain_tools)
    

    builder.add_node("assistant", Assistant(runnable))
    builder.add_node("tools", create_tool_node_with_fallback(langchain_tools))
    
    builder.add_edge(START, "assistant")
    builder.add_conditional_edges(
        "assistant",
        tools_condition,
    )
    builder.add_edge("tools", "assistant")

    graph = builder.compile()
    return graph, logger
        

    
