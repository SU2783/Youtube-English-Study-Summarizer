from datetime import datetime
from src.playlist_extractor import load_metadata


def make_markdown_content(video_id: str, content: str, save: bool = False):
    metadata = load_metadata(video_id)
    content = make_timestamp_link(content, metadata['video_url'])
    markdown = f"""# {metadata['title']} 

---

{content}

---

Source: {metadata['video_url']} - [{metadata['channels']}]({metadata['channel_url']})
"""

    if save:
        save_markdown(video_id, markdown)


def save_markdown(video_id: str, markdown: str):
    with open(f"markdown/{video_id}.md", "w", encoding='utf-8') as f:
        f.write(markdown)


def make_timestamp_link(markdown: str, video_url: str):
    cells = markdown.split('|')

    for cell in cells:
        if ":" in cell and cell.replace(':', '').strip().isdecimal():
            timestamp = cell.strip()
            timestamp_to_sec = change_timestamp_to_second(timestamp)
            timestamp_link = f"[{timestamp}]({video_url}&t={timestamp_to_sec})"
            markdown = markdown.replace(timestamp, timestamp_link)

    return markdown


def change_timestamp_to_second(timestamp: str):
    timestamp_length = len(timestamp.split(':'))

    if timestamp_length == 2:
        hms = datetime.strptime(timestamp, '%M:%S').time()
    elif timestamp_length == 3:
        hms = datetime.strptime(timestamp, '%H:%M:%S').time()
    else:
        raise ValueError(f"Invalid timestamp format: {timestamp}")

    return hms.hour * 3600 + hms.minute * 60 + hms.second
