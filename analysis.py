import glob
import json
import os

import pandas as pd


def load_json(user):
    '''Load {user}.json.'''
    with open(user + '.json') as f:
        return json.load(f)


def tweets_to_df(tweets):
    '''Convert tweet json to DataFrame with datetime index and reply_ratio.'''
    df = pd.DataFrame.from_dict(tweets, orient='index')
    df['Date'] = pd.to_datetime(df['created_at'])
    df['reply_ratio'] = df['reply_count']/df['retweet_count']
    return df.set_index('Date')


def load_df():
    '''Load DataFrame of all json files.'''
    tweets = {}
    for jfile in glob.glob('raw/*.json'):
        user, _ = os.path.splitext(jfile)
        tweets.update(load_json(user))
    return tweets_to_df(tweets)
