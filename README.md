# Youtube English Study Summarizer

## Introduction
This project is a summarizer for English study videos on YouTube. It is designed to help English learners study more efficiently.
The summarizer extracts the main contents of the video, provides a summary, and includes video timestamps and links for each summarized part.
Summarized contents are saved in a markdown file.

This summarizer works well with [`Obsidian`](https://obsidian.md/).
You can import generated markdown files into your Obsidian vault for a seamless note-taking and study experience.

<figure>
<p align="center">
 <img src = "./images/image.gif">
</p>
</figure>

---

## Usage

### 1. Clone the repository

```bash
git clone https://github.com/SU2783/Youtube-English-Study-Summarizer.git
```

### 2. Install the required libraries

```bash
pip install -r requirements.txt
```

or

```bash
uv sync
```


### 3. Get the GEMINI API key from the [Google AI Studio](https://aistudio.google.com/app/apikey)


### 4. Set the API key to `.env` file from root directory

```.env
GEMINI_API_KEY=<your_api_key>
```

or export it as an environment variable

- Linux Bash
```bash
export GEMINI_API_KEY=<your_api_key>
```

- Windows PowerShell
```powershell
$env:GEMINI_API_KEY=<your_api_key>
```

### 5. Run the summarizer from the root directory
```bash
python summarizer.py --url <youtube_url>
```

---


## Example

```bash
python summarizer.py --url https://www.youtube.com/watch?v=cfvZ48RnRXw
```

you can also use the playlist URL
```bash
python summarizer.py --url https://www.youtube.com/playlist?list=PLEzsBdrpZXC-T94osPAZva_BWFq4S8nL6
```

---


## Note

- The summarizer is not perfect. It may not provide the correct summary.
- It takes long time to extract and upload the main contents of the video and activate uploaded contents on the Google Upload Server. Please be patient.
- The summarizer is implemented using the [`Google Gemini`](https://gemini.google.com/app). It may not work properly if the model is not available.
- The default language of the summarized text is Korean. If you want to use another language, you can change the prompt in the `src/prompt.py` file. 
