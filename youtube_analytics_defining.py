# -*- coding: utf-8 -*-
"""Youtube_analytics_defining.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1z3fboqrdNBieU3USG1-pVju0tTvSuItI
"""

import requests
import pandas as pd
import time

API_KEY="AIzaSyBhndD3QJdaYWbC5bgy60IGCrAlbLfaRZA"
CHANNEL_ID="UCUjCgTvt2j_ldTd5VGXXLLQ"

def get_video_details(video_id):
  #collecting view, like, dislike and comment counts
    url_video_stats="https://www.googleapis.com/youtube/v3/videos?id="+video_id+"&part=statistics&key="+API_KEY
    response_video_stats=requests.get(url_video_stats).json()

    view_count=response_video_stats['items'][0]['statistics']['viewCount']
    like_count=response_video_stats['items'][0]['statistics']['likeCount']
    dislike_count=response_video_stats['items'][0]['statistics']['dislikeCount']
    comment_count=response_video_stats['items'][0]['statistics']['commentCount']

    return view_count, like_count, dislike_count, comment_count

def get_videos(df):
  #Make a API call
  pageToken=""
  url = "https://www.googleapis.com/youtube/v3/search?key="+API_KEY+"&channelId="+CHANNEL_ID+"&part=snippet,id&order=date&maxResults=10000"+pageToken
  response=requests.get(url).json()
  time.sleep(3)


  for video in response['items']:
    if video['id']['kind']=="youtube#video":
      video_id = video['id']['videoId']
      video_title=video['snippet']['title']
      video_title=str(video_title).replace('amp;','')
      video_title=str(video_title).split('|')[0]
      upload_date=video['snippet']['publishedAt']
      upload_date=str(upload_date).split('T')[0]

    view_count, like_count, dislike_count, comment_count = get_video_details(video_id)

    #save data in pandas df
    df=df.append(
        {'video_id':video_id, 'video_title':video_title,'upload_date':upload_date,
         'view_count':view_count, 'like_count':like_count, 'dislike_count':dislike_count, 
         'comment_count':comment_count}, ignore_index=True)
  return df

#build our dataframe
df = pd.DataFrame(columns=['video_id','video_title','upload_date','view_count','like_count','dislike_count','comment_count'])
df = get_videos(df)

df

