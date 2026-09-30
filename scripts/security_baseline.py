"""Small repository security gate with no third-party dependencies."""
from pathlib import Path
import re
import sys

ROOT=Path(__file__).resolve().parents[1]
TEXT_EXTENSIONS={".py",".yml",".yaml",".json",".toml",".md",".sql",".sh",".env.example"}
FORBIDDEN_PATTERNS=[
    re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH |DSA )?PRIVATE KEY-----"),
    re.compile(r"(?i)(?:aws_secret_access_key|private_key|client_secret|service_role)\s*[:=]\s*['"][^'"]{12,}['"]"),
]

def main()->int:
    failures=[]
    for path in ROOT.rglob("*"):
        if not path.is_file() or ".git" in path.parts or path.suffix not in TEXT_EXTENSIONS:
            continue
        try:
            text=path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        for pattern in FORBIDDEN_PATTERNS:
            if pattern.search(text):
                failures.append(str(path.relative_to(ROOT)))
                break
    if failures:
        print("Potential secret material detected in:")
        print("\n".join(sorted(failures)))
        return 1
    print("Repository security baseline: PASS")
    return 0

if __name__=="__main__":
    sys.exit(main())
