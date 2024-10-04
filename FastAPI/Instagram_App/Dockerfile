FROM python:3.9.19-slim

WORKDIR /app

COPY . .

RUN pip install --upgrade pip
RUN pip install -r requ.txt

# CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]



