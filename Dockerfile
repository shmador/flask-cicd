FROM python:3.11
WORKDIR /app

COPY app.py .
COPY requirements.txt .

RUN pip install --no-cache-dir --progress-bar off -r requirements.txt

EXPOSE 5000
CMD ["python", "app.py", "--host=0.0.0.0"]

