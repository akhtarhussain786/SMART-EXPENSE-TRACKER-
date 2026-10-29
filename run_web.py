"""
Launcher script for Smart Expense Tracker Web Application.
Starts Uvicorn server and automatically opens the default web browser.
"""

import sys
import os
import time
import webbrowser
import threading
import uvicorn

def open_browser():
    time.sleep(1.2)
    print("\n[INFO] Opening Web Browser at http://127.0.0.1:8000 ...")
    webbrowser.open("http://127.0.0.1:8000")

def main():
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    print("=" * 65)
    print("   🌐 STARTING SMART EXPENSE TRACKER WEB APPLICATION")
    print("   📍 URL: http://127.0.0.1:8000")
    print("   ✨ Features: Add Expense, Remove Expense, Live Auto-Categorize")
    print("=" * 65)

    # Launch browser in separate daemon thread
    threading.Thread(target=open_browser, daemon=True).start()

    # Start Uvicorn
    uvicorn.run("web_app:app", host="127.0.0.1", port=8000, log_level="info")

if __name__ == "__main__":
    main()

