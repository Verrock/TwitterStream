FROM python:3.8
WORKDIR /streamlit

COPY . .

EXPOSE 8501

RUN pip install -r requirements.txt

ENTRYPOINT ["streamlit", "run", "Sentiment_Analysis.py", "--server.port=8501", "--server.address=0.0.0.0"]
