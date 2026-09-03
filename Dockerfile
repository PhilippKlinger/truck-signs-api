FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

RUN apt-get update \
    && apt-get install --no-install-recommends --yes netcat-openbsd \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt ./
RUN python -m pip install --no-cache-dir -r requirements.txt

COPY . .

RUN sed -i 's/\r$//' /app/entrypoint.sh \
    && chmod +x /app/entrypoint.sh

WORKDIR /app/src

EXPOSE 8000

ENTRYPOINT ["/app/entrypoint.sh"]
