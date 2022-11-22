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

public_tweets = api.home_timeline()

#print(public_tweets[0].text)


#@@@@from specific users
print("==================tweets from certain users====================")
columns = ['User','tweets']
data_user = []

user = 'pontiff_lcy'
limit = 10
tweets_users = tweepy.Cursor(api.user_timeline,screen_name=user,count=200,tweet_mode='extended').items(limit)
#tweets = api.user_timeline(screen_name=user,count=limit,tweet_mode='extended') 200 at maximum

for tweet in tweets_users:
    data_user.append([tweet.user.screen_name,tweet.full_text])
df_user = pd.DataFrame(data_user,columns=columns)
print(df_user)

#@@@@from hashtags
print("==================tweets from hashtags====================")
columns = ['User','tweets']
data_hashtags = []

keywords = '政治'
limit = 100
tweets_keywords = tweepy.Cursor(api.search_tweets,q=keywords,count=100,tweet_mode='extended').items(limit)

for tweet in tweets_keywords:
    data_hashtags.append([tweet.user.screen_name,tweet.full_text])

df_hashtags = pd.DataFrame(data_hashtags,columns=columns)
print(df_hashtags)

print(len(data_hashtags))

#df_hashtags.to_csv('twitter_politics.csv')