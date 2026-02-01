import subprocess
from pathlib import Path
import sys
import re

PROMPT = """
You are a Kubernetes configuration generator.

YOU MUST FOLLOW THESE RULES STRICTLY:

1. Output ONLY the requested files
2. DO NOT add explanations, comments, or text
3. DO NOT merge files
4. DO NOT omit any file
5. EACH file MUST start with its exact header

OUTPUT FORMAT (MANDATORY):

--- namespace.yaml ---
<YAML>

--- backend.yaml ---
<YAML>

--- frontend.yaml ---
<YAML>

REQUIREMENTS:
- Namespace name: billpay
- Backend: Deployment + Service, port 8080, ClusterIP
- Frontend: Deployment + Service, port 80, ClusterIP
- Use image placeholders (example: backend:latest)
- No ingress
- Valid Kubernetes YAML
"""


def run_llm():
    return subprocess.run(
        ["ollama", "run", "llama3"],
        input=PROMPT,
        text=True,
        capture_output=True
    )


def parse_sections(text):
    pattern = re.compile(
        r"---\s*(namespace\.yaml|backend\.yaml|frontend\.yaml)\s*---\n(.*?)(?=\n---|\Z)",
        re.DOTALL
    )
    return {name: content.strip() for name, content in pattern.findall(text)}


def main():
    print("🤖 Generating Kubernetes manifests...")

    attempts = 2
    for attempt in range(1, attempts + 1):
        result = run_llm()

        if result.returncode != 0:
            print(result.stderr)
            sys.exit(1)

        output = result.stdout.strip()
        sections = parse_sections(output)

        required = {"namespace.yaml", "backend.yaml", "frontend.yaml"}
        missing = required - sections.keys()

        if not missing:
            root = Path(__file__).resolve().parent.parent
            k8s_dir = root / "k8s"
            k8s_dir.mkdir(exist_ok=True)

            for name, content in sections.items():
                (k8s_dir / name).write_text(content)

            print("✅ Kubernetes manifests generated successfully:")
            for name in required:
                print(f" - k8s/{name}")
            return

        print(f"⚠️ Attempt {attempt} failed, missing: {missing}")

    # Final failure
    print("\n❌ Failed after retries. Raw LLM output:\n")
    print(output)
    sys.exit(1)


if __name__ == "__main__":
    main()
