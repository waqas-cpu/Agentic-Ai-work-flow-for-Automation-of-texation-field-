# Agentic-Ai-work-flow-for-Automation-of-texation-field-
In this project we use Agentic Ai for Automation of Tax process 
from fpdf import FPDF

class PDF(FPDF):
    def header(self):
        # Font for the header
        self.set_font('Arial', 'B', 16)
        # Name
        self.cell(0, 10, 'Waqas Afzal', 0, 1, 'C')
        # Contact Info
        self.set_font('Arial', '', 10)
        self.cell(0, 5, 'AI Engineer Intern | Agentic AI & LLMs', 0, 1, 'C')
        self.cell(0, 5, 'Lahore, Pakistan | sialwaqas45@gmail.com', 0, 1, 'C')
        self.cell(0, 5, 'GitHub: github.com/waqas-cpu | LinkedIn: Waqas sial', 0, 1, 'C')
        self.ln(10)

    def section_title(self, title):
        self.set_font('Arial', 'B', 12)
        self.set_fill_color(200, 220, 255) # Light blue background
        self.cell(0, 6, title, 0, 1, 'L', 1)
        self.ln(2)

    def section_body(self, body):
        self.set_font('Arial', '', 10)
        self.multi_cell(0, 5, body)
        self.ln(3)
    
    def project_entry(self, name, tech, desc):
        self.set_font('Arial', 'B', 10)
        self.cell(0, 5, f"{name} | {tech}", 0, 1)
        self.set_font('Arial', '', 10)
        self.multi_cell(0, 5, desc)
        self.ln(3)

# Create PDF object
pdf = PDF()
pdf.add_page()
pdf.set_auto_page_break(auto=True, margin=15)

# --- PROFESSIONAL SUMMARY ---
pdf.section_title('PROFESSIONAL SUMMARY')
pdf.section_body(
    "Aspiring AI Engineer with a specialized focus on Agentic Workflows and LLM Orchestration. "
    "Passionate about moving beyond static chatbots to building autonomous systems that execute actions. "
    "Proficient in Python, LangChain, and CrewAI, with a portfolio of agentic projects on GitHub (waqas-cpu). "
    "Seeking an internship to apply multi-agent architecture knowledge in a production environment."
)

# --- TECHNICAL SKILLS ---
pdf.section_title('TECHNICAL SKILLS')
pdf.section_body(
    "- Core AI: Agentic Workflows, RAG, Prompt Engineering, Tool Calling/Function Calling.\n"
    "- Languages: Python, SQL, JavaScript.\n"
    "- Frameworks: LangChain, CrewAI, AutoGen, PyTorch, LlamaIndex.\n"
    "- Tools: OpenAI API, Ollama (Local LLMs), Pinecone/ChromaDB, Docker, Git."
)

# --- PROJECTS ---
pdf.section_title('KEY PROJECTS (GitHub: waqas-cpu)')

pdf.project_entry(
    "Autonomous Research Agent", 
    "Python, CrewAI, SerperDev API",
    "- Engineered a multi-agent system where a 'Researcher' agent scrapes the web and a 'Writer' agent compiles summaries.\n"
    "- Implemented autonomous delegation logic to handle complex queries without human intervention."
)

pdf.project_entry(
    "RAG Chatbot with Tool Use", 
    "LangChain, OpenAI, ChromaDB",
    "- Built a document-interaction system allowing users to query PDFs.\n"
    "- Integrated Function Calling enabling the LLM to switch between text retrieval and using a calculator tool for math queries."
)

pdf.project_entry(
    "Local LLM Optimization", 
    "Ollama, Llama 3, Linux",
    "- Deployed and optimized open-source LLMs locally for privacy-preserving inference.\n"
    "- Fine-tuned system prompts to improve reasoning capabilities of 7B parameter models."
)

# --- EDUCATION ---
pdf.section_title('EDUCATION')
pdf.section_body(
    "BS Computer Science / Artificial Intelligence\n"
    "Lahore, Pakistan\n"
    "Focus: Data Structures, Algorithms, Artificial Intelligence, NLP."
)

# --- CERTIFICATIONS ---
pdf.section_title('CERTIFICATIONS')
pdf.section_body(
    "- Generative AI with Large Language Models (DeepLearning.AI)\n"
    "- Python for Data Science"
)

# Output the file
pdf.output('Waqas_Afzal_Agentic_AI_CV.pdf')

print("SUCCESS: Your PDF 'Waqas_Afzal_Agentic_AI_CV.pdf' has been generated!")
