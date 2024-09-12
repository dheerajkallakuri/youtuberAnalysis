import requests,json
from googleapiclient.discovery import build

# Replace with your API key
API_KEY = 'YOUR_API_KEY'

def get_channel_id(handle):
    youtube = build("youtube", "v3", developerKey=API_KEY)
    
    # Search for the channel by its handle
    request = youtube.search().list(
        part="snippet",
        q=f"@{handle}",
        type="channel",
        maxResults=1
    )
    response = request.execute()

    if response['items']:
        # Extract the channel ID from the response
        channel_id = response['items'][0]['snippet']['channelId']
        return channel_id
    else:
        return None


def fetch_channel_data(api_key, channel_id):
    # Fetch channel details
    channel_url = f'https://www.googleapis.com/youtube/v3/channels?part=snippet,contentDetails,statistics&id={channel_id}&key={api_key}'
    response = requests.get(channel_url)
    channel_data = response.json()

    with open('data.json', 'w', encoding='utf-8') as f:
        json.dump(channel_data, f, ensure_ascii=False, indent=4)
    
    if 'items' not in channel_data or len(channel_data['items']) == 0:
        print('Error fetching channel data')
        return None
    
    channel_info = channel_data['items'][0]
    return {
        'channel_logo': channel_info['snippet']['thumbnails']['medium']['url'],
        'channel_name': channel_info['snippet']['title'],
        'channel_id': channel_info['snippet']['customUrl'],
        'youtube_id': channel_info['id'],
        'subscriber_count': channel_info['statistics']['subscriberCount'],
        'total_views': channel_info['statistics']['viewCount'],
        'total_videos': channel_info['statistics']['videoCount'],
        'location': channel_info['snippet'].get('country', 'N/A')  # 'country' is a part of snippet
    }

def fetch_top_rated_videos(api_key, channel_id):
    # Fetch the playlist ID for the uploaded videos of the channel
    playlist_url = f'https://www.googleapis.com/youtube/v3/channels?part=contentDetails&id={channel_id}&key={api_key}'
    response = requests.get(playlist_url)
    channel_data = response.json()

    if 'items' not in channel_data or len(channel_data['items']) == 0:
        print('Error fetching channel playlist data')
        return []

    playlist_id = channel_data['items'][0]['contentDetails']['relatedPlaylists']['uploads']

    # Fetch videos from the playlist
    video_list_url = f'https://www.googleapis.com/youtube/v3/playlistItems?part=snippet&playlistId={playlist_id}&maxResults=50&key={api_key}'
    response = requests.get(video_list_url)
    video_data = response.json()

    if 'items' not in video_data:
        print('Error fetching playlist videos data')
        return []

    # Fetch details for each video
    videos = []
    for item in video_data['items']:
        video_id = item['snippet']['resourceId']['videoId']
        video_title = item['snippet']['title']
        video_views = fetch_video_views(api_key, video_id)
        videos.append({
            'title': video_title,
            'video_id': video_id,
            'views': video_views
        })

    # Sort videos by view count (descending) and get top 5
    videos.sort(key=lambda x: x['views'], reverse=True)
    return videos[:5]

def fetch_video_views(api_key, video_id):
    # Fetch video details
    video_url = f'https://www.googleapis.com/youtube/v3/videos?part=statistics&id={video_id}&key={api_key}'
    response = requests.get(video_url)
    video_data = response.json()
    
    if 'items' not in video_data or len(video_data['items']) == 0:
        print(f'Error fetching video data for ID: {video_id}')
        return 0
    
    return int(video_data['items'][0]['statistics']['viewCount'])

def get_youtube_data(channel_id):
    CHANNEL_ID = channel_id
    channel_data = fetch_channel_data(API_KEY, CHANNEL_ID)
    if not channel_data:
        return

    top_videos = fetch_top_rated_videos(API_KEY, CHANNEL_ID)
    topr_videos = []
    for video in top_videos:
        video_url = f"https://www.youtube.com/watch?v={video['video_id']}"
        videoData = {
            'title': video['title'], 
            'link': video_url, 
            'views': video['views']
        }
        topr_videos.append(videoData)
    
    return {
            'logo_url': channel_data['channel_logo'],
            'name': channel_data['channel_name'],
            'id': channel_data['channel_id'],
            'subscribers': channel_data['subscriber_count'],
            'videos': channel_data['total_videos'],
            'views': channel_data['total_views'],
            'location': channel_data['location'],
            'top_videos': topr_videos
        }