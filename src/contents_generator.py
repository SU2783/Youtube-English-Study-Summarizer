import os
import time

from tqdm import tqdm
from pathlib import Path
from dotenv import load_dotenv

import google.generativeai as genai
from google.generativeai.models import list_models
from google.generativeai.types import RequestOptions, File
from google.generativeai import GenerationConfig, GenerativeModel

from src.markdown_maker import make_markdown_content
from src.file_manager import get_all_uploaded_files

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

        self.generated_contents = []

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
        Generate contents based on the given prompt.

        Args:
            prompt (str): Prompt for content generation.
        """
        all_contents_generated = False

        while not all_contents_generated:
            all_contents_generated = self._generate_contents(prompt=prompt)

            if not all_contents_generated:
                print("Content generation for all videos is not complete. Retrying in 1 minute...")
                time.sleep(60)
                continue

            break

    def _generate_contents(self, prompt: str):
        """
        Generate contents for all uploaded files.

        Args:
            prompt (str): Prompt for content generation.

        Returns:
            bool: True if all contents are generated, False otherwise.
        """
        progress_bar = tqdm(list(get_all_uploaded_files(only_ready=True)))  # For impatient people like me

        for uploaded_file in progress_bar:
            if uploaded_file.display_name in self.generated_contents:
                continue

            progress_bar.set_description(f"Generating content for {uploaded_file.display_name}...")

            response_content = self.generate_content(prompt=prompt, uploaded_file=uploaded_file)
            if response_content is None:
                continue

            file_name = Path(uploaded_file.display_name).stem
            make_markdown_content(file_name, response_content, save=True)

            self.generated_contents.append(uploaded_file.display_name)

            progress_bar.set_description(f"Generated content for {uploaded_file.display_name}")

        all_contents_generated = len(self.generated_contents) == len(list(get_all_uploaded_files(only_ready=False)))
        return all_contents_generated

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

        responses = self.model.generate_content(
            prompt,
            generation_config=self.generation_config,
            request_options=self.request_options,
            stream=False,
        )

        try:
            response_content = responses.text.strip()
        except ValueError:
            response_content = None

        return response_content

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