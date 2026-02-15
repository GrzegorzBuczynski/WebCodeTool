"""Agent models and schemas."""

from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field
from enum import Enum
import uuid


class AgentRole(str, Enum):
    """Agent role types."""
    SYSTEM = "system"
    USER = "user"
    ASSISTANT = "assistant"
    TOOL = "tool"


class Message(BaseModel):
    """Chat message."""
    role: AgentRole
    content: str
    tool_call_id: Optional[str] = None
    name: Optional[str] = None


class ToolCall(BaseModel):
    """Tool call representation."""
    id: str = Field(default_factory=lambda: f"call_{uuid.uuid4().hex[:16]}")
    name: str
    parameters: Dict[str, Any]


class AgentRequest(BaseModel):
    """Request to execute an agent task."""
    messages: List[Message] = Field(default_factory=list)
    task: Optional[str] = None
    max_iterations: Optional[int] = 10
    stream: bool = False


class AgentStep(BaseModel):
    """Single step in agent execution."""
    step_number: int
    thought: Optional[str] = None
    tool_calls: List[ToolCall] = Field(default_factory=list)
    tool_results: Dict[str, Any] = Field(default_factory=dict)
    response: Optional[str] = None
    error: Optional[str] = None


class AgentResponse(BaseModel):
    """Response from agent execution."""
    success: bool
    steps: List[AgentStep] = Field(default_factory=list)
    final_response: str
    error: Optional[str] = None
    iterations: int = 0
