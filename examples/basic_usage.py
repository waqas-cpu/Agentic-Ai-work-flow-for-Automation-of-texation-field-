"""
Example: Basic Usage of Tax Automation System with RAG
Demonstrates parallel agent execution with document retrieval
"""

import asyncio
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.rag import TaxDocumentRAG
from src.orchestrator import AgentOrchestrator
from src.utils import setup_logging, Config


async def main():
    """Main example function"""
    
    # Setup logging
    setup_logging(log_level="INFO")
    
    print("=" * 70)
    print("Tax Automation System - Basic Example")
    print("Demonstrating Parallel Agent Execution with RAG")
    print("=" * 70)
    print()
    
    # Initialize configuration
    config = Config()
    print(f"✓ Configuration loaded")
    
    # Initialize RAG system
    print(f"✓ Initializing RAG system...")
    rag_system = TaxDocumentRAG(
        embedding_model="huggingface",  # Using HuggingFace for demo
        vector_store_type="chroma",
        chunk_size=500,
        chunk_overlap=50
    )
    
    # Ingest sample tax documents
    print(f"✓ Ingesting sample tax documents...")
    sample_documents = [
        """
        Federal Income Tax Rules for 2024:
        - Standard deduction for single filers: $14,600
        - Standard deduction for married filing jointly: $29,200
        - Tax brackets: 10%, 12%, 22%, 24%, 32%, 35%, 37%
        - Personal exemption: None (suspended until 2025)
        """,
        """
        Tax Deduction Guidelines:
        - Mortgage interest is deductible up to $750,000 of debt
        - State and local tax (SALT) deduction limited to $10,000
        - Charitable contributions: Up to 60% of AGI for cash
        - Medical expenses: Deductible if exceed 7.5% of AGI
        """,
        """
        Business Tax Information:
        - Self-employment tax: 15.3% (12.4% Social Security + 2.9% Medicare)
        - Qualified Business Income (QBI) deduction: Up to 20%
        - Home office deduction available for qualified taxpayers
        - Vehicle expenses can be deducted using standard mileage rate
        """
    ]
    
    rag_system.ingest_documents(
        documents=sample_documents,
        metadata=[
            {"type": "federal_rules", "year": 2024},
            {"type": "deduction_guide", "year": 2024},
            {"type": "business_tax", "year": 2024}
        ]
    )
    
    # Initialize orchestrator with agents
    print(f"✓ Initializing agent orchestrator...")
    orchestrator = AgentOrchestrator(
        rag_system=rag_system,
        max_parallel_agents=5
    )
    
    # Display agent capabilities
    print(f"\n✓ Available agents and capabilities:")
    agent_status = orchestrator.get_agent_status()
    for agent_name, status in agent_status.items():
        print(f"\n  {status['agent_name']}:")
        for capability in status['capabilities']:
            print(f"    - {capability}")
    
    # Define tasks to run in parallel
    print(f"\n" + "=" * 70)
    print("Executing Parallel Tasks")
    print("=" * 70)
    
    tasks = [
        {
            "task_id": "task_1",
            "agent_type": "calculation",
            "type": "income_tax",
            "data": {
                "income": 75000,
                "filing_status": "single"
            }
        },
        {
            "task_id": "task_2",
            "agent_type": "document",
            "document_type": "W-2",
            "content": "Employee wages: $75,000, Federal tax withheld: $8,500"
        },
        {
            "task_id": "task_3",
            "agent_type": "deduction",
            "taxpayer_data": {
                "mortgage_interest": 12000,
                "charitable_donations": 3000,
                "medical_expenses": 8000
            },
            "tax_year": 2024
        },
        {
            "task_id": "task_4",
            "agent_type": "compliance",
            "filing_data": {
                "forms": ["1040", "Schedule A"],
                "deadline": "April 15, 2025"
            },
            "jurisdiction": "federal"
        },
        {
            "task_id": "task_5",
            "agent_type": "filing",
            "filing_type": "1040",
            "taxpayer_info": {
                "name": "John Doe",
                "ssn": "XXX-XX-XXXX",
                "filing_status": "single"
            }
        }
    ]
    
    print(f"\nStarting {len(tasks)} tasks in parallel...")
    print()
    
    # Execute tasks in parallel
    results = await orchestrator.process_tasks_parallel(tasks)
    
    # Display results
    print(f"\n" + "=" * 70)
    print("Task Results")
    print("=" * 70)
    
    for i, result in enumerate(results, 1):
        print(f"\n--- Task {i} ---")
        print(f"Status: {result.get('status', 'unknown')}")
        print(f"Agent: {result.get('agent_id', 'unknown')}")
        
        if result.get('status') == 'success':
            print(f"Context documents used: {result.get('context_used', 0)}")
            
            # Display task-specific info
            if 'calculation' in result:
                print(f"Calculation: {result['calculation']}")
            elif 'analysis' in result:
                print(f"Analysis: {result['analysis']}")
            elif 'optimization_suggestions' in result:
                print(f"Optimization: {result['optimization_suggestions']}")
            elif 'compliance_status' in result:
                print(f"Compliance: {result['compliance_status']}")
            elif 'guidance' in result:
                print(f"Filing Guidance: {result['guidance']}")
        else:
            print(f"Error: {result.get('error', 'Unknown error')}")
    
    # Display orchestrator statistics
    print(f"\n" + "=" * 70)
    print("System Statistics")
    print("=" * 70)
    
    stats = orchestrator.get_statistics()
    print(f"\nTotal agents: {stats['total_agents']}")
    print(f"Max parallel agents: {stats['max_parallel_agents']}")
    print(f"Active tasks: {stats['active_tasks']}")
    print(f"Completed tasks: {stats['completed_tasks']}")
    
    # RAG system stats
    rag_stats = rag_system.get_stats()
    print(f"\nRAG System:")
    print(f"  Vector store: {rag_stats['vector_store_path']}")
    print(f"  Chunk size: {rag_stats['chunk_size']}")
    print(f"  Initialized: {rag_stats['vector_store_initialized']}")
    
    # Shutdown
    print(f"\n✓ Shutting down orchestrator...")
    await orchestrator.shutdown()
    
    print(f"\n" + "=" * 70)
    print("Example completed successfully!")
    print("=" * 70)


if __name__ == "__main__":
    asyncio.run(main())
