FROM python:3.12-slim

WORKDIR /auth-service

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . ./auth

EXPOSE 8000

CMD ["uvicorn", "auth.main:app", "--host", "0.0.0.0", "--port", "8000"]