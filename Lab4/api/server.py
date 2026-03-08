import os
import socket
import redis
import psycopg2
from http.server import BaseHTTPRequestHandler, HTTPServer
from prometheus_client import start_http_server, Counter
import time


REQUEST_COUNT = Counter("api_requests_total", "Total API Requests")
hostname = socket.gethostname()

redis_host = os.getenv("REDIS_HOST")
db_host = os.getenv("DB_HOST")

# Connect to Redis
while True:
    try:
        redis_client = redis.Redis(host=redis_host, port=6379, decode_responses=True)
        redis_client.ping()
        print("Connected to Redis")
        break
    except:
        print("Redis not ready, retrying...")
        time.sleep(2)

# Connect to Postgres
while True:
    try:
        conn = psycopg2.connect(
            host=db_host,
            database="demo",
            user="demo",
            password="demo"
        )
        print("Connected to Postgres")
        break
    except Exception as e:
        print("Postgres not ready, retrying...")
        time.sleep(2)

class Handler(BaseHTTPRequestHandler):

    def do_GET(self):

        REQUEST_COUNT.inc()
        
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

start_http_server(9000)
server = HTTPServer(("0.0.0.0", 8080), Handler)
server.serve_forever()