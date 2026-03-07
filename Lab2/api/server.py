import os
import socket
import redis
import psycopg2
from http.server import BaseHTTPRequestHandler, HTTPServer

hostname = socket.gethostname()

redis_host = os.getenv("REDIS_HOST")
db_host = os.getenv("DB_HOST")

# Connect to Redis
redis_client = redis.Redis(host=redis_host, port=6379, decode_responses=True)

# Connect to Postgres
conn = psycopg2.connect(
    host=db_host,
    database="demo",
    user="demo",
    password="demo"
)

class Handler(BaseHTTPRequestHandler):

    def do_GET(self):

        # Redis test
        redis_client.set("visits", redis_client.incr("visits"))
        visits = redis_client.get("visits")

        # Postgres test
        cur = conn.cursor()
        cur.execute("SELECT version();")
        db_version = cur.fetchone()[0]

        response = f"""
hostname: {hostname}
redis_host: {redis_host}
db_host: {db_host}
visits: {visits}
postgres_version: {db_version}
"""

        self.send_response(200)
        self.end_headers()
        self.wfile.write(response.encode())


server = HTTPServer(("0.0.0.0", 8080), Handler)
server.serve_forever()