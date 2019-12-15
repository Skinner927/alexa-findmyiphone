FROM python:3.6-alpine

WORKDIR /app
ADD ./app.py ./requirements.txt ./serve.py /app/
RUN pip install -r requirements.txt
EXPOSE 8080
STOPSIGNAL SIGINT

CMD ["python", "serve.py"]
