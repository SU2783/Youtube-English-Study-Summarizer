import os
import json
import yt_dlp
import requests
from typing import Dict


def extract_playlists(
    playlist_url: str,
    video_dir: str = "assets/videos",
    audio_dir: str = "assets/audios",
    subtitle_dir: str = "assets/subtitles",
):
    # 컨텐츠를 저장할 폴더 생성
    os.makedirs(video_dir, exist_ok=True)
    os.makedirs(audio_dir, exist_ok=True)
    os.makedirs(subtitle_dir, exist_ok=True)

    # yt-dlp 옵션 설정
    ydl_opts = {
        'quiet': False,                  # 불필요한 출력 메시지 숨김 여부
        'extract_flat': False,           # 비디오 정보를 포함하여 추출
        'writesubtitles': True,          # 자막 다운로드 설정
        'writeautomaticsub': True,       # 자동 자막 다운로드 설정
        'subtitleslangs': ['en', 'ko'],  # 자막 언어 설정 (영어, 한국어)
        'outtmpl': f'{video_dir}/%(id)s.%(ext)s',  # 출력 파일 이름 형식,
    }

    # yt-dlp를 사용하여 재생목록의 모든 영상 URL, 제목, 자막을 추출
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        result = ydl.extract_info(playlist_url, download=False)

    # 재생목록이 비어있는 경우 예외 처리
    if 'entries' not in result:
        print("재생목록이 비어있습니다.")
        return

    for entry in result['entries']:
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
        channels = entry['channel']           # 채널명
        channel_url = entry['channel_url']    # 채널 URL
        formats = entry['requested_formats']  # 다운로드 가능한 포맷

        video_info = None
        audio_info = None

        # 다운로드 가능한 포맷
        for downloadable_format in formats:
            print(downloadable_format)
            download_url = downloadable_format['url']

            # 비디오 다운로드
            if downloadable_format['video_ext'] != 'none':
                video_info = downloadable_format
                video_ext = downloadable_format['video_ext']

                video_path = f"{video_dir}/{video_id}.{video_ext}"
                video_info['video_path'] = video_path
                save_contents(contents_url=download_url, save_path=video_path)

            # 오디오 다운로드
            if downloadable_format['audio_ext'] != 'none':
                audio_info = downloadable_format
                audio_ext = downloadable_format['audio_ext']

                audio_path = f"{audio_dir}/{video_id}.{audio_ext}"
                audio_info['audio_path'] = audio_path
                save_contents(contents_url=download_url, save_path=audio_path)

        # 자막이 존재하면 파일 경로를 출력
        if subtitles:
            subtitle_filepath = os.path.join(subtitle_dir, f"{video_id}.vtt")
            print(f"자막 파일 저장 위치: {subtitle_filepath}")
        else:
            automatic_subtitle = entry['requested_subtitles']
            save_automatic_subtitles(automatic_subtitle, video_id, subtitle_dir)

        # 영상 정보를 JSON 파일로 저장
        save_metadata(
            video_id=video_id,
            title=title,
            description=description,
            chapters=chapters,
            channels=channels,
            channel_url=channel_url,
            video_info=video_info,
            audio_info=audio_info,
        )

        print(f"영상 ID: {video_id}")
        print(f"영상 URL: {video_url}")
        print(f"영상 제목: {title}")
        print(f"영상 설명: \n{description}")
        print(f"챕터: {chapters}")
        print(f"채널명: {channels} - {channel_url}")
        print(f"자막: {subtitles}")
        print('-' * 50)


def save_contents(contents_url: str, save_path: str):
    print(f"다운로드 URL: {contents_url}")

    response = requests.get(contents_url, stream=True)
    with open(save_path, 'wb') as f:
        f.write(response.content)

    print(f"파일 저장 위치: {save_path}")


def save_metadata(
    video_id: str,
    title: str,
    description: str,
    chapters: list,
    channels: str,
    channel_url: str,
    video_info: str = None,
    audio_info: str = None,
):
    save_dir = os.path.join("assets", "metadata")
    save_path = os.path.join(save_dir, f"{video_id}.json")
    os.makedirs(save_dir, exist_ok=True)

    # 영상 정보를 JSON 파일로 저장
    metadata = {
        "title": title,
        "description": description,
        "chapters": chapters,
        "channels": channels,
        "channel_url": channel_url,
        "video_info": video_info,
        "audio_info": audio_info,
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
