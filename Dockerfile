FROM python:3.7.3-alpine3.9

WORKDIR app

COPY . .
RUN pip install -r requirements.txt --no-cache-dir

EXPOSE 8080

CMD ["python", "app.py"]
