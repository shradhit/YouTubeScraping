import os
import glob
import shutil

import string
import random

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

    file_image = randomString(8)

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
    print(meta['title'])
    files = os.listdir(source)
    #file_name_ = str(meta['title']).replace("|", "_")
    #file_name = str(file_name_).replace(":", "-")


    for f in files:
        if f.endswith('vtt'):
            file_envtt = './down/' + file_image + '.en.vtt'
            os.rename(f, file_envtt)

        elif f.endswith('json'):
            file_json = './down/' + file_image + '.json'
            os.rename(f, file_json)

        elif f.endswith('wav'):
            file_wav = './down/' + file_image + '.wav'
            os.rename(f, file_wav)

        else:
            continue



    #for f in files:
    #    if f.endswith('vtt') or f.endswith('json') or f.endswith('wav'):
    #        shutil.copy(f, dest)
    #        os.remove(f)
    #    else:
            # print(str(df['title']))
    #        continue
    #files_dest = os.listdir(dest)



    sub_titles = glob.glob('./down/' + file_image + '*.en.vtt')
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

        heatmap_polarity = sentiment_df['overall_polarity'].astype('float').values
        heatmap_polarity = heatmap_polarity.reshape(heatmap_polarity.shape[0], 1)

        sns_plot = sns.heatmap(data=heatmap_polarity[:20].T, robust=True, cmap='RdYlGn', yticklabels=False, xticklabels=5, cbar=True, cbar_kws={"orientation": "horizontal"})

        fig = sns_plot.get_figure()


        img_save1 = file_image +".png"

        fig.savefig("static/" + img_save1)

        print('DONE 7')

        #########

        comment_words = ' '
        stopwords = set(STOPWORDS)

        # iterate through the corpus
        for val in sentiment_df.Statement:

            # typecaste each val to string
            val = str(val)

            # split the value
            tokens = val.split()

            # Converts each token into lowercase
            for i in range(len(tokens)):
                tokens[i] = tokens[i].lower()

            for words in tokens:
                comment_words = comment_words + words + ' '

        wordcloud = WordCloud(width=800, height=800,
                              background_color='white',
                              stopwords=stopwords,
                              min_font_size=10).generate(comment_words)


        # Plot the WordCloud image
        plt.figure(figsize=(8, 8), facecolor=None)
        plt.imshow(wordcloud)
        plt.axis('off')
        plt.tight_layout(pad=0)
        img_save2 = file_image +"two.png"
        plt.savefig("static/" + img_save2)

        return render_template("new.html", graph_one=img_save1, graph_two=img_save2)

    return render_template("my-form.html")


def randomString(stringLength=8):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(stringLength))

