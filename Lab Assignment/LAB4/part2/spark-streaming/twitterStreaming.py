#code derived from example found at http://adilmoujahid.com/posts/2014/07/twitter-analytics/

import os

os.environ["SPARK_HOME"] = "C:\\Users\\Walter\\Spark-Hadoop\\spark-2.3.1-bin-hadoop2.7"
os.environ["HADOOP_HOME"]="C:\\winutils"

from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
import requests_oauthlib
import socket

# Replace the values below with yours
ACCESS_TOKEN = 'TWITTER_ACCESS_TOKEN'
ACCESS_SECRET = 'TWITTER_ACCESS_SECRET'
CONSUMER_KEY = 'TWITTER_CONSUMER_KEY'
CONSUMER_SECRET = 'TWITTER_CONSUMER_SECRET'
my_auth = requests_oauthlib.OAuth1(CONSUMER_KEY, CONSUMER_SECRET,ACCESS_TOKEN, ACCESS_SECRET)

class TweetsListener(StreamListener):

    def __init__(self, csocket):
        self.client_socket = csocket

    def on_data(self, data):
        try:
            print(data.split())
            self.client_socket.send(data)
            return True
        except BaseException as e:
            print("Error on_data: %s" % str(e))
        return True

    def on_error(self, status):
        print(status)
        return True


def sendData(c_socket):
    #set authentication keys
    auth = OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)

    #create connection
    twitter_stream = Stream(auth, TweetsListener(c_socket))

    #filter for tweets using term Trump
    twitter_stream.filter(track=['collusion'])


if __name__ == "__main__":
    #create and bind a socket to allow connection
    s = socket.socket()
    host = "localhost"
    port = 8888
    s.bind((host, port))

    #print("Listening on port: %s" % str(port))

    s.listen(5)  # Now wait for client connection.
    c = s.accept()
    addr = c  # Establish connection with client.

    #print("Received request from: " + str(addr))

    sendData(c)
