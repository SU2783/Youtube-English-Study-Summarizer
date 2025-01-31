import os
import json
import yt_dlp
import requests

from typing import Dict


def extract_playlists(
    playlist_url: str,
    audio_dir: str = "assets/audios",
):
    # 컨텐츠를 저장할 폴더 생성
    os.makedirs(audio_dir, exist_ok=True)

    # yt-dlp 옵션 설정
    ydl_opts = {
        'quiet': False,                   # 불필요한 출력 메시지 숨김 여부
        'extract_flat': False,            # 비디오 정보를 포함하여 추출
        'format': 'bestaudio/best',       # 오디오 다운로드 포맷
        'postprocessors': [{              # 다운로드 후 실행할 후처리기
            'key': 'FFmpegExtractAudio',  # 오디오 추출
            'preferredcodec': 'mp3',      # mp3로 변환
            'preferredquality': '192',    # 오디오 품질
        }],
        'outtmpl': f'{audio_dir}/%(id)s.%(ext)s',  # 출력 파일 이름 형식,
    }

    # yt-dlp를 사용하여 재생목록의 모든 영상 URL, 제목, 자막 등을 추출
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        result = ydl.extract_info(playlist_url, download=True)

    # 재생 목록 생성
    if 'entries' in result:
        video_list = result['entries']
    else:
        # 영상을 찾을 수 없는 경우 종료
        if 'id' not in result:
            print("영상을 찾을 수 없습니다.")
            return

        video_list = [result]

    # 재생목록의 모든 영상 정보를 추출
    for entry in video_list:
        del entry['formats']
        del entry['thumbnails']
        del entry['heatmap']
        del entry['automatic_captions']

        # 영상 정보
        video_id = entry['id']                # 영상 ID
        video_url = entry['original_url']     # 영상 URL
        title = entry['title']                # 영상 제목
        description = entry['description']    # 영상 설명
        chapters = entry['chapters']          # 영상 챕터
        subtitles = entry['subtitles']        # 자막
        channel = entry['channel']           # 채널명
        channel_url = entry['channel_url']    # 채널 URL
        audio_file_path = f"{audio_dir}/{video_id}.mp3"

        # 영상 정보를 JSON 파일로 저장
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

        print(f"영상 ID: {video_id}")
        print(f"영상 URL: {video_url}")
        print(f"영상 제목: {title}")
        print(f"영상 설명: \n{description}")
        print(f"챕터: {chapters}")
        print(f"채널명: {channel} - {channel_url}")
        print(f"자막: {subtitles}")
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
    save_dir = os.path.join("assets", "metadata")
    save_path = os.path.join(save_dir, f"{video_id}.json")
    os.makedirs(save_dir, exist_ok=True)

    # 영상 정보를 JSON 파일로 저장
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
    metadata_path = os.path.join(metadata_dir, f"{video_id}.json")

    if not os.path.exists(metadata_path):
        print(f'{video_id} 영상의 메타데이터가 존재하지 않습니다.')
        return None

    with open(metadata_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def save_automatic_subtitles(
    automatic_subtitle: Dict[str, Dict[str, str]],
    video_id: str,
    subtitle_dir: str = "subtitles",
):
    if automatic_subtitle is None:
        print("자막이 없습니다.")
        return

    for lang, content in automatic_subtitle.items():
        # 자동 생성 자막 정보
        url = content['url']
        language = content['name']
        ext = content['ext']
        print(f"자동 생성된 {language} 자막 url: {url}")

        # 자동 생성 자막 요청
        response = requests.get(url)
        if response.status_code != 200:
            continue

        # 자막을 지정된 폴더에 저장
        subtitle_filepath = os.path.join(subtitle_dir, f"{video_id}_{lang}.{ext}")
        with open(f"{subtitle_filepath}", 'wb') as f:
            f.write(response.content)


if __name__ == "__main__":
    playlist_url = "https://www.youtube.com/playlist?list=PLEzsBdrpZXC-T94osPAZva_BWFq4S8nL6"
    extract_playlists(playlist_url)