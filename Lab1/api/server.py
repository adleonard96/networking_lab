from http.server import BaseHTTPRequestHandler, HTTPServer
import socket

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        hostname = socket.gethostname()
        self.send_response(200)
        self.end_headers()
        self.wfile.write(f"Response from {hostname}".encode())

server = HTTPServer(("0.0.0.0", 8080), Handler)
server.serve_forever()