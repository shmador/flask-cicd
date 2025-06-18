FROM python:3.11
WORKDIR /app
COPY app.py .
COPY requirements.txt .
ENV RICH_NO_THREADS=1
RUN pip install --no-cache-dir -r requirements.txt
EXPOSE 5000
CMD ["python", "app.py", "--host=0.0.0.0"]
