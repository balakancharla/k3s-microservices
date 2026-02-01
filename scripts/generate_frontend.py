import subprocess
from pathlib import Path
import sys

PROMPT = """
You are a senior frontend engineer.

Generate a simple frontend microservice.

OUTPUT FORMAT (MANDATORY):
--- index.html ---
<code>

--- pay-bill.html ---
<code>

--- app.js ---
<code>

--- nginx.conf ---
<code>

REQUIREMENTS:
- Pure HTML + vanilla JavaScript
- Login page (username, password)
- Pay bill page (amount, bill type)
- On success show: Bill payment completed successfully
- Backend base URL: http://backend:8080
- No frameworks
- Clean, minimal UI
- No explanations
- No markdown
- Output ONLY the files in the specified format
"""


def main():
    print("🤖 Generating frontend code...")

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
    root = Path(__file__).resolve().parent.parent
    frontend_dir = root / "frontend"
    frontend_dir.mkdir(exist_ok=True)

    def extract(name):
        return output.split(f"--- {name} ---")[1].split("---")[0].strip()

    files = {
        "index.html": extract("index.html"),
        "pay-bill.html": extract("pay-bill.html"),
        "app.js": extract("app.js"),
        "nginx.conf": extract("nginx.conf"),
    }

    for fname, content in files.items():
        (frontend_dir / fname).write_text(content)

    print("✅ Frontend generated successfully")


if __name__ == "__main__":
    main()
