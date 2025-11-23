"""
Example: Complex Workflow with Sequential and Parallel Steps
Demonstrates a realistic tax filing workflow with multiple stages
"""

import asyncio
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.rag import TaxDocumentRAG
from src.orchestrator import AgentOrchestrator
from src.utils import setup_logging


async def main():
    """Main workflow example"""
    
    # Setup
    setup_logging(log_level="INFO")
    
    print("=" * 70)
    print("Tax Automation System - Complex Workflow Example")
    print("=" * 70)
    print()
    
    # Initialize systems
    rag_system = TaxDocumentRAG(
        embedding_model="huggingface",
        vector_store_type="chroma"
    )
    
    # Load comprehensive tax knowledge base
    print("Loading tax knowledge base...")
    tax_documents = [
        "Tax code section 179: Business equipment deduction...",
        "Form 1040 instructions: Line-by-line filing guide...",
        "State tax regulations: Multi-state filing requirements...",
        "IRS Publication 17: Your Federal Income Tax guide..."
    ]
    
    rag_system.ingest_documents(
        documents=tax_documents,
        metadata=[{"source": "irs", "type": f"doc_{i}"} for i in range(len(tax_documents))]
    )
    
    orchestrator = AgentOrchestrator(rag_system=rag_system)
    
    # Define complex workflow
    workflow = {
        "name": "Complete Tax Filing Workflow",
        "steps": [
            {
                "name": "Document Collection",
                "type": "parallel",
                "tasks": [
                    {
                        "agent_type": "document",
                        "document_type": "W-2",
                        "content": "Wages $80,000, Tax withheld $12,000"
                    },
                    {
                        "agent_type": "document",
                        "document_type": "1099-INT",
                        "content": "Interest income: $500"
                    },
                    {
                        "agent_type": "document",
                        "document_type": "Receipt",
                        "content": "Charitable donation: $2,500"
                    }
                ]
            },
            {
                "name": "Tax Calculation & Optimization",
                "type": "parallel",
                "tasks": [
                    {
                        "agent_type": "calculation",
                        "type": "total_tax",
                        "data": {"total_income": 80500, "filing_status": "married"}
                    },
                    {
                        "agent_type": "deduction",
                        "taxpayer_data": {
                            "standard_deduction": 29200,
                            "itemized_total": 25000
                        },
                        "tax_year": 2024
                    }
                ]
            },
            {
                "name": "Compliance Check",
                "type": "sequential",
                "tasks": [
                    {
                        "agent_type": "compliance",
                        "filing_data": {"forms": ["1040"], "state": "CA"},
                        "jurisdiction": "federal"
                    }
                ]
            },
            {
                "name": "Filing Preparation",
                "type": "sequential",
                "tasks": [
                    {
                        "agent_type": "filing",
                        "filing_type": "1040",
                        "taxpayer_info": {"name": "Jane & John Smith"}
                    }
                ]
            }
        ]
    }
    
    print("\nExecuting workflow with mixed parallel and sequential steps...")
    print()
    
    # Execute workflow
    results = await orchestrator.process_workflow(workflow)
    
    # Display results
    print(f"\n" + "=" * 70)
    print(f"Workflow Results: {results['workflow_name']}")
    print("=" * 70)
    
    for step in results['steps']:
        print(f"\n--- {step['step_name']} ({step['step_type']}) ---")
        print(f"Tasks completed: {len(step['results'])}")
        
        for task_result in step['results']:
            if task_result.get('status') == 'success':
                print(f"  ✓ {task_result.get('agent_id', 'unknown')}: Success")
            else:
                print(f"  ✗ Error: {task_result.get('error', 'Unknown')}")
    
    print(f"\nWorkflow Status: {results['status']}")
    print(f"Duration: {results['start_time']} to {results['end_time']}")
    
    await orchestrator.shutdown()
    print("\n✓ Workflow completed!")


if __name__ == "__main__":
    asyncio.run(main())
