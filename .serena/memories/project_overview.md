# Project Overview

## Purpose
This repository contains examples and explanations of how to use PydanticAI - a Python Agent Framework designed to make it easier to build production-grade applications with Generative AI. It serves as a tutorial repository demonstrating PydanticAI concepts and capabilities.

## Tech Stack
- **Python**: 3.9+ (uses Python 3.11 in current setup)
- **PydanticAI**: >=0.1.0 - Core agent framework
- **Pydantic**: >=2.0.0 - Data validation and settings management
- **OpenAI**: >=1.0.0 - LLM provider integration
- **python-dotenv**: >=1.0.0 - Environment variable management
- **pytest**: >=7.0.0 - Testing framework
- **nest_asyncio**: Required dependency for async operations

## Project Structure
```
├── src/
│   ├── introduction.py    # Main tutorial script with PydanticAI examples
│   └── utils/
│       └── markdown.py    # Utility for converting data to markdown format
├── data/                  # Data directory (likely for examples/datasets)
├── venv/                  # Virtual environment
├── requirements.txt       # Python dependencies
├── README.md             # Comprehensive project documentation
└── .env                  # Environment variables (not tracked in git)
```

## Core Concepts Demonstrated
1. **Agents**: Primary interface for LLM interactions
2. **Dependencies**: Type-safe system for runtime context injection
3. **Results**: Structured data validation and responses
4. **Messages and Chat History**: Complete conversation management
5. **Tools**: Function calling and external service integration

## Current Status
- PydanticAI is in early beta with API subject to change
- Known issues: Model parameter adjustments and message history with tools
- Active development/tutorial project by Dave Ebbelaar from Datalumina