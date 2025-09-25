import os
import subprocess
from google.genai import types

def run_python_file(working_directory:str, file_path:str, args=[]):
    abs_working_directory = os.path.abspath(working_directory)
    abs_file_path = os.path.abspath(os.path.join(working_directory, file_path))

    if not abs_file_path.startswith(abs_working_directory):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    
    if not os.path.isfile(abs_file_path):
        return f'Error: File "{file_path}" not found.'
    
    if not file_path.endswith('.py'):
        return f'Error: "{file_path}" is not a Python file.'
    
    try:
        final_args = ["python", abs_file_path]
        final_args.extend(args)
        result = subprocess.run(
            final_args,
            timeout= 30,
            capture_output=True,
            cwd=abs_working_directory
        )
        final_str = f"""
        STDOUT: {result.stdout}
        STDERR: {result.stderr}
        """

        if result.stdout == "" and result.stderr == "":
            final_str = "No output from script."
        if result.returncode != 0:
            final_str = f"Script exited with code {result.returncode}.\n" + final_str
        return final_str
    except Exception as e:
        return f"Error: executing Python file: {e}"
    

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Executes a Python file within the working directory and returns the output from the interpreter.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path to the Python file to execute, relative to the working directory.",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                items=types.Schema(
                    type=types.Type.STRING,
                    description="Optional arguments to pass to the Python file.",
                ),
                description="Optional arguments to pass to the Python file.",
            ),
        },
        required=["file_path"],
    ),
)