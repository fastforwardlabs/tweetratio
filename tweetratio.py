import backoff
import bs4
import json
import logging
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
logging.basicConfig(filename='log.log', level=logging.INFO,
                    format='%(levelname)s:%(asctime)s:%(message)s')


def get_tweets(user, ntweets=3200):
    '''Get most recent ntweets tweets for user.'''
    cursor = tweepy.Cursor(api.user_timeline, id=user, include_rts=False,
                           count=min(ntweets, 200))
    tweets = {}
    for tweet in cursor.items(ntweets):
        tweets[tweet._json['id_str']] = tweet._json
    return tweets


@backoff.on_exception(backoff.expo,
                      (requests.exceptions.Timeout,
                       requests.exceptions.ConnectionError,
                       AttributeError),
                      max_tries=8)
def scrape_reply_count_tweet(tweet):
    '''Scrape reply count from tweet page.'''
    url = (f"http://twitter.com/{tweet['user']['screen_name']}"
           f"/status/{tweet['id_str']}")
    try:
        page = bs4.BeautifulSoup(requests.get(url).text, 'lxml')
        span = (page
                .find("div", {"class": 'permalink-tweet'})
                .find("span", {"class": "ProfileTweet-actionCount"}))
        count = int(span.get('data-tweet-stat-count'))
    except:
        logging.error(f'Failed to scrape {url}')
        raise
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
                json_payload = json.loads(requests.get(url).text)
                if not json_payload["has_more_items"]:
                    return counts
                else:
                    html = json_payload['items_html']
            except json.decoder.JSONDecodeError:
                logging.exception(f'Failed at {url}')
                return counts
            timeline = bs4.BeautifulSoup(html, 'lxml')
            newcounts = scrape_reply_counts_timeline_slice(timeline)
            counts += newcounts
            pbar.update(len(newcounts))
            oldest_tweet_seen = counts[-1][0]
            url = root_url + f"?max_position={oldest_tweet_seen}"


def count_reply_counts(tweets):
    '''Returns number of tweets that have reply_count set.'''
    return sum(('reply_count' in tweet) and (tweet['reply_count'] is not None)
               for tweet in tweets.values())


def add_reply_counts(tweets):
    '''Add 'reply_count' to each tweet in tweets.'''
    user = list(tweets.values())[0]['user']['screen_name']
    print('--- Scraping timeline')
    reply_counts = scrape_reply_counts_timeline(user)
    for tweet_id, reply_count in reply_counts:
        try:
            tweets[tweet_id]['reply_count'] = reply_count
        except KeyError:
            pass
    logging.info(f'Added {count_reply_counts(tweets)}'
                 + ' reply counts from timeline')
    print('--- Getting missing tweets')
    for tweet_id, tweet in tqdm.tqdm(tweets.items()):
        if 'reply_count' not in tweet:
            try:
                tweet['reply_count'] = scrape_reply_count_tweet(tweet)
            except Exception as err:
                traceback.print_exc()
                return tweets
    logging.info(f'Acquired {count_reply_counts(tweets)} reply counts')
    return tweets


def load_json(jsonf):
    '''Load jsonf.'''
    with open(jsonf) as f:
        return json.load(f)


def save_json(data, jsonf):
    with open(jsonf, 'w') as f:
        json.dump(data, f)


def scrape_user(user):
    tweets = get_tweets(user)
    logging.info(f'Got {len(tweets)} tweets from API')
    tweets = add_reply_counts(tweets)
    return tweets


def get_user(user, save=True, rescrape=True):
    '''Gets tweets for user.'''
    logging.info(f'Get @{user}')
    rawf = f'raw/{user}.json'
    if rescrape or not os.path.exists(rawf):
        logging.info(f'Scrape @{user}')
        tweets = scrape_user(user)
        # Save only if scraping fresh data
        if save:
            logging.info(f'Save @{user}')
            save_json(tweets, rawf)
    else:
        logging.info(f'Load @{user}')
        tweets = load_json(rawf)
    return tweets


if __name__ == '__main__':
    get_user(sys.argv[1])
