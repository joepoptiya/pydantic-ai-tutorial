# Suggested Commands

## Environment Setup
```bash
# Install dependencies
pip install -r requirements.txt

# Set up environment variables (copy .env.example to .env and add OpenAI API key)
cp .env.example .env
# Edit .env to add: OPENAI_API_KEY=your_api_key_here
```

## Running the Project
```bash
# Run the main tutorial script
python src/introduction.py

# Run from project root (recommended)
python src/introduction.py
```

## Testing
```bash
# Run tests (when available)
python -m pytest

# Run tests with verbose output
python -m pytest -v
```

## Development
```bash
# Check Python version (requires 3.9+)
python --version

# List installed packages
pip list

# Check if required modules are available
python -c "import pydantic_ai; print('PydanticAI available')"
```

## Utilities
- **No linting/formatting tools configured** - consider adding black, flake8, or similar
- **No pre-commit hooks** - manual testing required
- Uses standard Python development practices