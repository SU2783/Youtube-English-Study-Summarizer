import os
from tqdm import tqdm
from pathlib import Path
from dotenv import load_dotenv

import google.generativeai as genai
from google.generativeai.models import list_models
from google.generativeai.types import RequestOptions, File
from google.generativeai import GenerationConfig, GenerativeModel
from google.api_core.exceptions import RetryError

from src.markdown_maker import make_markdown_content
from src.file_manager import get_all_uploaded_files, delete_uploaded_file, print_file_info

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))


class ContentsGenerator:
    def __init__(self,
                 model: str | GenerativeModel,
                 system_instruction: str = None,
                 ):
        """
        Initialize the ContentsGenerator class.

        Args:
            model (str | GenerativeModel): Model name or GenerativeModel instance.
            system_instruction (str): System instruction for the model.
        """
        if isinstance(model, str):
            model = self.create_model(model, system_instruction)

        self.model = model
        self.system_instruction = system_instruction
        self.generation_config = None
        self.request_options = None

    def set_generation_config(self, generation_config: GenerationConfig = None, request_options: RequestOptions = None):
        """
        Set the generation configuration and request options.

        Args:
            generation_config (GenerationConfig): Configuration for content generation.
            request_options (RequestOptions): Options for the request.
        """
        self.generation_config = generation_config
        self.request_options = request_options

    def generate_contents(self, prompt: str):
        """
        Generate contents for all uploaded files.

        Args:
            prompt (str): Prompt for content generation.
        """
        progress_bar = tqdm(list(get_all_uploaded_files(only_ready=True)))  # For impatient people like me

        for uploaded_file in progress_bar:
            progress_bar.set_description(f"Generating content for {uploaded_file.display_name}...")

            response_content = self.generate_content(prompt=prompt, uploaded_file=uploaded_file)
            if response_content is None:
                continue

            file_name = Path(uploaded_file.display_name).stem
            make_markdown_content(file_name, response_content, save=True)

            progress_bar.set_description(f"Generated content for {uploaded_file.display_name}")

            delete_uploaded_file(uploaded_file.name, progress_bar=progress_bar)

        self.check_remaining_files()

    def generate_content(self, prompt: str, uploaded_file: File = None):
        """
        Generate content for a specific uploaded file.

        Args:
            prompt (str): Prompt for content generation.
            uploaded_file (File): Uploaded file object.

        Returns:
            str: Generated content.
        """
        prompt = [prompt, uploaded_file] if uploaded_file else prompt

        try:
            responses = self.model.generate_content(
                prompt,
                generation_config=self.generation_config,
                request_options=self.request_options,
                stream=False,
            )
        except RetryError:
            print("RetryError occurred. Skipping content generation for this file.")
            return None

        try:
            response_content = responses.text.strip()
        except ValueError:
            response_content = None

        return response_content

    @staticmethod
    def check_remaining_files():
        """ Check if there are any remaining files that have not been processed. """

        remaining_files = list(get_all_uploaded_files(only_ready=False))
        if remaining_files:
            print("The following files remain unprocessed:")

            for uploaded_file in remaining_files:
                print_file_info(uploaded_file)

    @staticmethod
    def create_model(model_name: str = 'gemini-1.5-flash-002', system_instruction=None):
        """
        Create a GenerativeModel instance.

        Args:
            model_name (str): Name of the model.
            system_instruction (str): System instruction for the model.

        Returns:
            GenerativeModel: Instance of GenerativeModel.
        """
        return genai.GenerativeModel(
            model_name=model_name,
            system_instruction=system_instruction,
        )

    @staticmethod
    def print_all_available_models():
        """ Print all available models. """
        for model in list_models():
            print(model)


if __name__ == '__main__':
    ContentsGenerator.print_all_available_models()

    model_name = 'gemini-1.5-flash-002'
    system_instruction = "Create a content that is informative and engaging."
    contents_generator = ContentsGenerator(model_name, system_instruction)

    answer = contents_generator.generate_content("Write a script for a video about the history of the internet.")
    print(answer)