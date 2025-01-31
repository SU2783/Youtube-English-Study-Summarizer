import os
from tqdm import tqdm
import google.generativeai as genai


def get_all_uploaded_files(only_ready: bool = True):
    for uploaded_file in genai.list_files():
        if only_ready and uploaded_file.state.name != "ACTIVE":
            print(f"File {uploaded_file.display_name} is not ready yet. {uploaded_file.state=}")
            continue

        yield uploaded_file


def upload_file(file_path: str, mime_type: str = None, progress_bar: tqdm = None):
    if progress_bar:
        progress_bar.set_description(f"Uploading {file_path} to Google Server...")
    else:
        print(f"Uploading {file_path} to Google Server...")

    uploaded_file = genai.upload_file(path=file_path, mime_type=mime_type)

    if progress_bar:
        progress_bar.set_description(f"Completed uploading {uploaded_file.display_name=} {uploaded_file.name=}")
    else:
        print(f"Completed uploading {uploaded_file.display_name=} {uploaded_file.name=}")


def upload_files_from_directory(dir_path: str, mime_type: str = None):
    progress_bar = tqdm(os.listdir(dir_path))
    for file in progress_bar:
        audio_path = os.path.join(dir_path, file)
        upload_file(audio_path, mime_type=mime_type, progress_bar=progress_bar)


def delete_uploaded_file(file_name: str, progress_bar: tqdm = None):
    genai.delete_file(file_name)

    if progress_bar:
        progress_bar.set_description(f"{file_name} deleted")
    else:
        print(f"{file_name} deleted")


def delete_all_uploaded_files():
    progress_bar = tqdm(get_all_uploaded_files())
    for uploaded_file in progress_bar:
        delete_uploaded_file(uploaded_file.name, progress_bar=progress_bar)

