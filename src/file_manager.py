import os
from tqdm import tqdm
import google.generativeai as genai


def get_all_uploaded_files(only_ready: bool = True):
    """
    Generator to get all uploaded files.

    Args:
        only_ready (bool): If True, only return files that are in the ACTIVE state.

    Yields:
        uploaded_file: An uploaded file object.
    """
    for uploaded_file in genai.list_files():
        if only_ready and uploaded_file.state.name != "ACTIVE":
            print(f"File {uploaded_file.display_name} is not ready yet. {uploaded_file.state=}")
            continue

        yield uploaded_file


def upload_file(file_path: str, mime_type: str = None, progress_bar: tqdm = None):
    """
    Upload a file to the Google server.

    Args:
        file_path (str): Path to the file to be uploaded.
        mime_type (str): MIME type of the file.
        progress_bar (tqdm): Progress bar object for displaying upload progress.

    Returns:
        None
    """
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
    """
    Upload all files from a directory to the Google server.

    Args:
        dir_path (str): Path to the directory containing files to be uploaded.
        mime_type (str): MIME type of the files.

    Returns:
        None
    """
    progress_bar = tqdm(os.listdir(dir_path))
    for file in progress_bar:
        audio_path = os.path.join(dir_path, file)
        upload_file(audio_path, mime_type=mime_type, progress_bar=progress_bar)


def delete_uploaded_file(file_name: str, progress_bar: tqdm = None):
    """
    Delete an uploaded file from the Google server.

    Args:
        file_name (str): Name of the file to be deleted.
        progress_bar (tqdm): Progress bar object for displaying deletion progress.

    Returns:
        None
    """
    genai.delete_file(file_name)

    if progress_bar:
        progress_bar.set_description(f"{file_name} deleted")
    else:
        print(f"{file_name} deleted")


def delete_all_uploaded_files():
    """
    Delete all uploaded files from the Google server.

    Returns:
        None
    """
    progress_bar = tqdm(get_all_uploaded_files())
    for uploaded_file in progress_bar:
        delete_uploaded_file(uploaded_file.name, progress_bar=progress_bar)