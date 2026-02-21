#!/usr/bin/env python3
"""Simple HTTP server for Proverbs viewer."""
import http.server
import socketserver
import socket
import os

PORT = 8080

class MyHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        super().end_headers()

def get_ip():
    """Get the local IP address."""
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
    except Exception:
        ip = "127.0.0.1"
    finally:
        s.close()
    return ip

if __name__ == '__main__':
    os.chdir('/home/dangel/.openclaw/workspace')
    
    ip = get_ip()
    
    print(f"""
╔══════════════════════════════════════════════════════════════╗
║         PROVERBS FINANCIAL WISDOM VIEWER                     ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║  📱 Access from your phone:                                  ║
║                                                              ║
║     http://{ip}:{PORT}                                   ║
║                                                              ║
║  💻 Access from this computer:                              ║
║                                                              ║
║     http://localhost:{PORT}                                    ║
║     http://127.0.0.1:{PORT}                                    ║
║                                                              ║
║  Press Ctrl+C to stop the server                             ║
╚══════════════════════════════════════════════════════════════╝
""")
    
    with socketserver.TCPServer(("0.0.0.0", PORT), MyHandler) as httpd:
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n\nServer stopped.")
