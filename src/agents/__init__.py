"""
Agents module initialization
"""

from .base_agent import BaseAgent
from .tax_agents import (
    TaxCalculatorAgent,
    DocumentAnalyzerAgent,
    ComplianceCheckerAgent,
    DeductionOptimizerAgent,
    FilingAssistantAgent
)

__all__ = [
    'BaseAgent',
    'TaxCalculatorAgent',
    'DocumentAnalyzerAgent',
    'ComplianceCheckerAgent',
    'DeductionOptimizerAgent',
    'FilingAssistantAgent'
]
