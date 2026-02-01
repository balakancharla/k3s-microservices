import subprocess
from pathlib import Path
import sys

PROMPT = """
You are a senior DevOps engineer.

Generate a Jenkinsfile.

OUTPUT FORMAT (MANDATORY):
--- Jenkinsfile ---
<code>

REQUIREMENTS:
- Kubernetes pod agent
- Docker build and push stages
- Build frontend and backend images
- Deploy to k3s using kubectl
- Use environment variables for image tags
- No explanations
- No markdown
"""


def main():
    print("🤖 Generating Jenkinsfile...")

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

    jenkinsfile = output.split("--- Jenkinsfile ---")[1].strip()
    (root / "Jenkinsfile").write_text(jenkinsfile)

    print("✅ Jenkinsfile generated successfully")


if __name__ == "__main__":
    main()
