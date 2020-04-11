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
    ydl.download([input_])
    
