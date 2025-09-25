import os
from google.genai import types


def get_files_info(working_directory, directory="."):
    abbs_wrk_dir = os.path.abspath(working_directory)
    abs_dir = os.path.abspath(os.path.join(working_directory,directory))

    if not abs_dir.startswith(abbs_wrk_dir):
        return f'Error: "{directory}" is not a working directory'
    
    contents = os.listdir(abs_dir)
    final_resp = ""
    for content in contents:
        ctnt_path = os.path.join(abs_dir, content)
        is_dir = os.path.isdir(ctnt_path)
        size = os.path.getsize(ctnt_path)
        final_resp += f"\n - {content}: file_size={size} bytes, is_dir={is_dir}"
    return final_resp


schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
            ),
        },
    ),
)
