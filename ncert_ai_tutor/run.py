"""Launch script — starts FastAPI backend and React frontend."""

import subprocess
import sys
import os
import time
import shutil

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
REACT_DIR = os.path.join(PROJECT_ROOT, "frontend-react")


def find_npm():
    npm = shutil.which("npm")
    if npm:
        return npm
    # Windows: try common paths
    for p in [
        os.path.expandvars(r"%APPDATA%\npm\npm.cmd"),
        os.path.expandvars(r"%ProgramFiles%\nodejs\npm.cmd"),
    ]:
        if os.path.exists(p):
            return p
    return "npm"


def main():
    os.chdir(PROJECT_ROOT)

    env = os.environ.copy()
    env["PYTHONPATH"] = PROJECT_ROOT + os.pathsep + env.get("PYTHONPATH", "")

    print("=" * 60)
    print("  🎓 StudyMate AI — NCERT AI Tutor")
    print("  Starting services...")
    print("=" * 60)

    processes = []

    try:
        # Start FastAPI backend
        print("\n🚀 Starting FastAPI backend on http://127.0.0.1:8000 ...")
        backend = subprocess.Popen(
            [
                sys.executable, "-m", "uvicorn",
                "backend.main:app",
                "--host", "127.0.0.1",
                "--port", "8000",
                "--reload",
            ],
            env=env,
            cwd=PROJECT_ROOT,
        )
        processes.append(backend)

        time.sleep(3)

        # Start React dev server
        npm = find_npm()
        print("🎨 Starting React frontend on http://127.0.0.1:3000 ...")
        frontend = subprocess.Popen(
            [npm, "run", "dev"],
            env=env,
            cwd=REACT_DIR,
            shell=(os.name == "nt"),
        )
        processes.append(frontend)

        print("\n" + "=" * 60)
        print("  ✅ Both services running!")
        print("  📡 Backend API:  http://127.0.0.1:8000/docs")
        print("  🌐 Frontend UI:  http://127.0.0.1:3000")
        print("  Press Ctrl+C to stop both services.")
        print("=" * 60 + "\n")

        # Wait for either process to exit
        while True:
            for p in processes:
                if p.poll() is not None:
                    print(f"Process {p.pid} exited.")
                    raise KeyboardInterrupt
            time.sleep(1)

    except KeyboardInterrupt:
        print("\n🛑 Shutting down...")
        for p in processes:
            try:
                p.terminate()
                p.wait(timeout=5)
            except Exception:
                p.kill()
        print("Goodbye! 👋")


if __name__ == "__main__":
    main()
