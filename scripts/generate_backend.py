import subprocess
from pathlib import Path
import sys

PROMPT = """
You are a senior backend engineer.

Generate a production-ready Python Flask backend microservice.

OUTPUT FORMAT (MANDATORY):
--- app.py ---
<complete app.py code>

--- requirements.txt ---
<complete requirements.txt content>

REQUIREMENTS:
- Flask microservice
- POST /api/login
- POST /api/pay-bill
- GET /api/health
- JSON request/response only
- Simple hardcoded login validation
- Pay bill returns success message
- Runs on port 8080
- No debug mode
- Clean, readable structure
- No placeholders
- Code must be runnable
- Do NOT explain anything
- Do NOT use markdown
- Output ONLY the files in the specified format
"""


def generate_backend_code():
    print("🤖 Asking Ollama to generate backend microservice code...")

    result = subprocess.run(
        ["ollama", "run", "llama3"],
        input=PROMPT,
        text=True,
        capture_output=True
    )

    if result.returncode != 0:
        print(result.stderr)
        sys.exit(1)

    output = result.stdout.strip()

    project_root = Path(__file__).resolve().parent.parent
    backend_dir = project_root / "backend"    
    backend_dir.mkdir(exist_ok=True)

    try:
        app_code = output.split("--- app.py ---")[1].split("--- requirements.txt ---")[0].strip()
        requirements_code = output.split("--- requirements.txt ---")[1].strip()
    except IndexError:
        print("❌ Failed to parse LLM output. Raw output below:\n")
        print(output)
        sys.exit(1)

    app_file = backend_dir / "app.py"
    req_file = backend_dir / "requirements.txt"

    app_file.write_text(app_code)
    req_file.write_text(requirements_code)

    print("✅ Backend microservice generated successfully:")
    print(f" - {app_file}")
    print(f" - {req_file}")
    print("➡️ Review the files before running them!")


if __name__ == "__main__":
    generate_backend_code()
