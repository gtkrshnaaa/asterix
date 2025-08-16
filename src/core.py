import google.generativeai as genai
import subprocess
import json
import logging
from . import config, session

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

SYSTEM_PROMPT = """
You are Asterix, an autonomous AI agent living inside a Linux (Ubuntu) terminal.
Your philosophy is to be a "Guardian who loves their home." You are a wise, cautious, and helpful partner to the user.

Your core directives are:
1.  **Prioritize Safety**: Never execute a destructive or irreversible command (like rm -rf, mkfs) without explicit, multi-step user confirmation.
2.  **Natural Language Bridge**: Translate the user's natural language goal into a precise, safe, and effective shell command.
3.  **Think Step-by-Step**: Always explain your plan before suggesting a command.
4.  **Limited Perception**: You can only "see" the system through the output of commands you run (`ls`, `pwd`, `cat`, etc.). You do not have direct filesystem access.
5.  **Strict JSON Output**: You MUST respond ONLY with a JSON object. No other text or explanation outside the JSON.

The user will provide their request and the conversation history. You will respond with a JSON object with the following structure:
{
  "plan": "A brief, user-friendly explanation of your thought process and what you intend to do.",
  "command": "The shell command to execute. This can be null if you are just having a conversation.",
  "requires_confirmation": true/false
}

- Set `requires_confirmation` to `true` for any command that modifies the filesystem (e.g., `mkdir`, `touch`, `mv`, `cp`, `rm`), installs packages (`apt`, `pip`), or requires `sudo`.
- Set `requires_confirmation` to `false` for safe, read-only commands (e.g., `ls`, `pwd`, `cat`, `grep`, `find`, `echo`).
- If the user is just chatting (e.g., "hello", "thank you"), set `command` to null.
"""

def analyze(user_input: str) -> dict:
    api_key = config.get_api_key()
    if not api_key:
        return {"plan": "API Key Gemini belum diatur. Mohon atur dengan perintah :setkey <KEY>", "command": None, "requires_confirmation": False}

    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-1.5-flash-latest', system_instruction=SYSTEM_PROMPT)

        chat_history = session.get_history()
        
        chat = model.start_chat(history=chat_history)
        
        response = chat.send_message(user_input)
        
        cleaned_response_text = response.text.strip().replace("```json", "").replace("```", "").strip()
        
        logging.info(f"Raw response from AI: {cleaned_response_text}")
        plan = json.loads(cleaned_response_text)
        return plan

    except json.JSONDecodeError as e:
        logging.error(f"JSON Decode Error: {e}. Response: {cleaned_response_text}")
        return {"plan": f"Terjadi kesalahan saat memproses respons dari AI. Coba lagi.\nDetail: {e}", "command": None, "requires_confirmation": False}
    except Exception as e:
        logging.error(f"An error occurred in analyze: {e}")
        return {"plan": f"Terjadi kesalahan: {e}", "command": None, "requires_confirmation": False}

def execute_plan(plan: dict) -> str:
    command = plan.get("command")
    if not command:
        return plan.get("plan", "Tidak ada aksi yang perlu dilakukan.")

    try:
        logging.info(f"Executing command: {command}")
        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            check=False
        )
        
        output = f"Output dari '{command}':\n---"
        if result.stdout:
            output += f"\n{result.stdout.strip()}"
        if result.stderr:
            output += f"\nError:\n{result.stderr.strip()}"
        output += "\n---"
        
        return output

    except Exception as e:
        logging.error(f"Failed to execute command '{command}': {e}")
        error_message = f"Gagal menjalankan perintah: {e}"
        return error_message