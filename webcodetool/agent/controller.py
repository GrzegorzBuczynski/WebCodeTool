"""Agent controller for managing agentic workflows."""

import asyncio
from typing import List, Dict, Any, Optional, AsyncGenerator
import json

from .models import AgentRequest, AgentResponse, AgentStep, Message, AgentRole, ToolCall
from ..mcp import tool_registry
from ..config import settings


class AgentController:
    """Controller for managing agent execution."""
    
    def __init__(self):
        self.max_iterations = settings.max_iterations
    
    async def execute(
        self, 
        request: AgentRequest
    ) -> AgentResponse:
        """Execute an agent task."""
        steps: List[AgentStep] = []
        messages = list(request.messages)
        
        # Add task as initial user message if provided
        if request.task:
            messages.append(Message(role=AgentRole.USER, content=request.task))
        
        max_iterations = request.max_iterations or self.max_iterations
        
        for iteration in range(max_iterations):
            step = AgentStep(step_number=iteration + 1)
            
            try:
                # For this basic implementation, we'll simulate agent thinking
                # In a real implementation, this would call an LLM
                step.thought = await self._generate_thought(messages)
                
                # Determine if we need to use tools
                tool_calls = await self._determine_tool_calls(messages, step.thought)
                step.tool_calls = tool_calls
                
                if tool_calls:
                    # Execute tools
                    for tool_call in tool_calls:
                        try:
                            result = await tool_registry.execute_tool(
                                tool_call.name,
                                tool_call.parameters
                            )
                            step.tool_results[tool_call.name] = str(result)
                        except Exception as e:
                            step.tool_results[tool_call.name] = f"Error: {str(e)}"
                    
                    # Add tool results to messages
                    for tool_call in tool_calls:
                        result = step.tool_results.get(tool_call.name, "No result")
                        messages.append(Message(
                            role=AgentRole.TOOL,
                            content=result,
                            name=tool_call.name,
                            tool_call_id=tool_call.id
                        ))
                else:
                    # Generate final response
                    step.response = await self._generate_response(messages, step.thought)
                    steps.append(step)
                    break
                
                steps.append(step)
                
            except Exception as e:
                step.error = str(e)
                steps.append(step)
                return AgentResponse(
                    success=False,
                    steps=steps,
                    final_response=f"Error in iteration {iteration + 1}: {str(e)}",
                    error=str(e),
                    iterations=iteration + 1
                )
        
        # Generate final response
        final_response = steps[-1].response if steps and steps[-1].response else \
            "Task completed. Check the steps for details."
        
        return AgentResponse(
            success=True,
            steps=steps,
            final_response=final_response,
            iterations=len(steps)
        )
    
    async def execute_stream(
        self,
        request: AgentRequest
    ) -> AsyncGenerator[str, None]:
        """Execute agent task with streaming responses."""
        messages = list(request.messages)
        
        if request.task:
            messages.append(Message(role=AgentRole.USER, content=request.task))
        
        max_iterations = request.max_iterations or self.max_iterations
        
        yield f"data: {json.dumps({'type': 'start', 'max_iterations': max_iterations})}\n\n"
        
        for iteration in range(max_iterations):
            yield f"data: {json.dumps({'type': 'iteration', 'number': iteration + 1})}\n\n"
            
            try:
                thought = await self._generate_thought(messages)
                yield f"data: {json.dumps({'type': 'thought', 'content': thought})}\n\n"
                
                tool_calls = await self._determine_tool_calls(messages, thought)
                
                if tool_calls:
                    for tool_call in tool_calls:
                        yield f"data: {json.dumps({'type': 'tool_call', 'name': tool_call.name, 'parameters': tool_call.parameters})}\n\n"
                        
                        try:
                            result = await tool_registry.execute_tool(
                                tool_call.name,
                                tool_call.parameters
                            )
                            result_str = str(result)
                            yield f"data: {json.dumps({'type': 'tool_result', 'name': tool_call.name, 'result': result_str})}\n\n"
                            
                            messages.append(Message(
                                role=AgentRole.TOOL,
                                content=result_str,
                                name=tool_call.name,
                                tool_call_id=tool_call.id
                            ))
                        except Exception as e:
                            yield f"data: {json.dumps({'type': 'tool_error', 'name': tool_call.name, 'error': str(e)})}\n\n"
                else:
                    response = await self._generate_response(messages, thought)
                    yield f"data: {json.dumps({'type': 'response', 'content': response})}\n\n"
                    yield f"data: {json.dumps({'type': 'done', 'iterations': iteration + 1})}\n\n"
                    break
                    
            except Exception as e:
                yield f"data: {json.dumps({'type': 'error', 'message': str(e)})}\n\n"
                break
    
    async def _generate_thought(self, messages: List[Message]) -> str:
        """Generate agent's thought process."""
        # Basic implementation - in production, this would call an LLM
        if not messages:
            return "Starting to analyze the task..."
        
        last_message = messages[-1]
        if last_message.role == AgentRole.TOOL:
            return f"Received tool result from {last_message.name}. Analyzing..."
        elif last_message.role == AgentRole.USER:
            return f"Understanding the user's request: {last_message.content[:100]}..."
        
        return "Continuing task execution..."
    
    async def _determine_tool_calls(
        self, 
        messages: List[Message], 
        thought: str
    ) -> List[ToolCall]:
        """Determine which tools to call based on context."""
        # Basic implementation - in production, this would use LLM function calling
        # For demo purposes, we'll return an empty list to complete quickly
        return []
    
    async def _generate_response(self, messages: List[Message], thought: str) -> str:
        """Generate final response to user."""
        # Basic implementation - in production, this would call an LLM
        if not messages:
            return "Task completed successfully."
        
        last_user_message = None
        for msg in reversed(messages):
            if msg.role == AgentRole.USER:
                last_user_message = msg
                break
        
        if last_user_message:
            return f"I understand your request: '{last_user_message.content}'. The agentic coding server is now active and ready to process tasks with available tools."
        
        return "Agent execution completed. All tools are available and ready for use."
