import time
import argparse
from string import Template

import httpx
import llms
from pynput import keyboard
from pynput.keyboard import Key, Controller
import pyperclip


controller = Controller()
model = None

OLLAMA_ENDPOINT = "http://localhost:11434/api/generate"
OLLAMA_CONFIG = {
    "model": "mistral:7b-instruct-v0.2-q4_K_S",
#    "model": "qwen2:0.5b",
#    "model": "qwen2:1.5b",
#     "model" : "llama3.1",
    "keep_alive": "5m",
    "stream": False,
}

# Define prompt templates
PROMPT_TEMPLATES = {
    "fix_typos": Template(
        """
$text

Fix grammar, spelling and typos in the text above. Corrected text is:

"""
    ),
    "improve_writing": Template(
        """
$text

Improve the writing style of the text above, making it more clear and concise while preserving the original meaning. Improved text is:

"""
    ),
    "summarize": Template(
        """
$text

Summarize the main points of the text above in a concise manner. Summary:

"""
    ),
    "restructure_note": Template(
        """
$text

Fix typos and punctuation in the note above. POlish the note a little bit where appropriate but do not lose original meaning or intent. 

Polished note:
"""
    )
}

def fix_text(text, prompt_key):
    prompt = PROMPT_TEMPLATES[prompt_key].substitute(text=text)
    print(prompt)
    
    if model:
        response = model.complete(prompt, max_tokens=4096).text
        return response.strip()
    else:
        response = httpx.post(
            OLLAMA_ENDPOINT,
            json={"prompt": prompt, **OLLAMA_CONFIG},
            headers={"Content-Type": "application/json"},
            timeout=120,
        )
        print(response)
        if response.status_code != 200:
            print("Error", response.status_code)
            return None
        return response.json()["response"].strip()

def select_current_line():
    """Select the current line."""
    controller.press(Key.cmd)
    controller.press(Key.shift)
    controller.press(Key.left)
    controller.release(Key.cmd)
    controller.release(Key.shift)
    controller.release(Key.left)

def select_all_text():
    """Select all text in the current document."""
    with controller.pressed(Key.cmd):
        controller.tap('a')

def copy_selection():
    """Copy the current selection to clipboard."""
    with controller.pressed(Key.cmd):
        controller.tap('c')
    time.sleep(0.1)
    return pyperclip.paste()

def paste_text(text):
    """Paste the given text, replacing the current selection and matching style."""
    pyperclip.copy(text)
    time.sleep(0.1)
    with controller.pressed(Key.cmd):
        with controller.pressed(Key.alt):
            with controller.pressed(Key.shift):
                controller.tap('v')

def fix_text_scope(select_func, prompt_key):
    """Fix text within a specific scope using the specified prompt."""
    if select_func:
        select_func()
    
    text = copy_selection()
    if not text:
        return

    fixed_text = fix_text(text, prompt_key)
    if not fixed_text:
        return

    paste_text(fixed_text)

# Define a dictionary to map function keys to functions
function_key_map = {
    "<100>": ("F8", select_all_text, "restructure_note"),
    "<101>": ("F9", select_current_line, "fix_typos"),
    "<109>": ("F10", None, "fix_typos"),  # None means use current selection
    "<111>": ("F11", None, "improve_writing"),
}

def on_hotkey(key):
    """General handler for all hotkeys"""
    key_name, select_func, prompt_key = function_key_map[key]
    print(f'{key_name} pressed')
    fix_text_scope(select_func, prompt_key)

# Set up the GlobalHotKeys
hotkey_dict = {key: lambda k=key: on_hotkey(k) for key in function_key_map.keys()}

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Text processing with AI models")
    parser.add_argument("-m", "--model", help="Specify the model to use with pyllms")
    args = parser.parse_args()

    if args.model:
        model = llms.init(args.model)
        print(f"Using pyllms model: {args.model}")
    else:
        print(f"Using Ollama model: {OLLAMA_CONFIG['model']}")
    
    with keyboard.GlobalHotKeys(hotkey_dict) as h:
        h.join()
