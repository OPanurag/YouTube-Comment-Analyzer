import os
import youtube_dl
from googleapiclient.discovery import build
import csv

# Create a CSV file to store all data extracted
file = open(r'./comments/comment.csv', 'w')
text = csv.writer(file, delimiter=' ', escapechar=' ', skipinitialspace=True, lineterminator='\n')

# Set up YouTube API credentials (requires enabling YouTube Data API v3)
api_key = "AIzaSyBzup8AXTkgpL4slf-m9zvrtnmdmDzG9FM"

# Specify the YouTube video URL and video id
video_url = "https://youtu.be/G3g7HwG5BeQ"
video_id = "G3g7HwG5BeQ"

# Create a directory to store the downloaded comments
output_dir = "comments"
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Download the YouTube video and extract its comments
ydl_opts = {
            'writeinfojson': True,
            'format': 'best',
            'outtmpl': os.path.join(output_dir, '%(id)s.%(ext)s'),
            'skip_download': True,
            'writecomments': True,
            'youtube_include_comments': True,
            'ignoreerrors': True,
            'no_warnings': True
            }

with youtube_dl.YoutubeDL(ydl_opts) as ydl:
    ydl.download([video_url])

# Initialize the YouTube Data API client
youtube = build('youtube', 'v3', developerKey=api_key)

# Call the API to get comments (requires enabling YouTube Data API v3)
comments_response = youtube.commentThreads().list(
                                                    part='snippet',
                                                    videoId=video_id,
                                                    textFormat='plainText'
                                                ).execute()


# Extract the comments from the downloaded info.json file
info_file = os.path.join(output_dir, f"{video_id}.info.json")
if os.path.exists(info_file):
    with open(info_file, 'w+', encoding='utf-8') as file:
        info_data = file.read()
        comments_start_index = info_data.find('"comments": [')
        if comments_start_index != -1:
            comments_end_index = info_data.find(']', comments_start_index)
            comments_data = info_data[comments_start_index + 12:comments_end_index].strip()
            comments_list = eval(comments_data)

            # Process the comments
            for comment in comments_list:
                print(comment['textOriginal'])


# Process and print the comments from the API response to csv
text.writerows(
    comment['snippet']['topLevelComment']['snippet']['textOriginal'] for comment in comments_response['items'])
file.close()
