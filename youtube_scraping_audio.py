# can scrape audio
# url for playlist will scrape all the videos from the playlist..
    
from __future__ import unicode_literals
import youtube_dl

ydl_opts = {
    'format': 'bestaudio/best',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'wav',
        'preferredquality': '192'
    }],
    'postprocessor_args': [
        '-ar', '16000'
    ],
    'prefer_ffmpeg': True,
    'keepvideo': True
}

with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        meta = ydl.extract_info('https://www.youtube.com/watch?v=9bZkp7q19f0', download=True) 

        
#print('upload date : %s' %(meta['upload_date']))
#print('uploader    : %s' %(meta['uploader']))
#print('views       : %d' %(meta['view_count']))
#print('likes       : %d' %(meta['like_count']))
#print('dislikes    : %d' %(meta['dislike_count']))
#print('id          : %s' %(meta['id']))
#print('format      : %s' %(meta['format']))
#print('duration    : %s' %(meta['duration']))
#print('title       : %s' %(meta['title']))
#print('description : %s' %(meta['description']))


keys = ['upload_date', 'uploader', 'view_count', 'like_count', 
        'dislike_count', 'id', 'format', 'duration', 'title', 'description']

filtered_d = dict((k, meta[k]) for k in keys if k in meta)
df = pd.DataFrame.from_dict(filtered_d, orient='index').T
df.index = df['title'] 
