import os

os.environ["SPARK_HOME"] = "C:\\Users\\Walter\\Spark-Hadoop\\spark-2.3.1-bin-hadoop2.7"
os.environ["HADOOP_HOME"] = "C:\\winutils"

import json
from pyspark import SparkContext
from pyspark.streaming import StreamingContext

def convertTweet(tweet):
    #changes json to string and splits at spaces
    tweetStr = tweet.encode('utf-8')
    tweetDict = json.loads(tweetStr)
    text = tweetDict["text"]
    splitTweet = (text.encode('utf-8')).split(' ')
    return splitTweet

spark = SparkContext("local", "twitter wordCount")
sparkStream = StreamingContext(spark, 10)
IP = "localhost"
Port = 8888
lines = sparkStream.socketTextStream(IP, Port)

#convert/split each tweet into a flatmap
splitWords = lines.flatMap(lambda line: convertTweet(line))

#map each word to a value of 1, then reduce by key
wordCount = splitWords.map(lambda word: (word, 1)).reduceByKey(lambda x, y: x + y)

#print results
wordCount.pprint()

sparkStream.start()
sparkStream.awaitTermination()