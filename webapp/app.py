import os
import glob
import shutil

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

app = Flask(__name__)


@app.route('/')
def index():
    return '<h1> Youtube Sentimental Analysis!</h1>'


@app.route('/form_data')
def my_form():
    return render_template('my-form.html')


@ app.route("/form_data", methods=["GET", "POST"])
def form_data():

    if request.method == "POST":
        link = request.form['link']
    source = os.getcwd()
    dest = os.getcwd() + '/down/'

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
    print('DONE')

    keys = ['uploader', 'uploader_url', 'upload_date', 'creator', 'title', 'description', 'categories',
            'duration', 'view_count', 'like_count', 'dislike_count', 'average_rating', 'start_time', 'end_time',
            'release_date', 'release_year']

    filtered_d = dict((k, meta[k]) for k in keys if k in meta)
    df = pd.DataFrame.from_dict(filtered_d, orient='index').T
    df.index = df['title']
    files = os.listdir(source)
    file_name = str(meta['title']).replace("|", "_")
    print(file_name)

    for f in files:
        if f.startswith(file_name):
            shutil.move(f, dest)
            # print('done')
        else:
            # print(str(df['title']))
            continue

    sub_titles = glob.glob('./down/' + file_name + '*.en.vtt')
    print(sub_titles)
    if len(sub_titles) != 0:
        vtt = webvtt.read(sub_titles[0])

        start_list = list()
        end_list = list()
        # Storing all the lines as part of the lines list
        lines = []
        print('DONE 2')
        for x in range(len(vtt)):
            start_list.append(vtt[x].start)
            end_list.append(vtt[x].end)
        print('DONE 3')

        for line in vtt:
            lines.append(line.text.strip().splitlines())

        lines = [' '.join(item) for item in lines]
        print('DONE 4')

        final_df = pd.DataFrame({'Start_time': start_list, 'End_time': end_list, 'Statement': lines})

        sid_obj = SentimentIntensityAnalyzer()
        sentiment_scores_vader = [sid_obj.polarity_scores(article) for article in final_df.Statement]
        print('DONE 5')

        sentiment_category_positive = []
        sentiment_category_neutral = []
        sentiment_category_negative = []
        sentiment_category_compound = []

        for sentiments in sentiment_scores_vader:
            sentiment_category_positive.append(sentiments['pos'])
            sentiment_category_neutral.append(sentiments['neu'])
            sentiment_category_negative.append(sentiments['neg'])
            sentiment_category_compound.append(sentiments['compound'])

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
        print('DONE 6')
        return abcd

    return "DONE"

#return '''<form method ="POST"> Enter the Youtube link <input type ="text" name ="link"> <input type ="submit"> </form>'''




