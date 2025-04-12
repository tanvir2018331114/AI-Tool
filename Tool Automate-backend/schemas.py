
from pydantic import BaseModel
from typing import List, Dict, Any

class ToolCreate(BaseModel):
    name: str
    description: str
    input_params: List[Dict[str, Any]]
    output_type: str
    code: str

class TaskRequest(BaseModel):
    task: str
