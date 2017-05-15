import bs4
import json
import os
import requests
import sys
import tqdm
import traceback
import tweepy


auth = tweepy.OAuthHandler(
    os.environ['consumer_key'],
    os.environ['consumer_secret']
)
auth.set_access_token(
    os.environ['access_token'],
    os.environ['access_token_secret']
)
api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)


def get_tweets(user, ntweets=3200):
    '''Get most recent ntweets tweets for user.'''
    cursor = tweepy.Cursor(api.user_timeline, id=user, include_rts=False,
                           count=min(ntweets, 200))
    tweets = {}
    for tweet in cursor.items(ntweets):
        tweets[tweet._json['id_str']] = tweet._json
    for tweet in tweets.values():
        tweet['user'] = tweet['user']['screen_name']
    return tweets


def scrape_reply_count_tweet(tweet):
    '''Scrape reply count from tweet page.'''
    url = f"http://twitter.com/{tweet['user']}/status/{tweet['id_str']}"
    page = bs4.BeautifulSoup(requests.get(url).text, 'lxml')
    span = (page
            .find("div", {"class": 'permalink-tweet'})
            .find("span", {"class": "ProfileTweet-actionCount"}))
    count = int(span.get('data-tweet-stat-count'))
    return count


def scrape_reply_counts_timeline_slice(timeline):
    '''
    Scrape all reply counts from a bs4 object representing a slice of a user
    timeline.
    '''
    counts = []
    for tweet in timeline.find_all("div", {"class": "tweet"}):
        tweet_id = tweet.get('data-item-id')
        reply_count = int(tweet
                          .find('span', {'class': 'ProfileTweet-actionCount'})
                          .get('data-tweet-stat-count'))
        counts.append((tweet_id, reply_count))
    return counts


def scrape_reply_counts_timeline(user):
    '''Scrape all the reply counts possible from a users timeline.'''
    counts = []
    root_url = f"https://twitter.com/i/profiles/show/{user}/timeline/tweets"
    url = root_url
    with tqdm.tqdm(total=1000) as pbar:  # 1000 ~= maximum timeline length
        while True:
            try:
                html = json.loads(requests.get(url).text)['items_html']
            except json.decoder.JSONDecodeError:
                return counts
            timeline = bs4.BeautifulSoup(html, 'lxml')
            newcounts = scrape_reply_counts_timeline_slice(timeline)
            counts += newcounts
            pbar.update(len(newcounts))
            oldest_tweet_seen = counts[-1][0]
            url = root_url + f"?max_position={oldest_tweet_seen}"


def add_reply_counts(tweets):
    '''Add 'reply_count' to each tweet in tweets.'''
    user = list(tweets.values())[0]['user']
    print('--- Scraping timeline')
    reply_counts = scrape_reply_counts_timeline(user)
    for tweet_id, reply_count in reply_counts:
        try:
            tweets[tweet_id]['reply_count'] = reply_count
        except KeyError:
            pass
    print('--- Getting missing tweets')
    for tweet_id, tweet in tqdm.tqdm(tweets.items()):
        if 'reply_count' not in tweet:
            try:
                tweet['reply_count'] = scrape_reply_count_tweet(tweet)
            except Exception as err:
                traceback.print_exc()
                return tweets
    return tweets


def filter_tweets(tweets, min_retweet_count=50, min_year='2016'):
    '''Filter tweets for frontend.'''
    filter_keys = {'user', 'text', 'created_at', 'retweet_count',
                   'reply_count', 'id_str'}
    tweets = [{k: v for k, v in tweet.items() if k in filter_keys}
              for tweet_id, tweet in tweets.items()
              if (tweet['retweet_count'] > min_retweet_count)
              and (tweet['created_at'].split()[-1] >= min_year)]
    return tweets


def get_and_save_user(user):
    '''Write raw/{user}.json and compressed/{user}.json using API/scraping.'''
    tweets = get_tweets(user)
    tweets = add_reply_counts(tweets)
    with open(f'raw/{user}.json', 'w') as f:
        json.dump(tweets, f)
    with open(f'compressed/{user}.json', 'w') as f:
        json.dump(filter_tweets(tweets), f)


if __name__ == '__main__':
    get_and_save_user(sys.argv[1])
