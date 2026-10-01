"""Final repository-level enterprise validation gate."""
from __future__ import annotations
from pathlib import Path
import re
import sys

ROOT=Path(__file__).resolve().parents[1]
errors=[]

def require(path:str)->None:
    if not (ROOT/path).exists():
        errors.append(f"missing required path: {path}")

for path in ["README.md","LICENSE","SECURITY.md","CONTRIBUTING.md","CODEOWNERS",".github/workflows/ci.yml","schemas/api/openapi.yaml","docs/architecture/phases.md","docs/architecture/phase-27.md"]:
    require(path)

phase_doc=(ROOT/"docs/architecture/phases.md").read_text(encoding="utf-8")
for n in range(28):
    if f"Phase {n} " not in phase_doc:
        errors.append(f"phase {n} missing from phase index")

migration_numbers=[]
for path in (ROOT/"db/migrations").glob("*.sql"):
    match=re.match(r"(\d{4})_",path.name)
    if match:
        migration_numbers.append(int(match.group(1)))
if sorted(migration_numbers)!=list(range(1,22)):
    errors.append(f"migration sequence mismatch: {sorted(migration_numbers)}")

for path in ROOT.rglob("*"):
    if not path.is_file() or ".git" in path.parts:
        continue
    if path.suffix.lower() not in {".py",".md",".yaml",".yml",".js",".html",".css"}:
        continue
    try:
        text_value=path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        continue
    forbidden=("god"+"eye").lower()
    if forbidden in text_value.lower() or ("god"+"s"+" eye").lower() in text_value.lower():
        errors.append(f"forbidden historical product terminology found: {path}")
    if path.name=="app.js" and "apps/world-monitor" in str(path) and "innerHTML" in text_value:
        errors.append("World Monitor must not interpolate untrusted content with innerHTML")

ci=(ROOT/".github/workflows/ci.yml").read_text(encoding="utf-8")
if "actions/checkout@3d3c42e5aac5ba805825da76410c181273ba90b1" not in ci:
    errors.append("checkout action is not pinned to the approved immutable v7.0.1 commit")
if "information_schema.tables" not in ci or '= "44"' not in ci:
    errors.append("CI schema gate does not verify the expected 44-table schema")

readme=(ROOT/"README.md").read_text(encoding="utf-8")
if "Phase 0 and Phase 1 are implemented" in readme or "Phases 0–15 are now implemented" in readme or "Early foundation / active development" in readme:
    errors.append("README contains stale phase-status claims")

print("ENTERPRISE AUDIT: PASS" if not errors else "ENTERPRISE AUDIT: FAIL")
for error in errors:
    print(" - "+error)
sys.exit(1 if errors else 0)
