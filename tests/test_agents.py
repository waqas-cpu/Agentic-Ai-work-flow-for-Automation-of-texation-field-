"""
Tests for agent functionality
"""

import pytest
import asyncio
from src.agents import (
    TaxCalculatorAgent,
    DocumentAnalyzerAgent,
    ComplianceCheckerAgent
)


@pytest.mark.asyncio
async def test_tax_calculator_agent():
    """Test tax calculator agent"""
    agent = TaxCalculatorAgent(agent_id="test_001")
    
    task = {
        "type": "income_tax",
        "data": {"income": 50000, "filing_status": "single"}
    }
    
    result = await agent.process_task(task)
    
    assert result["status"] == "success"
    assert result["agent_id"] == "test_001"


@pytest.mark.asyncio
async def test_document_analyzer_agent():
    """Test document analyzer agent"""
    agent = DocumentAnalyzerAgent(agent_id="test_002")
    
    task = {
        "document_type": "W-2",
        "content": "Employee wages: $60,000"
    }
    
    result = await agent.process_task(task)
    
    assert result["status"] == "success"
    assert result["document_type"] == "W-2"


@pytest.mark.asyncio
async def test_compliance_checker_agent():
    """Test compliance checker agent"""
    agent = ComplianceCheckerAgent(agent_id="test_003")
    
    task = {
        "filing_data": {"forms": ["1040"]},
        "jurisdiction": "federal"
    }
    
    result = await agent.process_task(task)
    
    assert result["status"] == "success"
    assert result["jurisdiction"] == "federal"


def test_agent_capabilities():
    """Test agent capability reporting"""
    agent = TaxCalculatorAgent(agent_id="test_001")
    
    capabilities = agent.get_capabilities()
    
    assert isinstance(capabilities, list)
    assert len(capabilities) > 0
    assert "income_tax_calculation" in capabilities


def test_agent_status():
    """Test agent status"""
    agent = TaxCalculatorAgent(agent_id="test_001")
    
    status = agent.get_status()
    
    assert status["agent_id"] == "test_001"
    assert "status" in status
    assert "tasks_completed" in status
