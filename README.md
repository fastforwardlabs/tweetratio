# Twitter reply-to-retweet ratio scraping code

## Installation

Requirements: Python 3.6+

```bash
$ git clone git@github.com:fastforwardlabs/tweetratio.git
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

A minified copy of the tweets, which contains only the keys necessary for [the
visualization](http://www.fastforwardlabs.com/tweetratio/), is saved to
`processed/realDonaldTrump.json`.

## Analysis

`analysis.py` contains simple code to load the tweets as a pandas DataFrame.
For example:

```python
>>> import analysis
>>> tweets = analysis.load_df()
>>> analysis.plot_trend(tweets)
```
