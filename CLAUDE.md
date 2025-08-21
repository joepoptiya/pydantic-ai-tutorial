# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This repository contains examples and tutorials for **PydanticAI** - a Python Agent Framework for building production-grade Generative AI applications. PydanticAI is in early beta, so the API is subject to change.

## Commands

### Environment Setup
```bash
# Install dependencies
pip install -r requirements.txt

# Set up environment variables (requires OpenAI API key)
cp .env.example .env
# Edit .env to add: OPENAI_API_KEY=your_api_key_here
```

### Running the Tutorial
```bash
# Run main tutorial script
python src/introduction.py
```

### Testing
```bash
# Run tests (basic pytest setup)
python -m pytest

# Test individual components
python -c "import pydantic_ai; print('PydanticAI available')"
```

## Architecture

### Core Structure
- `src/introduction.py` - Main tutorial demonstrating PydanticAI concepts
- `src/utils/markdown.py` - Utility for converting Pydantic models to markdown
- `requirements.txt` - Python dependencies including PydanticAI >=0.1.0

### Key Dependencies
- **PydanticAI** (>=0.1.0) - Agent framework
- **OpenAI** (>=1.0.0) - LLM provider  
- **Pydantic** (>=2.0.0) - Data validation
- **python-dotenv** - Environment management
- **nest_asyncio** - Async compatibility

### PydanticAI Concepts Demonstrated
1. **Basic Agents** - Simple agent creation with system prompts
2. **Structured Responses** - Using Pydantic models for response validation
3. **Dependencies** - Type-safe context injection
4. **Tools** - Function calling and external service integration
5. **Message History** - Conversation continuity

## Development Notes

### Code Style
- Uses type hints throughout (`typing` module)
- Module-level docstrings with purpose explanation
- Snake_case for variables/functions, PascalCase for classes
- Clear section organization with comment headers
- OpenAI model initialization: `OpenAIModel("gpt-4o")`

### Environment Requirements
- Python 3.9+ required
- Valid OpenAI API key in `.env` file
- Virtual environment recommended (`venv/` directory present)

### Known Issues
- **Model Parameters**: Limited ability to adjust temperature/other params
- **Message History with Tools**: Known API issues with tool_call_ids
- **Beta Status**: API subject to change, test thoroughly

### Testing Approach
- Basic pytest setup available
- Manual testing via script execution required
- No automated linting/formatting tools configured
- Requires valid OpenAI API key for full testing