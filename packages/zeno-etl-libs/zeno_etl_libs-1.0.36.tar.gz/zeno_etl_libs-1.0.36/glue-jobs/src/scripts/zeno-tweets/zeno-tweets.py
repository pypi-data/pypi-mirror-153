"""
Automailer for Zeno Tweets
author : neha.karekar@zeno.health
"""

import argparse
import sys
import re

sys.path.append('../../../..')

from zeno_etl_libs.logger import get_logger
from zeno_etl_libs.db.db import DB
from zeno_etl_libs.helper.aws.s3 import S3
from zeno_etl_libs.helper import helper
import pandas as pd
import dateutil
from dateutil.tz import gettz
from zeno_etl_libs.helper.email.email import Email
import numpy as np
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk.tokenize import word_tokenize, RegexpTokenizer, sent_tokenize
from nltk.corpus import stopwords
import time
import datetime
import os
import nltk

nltk.download('stopwords')
nltk.download('punkt')  # divides a whole text data into sentences
nltk.download('vader_lexicon')
import tweepy

parser = argparse.ArgumentParser(description="This is ETL script.")
parser.add_argument('-e', '--env', default="dev", type=str, required=False,
                    help="This is env(dev, stag, prod)")
parser.add_argument('-d', '--full_run', default=0, type=int, required=False)
parser.add_argument('-et', '--email_to', default="kuldeep.singh@zeno.health,neha.karekar@zeno.health", type=str, required=False)
args, unknown = parser.parse_known_args()
email_to = args.email_to
env = args.env
full_run = args.full_run
os.environ['env'] = env
logger = get_logger()
logger.info(f"full_run: {full_run}")

rs_db = DB(read_only=False)
rs_db.open_connection()

s3 = S3()

schema = 'prod2-generico'
table_name = 'zeno-tweets'
table_info = helper.get_table_info(db=rs_db, table_name=table_name, schema=schema)

# max of data
table_q = """
select
            date(max("tweet-created-at")) max_exp
        from
            "prod2-generico"."zeno-tweets" 
        """
max_exp_date = rs_db.get_df(table_q)
max_exp_date['max_exp'].fillna(np.nan, inplace=True)
print(max_exp_date.info())
max_exp_date = max_exp_date['max_exp'].to_string(index=False)
print(max_exp_date)

# params
if full_run or max_exp_date == 'NaN':
    start = '2017-05-13'
else:
    start = max_exp_date
start = dateutil.parser.parse(start)
print(start)
# defining keys and tokens

consumer_key = 'c57SU7sulViKSmjsOTi4kTO3W'
consumer_secret = 'cNT3yk5ibQ315AWNCJHgE9ipCGlM1XnenHZu9cBWaVL3q7fPew'
access_token = '796747210159517701-DhOBQgwzeb6q4eXlI4WjwPRJH1CuEIT'
access_token_secret = 'sMrnPZ4ExI8um43wquUvFEUCTyY61HYRf7z3jv00ltXlt'


# making api connection

# authentication

def auth(consumer_key, consumer_secret, access_token, access_token_secret):
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)
    return api


api = auth(consumer_key, consumer_secret, access_token, access_token_secret)


# remove url
def remove_url(txt):
    """Replace URLs found in a text string with nothing
    (i.e. it will remove the URL from the string).

    Parameters
    ----------
    txt : string
        A text string that you want to parse and remove urls.

    Returns
    -------
    The same txt string with url's removed.
    """

    return " ".join(re.sub("([^0-9A-Za-z \t])|(\w+:\/\/\S+)", "", txt).split())


# searching for the keyword in tweeter and tokenizing it
def tweet(search_term, count=100000):
    # Create a custom search term and define the number of tweets
    tweets = api.search_tweets(search_term, count=count)

    # Remove URLs
    tweets_no_urls = [remove_url(tweet.text) for tweet in tweets]
    # lowercase
    tweet_data = [sent_tokenize(x.lower()) for x in tweets_no_urls]
    tweet_data = pd.DataFrame(data=tweet_data, columns=['tweetext'])
    tweet_att = [[search_term, x.lang, x.user.location, x.created_at, x.id, x.user.name,
                  x.user.followers_count, x.user.friends_count, x.text, x.place, x.user.time_zone] for x in tweets]
    tweet_att = pd.DataFrame(data=tweet_att, columns=['search_term', 'lang', 'loc', 'created-at', 'id', 'username',
                                                      'followers', 'friends', 'og tweet', 'place', 'Tz'])
    final_data = pd.concat([tweet_data, tweet_att], axis=1)
    return final_data


# removing stopwords
def remove_sw(sent, corpus):
    stop_words = set(stopwords.words(corpus))

    word_tokens = word_tokenize(sent)

    filtered_sentence = [w for w in word_tokens if not w.lower() in stop_words]

    filtered_sentence = []

    for w in word_tokens:
        if w not in stop_words:
            filtered_sentence.append(w)
    filtered_sentence = ' '.join(filtered_sentence)
    return [filtered_sentence]


# finding sentiment intensity analyzer
def sentiment_analyser(lst):
    sid = SentimentIntensityAnalyzer()
    sentiment = [sid.polarity_scores(x) for x in lst]
    neg = [sid.polarity_scores(x)['neg'] for x in lst]
    neu = [sid.polarity_scores(x)['neu'] for x in lst]
    pos = [sid.polarity_scores(x)['pos'] for x in lst]
    comp = [sid.polarity_scores(x)['compound'] for x in lst]

    return neg[0], neu[0], pos[0], comp[0]


# running all above functions
def run_all(search_term, count=1000000):
    print("API handshake successful")
    print("Searching for term ", search_term)
    tweet_data = tweet(search_term, count=count)
    print(tweet_data)
    # print(tweet_data)
    print("Removing stopwords")
    sw = 'english'
    if tweet_data.empty:
        return tweet_data
    else:
        tweet_data['tweetext_filter'] = tweet_data['tweetext'].apply(lambda x: remove_sw(x, sw), 1)
        print(tweet_data)
        print("Analysing sentiment for ", search_term)
        print(tweet_data)
        tweet_data['neg', 'neu', 'pos', 'comp'] = tweet_data['tweetext_filter'].apply(lambda x: sentiment_analyser(x), 1)
        tweet_data[['neg', 'neu', 'pos', 'comp']] = tweet_data['neg', 'neu', 'pos', 'comp'].apply(pd.Series)
        tweet_data.drop(columns=('neg', 'neu', 'pos', 'comp'), inplace=True)
        # sentiment, neg, neu, pos, comp = sentiment_analyser(tweets)
        # df = build_df(pos,neg,neu,comp, tweets)
        print('Done \n')
        return tweet_data


search_terms = ['#zeno_health','@zeno_health']
tws = pd.DataFrame()
try:
    for search_term in search_terms:
        tw = run_all(search_term, count=1000000)
        tws = pd.concat([tws, tw], axis=0)
        print('Done')
        tws = tws[((tws['lang'].isin(['en', 'hi']) & (~tws['tweetext'].str.startswith('rt'))))]
except BaseException as e:
    print('failed on_status,', str(e))
    time.sleep(3)
tws

if tws.empty:
    print('DataFrame is empty!')
    exit()
tws = tws[
    ['og tweet', 'id', 'created-at', 'search_term', 'lang', 'loc', 'username', 'followers', 'friends', 'neg', 'neu',
     'pos', 'comp']]
dict = {'id': 'tweet-id',
        'og tweet': 'tweet',
        'search_term': 'search-term',
        'lang': 'language',
        'loc': 'location',
        'created-at': 'tweet-created-at',
        'pos': 'positive-sentiment',
        'neu': 'neutral-sentiment',
        'neg': 'negative-sentiment',
        'comp': 'compound-sentiment'}
tws.rename(columns=dict, inplace=True)
tws['tweet-created-at'] = pd.to_datetime(tws['tweet-created-at']). \
    dt.tz_convert('Asia/Kolkata').dt.tz_localize(None)
# etl
tws['created-at'] = datetime.datetime.now(tz=gettz('Asia/Kolkata')).strftime('%Y-%m-%d %H:%M:%S')
tws['updated-at'] = datetime.datetime.now(tz=gettz('Asia/Kolkata')).strftime('%Y-%m-%d %H:%M:%S')
tws['created-by'] = 'etl-automation'
tws['updated-by'] = 'etl-automation'
tws['tweet-type'] = np.where(tws['negative-sentiment'] >= tws['positive-sentiment'], 'Detractor', 'Promoter')
tws_mail = tws[['tweet-id', 'tweet', 'tweet-created-at', 'search-term', 'language', 'location', 'username', 'followers',
                'friends', 'tweet-type']]
tws_mail = tws_mail.sort_values(by=['tweet-type'], ascending=True)
print(tws_mail)

tws.columns = [c.replace('_', '-') for c in tws.columns]
if isinstance(table_info, type(None)):
    raise Exception(f"table: {table_name} do not exist, create the table first")
else:
    logger.info(f"Table:{table_name} exists")
print(start)
truncate_query = f''' DELETE FROM "{schema}"."{table_name}" where "tweet-created-at" >='{start}' '''
print(truncate_query)
rs_db.execute(truncate_query)
s3.write_df_to_db(df=tws[table_info['column_name']], table_name=table_name, db=rs_db,
                  schema=schema)
file_name = 'Zeno_Tweets.xlsx'
file_path = s3.write_df_to_excel(data={'Zeno Tweets': tws_mail}, file_name=file_name)

email = Email()
# file_path ='/Users/Lenovo/Downloads/utter.csv'
email.send_email_file(subject="Zeno Tweets",
                      mail_body='Zeno Tweets',
                      to_emails=email_to, file_uris=[], file_paths=[file_path])

# Closing the DB Connection
rs_db.close_connection()
