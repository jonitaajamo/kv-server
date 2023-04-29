FROM python:3.11-slim-buster

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY kv_server/ /kv_server/

EXPOSE 80

CMD ["uvicorn", "kv_server.main:app", "--host", "0.0.0.0", "--port", "80"]
