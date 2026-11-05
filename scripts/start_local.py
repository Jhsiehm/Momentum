"""Open the private local workspace; keep this terminal open for scheduled checks."""
from pathlib import Path
import socket
import subprocess
import sys
import threading
import webbrowser

ROOT = Path(__file__).resolve().parents[1]
URL = 'http://127.0.0.1:8765/'

def main():
    try:
        with socket.create_connection(('127.0.0.1', 8765), timeout=1):
            print('A local service is already listening on port 8765. Opening the workspace URL.')
            webbrowser.open(URL)
            return
    except OSError:
        pass
    print('Starting the local workspace. Keep this window open for automatic checks. Press Control-C to stop.')
    timer = threading.Timer(2, lambda: webbrowser.open(URL))
    timer.daemon = True
    timer.start()
    try:
        subprocess.run([sys.executable, '-m', 'engine', 'serve', '--port', '8765'], cwd=ROOT, check=True)
    except KeyboardInterrupt:
        print('\nWorkspace stopped; saved records are retained.')

if __name__ == '__main__':
    main()
