import tweepy
import pandas as pd
import configparser

#@@@@configs
config = configparser.ConfigParser()
config.read('config.ini')

api_key = config['twitter']['api_key']
api_key_secret = config['twitter']['api_key_secret']
access_token = config['twitter']['access_token']
access_token_secret = config['twitter']['access_token_secret']

#@@@@authentication

auth = tweepy.OAuthHandler(api_key,api_key_secret)
auth.set_access_token(access_token,access_token_secret)

api = tweepy.API(auth)

class Linstener(tweepy.Stream):
    tweets = []
    limit = 50
    def on_status(self,status):
        self.tweets.append(status)
        #print(status.user.screen_name + ':'+ status.text)
        if len(self.tweets) == self.limit:
            self.disconnect()

stream_tweet = Linstener(api_key,api_key_secret,access_token,access_token_secret)

# stream by keywords
keywords = ['python']
stream_tweet.filter(track=keywords)

#dataframe
columns = ['User','Tweet']
data = []

for tweet in stream_tweet.tweets:
    if not tweet.truncated:
        data.append([tweet.user.screen_name,tweet.text])
    else:
        data.append([tweet.user.screen_name, tweet.extended_tweet['full_text']])

df = pd.DataFrame(data,columns=columns)
df.to_csv('twitter_python.csv')
print(df)