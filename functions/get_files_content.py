import os
from config import MAX_CHARS
from google.genai import types

def get_files_content(working_directory, file_path):
    abbs_wrk_dir = os.path.abspath(working_directory)
    abs_file_path = os.path.abspath(os.path.join(working_directory, file_path))

    if not abs_file_path.startswith(abbs_wrk_dir):
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'

    if not os.path.isfile(abs_file_path):
        return f'Error: File not found or is not a regular file: "{file_path}"'
    try:
        with open(abs_file_path, 'r', encoding='utf-8') as f:
            file_content_str = f.read(MAX_CHARS)
            if len(file_content_str) == MAX_CHARS:
                file_content_str += f'[...File "{file_path}" truncated to {MAX_CHARS} characters...]'
            return file_content_str
    except Exception as e:
        return f'Error reading file "{file_path}": {e}'


schema_get_files_content = types.FunctionDeclaration(
    name="get_file_content",
    description=f"Reads and returns the first {MAX_CHARS} characters of the content from a specified file within the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the file whose content should be read, relative to the working directory.",
            ),
        },
        required=["file_path"],
    ),
)