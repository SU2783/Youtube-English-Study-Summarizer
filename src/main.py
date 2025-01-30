from playlist_extractor import extract_playlists
from dotenv import load_dotenv

load_dotenv()

if __name__ == '__main__':
    # 재생목록 URL
    playlist_url = "https://www.youtube.com/playlist?list=PLEzsBdrpZXC-T94osPAZva_BWFq4S8nL6"

    # 재생목록의 모든 영상 URL, 제목, 자막을 추출
    extract_playlists(playlist_url)