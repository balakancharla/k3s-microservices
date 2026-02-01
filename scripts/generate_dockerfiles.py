import subprocess
from pathlib import Path
import sys

PROMPT = """
You are a DevOps engineer.

Generate Dockerfiles.

OUTPUT FORMAT (MANDATORY):
--- backend/Dockerfile ---
<code>

--- frontend/Dockerfile ---
<code>

REQUIREMENTS:
- Backend: Python 3.11 slim, Flask, gunicorn, port 8080
- Frontend: Nginx serving static files
- Optimized for k3s
- Non-root where possible
- No explanations
- No markdown
"""


def main():
    print("🤖 Generating Dockerfiles...")

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

    backend_docker = output.split("--- backend/Dockerfile ---")[1].split("--- frontend/Dockerfile ---")[0].strip()
    frontend_docker = output.split("--- frontend/Dockerfile ---")[1].strip()

    (root / "backend" / "Dockerfile").write_text(backend_docker)
    (root / "frontend" / "Dockerfile").write_text(frontend_docker)

    print("✅ Dockerfiles generated successfully")


if __name__ == "__main__":
    main()
