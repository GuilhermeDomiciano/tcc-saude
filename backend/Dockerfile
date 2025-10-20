FROM python:3.12-slim
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1
WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential curl ca-certificates && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install -U pip && pip install -r requirements.txt

# Copy the backend source (there is no ./app directory; main.py is at repo root)
COPY . .

EXPOSE 8000
CMD ["bash","-lc","echo 'api blank' && sleep infinity"]
