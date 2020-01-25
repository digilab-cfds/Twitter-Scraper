import tweepy
from tweepy import OAuthHandler
import pandas as pd

def get_create_date(result):
    return result.created_at.strftime("%m/%d/%Y")

def get_tweet_id(result):
    return result.id

def search_tweets(queries, max_date, tweet_attributes):
    for query in queries:
        search_results = api.search(q=query, lang='id', result_type='recent', count=1, tweet_mode='extended')
        last_date = get_create_date(search_results[0])
        print(last_date)
        last_id = get_tweet_id(search_results[0])    

        while last_date != max_date:
            
            search_results = api.search(q=query, lang='id',max_id=last_id-1, count=100, tweet_mode="extended")

            for result in search_results:
                tweet_attributes['id'].append(result.id)
                tweet_attributes['date'].append(result.created_at.strftime("%m/%d/%Y"))
                tweet_attributes['time'].append(result.created_at.strftime("%H:%M:%S"))
                tweet_attributes['user_id'].append(result.user.id_str)
                tweet_attributes['name'].append(result.user.name)
                tweet_attributes['username'].append(result.user.screen_name)
                tweet_attributes['tweet'].append(result.full_text)
                tweet_attributes['retweet_count'].append(result.retweet_count)
                tweet_attributes['favorite_count'].append(result.favorite_count)
                url = 'https://twitter.com/{username}/status/{id_tweet}'.format(username=result.user.screen_name, id_tweet=result.id)
                tweet_attributes['link_tweet'].append(url)
                
                try:
                    tweet_attributes['url_in_tweet'].append(result.entities['urls'][0]['url'])
                except:
                    tweet_attributes['url_in_tweet'].append('-')
                
                try:
                    tweet_attributes['in_reply_to_status'].append(result.in_reply_to_screen_name)
                except:
                    tweet_attributes['in_reply_to_status'].append('')
                    
                tweet_attributes['is_quote_status'].append(result.is_quote_status)
                tweet_attributes['hashtags'].append(result.entities['hashtags'])

            last_date = get_create_date(result)
            last_id = get_tweet_id(result)   
            print(last_date)
            if last_date == max_date:
                break

    
    tweet_attributes_df = pd.DataFrame(tweet_attributes)
    return tweet_attributes_df

ACCESS_TOKEN = '...'
ACCESS_SECRET = '...'
API_KEY = '...'
API_SECRET = '...'

tweet_attributes = {
        'id' : [],
        'date' : [],
        'time' : [],
        'user_id' : [],
        'name' : [],
        'username' : [],
        'tweet' : [],
        'retweet_count' : [],
        'favorite_count' : [],
        'link_tweet' : [],
        'url_in_tweet' : [],
        'hashtags' : [],
        'in_reply_to_status' : [],
        'is_quote_status' : []
        }

auth = OAuthHandler(API_KEY, API_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)
api = tweepy.API(auth, wait_on_rate_limit=True,
                 wait_on_rate_limit_notify=True)

queries = ['#nkcthi -filter:retweets']
search_results = search_tweets(queries=queries, max_date='01/20/2020', tweet_attributes=tweet_attributes)


