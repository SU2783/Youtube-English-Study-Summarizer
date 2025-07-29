import os
import json
import yt_dlp
import requests
import traceback

from typing import Dict


def extract_playlists(
    playlist_url: str,
    audio_dir: str = "assets/audios",
):
    """
    Save all videos in the playlist as audio files.

    Args:
        playlist_url (str): YouTube Playlist URL
        audio_dir (str): Directory to save audio files

    Returns:
        None
    """
    # Create a folder to save the content
    os.makedirs(audio_dir, exist_ok=True)

    # Set yt-dlp options
    ydl_opts = {
        'quiet': False,                   # Hide unnecessary output messages
        'extract_flat': False,            # Extract with video information
        'ignoreerrors': True,             # Ignore errors and continue
        'format': 'bestaudio/best',       # Audio download format
        'postprocessors': [{              # Postprocessor to run after download
            'key': 'FFmpegExtractAudio',  # Extract audio
            'preferredcodec': 'mp3',      # Convert to mp3
            'preferredquality': '192',    # Audio quality
        }],
        'outtmpl': f'{audio_dir}/%(id)s.%(ext)s',  # Output file name format
    }

    # Use yt-dlp to extract all video URLs, titles, subtitles, etc. from the playlist
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        result = ydl.extract_info(playlist_url, download=True)

    # Create a playlist
    if 'entries' in result:
        video_list = result['entries']
    else:
        # Exit if no videos are found
        if 'id' not in result:
            print("Video not found.")
            return

        video_list = [result]

    # Extract all video information from the playlist
    for entry in video_list:
        if entry is None:
            continue

        del entry['formats']
        del entry['thumbnails']
        del entry['heatmap']
        del entry['automatic_captions']

        # Video information
        video_id = entry['id']  # Video ID
        video_url = entry['original_url']  # Video URL
        title = entry['title']  # Video title
        description = entry['description']  # Video description
        chapters = entry['chapters']  # Video chapters
        subtitles = entry['subtitles']  # Subtitles
        channel = entry['channel']  # Channel name
        channel_url = entry['channel_url']  # Channel URL
        audio_file_path = f"{audio_dir}/{video_id}.mp3"

        # Save video information as a JSON file
        save_metadata(
            video_id=video_id,
            video_url=video_url,
            title=title,
            description=description,
            chapters=chapters,
            channel=channel,
            channel_url=channel_url,
            audio_file_path=audio_file_path,
        )

        print(f"Video ID: {video_id}")
        print(f"Video URL: {video_url}")
        print(f"Video Title: {title}")
        print(f"Video Description: \n{description}")
        print(f"Chapters: {chapters}")
        print(f"Channel: {channel} - {channel_url}")
        print('-' * 50)


def save_metadata(
    video_id: str,
    video_url: str,
    title: str,
    description: str,
    chapters: list,
    channel: str,
    channel_url: str,
    audio_file_path: str,
):
    """
    Save video metadata as a JSON file.

    Args:
        video_id (str): Video ID
        video_url (str): Video URL
        title (str): Video title
        description (str): Video description
        chapters (list): Video chapters
        channel (str): Channel name
        channel_url (str): Channel URL
        audio_file_path (str): Path to the audio file

    Returns:
        None
    """
    save_dir = os.path.join("assets", "metadata")
    save_path = os.path.join(save_dir, f"{video_id}.json")
    os.makedirs(save_dir, exist_ok=True)

    # Save video information as a JSON file
    metadata = {
        "title": title,
        "description": description,
        "chapters": chapters,
        "channel": channel,
        "channel_url": channel_url,
        "video_url": video_url,
        "audio_file_path": audio_file_path,
    }

    with open(save_path, 'w', encoding='utf-8') as f:
        json.dump(metadata, f, ensure_ascii=False, indent=4)


def load_metadata(video_id: str, metadata_dir: str = "assets/metadata"):
    """
    Load video metadata from a JSON file.

    Args:
        video_id (str): Video ID
        metadata_dir (str): Directory where metadata files are stored

    Returns:
        dict: Video metadata if exists, None otherwise
    """
    metadata_path = os.path.join(metadata_dir, f"{video_id}.json")

    if not os.path.exists(metadata_path):
        print(f'Metadata for video {video_id} does not exist.')
        return None

    with open(metadata_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def save_automatic_subtitles(
    automatic_subtitle: Dict[str, Dict[str, str]],
    video_id: str,
    subtitle_dir: str = "subtitles",
):
    """
    Save automatically generated subtitles.

    Args:
        automatic_subtitle (dict): Dictionary containing subtitle information
        video_id (str): Video ID
        subtitle_dir (str): Directory to save subtitles

    Returns:
        None
    """
    if automatic_subtitle is None:
        print("No subtitles available.")
        return

    for lang, content in automatic_subtitle.items():
        # Automatically generated subtitle information
        url = content['url']
        language = content['name']
        ext = content['ext']
        print(f"Automatically generated {language} subtitle url: {url}")

        # Request automatically generated subtitles
        response = requests.get(url)
        if response.status_code != 200:
            continue

        # Save subtitles to the specified folder
        subtitle_filepath = os.path.join(subtitle_dir, f"{video_id}_{lang}.{ext}")
        with open(f"{subtitle_filepath}", 'wb') as f:
            f.write(response.content)


if __name__ == "__main__":
    playlist_url = "https://www.youtube.com/playlist?list=PLEzsBdrpZXC-T94osPAZva_BWFq4S8nL6"
    extract_playlists(playlist_url)