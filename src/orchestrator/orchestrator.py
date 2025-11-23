"""
Agent Orchestrator - Manages Multiple Agents Working in Parallel
Coordinates task distribution and parallel execution
"""

import asyncio
from typing import Dict, Any, List, Optional
from concurrent.futures import ThreadPoolExecutor
import logging
from datetime import datetime

from ..agents import (
    TaxCalculatorAgent,
    DocumentAnalyzerAgent,
    ComplianceCheckerAgent,
    DeductionOptimizerAgent,
    FilingAssistantAgent
)

logger = logging.getLogger(__name__)


class AgentOrchestrator:
    """
    Orchestrates multiple tax agents working in parallel.
    Handles task routing, load balancing, and result aggregation.
    """
    
    def __init__(
        self,
        rag_system=None,
        max_parallel_agents: int = 5,
        llm_model: str = "gpt-4"
    ):
        """
        Initialize the orchestrator
        
        Args:
            rag_system: RAG system instance for agents
            max_parallel_agents: Maximum number of agents to run in parallel
            llm_model: LLM model for agents
        """
        self.rag_system = rag_system
        self.max_parallel_agents = max_parallel_agents
        self.llm_model = llm_model
        
        # Initialize agent pool
        self.agents = self._initialize_agents()
        
        # Task queue and execution tracking
        self.task_queue: asyncio.Queue = asyncio.Queue()
        self.active_tasks: Dict[str, Any] = {}
        self.completed_tasks: List[Dict[str, Any]] = []
        
        logger.info(f"Orchestrator initialized with {len(self.agents)} agents")
    
    def _initialize_agents(self) -> Dict[str, Any]:
        """Initialize all specialized agents"""
        agents = {
            "tax_calculator": TaxCalculatorAgent(
                agent_id="calc_001",
                rag_system=self.rag_system,
                llm_model=self.llm_model
            ),
            "document_analyzer": DocumentAnalyzerAgent(
                agent_id="doc_001",
                rag_system=self.rag_system,
                llm_model=self.llm_model
            ),
            "compliance_checker": ComplianceCheckerAgent(
                agent_id="comp_001",
                rag_system=self.rag_system,
                llm_model=self.llm_model
            ),
            "deduction_optimizer": DeductionOptimizerAgent(
                agent_id="deduct_001",
                rag_system=self.rag_system,
                llm_model=self.llm_model
            ),
            "filing_assistant": FilingAssistantAgent(
                agent_id="file_001",
                rag_system=self.rag_system,
                llm_model=self.llm_model
            )
        }
        return agents
    
    async def process_tasks_parallel(
        self,
        tasks: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """
        Process multiple tasks in parallel using appropriate agents
        
        Args:
            tasks: List of task dictionaries
            
        Returns:
            List of results from all tasks
        """
        logger.info(f"Processing {len(tasks)} tasks in parallel")
        
        # Create async tasks for each input task
        async_tasks = []
        for task in tasks:
            agent = self._route_task(task)
            if agent:
                async_task = asyncio.create_task(
                    self._execute_task(agent, task)
                )
                async_tasks.append(async_task)
        
        # Execute all tasks concurrently
        results = await asyncio.gather(*async_tasks, return_exceptions=True)
        
        # Process results
        processed_results = []
        for i, result in enumerate(results):
            if isinstance(result, Exception):
                logger.error(f"Task {i} failed with exception: {result}")
                processed_results.append({
                    "status": "error",
                    "error": str(result),
                    "task_index": i
                })
            else:
                processed_results.append(result)
        
        logger.info(f"Completed {len(processed_results)} tasks")
        return processed_results
    
    def _route_task(self, task: Dict[str, Any]) -> Optional[Any]:
        """
        Route task to appropriate agent based on task type
        
        Args:
            task: Task dictionary
            
        Returns:
            Selected agent or None
        """
        task_type = task.get("agent_type", "")
        
        agent_mapping = {
            "calculation": "tax_calculator",
            "document": "document_analyzer",
            "compliance": "compliance_checker",
            "deduction": "deduction_optimizer",
            "filing": "filing_assistant"
        }
        
        agent_key = agent_mapping.get(task_type)
        if agent_key and agent_key in self.agents:
            logger.debug(f"Routing task to {agent_key}")
            return self.agents[agent_key]
        
        # Default to tax calculator if type not specified
        logger.warning(f"Unknown task type: {task_type}, using default agent")
        return self.agents.get("tax_calculator")
    
    async def _execute_task(
        self,
        agent: Any,
        task: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Execute a single task with an agent
        
        Args:
            agent: Agent instance
            task: Task dictionary
            
        Returns:
            Task result
        """
        task_id = task.get("task_id", f"task_{datetime.now().timestamp()}")
        
        try:
            # Record task start
            self.active_tasks[task_id] = {
                "agent": agent.agent_name,
                "start_time": datetime.now(),
                "status": "running"
            }
            
            # Execute task
            result = await agent.process_task(task)
            result["task_id"] = task_id
            
            # Record completion
            completion_record = {
                "task_id": task_id,
                "agent": agent.agent_name,
                "start_time": self.active_tasks[task_id]["start_time"],
                "end_time": datetime.now(),
                "result": result
            }
            self.completed_tasks.append(completion_record)
            
            # Remove from active tasks
            del self.active_tasks[task_id]
            
            return result
            
        except Exception as e:
            logger.error(f"Task execution failed: {e}")
            if task_id in self.active_tasks:
                del self.active_tasks[task_id]
            return {
                "status": "error",
                "task_id": task_id,
                "error": str(e)
            }
    
    async def process_workflow(
        self,
        workflow: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Process a complex workflow with multiple steps
        Some steps can run in parallel, others sequentially
        
        Args:
            workflow: Workflow specification
            
        Returns:
            Workflow results
        """
        logger.info(f"Processing workflow: {workflow.get('name', 'unnamed')}")
        
        workflow_results = {
            "workflow_name": workflow.get("name", "unnamed"),
            "start_time": datetime.now().isoformat(),
            "steps": []
        }
        
        steps = workflow.get("steps", [])
        
        for step in steps:
            step_type = step.get("type", "parallel")
            tasks = step.get("tasks", [])
            
            if step_type == "parallel":
                # Execute tasks in parallel
                step_results = await self.process_tasks_parallel(tasks)
            else:
                # Execute tasks sequentially
                step_results = []
                for task in tasks:
                    agent = self._route_task(task)
                    if agent:
                        result = await self._execute_task(agent, task)
                        step_results.append(result)
            
            workflow_results["steps"].append({
                "step_name": step.get("name", "unnamed_step"),
                "step_type": step_type,
                "results": step_results
            })
        
        workflow_results["end_time"] = datetime.now().isoformat()
        workflow_results["status"] = "completed"
        
        logger.info(f"Workflow completed: {workflow_results['workflow_name']}")
        return workflow_results
    
    def get_agent_status(self) -> Dict[str, Any]:
        """Get status of all agents"""
        return {
            agent_name: agent.get_status()
            for agent_name, agent in self.agents.items()
        }
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get orchestrator statistics"""
        return {
            "total_agents": len(self.agents),
            "max_parallel_agents": self.max_parallel_agents,
            "active_tasks": len(self.active_tasks),
            "completed_tasks": len(self.completed_tasks),
            "agent_status": self.get_agent_status()
        }
    
    async def shutdown(self):
        """Gracefully shutdown the orchestrator"""
        logger.info("Shutting down orchestrator")
        
        # Wait for active tasks to complete
        if self.active_tasks:
            logger.info(f"Waiting for {len(self.active_tasks)} active tasks")
            await asyncio.sleep(1)
        
        # Reset all agents
        for agent in self.agents.values():
            agent.reset()
        
        logger.info("Orchestrator shutdown complete")
