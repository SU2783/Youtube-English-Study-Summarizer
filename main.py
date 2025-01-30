import os
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


def main(
    playlists: str,
    model_name: str = 'gemini-1.5-flash',
    generation_config: genai.GenerationConfig = None,
    request_options: RequestOptions = None,
):
    # 생성 모델 및 시스템 지시사항 설정
    contents_generator = ContentsGenerator(model_name, system_instruction)
    contents_generator.set_generation_config(generation_config, request_options)

    # 재생목록의 모든 영상 및 영상 정보를 추출
    extract_playlists(playlists)

    # 추출한 영상을 업로드
    upload_files_from_directory(dir_path='assets/audios')

    # 업로드 한 모든 영상에 대한 컨텐츠 생성
    contents_generator.generate_contents(prompt)

    # 업로드 한 모든 영상 삭제
    delete_all_uploaded_files()

    print("모든 영상에 대한 컨텐츠 생성이 완료되었습니다.")


if __name__ == '__main__':
    # 재생목록 URL
    playlist_url = "https://www.youtube.com/playlist?list=PLEzsBdrpZXC-T94osPAZva_BWFq4S8nL6"

    # 생성 모델 이름
    model_name = 'gemini-1.5-flash'

    # 생성 모델 Config 설정
    generation_config = genai.GenerationConfig(
        response_mime_type="text/plain",
    )
    request_options = RequestOptions(
        retry=Retry(maximum=5, timeout=60*10),
        timeout=60*10,
    )

    main(playlist_url, model_name, generation_config, request_options)