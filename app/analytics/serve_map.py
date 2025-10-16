#!/usr/bin/env python3
import http.server
import socketserver
import os

os.chdir('figures')
PORT = 8000

Handler = http.server.SimpleHTTPRequestHandler
with socketserver.TCPServer(("", PORT), Handler) as httpd:
    print(f"Map server running at http://localhost:{PORT}")
    print("Press Ctrl+C to stop")
    httpd.serve_forever()