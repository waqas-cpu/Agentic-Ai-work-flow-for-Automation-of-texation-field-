"""
Tax Automation System - Main Package Initialization
"""

from .agents import (
    BaseAgent,
    TaxCalculatorAgent,
    DocumentAnalyzerAgent,
    ComplianceCheckerAgent,
    DeductionOptimizerAgent,
    FilingAssistantAgent
)
from .rag import TaxDocumentRAG
from .orchestrator import AgentOrchestrator
from .utils import Config, setup_logging

__version__ = "1.0.0"

__all__ = [
    'BaseAgent',
    'TaxCalculatorAgent',
    'DocumentAnalyzerAgent',
    'ComplianceCheckerAgent',
    'DeductionOptimizerAgent',
    'FilingAssistantAgent',
    'TaxDocumentRAG',
    'AgentOrchestrator',
    'Config',
    'setup_logging'
]
