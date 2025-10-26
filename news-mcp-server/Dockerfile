FROM python:3.9.7-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY news-server.py .
CMD ["python", "news-server.py"]
