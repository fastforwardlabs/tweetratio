# Twitter reply-to-retweet ratio scraping code

This is the scraping and front-end code used to acquire and visualize the data
discussed in [A Quick Look at the Reply-to-Retweet
Ratio](http://blog.fastforwardlabs.com/2017/05/15/reply-retweet-ratio.html).

## Installation

Requirements: Python 3.6+ (f-strings!)

```bash
$ git clone git@github.com:fastforwardlabs/tweetratio.git
$ cd tweetratio
$ python3 -m virtualenv venv
$ source venv/bin/activate
$ pip install -r requirements.txt
$ mkdir -p raw minified csv  # for output
```

## Usage

To download `realDonaldTrump`'s last 3200 tweets as json, and add a
`reply_count` field to each tweet, do

```python
>>> import tweetratio
>>> tweetratio.get_user('realDonaldTrump')
```

This code has to scrape as well as make API calls, so it will take 30-60
minutes, depending on the speed of your internet connection.

The tweets can then be found in `raw/realDonaldTrump.json`.

If you want a minified copy of the tweets, which contains only the keys
necessary for [the visualization](http://www.fastforwardlabs.com/tweetratio/),
and the same data as a CSV file, do

```python
>>> import analysis
>>> analysis.process('realDonaldTrump')
```

The minifed JSON is saved to `minified/realDonaldTrump.json`. The CSV is saved
to `csv/realDonaldTrump.csv`.

## Frontend

To run [the
visualization](http://blog.fastforwardlabs.com/2017/05/15/reply-retweet-ratio.html)
locally, download and minify the data for `realDonaldTrump`, `BernieSanders`,
`BarackObama`, `HillaryClinton`, `GovMikeHuckabee`, `dril` and `SpeakerRyan`
(see above). If you'd like to plot other accounts, download those and change
[`web/app.js`](https://github.com/fastforwardlabs/tweetratio/blob/master/web/app.js#L9-L18).

Then
```bash
$ mv processed/* web/data/
$ cd web
$ python3 -m http.server
```
and visit `localhost:8000`

## Analysis

`analysis.py` contains simple code to load the tweets as a pandas DataFrame.
For example:

```python
>>> import analysis
>>> tweets = analysis.load_df()
>>> analysis.plot_trend(tweets)
```
![](fig.png)

## U.S. Senators

[`senators.py`](senators.py) demonstrates how to download the tweets for a list
of accounts (in this case the U.S. senators as of June 2017).
