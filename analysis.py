import glob
import logging
import tweetratio

import matplotlib.pyplot as plt
import pandas as pd


def tweets_to_df(tweets):
    '''Convert tweet json to DataFrame with datetime index and reply_ratio.'''
    df = pd.DataFrame.from_dict(tweets, orient='index')
    df['created_at'] = pd.to_datetime(df['created_at'])
    df['user'] = df['user'].apply(lambda user_dict: user_dict['screen_name'])
    df['replies_per_retweet'] = df['reply_count']/df['retweet_count']
    return df.set_index('created_at')


def load_df():
    '''Load DataFrame of all json files.'''
    tweets = {}
    for jsonf in glob.glob('raw/*.json'):
        tweets.update(tweetratio.load_json(jsonf))
    return tweets_to_df(tweets)


def n_worst_tweets(df, n=5):
    return df.sort_values('replies_per_retweet', ascending=False).iloc[:n]


def save_worst_tweets(df, min_retweets=50):
    (df
     .query(f'retweet_count > {min_retweets}')
     .groupby('user').apply(n_worst_tweets)
     [['user', 'replies_per_retweet', 'created_at', 'reply_count',
       'retweet_count', 'id_str', 'text']]
     .to_csv('worst_tweets.csv'))


def plot_trend(df, sample='W', start="2016", min_retweets=50,
               users=('realDonaldTrump', 'dril', 'BernieSanders')):
    fig, ax = plt.subplots()
    df = (df[df['user'].isin(users)]
          .loc[start:]
          .query(f'retweet_count > {min_retweets}'))
    ax = (df
          .groupby([pd.TimeGrouper(sample), 'user'])['replies_per_retweet']
          .mean()
          .unstack()
          .plot(ax=ax))
    ax.set_ylabel('Replies per retweet')
    fig.savefig("fig.png", bbox_inches='tight')


def clobber_user(tweets):
    for tweet_id, tweet in tweets.items():
        try:
            tweet['user'] = tweet['user']['screen_name']
        except TypeError:
            pass
    return tweets


def filter_tweets(tweets, min_retweet_count=50, min_year='2016'):
    '''Filter tweets for frontend.'''
    filter_keys = {'user', 'text', 'created_at', 'retweet_count',
                   'reply_count', 'id_str'}
    filtered_tweets = [{k: v for k, v in tweet.items() if k in filter_keys}
                       for tweet_id, tweet in tweets.items()
                       if (tweet['retweet_count'] > min_retweet_count)
                       and (tweet['created_at'].split()[-1] >= min_year)]
    logging.info(f'Filtered {len(tweets)} to {len(filtered_tweets)} tweets')
    return filtered_tweets


def write_csv(tweets, csvf):
    pd.DataFrame(tweets).to_csv(csvf)


def merge_jsons(infiles):
    '''
    Merge a list of json files, oldest first. If a key exists in several files,
    value in newest file is preferred.
    '''
    merged_tweets = {}
    tweetses = [tweetratio.load_json(infile) for infile in infiles]
    for tweets in tweetses:
        merged_tweets.update(tweets)
    return merged_tweets


def process(user, **kwargs):
    '''Write minified json and csv for user.'''
    tweets = tweetratio.load_json(f'raw/{user}.json')
    tweets = clobber_user(tweets)
    tweets = filter_tweets(tweets, **kwargs)
    tweetratio.save_json(tweets, f'minified/{user}.json')
    write_csv(tweets, f'csv/{user}.csv')
