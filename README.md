# Data Stream Twitter


## Getting started
Change the sentence/word/hashtag you want to track in the kafka producer/kafka_twitter_producer.py
Change the bearer_token for your Twitter API Token in producer/config.py

To launch the project : docker compose up 

## Twitter stream

WARNING: This project may not work anymore since I did not maintain and follow the possible Twitter API changes.

## Imporvement to be done

- [ ] Implement a better sentiment analysis using Spark
- [ ] Configure and parametrize with Hydra
- [ ] Better visualisation using boards such as Kibana, Plotly or other. (Currently a simple PoC with Streamlit)


## Project status

Project done a year ago. Not maintained, may not work anymore due to Twitter API Change.