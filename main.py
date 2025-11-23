"""
Main entry point for the Tax Automation System
Provides CLI interface for running the system
"""

import asyncio
import argparse
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

from src.rag import TaxDocumentRAG
from src.orchestrator import AgentOrchestrator
from src.utils import setup_logging, Config, load_documents_from_directory


def parse_arguments():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(
        description="Tax Automation System with Agentic AI and RAG"
    )
    
    parser.add_argument(
        "--mode",
        choices=["demo", "workflow", "interactive"],
        default="demo",
        help="Execution mode"
    )
    
    parser.add_argument(
        "--log-level",
        choices=["DEBUG", "INFO", "WARNING", "ERROR"],
        default="INFO",
        help="Logging level"
    )
    
    parser.add_argument(
        "--docs-dir",
        type=str,
        help="Directory containing tax documents to ingest"
    )
    
    return parser.parse_args()


async def run_demo(orchestrator):
    """Run demonstration mode"""
    print("\n🤖 Running Demo Mode: Parallel Agent Execution\n")
    
    tasks = [
        {
            "agent_type": "calculation",
            "type": "income_tax",
            "data": {"income": 100000, "filing_status": "married"}
        },
        {
            "agent_type": "document",
            "document_type": "W-2",
            "content": "Wages: $100,000, Federal tax: $15,000"
        },
        {
            "agent_type": "compliance",
            "filing_data": {"forms": ["1040"]},
            "jurisdiction": "federal"
        }
    ]
    
    print(f"Executing {len(tasks)} tasks in parallel...\n")
    results = await orchestrator.process_tasks_parallel(tasks)
    
    print("\n📊 Results:")
    for i, result in enumerate(results, 1):
        status_icon = "✓" if result.get("status") == "success" else "✗"
        print(f"{status_icon} Task {i}: {result.get('status', 'unknown')}")
    
    return results


async def run_workflow(orchestrator):
    """Run workflow mode"""
    print("\n📋 Running Workflow Mode: Multi-Step Tax Processing\n")
    
    workflow = {
        "name": "Basic Tax Filing",
        "steps": [
            {
                "name": "Document Analysis",
                "type": "parallel",
                "tasks": [
                    {"agent_type": "document", "document_type": "W-2", "content": "Income data"},
                    {"agent_type": "document", "document_type": "1099", "content": "Interest data"}
                ]
            },
            {
                "name": "Tax Calculation",
                "type": "sequential",
                "tasks": [
                    {"agent_type": "calculation", "data": {"income": 85000}}
                ]
            }
        ]
    }
    
    results = await orchestrator.process_workflow(workflow)
    
    print(f"\n✓ Workflow '{results['workflow_name']}' completed")
    print(f"  Steps: {len(results['steps'])}")
    print(f"  Status: {results['status']}")
    
    return results


async def run_interactive(orchestrator):
    """Run interactive mode"""
    print("\n💬 Interactive Mode\n")
    print("Commands:")
    print("  status  - Show agent status")
    print("  stats   - Show system statistics")
    print("  task    - Execute a custom task")
    print("  quit    - Exit")
    print()
    
    while True:
        try:
            command = input(">>> ").strip().lower()
            
            if command == "quit":
                break
            elif command == "status":
                status = orchestrator.get_agent_status()
                for name, info in status.items():
                    print(f"\n{info['agent_name']}:")
                    print(f"  Status: {info['status']}")
                    print(f"  Tasks completed: {info['tasks_completed']}")
            elif command == "stats":
                stats = orchestrator.get_statistics()
                print(f"\nSystem Statistics:")
                print(f"  Total agents: {stats['total_agents']}")
                print(f"  Active tasks: {stats['active_tasks']}")
                print(f"  Completed tasks: {stats['completed_tasks']}")
            elif command == "task":
                print("Task execution not implemented in demo")
            else:
                print("Unknown command")
        
        except KeyboardInterrupt:
            print("\nExiting...")
            break
        except Exception as e:
            print(f"Error: {e}")


async def main():
    """Main function"""
    args = parse_arguments()
    
    # Setup logging
    setup_logging(log_level=args.log_level)
    
    # Load configuration
    config = Config()
    
    print("=" * 70)
    print("🎯 Tax Automation System with Agentic AI and RAG")
    print("=" * 70)
    
    # Initialize RAG system
    print("\n🔧 Initializing RAG system...")
    rag_system = TaxDocumentRAG(
        embedding_model="huggingface",
        vector_store_type="chroma"
    )
    
    # Ingest documents if directory provided
    if args.docs_dir:
        print(f"\n📚 Loading documents from {args.docs_dir}...")
        docs = load_documents_from_directory(args.docs_dir)
        if docs:
            # Filter out documents with empty content
            valid_docs = [d for d in docs if d.get('content')]
            if valid_docs:
                rag_system.ingest_documents(
                    documents=[d['content'] for d in valid_docs],
                    metadata=[{"name": d['name']} for d in valid_docs]
                )
                print(f"✓ Ingested {len(valid_docs)} documents")
            else:
                print("⚠ No valid documents found")
    else:
        # Load sample documents
        print("\n📚 Loading sample tax documents...")
        sample_docs = [
            "Tax regulations for 2024: Standard deduction, tax brackets...",
            "Business expense deduction rules and limits...",
            "State tax filing requirements and deadlines..."
        ]
        rag_system.ingest_documents(sample_docs)
        print(f"✓ Loaded {len(sample_docs)} sample documents")
    
    # Initialize orchestrator
    print("🤖 Initializing agent orchestrator...")
    orchestrator = AgentOrchestrator(
        rag_system=rag_system,
        max_parallel_agents=config.get("max_parallel_agents", 5)
    )
    print(f"✓ {orchestrator.get_statistics()['total_agents']} agents ready")
    
    # Run selected mode
    try:
        if args.mode == "demo":
            await run_demo(orchestrator)
        elif args.mode == "workflow":
            await run_workflow(orchestrator)
        elif args.mode == "interactive":
            await run_interactive(orchestrator)
    except KeyboardInterrupt:
        print("\n\nInterrupted by user")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        # Cleanup
        print("\n🔒 Shutting down...")
        await orchestrator.shutdown()
        print("✓ Shutdown complete")
    
    print("\n" + "=" * 70)
    print("Thank you for using Tax Automation System!")
    print("=" * 70)


if __name__ == "__main__":
    asyncio.run(main())
