# can scrape audio
# url for playlist will scrape all the videos from the playlist..
    
    
from __future__ import unicode_literals
import youtube_dl


url = input() 
input_ = url + '&page=1'


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
    meta = ydl.extract_info(input_, download=True) 
    
    
print('upload date : %s' %(meta['upload_date']))
print('uploader    : %s' %(meta['uploader']))
print('views       : %d' %(meta['view_count']))
print('likes       : %d' %(meta['like_count']))
print('dislikes    : %d' %(meta['dislike_count']))
print('id          : %s' %(meta['id']))
print('format      : %s' %(meta['format']))
print('duration    : %s' %(meta['duration']))
print('title       : %s' %(meta['title']))
print('description : %s' %(meta['description']))


keys_to_include = set(('upload_date'))
dict2 = {k:v for k,v in meta.items() if k in keys_to_include}
df = pd.DataFrame(dict2, index = [0])
# saving file to CSV
df.to_csv('per_video.csv')
