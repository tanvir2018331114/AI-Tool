from models import Tool
from sqlalchemy.orm import Session
from embedding_utils import get_embedding
from langgraph_runner import build_graph
import numpy as np

def cosine_similarity(a, b):
    a, b = np.array(a), np.array(b)
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

def match_tools(task: str, db: Session, threshold: float = 0.75):
    task_embedding = get_embedding(task)
    tools = db.query(Tool).all()
    
    matches = []
    for tool in tools:
        if tool.embedding:
            similarity = cosine_similarity(task_embedding, tool.embedding)
            if similarity > threshold:
                matches.append((similarity, tool))
        else:
            if tool.name.lower() in task.lower() or any(word in task.lower() for word in tool.description.lower().split()):
                matches.append((0.5, tool))

    matches.sort(reverse=True)
    return [tool for _, tool in matches]

def execute_workflow(task: str, db: Session):
    tools = match_tools(task, db)
    if not tools:
        return [{"tool": "None", "result": "No tools matched"}]

    
    graph, logger = build_graph(tools)
    result = graph.invoke({"messages": ("user", task)})
    

    called_tools = logger.called_tools
    
    nodes = [{"id": "assistant", 
              "type": "default",
        "data": {"label": "Assistant"},"position": {"x": 250, "y": 0}}]
    y_offset = 100
    current_y = y_offset
    for tool_name in called_tools:
        nodes.append({"id": tool_name,"type": "default", "data": {"label": tool_name},"position": {"x": 250, "y": current_y}})
        current_y += y_offset

    edges = []
    last_node = "assistant"
    for tool_name in called_tools:
        edges.append({"id": f"{last_node}-{tool_name}","source": last_node, "target": tool_name})
        last_node = tool_name
    edges.append({"id": f"{last_node}-{tool_name}","source": last_node, "target": "assistant"})
    
    return {
        "nodes": nodes,
        "edges": edges,
        "result":result
    }
