FROM python:3.11-slim
WORKDIR /app
COPY honeypot/decoy_server.py /app/decoy_server.py
ENV PYTHONUNBUFFERED=1
EXPOSE 2222
CMD ["python", "/app/decoy_server.py"]
