"""
PydanticAI PDF Processing Tutorial

This tutorial demonstrates how to use PydanticAI to process PDF documents,
extract structured data, and build intelligent document processing agents.

Based on the introduction.py pattern but using real PDF invoice data as the source.
"""

import os
from typing import List, Optional, Dict, Union
from dataclasses import dataclass
from pathlib import Path

import pypdf
from pydantic import BaseModel, Field
from pydantic_ai import Agent, RunContext
from pydantic_ai.models.openai import OpenAIModel

from utils.markdown import to_markdown

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

# Initialize the model
model = OpenAIModel("gpt-4o")

# PDF Text Extraction Utility
def extract_pdf_text(pdf_path: str) -> str:
    """Extract text content from a PDF file."""
    try:
        with open(pdf_path, 'rb') as file:
            pdf_reader = pypdf.PdfReader(file)
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text() + "\n"
            return text
    except Exception as e:
        return f"Error reading PDF: {e}"

# Load the sample invoice PDF
PDF_PATH = "../data/sample-invoice.pdf"
INVOICE_TEXT = extract_pdf_text(PDF_PATH)

print("=============================================================")
print("PYDANTIC AI PDF PROCESSING TUTORIAL")  
print("=============================================================\n")

print(f"📄 Loaded PDF: {PDF_PATH}")
print(f"📊 Extracted {len(INVOICE_TEXT)} characters of text\n")

# --------------------------------------------------------------
# 1. Basic PDF Processing Agent
# --------------------------------------------------------------

print("# --------------------------------------------------------------")
print("# 1. Basic PDF Processing Agent")  
print("# --------------------------------------------------------------\n")

"""
This example demonstrates basic PDF text processing with PydanticAI.
Key concepts:
- Loading and processing PDF documents
- Creating agents that work with document content
- Simple Q&A over PDF text
"""

# Basic agent with PDF content knowledge
basic_pdf_agent = Agent(
    model=model,
    system_prompt=(
        f"You are a helpful assistant that can answer questions about this invoice document:\n\n"
        f"{INVOICE_TEXT[:1000]}...\n\n"  # First 1000 chars for context
        "Answer questions clearly and concisely based on the invoice content."
    ),
)

response = basic_pdf_agent.run_sync("What company issued this invoice?")
print(f"💬 Question: What company issued this invoice?")
print(f"🤖 Answer: {response.output}\n")

print(f"📈 Usage: {response.usage()}")
print(f"📜 Message History: {len(response.all_messages())} messages\n")

# --------------------------------------------------------------
# 2. Structured Invoice Data Extraction
# --------------------------------------------------------------

print("# --------------------------------------------------------------")
print("# 2. Structured Invoice Data Extraction")
print("# --------------------------------------------------------------\n")

"""
This example demonstrates structured data extraction from PDF invoices.
Key concepts:
- Defining Pydantic models for invoice structure
- Extracting structured data from unstructured PDF text
- Validation and formatting of extracted data
"""

class InvoiceHeader(BaseModel):
    """Header information from the invoice."""
    company_name: str = Field(description="Name of the issuing company")
    company_address: str = Field(description="Company address")
    customer_name: str = Field(description="Customer name")
    customer_address: str = Field(description="Customer address")
    invoice_number: str = Field(description="Invoice number")
    invoice_date: str = Field(description="Invoice date")
    customer_number: str = Field(description="Customer number")

class LineItem(BaseModel):
    """Individual line item from the invoice."""
    service_description: str = Field(description="Description of the service")
    amount_without_vat: float = Field(description="Amount without VAT")
    quantity: int = Field(description="Quantity")
    total_amount: float = Field(description="Total line amount")

class InvoiceSummary(BaseModel):
    """Summary totals from the invoice."""
    subtotal: float = Field(description="Total amount before VAT")
    vat_rate: float = Field(description="VAT rate as percentage")
    vat_amount: float = Field(description="VAT amount")
    gross_total: float = Field(description="Final total including VAT")

class StructuredInvoice(BaseModel):
    """Complete structured invoice data."""
    header: InvoiceHeader
    line_items: List[LineItem]
    summary: InvoiceSummary

# Agent for extracting structured invoice data
extraction_agent = Agent(
    model=model,
    output_type=StructuredInvoice,
    system_prompt=(
        "You are an expert at extracting structured data from invoice documents. "
        "Analyze the provided invoice text and extract all relevant information into the structured format. "
        "Be precise with numbers and ensure all fields are filled accurately."
    ),
)

response = extraction_agent.run_sync(f"Extract structured data from this invoice:\n\n{INVOICE_TEXT}")
print("📋 Extracted Structured Invoice Data:")
print(response.output.model_dump_json(indent=2))
print()

# Store extracted data for later use
extracted_invoice = response.output

# --------------------------------------------------------------
# 3. Invoice Analysis with Dependencies
# --------------------------------------------------------------

print("# --------------------------------------------------------------")
print("# 3. Invoice Analysis with Dependencies")  
print("# --------------------------------------------------------------\n")

"""
This example demonstrates invoice analysis with dependency injection.
Key concepts:
- Injecting invoice content and metadata as dependencies
- Dynamic system prompts based on document content
- Contextual analysis using dependencies
"""

@dataclass
class InvoiceContext:
    """Context containing invoice data and metadata."""
    pdf_path: str
    raw_text: str
    extracted_data: StructuredInvoice
    file_size_kb: float

class AnalysisResult(BaseModel):
    """Result of invoice analysis."""
    analysis_summary: str = Field(description="Summary of the invoice analysis")
    key_findings: List[str] = Field(description="Key findings from the analysis")
    anomalies: List[str] = Field(description="Any anomalies or issues found")
    recommendations: List[str] = Field(description="Recommendations for action")

# Create invoice context
file_size = os.path.getsize(PDF_PATH) / 1024  # Size in KB
invoice_context = InvoiceContext(
    pdf_path=PDF_PATH,
    raw_text=INVOICE_TEXT,
    extracted_data=extracted_invoice,
    file_size_kb=file_size
)

# Analysis agent with dependencies
analysis_agent = Agent(
    model=model,
    deps_type=InvoiceContext,
    output_type=AnalysisResult,
    system_prompt=(
        "You are an expert invoice analyst. Analyze the provided invoice data thoroughly and provide insights. "
        "Look for calculation errors, unusual patterns, and provide actionable recommendations."
    ),
)

@analysis_agent.system_prompt
async def add_invoice_context(ctx: RunContext[InvoiceContext]) -> str:
    return f"""
Invoice Analysis Context:
- File: {ctx.deps.pdf_path} ({ctx.deps.file_size_kb:.1f} KB)
- Company: {ctx.deps.extracted_data.header.company_name}
- Customer: {ctx.deps.extracted_data.header.customer_name}
- Invoice #: {ctx.deps.extracted_data.header.invoice_number}
- Total: €{ctx.deps.extracted_data.summary.gross_total:.2f}
- Line Items: {len(ctx.deps.extracted_data.line_items)}

Use this context to provide detailed analysis.
"""

response = analysis_agent.run_sync(
    "Analyze this invoice for accuracy, completeness, and any notable characteristics.",
    deps=invoice_context
)

print("🔍 Invoice Analysis Results:")
print(response.output.model_dump_json(indent=2))
print()

# --------------------------------------------------------------
# 4. Invoice Query Tools
# --------------------------------------------------------------

print("# --------------------------------------------------------------")
print("# 4. Invoice Query Tools")
print("# --------------------------------------------------------------\n")

"""
This example demonstrates tool integration for invoice processing.
Key concepts:
- Creating tools for invoice calculations and lookups
- Function calling with invoice data
- Complex queries using multiple tools
"""

class QueryResponse(BaseModel):
    """Response to invoice queries."""
    answer: str = Field(description="Direct answer to the query")
    calculations: Optional[Dict[str, float]] = Field(description="Any calculations performed")
    references: List[str] = Field(description="References to specific invoice sections")

# Agent with invoice processing tools
tools_agent = Agent(
    model=model,
    deps_type=InvoiceContext,
    output_type=QueryResponse,
    system_prompt=(
        "You are an invoice processing assistant with access to calculation and lookup tools. "
        "Use the available tools to answer questions accurately and provide detailed responses."
    ),
)

@tools_agent.tool
async def calculate_line_totals(ctx: RunContext[InvoiceContext]) -> Dict[str, float]:
    """Calculate totals for all line items in the invoice."""
    totals = {}
    for i, item in enumerate(ctx.deps.extracted_data.line_items):
        service_key = item.service_description[:30].replace(" ", "_")
        totals[f"line_{i+1}_{service_key}"] = item.total_amount
    
    totals["subtotal"] = sum(item.total_amount for item in ctx.deps.extracted_data.line_items)
    return totals

@tools_agent.tool  
async def lookup_transaction_details(ctx: RunContext[InvoiceContext], transaction_type: str) -> Dict[str, Union[str, float]]:
    """Look up details for specific transaction types in the invoice."""
    details = {}
    text_lower = ctx.deps.raw_text.lower()
    
    # Search for transaction fees
    if "transaction" in transaction_type.lower():
        lines = ctx.deps.raw_text.split('\n')
        for line in lines:
            if "transaction fee" in line.lower() and transaction_type.lower() in line.lower():
                details[f"found_{transaction_type}"] = line.strip()
    
    # Search for basic fees
    if "basic" in transaction_type.lower():
        lines = ctx.deps.raw_text.split('\n')
        for line in lines:
            if "basic fee" in line.lower():
                details[f"found_basic_fee"] = line.strip()
                
    return details

@tools_agent.tool
async def validate_calculations(ctx: RunContext[InvoiceContext]) -> Dict[str, Union[bool, str, float]]:
    """Validate the mathematical calculations in the invoice."""
    invoice_data = ctx.deps.extracted_data
    
    # Calculate expected totals
    calculated_subtotal = sum(item.total_amount for item in invoice_data.line_items)
    calculated_vat = calculated_subtotal * (invoice_data.summary.vat_rate / 100)
    calculated_total = calculated_subtotal + calculated_vat
    
    validation = {
        "subtotal_correct": abs(calculated_subtotal - invoice_data.summary.subtotal) < 0.01,
        "vat_correct": abs(calculated_vat - invoice_data.summary.vat_amount) < 0.01,
        "total_correct": abs(calculated_total - invoice_data.summary.gross_total) < 0.01,
        "calculated_subtotal": calculated_subtotal,
        "calculated_vat": calculated_vat,
        "calculated_total": calculated_total,
        "stated_subtotal": invoice_data.summary.subtotal,
        "stated_vat": invoice_data.summary.vat_amount,
        "stated_total": invoice_data.summary.gross_total
    }
    
    return validation

# Test the tools
response = tools_agent.run_sync(
    "What are the transaction fees T1 and T3 in this invoice, and do the calculations look correct?",
    deps=invoice_context
)

print("🔧 Tool-Based Query Results:")
print(response.output.model_dump_json(indent=2))
print()

# --------------------------------------------------------------
# 5. Multi-Agent Invoice Processing Pipeline
# --------------------------------------------------------------

print("# --------------------------------------------------------------") 
print("# 5. Multi-Agent Invoice Processing Pipeline")
print("# --------------------------------------------------------------\n")

"""
This example demonstrates a multi-agent system for comprehensive invoice processing.
Key concepts:
- Agent delegation and coordination
- Specialized agents for different tasks
- Pipeline processing with multiple agents
"""

# Define model classes first
class ValidationResults(BaseModel):
    """Validation results for invoice data."""
    subtotal_correct: bool
    vat_correct: bool
    total_correct: bool
    completeness_check: bool

class BusinessInsights(BaseModel):
    """Business insights from invoice analysis."""
    insights: List[str]

class ProcessingReport(BaseModel):
    """Comprehensive invoice processing report."""
    extraction_status: str = Field(description="Status of data extraction")
    validation_results: ValidationResults = Field(description="Validation check results")
    business_insights: BusinessInsights = Field(description="Business insights from analysis")
    processing_time: str = Field(description="Processing time information")
    confidence_score: float = Field(description="Overall confidence in processing", ge=0, le=1)

# Data Extraction Agent
extraction_specialist = Agent(
    model=model,
    output_type=StructuredInvoice,
    system_prompt=(
        "You are a specialized data extraction agent. Your only job is to extract "
        "structured data from invoices with maximum accuracy. Focus on precision."
    ),
)

# Validation Agent
validation_specialist = Agent(
    model=model,
    deps_type=InvoiceContext,
    output_type=ValidationResults,
    system_prompt=(
        "You are a validation specialist. Check extracted invoice data for mathematical "
        "accuracy, completeness, and consistency. Return validation results."
    ),
)

# Business Analysis Agent  
business_analyst = Agent(
    model=model,
    deps_type=InvoiceContext, 
    output_type=BusinessInsights,
    system_prompt=(
        "You are a business analyst specializing in invoice analysis. Provide "
        "business insights, trends, and strategic recommendations based on invoice data."
    ),
)

# Coordinator Agent
coordinator = Agent(
    model=model,
    deps_type=InvoiceContext,
    output_type=ProcessingReport,
    system_prompt=(
        "You are the processing coordinator. Orchestrate the invoice processing pipeline "
        "and compile comprehensive reports from all agent outputs."
    ),
)

@coordinator.tool
async def delegate_extraction(ctx: RunContext[InvoiceContext]) -> StructuredInvoice:
    """Delegate data extraction to specialist agent."""
    result = await extraction_specialist.run(
        f"Extract structured data from this invoice:\n\n{ctx.deps.raw_text}",
        usage=ctx.usage
    )
    return result.output

@coordinator.tool
async def delegate_validation(ctx: RunContext[InvoiceContext], extracted_data: StructuredInvoice) -> ValidationResults:
    """Delegate validation to specialist agent."""
    # Update context with extracted data
    updated_context = InvoiceContext(
        pdf_path=ctx.deps.pdf_path,
        raw_text=ctx.deps.raw_text,
        extracted_data=extracted_data,
        file_size_kb=ctx.deps.file_size_kb
    )
    
    result = await validation_specialist.run(
        "Validate the extracted invoice data for accuracy and completeness.",
        deps=updated_context,
        usage=ctx.usage
    )
    return result.output

@coordinator.tool
async def delegate_analysis(ctx: RunContext[InvoiceContext]) -> BusinessInsights:
    """Delegate business analysis to specialist agent."""
    result = await business_analyst.run(
        "Provide business insights and recommendations based on this invoice.",
        deps=ctx.deps,
        usage=ctx.usage
    )
    return result.output

# Run the multi-agent processing pipeline
print("🚀 Starting Multi-Agent Invoice Processing Pipeline...")

response = coordinator.run_sync(
    "Process this invoice through the complete pipeline: extraction, validation, and business analysis.",
    deps=invoice_context
)

print("\n📊 Comprehensive Processing Report:")
print(response.output.model_dump_json(indent=2))

print(f"\n💰 Total Usage Across All Agents: {response.usage()}")
print(f"📝 Total Messages: {len(response.all_messages())}")

print("\n✅ PDF Invoice Processing Tutorial Complete!")
print("=============================================================")