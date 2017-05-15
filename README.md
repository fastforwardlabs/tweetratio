# Twitter reply-to-retweet scraping code

## Installation

Requirements: Python 3.6+

```bash
$ git clone <URL>
$ cd tweetratio
$ python3 -m virtualenv venv
$ source venv/bin/activate
$ pip install -r requirements.txt
$ mkdir raw processed  # for output
```

## Usage

To download `realDonaldTrump`'s last 3200 tweets as json, and add a
`reply_count` field to each tweet, do

```bash
$ python3 tweetratio.py realDonaldTrump
```

This code has to scrape as well as make API calls, so it will take 30-60
minutes, depending on the speed of your internet connection.

The tweets can then be found in `raw/realDonaldTrump.json`.

## Analysis

`analysis.py` contains simple code to load the tweets as a pandas DataFrame.
For example:

```python
>>> import analysis
>>> tweets = analysis.load_df()
>>> tweets['replies_per_retweet'] = tweets['reply_count']/tweets['retweet_count']
>>> sample = 'W'                                         # sample weekly
>>> start = "2016"                                       # don't plot old tweets
>>> users=('realDonaldTrump', 'dril', 'HillaryClinton')  # only plot these users
>>> fig, ax = plt.subplots()
>>> df = df[df['user'].isin(users)].loc[start:]
>>> df = df[np.isfinite(df['replies_per_retweet'])]
>>> ax = (df
...       .groupby([pd.TimeGrouper(sample), 'user'])['replies_per_retweet']
...       .mean()
...       .unstack()
...       .plot())
>>> fig.savefig("fig.png", bbox_inches='tight')
```

A minified copy of the tweets, which contains only the keys necessary for [the
visualization](<URL>), is saved to `processed/realDonaldTrump.json`.
