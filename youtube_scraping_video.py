# can also download playlist if the url refers to a playlist

import youtube_dl
yout_url = 'https://www.youtube.com/watch?v=T-g39o0rDos'
with youtube_dl.YoutubeDL({}) as ydl:
    ydl.download([yout_url])
