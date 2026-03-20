import json
import os
import socket
import threading
import urllib.request
from http.server import BaseHTTPRequestHandler, HTTPServer

API_BASE = os.getenv("API_BASE", "http://backend:8000/api/v1")
MODE = os.getenv("MODE", "ssh")
PORT = int(os.getenv("PORT", "2222"))
CHANNEL = os.getenv("CHANNEL", MODE)


def _post(path, payload):
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        f"{API_BASE}{path}",
        data=data,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=3) as resp:
        return json.loads(resp.read().decode("utf-8"))


def _start_session(source_ip):
    return _post(
        "/sessions/start",
        {"attacker_id": f"decoy-{MODE}", "source_ip": source_ip, "channel": CHANNEL},
    )


def _send_command(session_id, command):
    return _post(
        f"/sessions/{session_id}/command",
        {"command": command, "typing_duration_ms": 800},
    )


class DecoyHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        session = _start_session(self.client_address[0])
        _send_command(session["session_id"], f"GET {self.path}")
        body = f"<html><body><h2>Service {MODE}</h2><p>Temporarily under maintenance.</p></body></html>"
        self.send_response(200)
        self.send_header("Content-Type", "text/html")
        self.end_headers()
        self.wfile.write(body.encode("utf-8"))

    def do_POST(self):
        length = int(self.headers.get("Content-Length", "0"))
        payload = self.rfile.read(length).decode("utf-8", errors="ignore")
        session = _start_session(self.client_address[0])
        _send_command(session["session_id"], f"POST {self.path} {payload[:200]}")
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(b"{\"status\":\"ok\"}")

    def log_message(self, *_args, **_kwargs):
        return


def run_http():
    server = HTTPServer(("0.0.0.0", PORT), DecoyHTTPRequestHandler)
    server.serve_forever()


def run_tcp():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(("0.0.0.0", PORT))
    sock.listen(50)

    while True:
        conn, addr = sock.accept()
        source_ip = addr[0]
        session = _start_session(source_ip)
        try:
            conn.sendall(b"SSH-2.0-OpenSSH_8.2p1 Ubuntu-4ubuntu0.5\n")
            data = conn.recv(1024)
            command = data.decode("utf-8", errors="ignore").strip() or "<connect>"
            _send_command(session["session_id"], command)
            conn.sendall(b"Access denied\n")
        except Exception:
            pass
        finally:
            conn.close()


def main():
    if MODE == "http":
        run_http()
    else:
        run_tcp()


if __name__ == "__main__":
    main()
