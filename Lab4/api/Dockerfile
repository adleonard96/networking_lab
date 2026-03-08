FROM python:3.11-slim

WORKDIR /app

COPY server.py .

RUN pip install redis psycopg2-binary prometheus-client

CMD ["python", "server.py"]