import os
import google.generativeai as genai


def get_all_uploaded_files(only_ready: bool = True):
    for uploaded_file in genai.list_files():
        if only_ready and uploaded_file.state != 2:
            print(f"File {uploaded_file.display_name} is not ready yet. {uploaded_file.state=}")
            continue

        yield uploaded_file


def upload_file(file_path: str):
    print(f"Uploading {file_path}...")
    uploaded_file = genai.upload_file(path=file_path)
    print(f"Completed uploading {uploaded_file.display_name=} {uploaded_file.name=}")


def upload_files_from_directory(dir_path: str):
    for file in os.listdir(dir_path):
        audio_path = os.path.join(dir_path, file)
        upload_file(audio_path)


def delete_uploaded_file(file_name: str):
    genai.delete_file(file_name)
    print(f"{file_name} deleted")


def delete_all_uploaded_files():
    for uploaded_file in genai.list_files():
        delete_uploaded_file(uploaded_file.name)

