FROM python:3.9-slim

WORKDIR /app

# Install netcat and curl for connectivity checks
RUN apt-get update && apt-get install -y netcat-openbsd curl && rm -rf /var/lib/apt/lists/* 

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]