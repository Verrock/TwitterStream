FROM python:3.10
WORKDIR /producer
COPY . .
RUN pip install -r requirements.txt
CMD ["python3", "kafka_twitter_producer.py"]
