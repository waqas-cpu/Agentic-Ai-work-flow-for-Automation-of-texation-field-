"""
Tests for orchestrator
"""

import pytest
import asyncio
from src.orchestrator import AgentOrchestrator
from src.rag import TaxDocumentRAG


@pytest.mark.asyncio
async def test_orchestrator_initialization():
    """Test orchestrator initialization"""
    rag = TaxDocumentRAG(embedding_model="huggingface")
    orchestrator = AgentOrchestrator(rag_system=rag)
    
    assert orchestrator is not None
    assert len(orchestrator.agents) == 5  # 5 specialized agents


@pytest.mark.asyncio
async def test_parallel_task_execution():
    """Test parallel task execution"""
    rag = TaxDocumentRAG(embedding_model="huggingface")
    orchestrator = AgentOrchestrator(rag_system=rag)
    
    tasks = [
        {"agent_type": "calculation", "data": {"income": 50000}},
        {"agent_type": "document", "document_type": "W-2", "content": "test"}
    ]
    
    results = await orchestrator.process_tasks_parallel(tasks)
    
    assert len(results) == 2
    assert all(r.get("status") in ["success", "error"] for r in results)


@pytest.mark.asyncio
async def test_workflow_execution():
    """Test workflow execution"""
    rag = TaxDocumentRAG(embedding_model="huggingface")
    orchestrator = AgentOrchestrator(rag_system=rag)
    
    workflow = {
        "name": "Test Workflow",
        "steps": [
            {
                "name": "Step 1",
                "type": "parallel",
                "tasks": [
                    {"agent_type": "calculation", "data": {"income": 50000}}
                ]
            }
        ]
    }
    
    result = await orchestrator.process_workflow(workflow)
    
    assert result["workflow_name"] == "Test Workflow"
    assert result["status"] == "completed"
    assert len(result["steps"]) == 1


def test_agent_status():
    """Test getting agent status"""
    rag = TaxDocumentRAG(embedding_model="huggingface")
    orchestrator = AgentOrchestrator(rag_system=rag)
    
    status = orchestrator.get_agent_status()
    
    assert len(status) == 5
    assert "tax_calculator" in status
    assert "document_analyzer" in status


def test_orchestrator_statistics():
    """Test orchestrator statistics"""
    rag = TaxDocumentRAG(embedding_model="huggingface")
    orchestrator = AgentOrchestrator(rag_system=rag)
    
    stats = orchestrator.get_statistics()
    
    assert stats["total_agents"] == 5
    assert "max_parallel_agents" in stats
    assert "active_tasks" in stats
