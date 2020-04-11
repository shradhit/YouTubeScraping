#creates two csv files 'per_video_related' and 'per_video'

from bs4 import BeautifulSoup #for scraping
import requests               #required for reading the file
import pandas as pd           #(optional) Pandas for dataframes 
import json                   #(optional) If you want to export json
import os

Vid={}
Link = 'https://www.youtube.com/watch?v=ATDYLTnGJV0'
source= requests.get(url).text
soup=BeautifulSoup(source,'lxml')
div_s = soup.findAll('div')


# Title 
Title = div_s[1].find('span',class_='watch-title').text.strip()
Vid['Title']=Title

# Date Published 
Vid['date_pub'] = div_s[1].find(class_ = 'watch-time-text').text.replace('Published on ', '')


# Link  Information
Link = url
source= requests.get(url).text
Vid['Link']=Link


# Informations about the channel
Channel_name = div_s[1].find('a',class_="yt-uix-sessionlink spf-link").text.strip()

Channel_link = ('www.youtube.com'+div_s[1].find('a',class_="yt-uix-sessionlink spf-link").get('href'))

Subscribers = div_s[1].find('span',class_="yt-subscription-button-subscriber-count-branded-horizontal yt-subscriber-count").text.strip()
if(len(Channel_name) ==0):
    Channel_name ='None'
    Channel_link = 'None'
    Subscribers = 'None'

Vid['Channel'] = Channel_name
Vid['Channel_link'] = Channel_link
Vid['Channel_subscribers'] = Subscribers


# Video Counts 
View_count = div_s[1].find(class_= 'watch-view-count')
View_count = View_count.text.strip().split()[0]
Vid['Views'] = View_count



# Likes 
Likes = div_s[1].find('button',class_="yt-uix-button yt-uix-button-size-default yt-uix-button-opacity yt-uix-button-has-icon no-icon-markup like-button-renderer-like-button like-button-renderer-like-button-unclicked yt-uix-clickcard-target yt-uix-tooltip" ).text.strip()
Vid['Likes']=Likes
Dislikes = div_s[1].find('button',class_="yt-uix-button yt-uix-button-size-default yt-uix-button-opacity yt-uix-button-has-icon no-icon-markup like-button-renderer-dislike-button like-button-renderer-dislike-button-unclicked yt-uix-clickcard-target yt-uix-tooltip" ).text.strip()
Vid['Dislikes']=Dislikes


## Related Video
Related_videos = div_s[1].findAll('a',class_='content-link spf-link yt-uix-sessionlink spf-link')
Title_Related=[]
Link_Related =[]
for i in range(len(Related_videos)):
    Title_Related.append(Related_videos[i].get('title'))
    Link_Related.append(Related_videos[i].get('href'))
Related_dictionary = dict(zip(Title_Related, Link_Related))    
Vid['Related_vids']=Related_dictionary



# Decription 
decription = div_s[1].find_all('script')#.text.strip()
string_dec = str(decription[1]).split(',')
for x in string_dec:
    if 'shortDescription' in x:
        Vid['Views'] = x



#soup = BeautifulSoup(requests.get("your_url").text, 'lxml')

#soup=BeautifulSoup(source,'html.parser')
#div_s = soup.findAll('div')



# Title 
Title = div_s[1].find('span',class_='watch-title').text.strip()
Vid['Title']=Title

# Date Published 
Vid['date_pub'] = div_s[1].find(class_ = 'watch-time-text').text.replace('Published on ', '')


# Link  Information
Link = url
source= requests.get(url).text
Vid['Link']=Link


# Informations about the channel
Channel_name = div_s[1].find('a',class_="yt-uix-sessionlink spf-link").text.strip()

Channel_link = ('www.youtube.com'+div_s[1].find('a',class_="yt-uix-sessionlink spf-link").get('href'))

Subscribers = div_s[1].find('span',class_="yt-subscription-button-subscriber-count-branded-horizontal yt-subscriber-count").text.strip()
if(len(Channel_name) ==0):
    Channel_name ='None'
    Channel_link = 'None'
    Subscribers = 'None'

Vid['Channel'] = Channel_name
Vid['Channel_link'] = Channel_link
Vid['Channel_subscribers'] = Subscribers


# Video Counts 
View_count = div_s[1].find(class_= 'watch-view-count')
View_count = View_count.text.strip().split()[0]
Vid['Views'] = View_count



# Likes 
Likes = div_s[1].find('button',class_="yt-uix-button yt-uix-button-size-default yt-uix-button-opacity yt-uix-button-has-icon no-icon-markup like-button-renderer-like-button like-button-renderer-like-button-unclicked yt-uix-clickcard-target yt-uix-tooltip" ).text.strip()
Vid['Likes']=Likes
Dislikes = div_s[1].find('button',class_="yt-uix-button yt-uix-button-size-default yt-uix-button-opacity yt-uix-button-has-icon no-icon-markup like-button-renderer-dislike-button like-button-renderer-dislike-button-unclicked yt-uix-clickcard-target yt-uix-tooltip" ).text.strip()
Vid['Dislikes']=Dislikes


## Related Video
Related_videos = div_s[1].findAll('a',class_='content-link spf-link yt-uix-sessionlink spf-link')
Title_Related=[]
Link_Related =[]
for i in range(len(Related_videos)):
    Title_Related.append(Related_videos[i].get('title'))
    Link_Related.append(Related_videos[i].get('href'))
Related_dictionary = dict(zip(Title_Related, Link_Related))    
Vid['Related_vids']=Related_dictionary



# Decription 
decription = div_s[1].find_all('script')#.text.strip()
string_dec = str(decription[1]).split(',')
for x in string_dec:
    if 'shortDescription' in x:
        Vid['Views'] = x


df_related = pd.DataFrame.from_dict(data = Vid['Related_vids'], orient='index', columns = ['link'])
df_related['Title'] = Vid['Title']
# saving file to CSV
df_related.to_csv('per_video_related.csv')
keys_to_exclude = set(('Related_vids'))
dict2 = {k:v for k,v in Vid.items() if k not in keys_to_exclude}
df = pd.DataFrame(dict2, index = [0])
# saving file to CSV
df.to_csv('per_video.csv')
