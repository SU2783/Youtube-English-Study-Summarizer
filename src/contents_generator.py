import os
import time
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
        if isinstance(model, str):
            model = self.create_model(model, system_instruction)

        self.model = model
        self.system_instruction = system_instruction
        self.generation_config = None
        self.request_options = None

        self.generated_contents = []

    def set_generation_config(self, generation_config: GenerationConfig = None, request_options: RequestOptions = None):
        self.generation_config = generation_config
        self.request_options = request_options

    def generate_contents(self, prompt: str):
        all_contents_generated = False

        while not all_contents_generated:
            all_contents_generated = self._generate_contents(prompt=prompt)

            if not all_contents_generated:
                print("모든 영상에 대한 컨텐츠 생성이 완료되지 않았습니다. 1분 후 다시 시도합니다.")
                time.sleep(60)
                continue

            break

    def _generate_contents(self, prompt: str):
        for uploaded_file in get_all_uploaded_files(only_ready=True):
            if uploaded_file.display_name in self.generated_contents:
                continue

            print(f"Generating content for {uploaded_file.display_name}...")

            response_content = self.generate_content(prompt=prompt, uploaded_file=uploaded_file)

            file_name = Path(uploaded_file.display_name).stem
            make_markdown_content(file_name, response_content, save=True)

            self.generated_contents.append(uploaded_file.display_name)

            print(f"Generated content for {uploaded_file.display_name}")

        all_contents_generated = len(self.generated_contents) == len(list(get_all_uploaded_files(only_ready=False)))
        return all_contents_generated

    def generate_content(self, prompt: str, uploaded_file: File = None):
        prompt = [prompt, uploaded_file] if uploaded_file else prompt

        responses = self.model.generate_content(
            prompt,
            generation_config=self.generation_config,
            request_options=self.request_options,
            stream=False,
        )
        response_content = responses.text.strip()
        return response_content

    @staticmethod
    def create_model(model_name: str = 'gemini-1.5-flash-002', system_instruction=None):
        return genai.GenerativeModel(
            model_name=model_name,
            system_instruction=system_instruction,
        )

    @staticmethod
    def print_all_available_models():
        for model in list_models():
            print(model)


if __name__ == '__main__':
    ContentsGenerator.print_all_available_models()

    model_name = 'gemini-1.5-flash-002'
    system_instruction = "Create a content that is informative and engaging."
    contents_generator = ContentsGenerator(model_name, system_instruction)

    answer = contents_generator.generate_content("Write a script for a video about the history of the internet.")
    print(answer)