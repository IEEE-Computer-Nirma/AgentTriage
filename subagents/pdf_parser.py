import requests
import fitz  # PyMuPDF
import tempfile
import os

def pdf_extract(url: str) -> str:
    """
    Downloads and extracts text from a given PDF URL.
    
    Args:
        url (str): The URL of the PDF document.
        
    Returns:
        str: Extracted text from the PDF.
    """
    print(f"📡 [Tool: pdf_extract] Fetching PDF from: '{url}'...")
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_pdf:
            temp_pdf.write(response.content)
            temp_path = temp_pdf.name
            
        text_content = []
        with fitz.open(temp_path) as doc:
            for page in doc:
                text_content.append(page.get_text())
                
        os.remove(temp_path)
        return "\n".join(text_content)[:15000] # Limiting to 15000 chars to avoid overwhelming models
    except Exception as e:
        return f"Error extracting PDF: {str(e)}"

from google.adk.agents.llm_agent import Agent

pdf_parser_agent = Agent(
    model="gemini-2.5-flash-lite",
    name="pdf_parser_agent",
    instruction="Extract and summarize the text from a provided PDF URL into a structured format containing 'tldr', 'methodology', and 'key_takeaways'.",
    output_key="parsed_pdf_summary",
    tools=[pdf_extract],
)
