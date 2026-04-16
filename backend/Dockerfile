ARG PYTHON_VERSION=3.13.13
FROM python:${PYTHON_VERSION}-slim

WORKDIR /app

RUN python -m pip install --upgrade pip
COPY requirements.txt .
RUN python -m pip install --no-cache-dir -r requirements.txt

EXPOSE 8000

CMD ["python3", "start_uvicorn.py"]
