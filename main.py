from src.playlist_extractor import extract_playlists
from src.file_manager import upload_files_from_directory
from dotenv import load_dotenv

load_dotenv()

if __name__ == '__main__':
    # 재생목록 URL
    playlist_url = "https://www.youtube.com/playlist?list=PLEzsBdrpZXC-T94osPAZva_BWFq4S8nL6"

    # 재생목록의 모든 영상 및 영상 정보를 추출
    extract_playlists(playlist_url)

    # 추출한 영상을 업로드
    upload_files_from_directory(dir_path='assets/audios')

    print("Done!")