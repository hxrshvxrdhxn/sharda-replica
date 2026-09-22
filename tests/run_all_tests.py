import subprocess
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

def run_suite(name: str, script_path: str):
    print("\n" + "=" * 80)
    print(f"RUNNING TEST SUITE: {name}")
    print("=" * 80)
    cmd = [str(BASE_DIR / "venv" / "Scripts" / "python.exe"), script_path]
    res = subprocess.run(cmd, cwd=str(BASE_DIR), capture_output=True, text=True, encoding="utf-8", errors="ignore")
    print(res.stdout)
    if res.stderr and "Error" in res.stderr:
        print("STDERR:", res.stderr)
    return res.returncode == 0

def run_pytest_suite(name: str, test_file: str):
    print("\n" + "=" * 80)
    print(f"RUNNING PYTEST SUITE: {name}")
    print("=" * 80)
    cmd = [str(BASE_DIR / "venv" / "Scripts" / "pytest.exe"), test_file, "-v", "-s"]
    res = subprocess.run(cmd, cwd=str(BASE_DIR), capture_output=True, text=True, encoding="utf-8", errors="ignore")
    print(res.stdout)
    if res.stderr and "Error" in res.stderr:
        print("STDERR:", res.stderr)
    return res.returncode == 0

def main():
    print("*" * 80)
    print("      SHARDA UNIVERSITY FULL ENTERPRISE END-TO-END (E2E) TEST RUNNER")
    print("*" * 80)

    suites = [
        ("1. Frontend Playwright E2E Suite", "tests/test_playwright_e2e.py"),
        ("2. Exact Replica & Backend Gemini RAG E2E Suite", "tests/test_replica_e2e.py"),
        ("3. All Footer Links In-App Routing Audit (69 Links)", "tests/test_all_footer_links.py"),
        ("4. All Header Navigation In-App Routing Audit (212 Links)", "tests/test_all_header_links.py"),
        ("5. Multi-Tier Deep Routes & Interactive Flows", "tests/test_exhaustive_suite.py")
    ]

    results = []

    for name, path in suites:
        ok = run_pytest_suite(name, path) if "pytest" in name or "exhaustive" in path else run_suite(name, path)
        results.append((name, ok))

    # Backend API tests
    backend_ok = run_pytest_suite("6. Backend FastAPI & CRM Security Suite", "tests/test_backend_api.py")
    results.append(("6. Backend FastAPI & CRM Security Suite", backend_ok))

    print("\n" + "=" * 80)
    print("                     E2E QUALITY AUDIT SCORECARD")
    print("=" * 80)
    all_passed = True
    for name, ok in results:
        status = "[PASS 100%]" if ok else "[FAIL]"
        if not ok:
            all_passed = False
        print(f" {status:<15} : {name}")
    print("=" * 80)

    if all_passed:
        print("\n>>> ALL END-TO-END TESTS PASSED WITH 100% ZERO DEFECTS! <<<\n")
        sys.exit(0)
    else:
        print("\n>>> Some test suites reported notices. <<<\n")
        sys.exit(1)

if __name__ == "__main__":
    main()
