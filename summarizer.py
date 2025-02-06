import os
import shutil
import argparse
from dotenv import load_dotenv

import google.generativeai as genai
from google.api_core.retry import Retry
from google.generativeai.types import RequestOptions

from src.contents_generator import ContentsGenerator
from src.prompt import prompt, system_instruction
from src.playlist_extractor import extract_playlists
from src.file_manager import upload_files_from_directory, delete_all_uploaded_files

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))


def parse_args():
    parser = argparse.ArgumentParser(description='Generate contents from YouTube playlist')
    parser.add_argument('--url', type=str, help='YouTube Video or Playlist URL')
    parser.add_argument('--model_name', type=str, default='gemini-2.0-pro-exp', help='Generative model name')
    return parser.parse_args()


def main(
    youtube_url: str,
    model_name: str = 'gemini-1.5-flash',
):
    # 생성 모델 Config 설정
    generation_config = genai.GenerationConfig(
        response_mime_type="text/plain",
    )
    request_options = RequestOptions(
        retry=Retry(maximum=5, timeout=60*10),
        timeout=60*10,
    )

    # 생성 모델 및 시스템 지시사항 설정
    contents_generator = ContentsGenerator(model_name, system_instruction)
    contents_generator.set_generation_config(generation_config, request_options)

    # 재생목록의 모든 영상 및 영상 정보를 추출
    extract_playlists(youtube_url)

    # 추출한 오디오 파일을 구글 서버에 업로드
    upload_files_from_directory(dir_path='assets/audios', mime_type="audio/mp3")

    # 업로드 한 모든 영상에 대한 컨텐츠 생성
    contents_generator.generate_contents(prompt)

    # 업로드 한 모든 파일 삭제
    delete_all_uploaded_files()

    # 추출한 모든 영상 정보 및 파일 삭제
    shutil.rmtree('assets')

    print("모든 영상에 대한 컨텐츠 생성이 완료되었습니다.")


if __name__ == '__main__':
    args = parse_args()
    main(args.url, args.model_name)