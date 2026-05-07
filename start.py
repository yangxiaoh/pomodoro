#!/usr/bin/env python3
"""
Pomodoro Timer Launcher
Opens the tomato clock in the default browser.
"""

import os
import sys
import webbrowser
import signal
import http.server
import socketserver
import threading
import time


PORT = 18725
DIR = os.path.dirname(os.path.abspath(__file__))

# 用于优雅关闭的信号量
_shutdown_event = threading.Event()


class QuietHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIR, **kwargs)

    def log_message(self, format, *args):
        pass


def start_server():
    server = socketserver.TCPServer(("127.0.0.1", PORT), QuietHandler)
    server.serve_forever()


def open_browser():
    time.sleep(0.5)
    webbrowser.open(f"http://127.0.0.1:{PORT}")


def handle_signal(sig, frame):
    _shutdown_event.set()


def main():
    print()
    print("  ╭──────────────────────╮")
    print("  │   🍅 番茄钟 Pomodoro │")
    print("  ╰──────────────────────╯")
    print()

    signal.signal(signal.SIGINT, handle_signal)
    signal.signal(signal.SIGTERM, handle_signal)

    server_thread = threading.Thread(target=start_server, daemon=True)
    server_thread.start()

    open_browser()

    try:
        _shutdown_event.wait()
    except KeyboardInterrupt:
        pass

    print("\n  👋 再见！")


if __name__ == "__main__":
    main()
