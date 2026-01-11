FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .

# Upgrade pip first
RUN pip install --upgrade pip --default-timeout=200

# Install heavy packages with increased timeout
RUN pip install --default-timeout=200 --no-cache-dir -r requirements.txt -i https://pypi.org/simple

COPY . .

EXPOSE 9000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
