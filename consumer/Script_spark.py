# Imports
from pyspark import SparkContext 
from pyspark.sql import SparkSession
from pyspark.streaming import StreamingContext
from pyspark.sql import functions as F
from pyspark.sql.functions import *
from pyspark.sql.types import *
import json
import time
import pymongo
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import builtins
import time

time.sleep(90)

# Initialisation de Spark
connectionString = "mongodb://root:password@mongo:27017/"

spark = SparkSession.builder.appName("ProjetBigData")\
        .master("spark://spark:7077")\
        .config('spark.jars.packages', 'org.mongodb.spark:mongo-spark-connector_2.12:3.0.1') \
        .config('spark.mongodb.input.uri',connectionString) \
        .config('spark.mongodb.output.uri',connectionString) \
        .config("spark.jars.packages", "org.apache.spark:spark-sql-kafka-0-10_2.12:3.1.2") \
        .getOrCreate()

# Récupération d'un json pour servir de schéma

mySchema = StructType([StructField("id", StringType(), True)])
mySchema2 = StructType([StructField("created_at", StringType(), True)])
mySchema3 = StructType([StructField("author_id", StringType(), True)])
mySchema4 = StructType([StructField("lang", StringType(), True)])
mySchema5 = StructType([StructField("source", StringType(), True)])
mySchema6 = StructType([StructField("text", StringType(), True)])

# Lecture des données envoyées par Kafka

topic = "tweet_lyon"
bootstrap_server = "kafka:9092"

df1 = spark.readStream\
          .format("kafka")\
          .option("kafka.bootstrap.servers", bootstrap_server)\
          .option("subscribe", topic)\
          .option("startingOffsets", "latest")\
          .load()

values = df1.select(
    from_json(df1.value.cast("string"), mySchema).alias("id"),
    from_json(df1.value.cast("string"), mySchema2).alias("created_at"),
    from_json(df1.value.cast("string"), mySchema3).alias("author_id"),
    from_json(df1.value.cast("string"), mySchema4).alias("lang"),
    from_json(df1.value.cast("string"), mySchema5).alias("source"),
    from_json(df1.value.cast("string"), mySchema6).alias("text"),
)

df = values.select("id.*", "created_at.*", "author_id.*", "lang.*","source.*","text.*")
df.printSchema()

# Nettoyage du texte. Retire @Pseudo, hyperlinks (https://[...].[...]) et hastag
df = df.withColumn("text", F.regexp_replace("text", r"(@[A-Za-z0-9-_]+)", ""))
df = df.withColumn("text", F.regexp_replace("text", r"(http[A-Za-z0-9-:/._]+)", ""))
df = df.withColumn("text", F.regexp_replace("text", r"(#[A-Za-z0-9-:/._]+)", ""))

# Modèle d'analyse de sentiment VADER 
analyzer = SentimentIntensityAnalyzer()

# Prédit le sentiment en prenant le compound score
def compound_sentiment(text):
    vs = analyzer.polarity_scores(text)
    compound_score = vs['compound']
    if compound_score>=0.5:
        return 'positif'
    elif compound_score<=-0.5:
        return 'negatif'
    else:
        return 'neutre'
    
# User-Defined Functions:
udf_compound = F.udf(lambda x : analyzer.polarity_scores(x)['compound'], FloatType())
udf_sentiment = F.udf(lambda x : compound_sentiment(x), StringType())

# Rajout des colonnes "compound" et "sentiment"
df2 = df.withColumn('compound', udf_compound(df.text)) \
        .withColumn('sentiment', udf_sentiment(df.text))

# Connection à MongoDB
database = "Database_tweet"
collection = "tweets"

class WriteRowMongo:
    def open(self, partition_id, epoch_id):
        self.myclient = pymongo.MongoClient(connectionString)
        self.mydb = self.myclient[database]
        self.mycol = self.mydb[collection]
        return True

    def process(self, row):
        self.mycol.insert_one(row.asDict())

    def close(self, error):
        self.myclient.close()
        return True

# Ecriture des données dans MongoDB
streamingQuery = df2.writeStream.foreach(WriteRowMongo()).start()

# Arrêt du stream
streamingQuery.awaitTermination()     
