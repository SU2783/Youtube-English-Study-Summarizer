import os
import yt_dlp
import requests
from typing import Dict


def save_automatic_subtitles(
    automatic_subtitle: Dict[str, Dict[str, str]],
    video_id: str,
    subtitle_dir: str = "subtitles",
):
    if automatic_subtitle is None:
        print("자막이 없습니다.")
        return

    for lang, content in automatic_subtitle.items():
        url = content['url']
        language = content['name']
        ext = content['ext']
        print(f"자동 생성된 {language} 자막 url: {url}")

        # 자동 생성된 자막 요청
        response = requests.get(url)
        if response.status_code != 200:
            continue

        # 자막을 지정된 폴더에 저장
        subtitle_filepath = os.path.join(subtitle_dir, f"{video_id}_{lang}.{ext}")
        with open(f"{subtitle_filepath}", 'wb') as f:
            f.write(response.content)


def extract_playlists(
    playlist_url: str,
    subtitle_dir: str = "subtitles",
):
    # 자막을 저장할 폴더 생성
    if not os.path.exists(subtitle_dir):
        os.makedirs(subtitle_dir)

    # yt-dlp 옵션 설정
    ydl_opts = {
        'quiet': False,                  # 불필요한 출력 메시지 숨김 여부
        'extract_flat': False,           # 비디오 정보를 포함하여 추출
        'writesubtitles': True,          # 자막 다운로드 설정
        'writeautomaticsub': True,       # 자동 자막 다운로드 설정
        'subtitleslangs': ['en', 'ko'],  # 자막 언어 설정 (영어, 한국어)
        'outtmpl': '%(id)s.%(ext)s',     # 출력 파일 이름 형식
    }

    # yt-dlp를 사용하여 재생목록의 모든 영상 URL, 제목, 자막을 추출
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        result = ydl.extract_info(playlist_url, download=False)

    # 재생목록이 비어있는 경우 예외 처리
    if 'entries' not in result:
        print("재생목록이 비어있습니다.")
        return

    # 비디오 URL, 제목, 자막 출력
    for entry in result['entries']:
        del entry['formats']
        del entry['requested_formats']
        del entry['thumbnails']
        del entry['heatmap']
        del entry['automatic_captions']

        video_id = entry['id']              # 영상 ID
        video_url = entry['original_url']   # 영상 URL
        title = entry['title']              # 영상 제목
        description = entry['description']  # 영상 설명
        chapters = entry['chapters']        # 영상 챕터
        subtitles = entry['subtitles']      # 자막
        channels = entry['channel']         # 채널명
        channel_url = entry['channel_url']  # 채널 URL

        print(f"영상 ID: {video_id}")
        print(f"영상 URL: {video_url}")
        print(f"영상 제목: {title}")
        print(f"영상 설명: \n{description}")
        print(f"챕터: {chapters}")
        print(f"채널명: {channels} - {channel_url}")
        print(f"자막: {subtitles}")

        # 자막이 존재하면 파일 경로를 출력
        if subtitles:
            subtitle_filepath = os.path.join(subtitle_dir, f"{video_id}.vtt")
            print(f"자막 파일 저장 위치: {subtitle_filepath}")
        else:
            automatic_subtitle = entry['requested_subtitles']
            save_automatic_subtitles(automatic_subtitle, video_id, subtitle_dir)

        print('-' * 50)