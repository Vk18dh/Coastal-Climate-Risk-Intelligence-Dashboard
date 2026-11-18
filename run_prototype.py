"""
Coastal Climate Risk Intelligence Dashboard — Master Prototype Launcher.

Starts both the FastAPI Backend (port 8000) and the React Frontend (port 5173),
and monitors both processes for a smooth demonstration.

Usage:
    python run_prototype.py
"""
import os
import sys
import time
import subprocess
import webbrowser

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
BACKEND_DIR = os.path.join(ROOT_DIR, "backend")
FRONTEND_DIR = os.path.join(ROOT_DIR, "frontend")

# Use virtual environment python if present
VENV_PYTHON = os.path.join(BACKEND_DIR, ".venv", "Scripts", "python.exe")
PYTHON_EXE = VENV_PYTHON if os.path.exists(VENV_PYTHON) else sys.executable

def main():
    print("=" * 70)
    print(" COASTAL CLIMATE RISK INTELLIGENCE DASHBOARD — PROTOTYPE LAUNCHER")
    print("=" * 70)
    print(f"[*] Root directory: {ROOT_DIR}")
    print(f"[*] Backend Python: {PYTHON_EXE}")

    # 1. Start FastAPI Backend
    print("\n[1/2] Launching FastAPI Backend on http://127.0.0.1:8000...")
    backend_cmd = [
        PYTHON_EXE,
        "-m",
        "uvicorn",
        "main:app",
        "--host",
        "0.0.0.0",
        "--port",
        "8000",
        "--reload",
    ]
    backend_proc = subprocess.Popen(
        backend_cmd,
        cwd=BACKEND_DIR,
        shell=(sys.platform == "win32"),
    )

    # Give backend a moment to initialize
    time.sleep(2)

    # 2. Start Vite Frontend
    print("[2/2] Launching React/Vite Frontend on http://localhost:5173...")
    npm_cmd = "npm run dev"
    frontend_proc = subprocess.Popen(
        npm_cmd,
        cwd=FRONTEND_DIR,
        shell=True,
    )

    # Wait for Vite to spin up and open browser
    time.sleep(3)
    target_url = "http://localhost:5173"
    print(f"\n[+] Opening browser at {target_url}...")
    try:
        webbrowser.open(target_url)
    except Exception:
        pass

    print("\n" + "=" * 70)
    print(" PROTOTYPE IS LIVE!")
    print(f" Frontend:  {target_url}")
    print(" Backend:   http://127.0.0.1:8000")
    print(" API Docs:  http://127.0.0.1:8000/docs")
    print(" Press Ctrl+C at any time to shut down both servers.")
    print("=" * 70 + "\n")

    try:
        while True:
            time.sleep(1)
            if backend_proc.poll() is not None:
                print("Backend process terminated.")
                break
            if frontend_proc.poll() is not None:
                print("Frontend process terminated.")
                break
    except KeyboardInterrupt:
        print("\n[*] Shutting down prototype services...")
    finally:
        try:
            backend_proc.terminate()
            frontend_proc.terminate()
        except Exception:
            pass
        print("[+] Prototype stopped successfully.")

if __name__ == "__main__":
    main()

