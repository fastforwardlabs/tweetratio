import glob
import json
import os

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


def load_json(user):
    '''Load {user}.json.'''
    with open(user + '.json') as f:
        return json.load(f)


def tweets_to_df(tweets):
    '''Convert tweet json to DataFrame with datetime index and reply_ratio.'''
    df = pd.DataFrame.from_dict(tweets, orient='index')
    df['Date'] = pd.to_datetime(df['created_at'])
    df['replies_per_retweet'] = df['reply_count']/df['retweet_count']
    return df.set_index('Date').query('retweet_count > 50')


def load_df():
    '''Load DataFrame of all json files.'''
    tweets = {}
    for jfile in glob.glob('raw/*.json'):
        user, _ = os.path.splitext(jfile)
        tweets.update(load_json(user))
    return tweets_to_df(tweets)


def n_worst_tweets(df, n=5):
    return df.sort_values('replies_per_retweet', ascending=False).iloc[:n]


def save_worst_tweets(df):
    (df.groupby('user').apply(n_worst_tweets)
     [['user', 'replies_per_retweet', 'created_at', 'reply_count',
       'retweet_count', 'id_str', 'text']]
     .to_csv('worst_tweets.csv'))


def plot_trend(df, sample='W', start="2016",
               users=('realDonaldTrump', 'dril', 'BernieSanders')):
    fig, ax = plt.subplots()
    df = df[df['user'].isin(users)].loc[start:]
    df = df[np.isfinite(df['replies_per_retweet'])]
    ax = (df
          .groupby([pd.TimeGrouper(sample), 'user'])['replies_per_retweet']
          .mean()
          .unstack()
          .plot(ax=ax))
    ax.set_ylabel('Replies per retweet')
    fig.savefig("fig.png", bbox_inches='tight')
