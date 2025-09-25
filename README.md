# AI-codez

An AI-powered coding assistant built with Google Gemini API that can interact with your local file system and execute Python code safely.

## Features

- **List files and directories** in specified directories
- **Read file contents** for code analysis
- **Write or overwrite files** with new content
- **Execute Python files** with optional command-line arguments
- **Built-in calculator example** in the `calculator/` directory

## Prerequisites

- Python 3.12+
- Google Gemini API key
- UV package manager

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/AI-codez.git
   cd AI-codez
   ```

2. Install dependencies using UV:
   ```bash
   uv sync
   ```

3. Create a `.env` file with your Google Gemini API key:
   ```
   GEMINI_API_KEY=your_api_key_here
   ```

## Usage

### Running the AI Coding Assistant

Run the main AI agent with a prompt:

```bash
uv run main.py "your coding task or question"
```

For verbose output (shows tokens used and function calls):

```bash
uv run main.py "analyze the calculator code" --verbose
```

### Examples

- List files in root directory:
  ```bash
  uv run main.py "what files are in the root?"
  ```

- Calculate something using the calculator:
  ```bash
  uv run python calculator/main.py "3 + 5"
  ```

- Analyze code:
  ```bash
  uv run main.py "how does the calculator render results?"
  ```

## Project Structure

```
AI-codez/
├── main.py                 # Main AI agent script
├── config.py               # Configuration (if any)
├── .env                    # Environment variables (API keys)
├── pyproject.toml          # Project dependencies
├── uv.lock                 # UV lockfile
├── tests.py               # Test scripts
├── calculator/            # Calculator example application
│   ├── main.py           # Calculator entry point
│   ├── tests.py          # Calculator tests
│   ├── pkg/              # Calculator package
│   │   ├── calculator.py # Calculator logic
│   │   └── render.py     # Output formatting
│   └── lorem.txt         # Sample file
├── functions/             # AI agent functions
│   ├── get_files_info.py # List files/directories
│   ├── get_files_content.py # Read file content
│   ├── write_file.py     # Write files
│   └── run_python_file.py # Execute Python scripts
├── call_function.py      # Function dispatcher
└── README.md             # This file
```

## Security Features

- All file operations are restricted to the working directory (`calculator/` for the assistant)
- Python execution is sandboxed to prevent system-level modifications
- API key required for operation

## API Key Setup

1. Get your free Google Gemini API key from [Google AI Studio](https://aistudio.google.com/)
2. Add it to the `.env` file as shown above

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests
5. Submit a pull request

## License

MIT License - see LICENSE file for details

## Disclaimer

This tool executes code and modifies files based on AI responses. Use caution and review generated code before execution. The authors are not responsible for any unintended consequences of using this tool.
