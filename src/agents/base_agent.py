"""
Base Agent Class for Taxation Automation
Provides common functionality for all specialized tax agents
"""

import asyncio
from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class BaseAgent(ABC):
    """
    Abstract base class for all tax automation agents.
    Defines the interface and common functionality.
    """
    
    def __init__(
        self,
        agent_id: str,
        agent_name: str,
        rag_system: Optional[Any] = None,
        llm_model: str = "gpt-4"
    ):
        """
        Initialize the base agent
        
        Args:
            agent_id: Unique identifier for the agent
            agent_name: Human-readable name
            rag_system: RAG system instance for document retrieval
            llm_model: Language model to use
        """
        self.agent_id = agent_id
        self.agent_name = agent_name
        self.rag_system = rag_system
        self.llm_model = llm_model
        self.status = "initialized"
        self.task_history: List[Dict[str, Any]] = []
        
        logger.info(f"Agent {self.agent_name} ({self.agent_id}) initialized")
    
    @abstractmethod
    async def process_task(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process a task assigned to this agent
        
        Args:
            task: Task specification dictionary
            
        Returns:
            Result dictionary with status and output
        """
        pass
    
    @abstractmethod
    def get_capabilities(self) -> List[str]:
        """
        Return list of capabilities this agent provides
        
        Returns:
            List of capability strings
        """
        pass
    
    async def retrieve_context(
        self,
        query: str,
        k: int = 5
    ) -> List[Dict[str, Any]]:
        """
        Retrieve relevant context from RAG system
        
        Args:
            query: Query for context retrieval
            k: Number of documents to retrieve
            
        Returns:
            List of relevant documents
        """
        if not self.rag_system:
            logger.warning(f"Agent {self.agent_name} has no RAG system")
            return []
        
        try:
            context = self.rag_system.retrieve(query, k=k)
            logger.info(f"Agent {self.agent_name} retrieved {len(context)} context documents")
            return context
        except Exception as e:
            logger.error(f"Failed to retrieve context: {e}")
            return []
    
    async def generate_response(
        self,
        prompt: str,
        context: Optional[List[Dict[str, Any]]] = None
    ) -> str:
        """
        Generate a response using LLM with optional context
        
        Args:
            prompt: User prompt
            context: Optional context from RAG
            
        Returns:
            Generated response
        """
        # Build full prompt with context
        full_prompt = self._build_prompt_with_context(prompt, context)
        
        # Simulate LLM call (in production, use actual LLM API)
        response = await self._call_llm(full_prompt)
        
        return response
    
    def _build_prompt_with_context(
        self,
        prompt: str,
        context: Optional[List[Dict[str, Any]]]
    ) -> str:
        """Build prompt with RAG context"""
        if not context:
            return prompt
        
        context_text = "\n\n".join([
            f"Context {i+1}:\n{doc['content']}"
            for i, doc in enumerate(context)
        ])
        
        full_prompt = f"""Based on the following context, answer the question.

Context:
{context_text}

Question: {prompt}

Answer:"""
        
        return full_prompt
    
    async def _call_llm(self, prompt: str) -> str:
        """
        Call LLM API (mock implementation)
        In production, integrate with actual LLM API
        """
        # Simulate API call delay
        await asyncio.sleep(0.1)
        
        # Mock response
        return f"[Response from {self.agent_name} using {self.llm_model}]: Processed request successfully"
    
    def log_task(self, task: Dict[str, Any], result: Dict[str, Any]):
        """Log completed task"""
        task_record = {
            "timestamp": datetime.now().isoformat(),
            "task": task,
            "result": result,
            "agent_id": self.agent_id
        }
        self.task_history.append(task_record)
        logger.info(f"Agent {self.agent_name} logged task completion")
    
    def get_status(self) -> Dict[str, Any]:
        """Get current agent status"""
        return {
            "agent_id": self.agent_id,
            "agent_name": self.agent_name,
            "status": self.status,
            "tasks_completed": len(self.task_history),
            "capabilities": self.get_capabilities()
        }
    
    def reset(self):
        """Reset agent state"""
        self.status = "initialized"
        self.task_history = []
        logger.info(f"Agent {self.agent_name} reset")
