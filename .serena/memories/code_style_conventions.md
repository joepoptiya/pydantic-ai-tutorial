# Code Style and Conventions

## Python Style
- **Type Hints**: Used throughout (`from typing import Dict, List, Optional`)
- **Docstrings**: Module-level docstrings with triple quotes explaining purpose
- **Imports**: Grouped logically (standard library, third-party, local imports)
- **Variable Naming**: Snake_case for variables and functions
- **Class Naming**: PascalCase for classes (e.g., `ResponseModel`, `CustomerDetails`)

## PydanticAI Patterns
- **Agent Creation**: Use descriptive system prompts
- **Model Integration**: OpenAI model initialization with `OpenAIModel("gpt-4o")`
- **Structured Responses**: Pydantic models for response validation
- **Async Operations**: `nest_asyncio.apply()` for notebook/script compatibility

## Code Organization
- **Comments**: Section headers with dashes for organization
- **Examples**: Each concept demonstrated with working code
- **Error Handling**: Basic error handling patterns shown
- **Dependencies**: Clear separation of utilities in `utils/` directory

## File Structure Patterns
- Main logic in `src/` directory
- Utilities separated into `src/utils/`
- Clear module-level documentation
- Environment variables managed with python-dotenv

## Documentation Style
- Comprehensive README with setup instructions
- Inline comments explaining PydanticAI concepts
- Section-based organization with clear headers
- Practical examples over theoretical explanations