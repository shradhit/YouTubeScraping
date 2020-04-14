import os
import glob

import youtube_dl

from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from wordcloud import WordCloud, STOPWORDS

import webvtt
import numpy as np
import pandas as pd

import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
import seaborn as sns

from flask import Flask, request, render_template, jsonify
#os.chdir("/Users/shradhitsubudhi/Documents/youtube/downloads")


app = Flask(__name__, static_url_path="")

@app.route('/')
def index():
    """Return the main page."""
    return render_template('theme.html')



app = Flask(__name__)

@app.route('/')
def index():
    return '<h1> Youtube Sentimental Analysis!</h1>'\

@app.route("/form_data", methods=["GET", "POST"])
def form_data():

    global link
    if request.method =="POST":
        link = request.form.get('link')

        ydl_opts = {'writesubtitles': True,
                    'writeautomaticsub': True,
                    'writeinfojson': True,
                    'format': 'bestaudio/best',
                    'keepvideo': False,
                    'postprocessors': [{'key': 'FFmpegExtractAudio',
                                        'preferredcodec': 'wav',
                                        'preferredquality': '192'}],
                    'postprocessor_args': ['-ar', '16000']}


        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            meta = ydl.extract_info(link, download=True)

        sub_titles = glob.glob('./*.en.vtt')
        print(sub_titles[0])
        vtt = webvtt.read(sub_titles[0])

        start_list = list()
        end_list = list()

        # Storing all the lines as part of the lines list
        lines = []

        for x in range(len(vtt)):
            start_list.append(vtt[x].start)
            end_list.append(vtt[x].end)

        for line in vtt:
            lines.append(line.text.strip().splitlines())

        lines = [' '.join(item) for item in lines]

        final_df = pd.DataFrame({'Start_time': start_list, 'End_time': end_list, 'Statement': lines})
        #final_df.head()

        sid_obj = SentimentIntensityAnalyzer()

        # Compute sentiment scores and labels
        sentiment_scores_vader = [sid_obj.polarity_scores(article) for article in final_df.Statement]

        sentiment_category_positive = []
        sentiment_category_neutral = []
        sentiment_category_negative = []
        sentiment_category_compound = []

        for sentiments in sentiment_scores_vader:
            sentiment_category_positive.append(sentiments['pos'])
            sentiment_category_neutral.append(sentiments['neu'])
            sentiment_category_negative.append(sentiments['neg'])
            sentiment_category_compound.append(sentiments['compound'])

        # Sentiment statistics per statement
        sentiment_df = pd.DataFrame([[article for article in final_df.Statement],
                                     sentiment_category_positive,
                                     sentiment_category_neutral,
                                     sentiment_category_negative,
                                     sentiment_category_compound]).T

        sentiment_df['Start_time'] = start_list
        sentiment_df['End_time'] = end_list

        sentiment_df.columns = ['Statement', 'positive_polarity', 'neutral_polarity', 'negative_polarity',
                                'overall_polarity', 'Start_time', 'End_time']
        abcd = sentiment_df.to_json()
        return abcd
    return '''<form method ="POST">
                Enter the Youtube link <input type ="text" name ="link">
                <input type ="submit">
                </form>'''

