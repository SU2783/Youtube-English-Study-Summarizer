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
    parser.add_argument('--model_name', type=str, default='gemini-2.5-flash', help='Generative model name')
    return parser.parse_args()


def main(
    youtube_url: str,
    model_name: str = 'gemini-2.5-flash',
):
    # Set up generative model config
    generation_config = genai.GenerationConfig(
        response_mime_type="text/plain",
    )
    request_options = RequestOptions(
        retry=Retry(maximum=5, timeout=60*10),
        timeout=60*10,
    )

    # Set up generative model and system instructions
    contents_generator = ContentsGenerator(model_name, system_instruction)
    contents_generator.set_generation_config(generation_config, request_options)

    # Extract all videos and video information from the playlist
    extract_playlists(youtube_url)

    # Upload extracted audio files to Google server
    upload_files_from_directory(dir_path='assets/audios', mime_type="audio/mp3")

    # Generate content for all uploaded videos
    contents_generator.generate_contents(prompt)

    # Delete all uploaded files
    delete_all_uploaded_files()

    # Delete all extracted video information and files
    shutil.rmtree('assets')

    print("Content generation for all videos has been completed.")


if __name__ == '__main__':
    args = parse_args()
    main(args.url, args.model_name)
