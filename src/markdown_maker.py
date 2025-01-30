from datetime import datetime
from src.playlist_extractor import load_metadata


def make_markdown_content(video_id: str, content: str, save: bool = False):
    metadata = load_metadata(video_id)
    video_url = metadata['video_url']
    video_title = metadata['title']
    channel = metadata['channel']
    channel_url = metadata['channel_url']
    embed_video_url = video_url.replace('watch?v=', 'embed/')

    content = make_timestamp_embed_link(content, video_title, embed_video_url)
    content = content.replace("```markdown", "").replace("```", "")

    markdown = f"""# {video_title} 
    
---

<iframe title="{video_title}" src="{embed_video_url}?amp;feature=oembed" allowfullscreen="" allow="fullscreen" style="aspect-ratio: 1.76991 / 1; width: 100%; height: 100%;"></iframe>

`Source: {video_title}` [Link]({video_url})
`Channel: {channel}` [Link]({channel_url})

---

{content}

"""

    if save:
        save_markdown(video_id, markdown)


def save_markdown(video_id: str, markdown: str):
    with open(f"markdown/{video_id}.md", "w", encoding='utf-8') as f:
        f.write(markdown)


def make_timestamp_embed_link(markdown: str, video_title: str, embed_video_url: str):
    lines = markdown.split('<summary>')

    for line in lines:
        if '</summary>' not in line:
            continue

        timestamp = line.split('</summary>')[0]
        timestamp_to_sec = change_timestamp_to_second(timestamp)
        timestamp_link = f"""<iframe title="{video_title};" src="{embed_video_url}?start={timestamp_to_sec}&amp;feature=oembed" allowfullscreen="" allow="fullscreen" style="aspect-ratio: 1.76991 / 1; width: 100%; height: 100%;"></iframe>"""
        markdown = markdown.replace(f'<summary>{timestamp}</summary>', f'<details><summary>영상: {timestamp}</summary>{timestamp_link}</details>')

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
