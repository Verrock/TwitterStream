from re import search
from kafka import KafkaProducer
from kafka.errors import KafkaError
import tweepy
import json
import time
import config

time.sleep(90)

class MyStream(tweepy.StreamingClient):
    #Create the kafka producer to be used
    producer = KafkaProducer(bootstrap_servers=['kafka:9092'], value_serializer=lambda m: json.dumps(m).encode('utf-8'))

    #Activate on connection with the twitter API, print "connected" if successfull
    def on_connect(self):
        print("Connected")

    #Activate every time a tweet correspod to our filter
    def on_tweet(self, tweet):
        data = tweet.data
        data["id"] = (tweet.id)
        data["created_at"] = str(tweet.created_at)
        data["author_id"] = str(tweet.author_id)
        data["lang"] = str(tweet.lang)
        data["source"] = str(tweet.source)
        data["text"] = str(tweet.text)
        self.producer.send('tweet_lyon', data)


if __name__ == '__main__': 
    bear_token = config.bearer_token
    stream = MyStream(bearer_token=bear_token)
    stream.add_rules(tweepy.StreamRule("#Brexit lang:en -is:retweet"))
    #stream.delete_rules(['1570674960586137602'])
    print(stream.get_rules())
    stream.filter(tweet_fields=['author_id', 'created_at', 'lang', 'source'])
