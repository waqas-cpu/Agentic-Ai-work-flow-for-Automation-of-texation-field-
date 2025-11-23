import os
from crewai import Agent, Task, Crew, Process
from langchain_openai import ChatOpenAI

# =============================================================================
# 1. CONFIGURATION
# =============================================================================
# Replace with your API Key or use os.getenv("OPENAI_API_KEY")
os.environ["OPENAI_API_KEY"] = "YOUR_OPENAI_API_KEY_HERE"

# We use a capable model (GPT-4) for complex reasoning, or GPT-3.5 for speed
llm = ChatOpenAI(model="gpt-4", temperature=0.2)

# =============================================================================
# 2. AGENT DEFINITIONS (The Team)
# =============================================================================

# Agent 1: Gathers raw financial data
data_collector = Agent(
    role='Senior Financial Data Collector',
    goal='Extract accurate income and expense data from raw transaction logs',
    backstory="""You are an expert at sifting through messy bank logs and 
    invoices. You categorize every transaction precisely as 'Income', 
    'Deductible Expense', or 'Non-Deductible'.""",
    verbose=True,
    allow_delegation=False,
    llm=llm
)

# Agent 2: Calculates the Tax
tax_analyst = Agent(
    role='Chief Tax Calculator',
    goal='Calculate the final tax liability based on net income and current tax brackets',
    backstory="""You are a precise mathematician. You take categorized data 
    and apply the following tax rules: 
    - 0% tax on first $10,000 
    - 10% tax on income between $10,001 and $50,000 
    - 20% tax on anything above $50,000. 
    You strictly follow these brackets.""",
    verbose=True,
    allow_delegation=False,
    llm=llm
)

# Agent 3: Audits the process (Quality Assurance)
compliance_auditor = Agent(
    role='IRS Compliance Auditor',
    goal='Verify that the calculated tax matches the data and report any anomalies',
    backstory="""You are a suspicious auditor. You double-check the work of the 
    Tax Calculator. If the math looks wrong or deductions seem too high (over 
    50% of income), you flag it as 'High Risk'. Otherwise, you mark it 'Approved'.""",
    verbose=True,
    allow_delegation=True, # Can ask the others questions if needed
    llm=llm
)

# =============================================================================
# 3. TASK DEFINITIONS (The Work)
# =============================================================================

# Simulated raw data input
client_data = """
    Transaction Log for User ID 998:
    - Jan 1: Payment received from Client A: +$40,000
    - Feb 4: Payment received from Client B: +$25,000
    - Mar 10: Office Supplies purchase: -$5,000
    - Apr 15: Client Dinner (50% deductible): -$2,000
    - May 20: Server Hosting Costs: -$3,000
"""

task_collect_data = Task(
    description=f"""Analyze the following client data: {client_data}. 
    Create a summary report listing Total Income and Total Deductible Expenses.""",
    agent=data_collector,
    expected_output="A clear summary text with Total Income and Total Expenses."
)

task_calculate_tax = Task(
    description="""Using the summary provided by the Data Collector, calculate 
    the taxable income (Income - Expenses) and then calculate the exact tax 
    owed based on the tax brackets in your backstory.""",
    agent=tax_analyst,
    expected_output="A step-by-step calculation showing the final Tax Bill.",
    context=[task_collect_data] # Waits for collector to finish
)

task_audit = Task(
    description="""Review the calculated tax bill. Check if the deductions look 
    reasonable. Generate a final 'Audit Certificate' stating if the return is 
    Approved or Flagged for Review.""",
    agent=compliance_auditor,
    expected_output="A formal Audit Certificate text.",
    context=[task_calculate_tax] # Waits for calculator to finish
)

# =============================================================================
# 4. CREW EXECUTION (The Automation)
# =============================================================================

tax_crew = Crew(
    agents=[data_collector, tax_analyst, compliance_auditor],
    tasks=[task_collect_data, task_calculate_tax, task_audit],
    process=Process.sequential, # Changes to 'hierarchical' or 'parallel' depending on complexity
    verbose=True
)

print("### STARTING TAXATION AUTOMATION CREW ###")
result = tax_crew.kickoff()

print("\n\n########################")
print("## FINAL AUDIT REPORT ##")
print("########################\n")
print(result)
