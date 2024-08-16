# AI-powered Typing Assistant with local (through Ollama) or external models (through PyLLMs)

This script runs in the background and listens for hotkeys, then uses a Large Language Model to fix or improve text. It's inspired by Andrej Karpathy's tweet about GPT's ability to correct minor typos, allowing for faster writing.

## Features

- Uses Ollama or any external model supported by PyLLMs for text processing
- Supports multiple hotkeys for different text operations
- Can fix typos, improve writing style, and restructure notes

## Setup

1. Set up Ollama (if using Ollama):
   - Install Ollama: https://github.com/ollama/ollama
   - Run: `ollama run mistral:7b-instruct-v0.2-q4_K_S`

2. Install dependencies:
   ```
   pip install pynput pyperclip httpx pyllms
   ```

3. Run the script:
   ```
   python key.py
   ```

## Usage

Default Hotkeys:
- F8: Restructure and polish the entire note
- F9: Fix typos in the current line
- F10: Fix typos in the current selection
- F11: Improve writing style of the current selection

Note: On macOS, you may need to add the script (IDE/terminal) to both accessibility and input monitoring settings.

## Customization

The script can be easily customized:
- Modify `OLLAMA_CONFIG` to change the Ollama model or settings
- Edit `PROMPT_TEMPLATES` to change how text is processed
- Adjust `function_key_map` to modify hotkey assignments or add new operations

To extend mappings:
1. Add a new prompt template to `PROMPT_TEMPLATES`:
   ```python
   "new_operation": Template("Your prompt here $text"),
   ```
2. Add a new entry to `function_key_map`:
   ```python
   "<key_code>": ("Key_Name", select_function, "new_operation"),
   ```
   Where `<key_code>` is the pynput key code, `"Key_Name"` is a descriptive name,
   `select_function` is either `None` or a function to select text, and
   `"new_operation"` is the key of your new prompt template.

## Command-line Options

- Use `-m` or `--model` to specify a PyLLMs model instead of Ollama

Examples:
```
python key.py -m gpt-4o-mini
```

## Notes

- The script is designed for macOS. Keyboard shortcuts may need adjustment for Linux or Windows.
- Ensure you have the necessary permissions for keyboard input monitoring.
- When using PyLLMs models, make sure you have the required API keys set up in your environment.
