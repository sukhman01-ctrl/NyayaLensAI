# pyrefly: ignore[missing-import]
import uvicorn
import sys
import os

if __name__ == "__main__":
    # Ensure current dir is in sys.path
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    print("[NyayaLens AI] Starting Backend Server on http://127.0.0.1:8000 ...")
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=False)
