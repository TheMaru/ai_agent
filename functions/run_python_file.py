import os
import subprocess

from google.genai import types


def run_python_file(working_directory, file_path, args=[]):
    base_dir = os.path.abspath(working_directory)
    full_path = os.path.abspath(os.path.join(working_directory, file_path))

    if not full_path.startswith(base_dir + os.sep) and full_path != base_dir:
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

    if not os.path.exists(full_path):
        return f'Error: File "{file_path}" not found.'

    if not full_path[-3:] == ".py":
        return f'Error: "{file_path}" is not a Python file.'

    try:
        command_list = ["python", full_path]
        command_list.extend(args)

        file_directory = os.path.dirname(full_path)

        result = subprocess.run(
            command_list, capture_output=True, timeout=30, cwd=file_directory, text=True
        )
        result_str = ""

        if len(result.stdout) > 0:
            result_str += f"STDOUT: {result.stdout}\n"
        if len(result.stderr) > 0:
            result_str += f"STDERR: {result.stderr}\n"
        if result.returncode != 0:
            result_str += f"Process exited with code {result.returncode}"
        if len(result_str) <= 0:
            result_str = "No output produced"

        return result_str

    except Exception as e:
        return f"Error: executing Python file: {e}"


schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="This function will run a file with the extension .py aka python file, args can be ommited and is only needed for some files, please don't ask for args, constrained to the working directory",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the file which content should be exectued, relative to the working directory.",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                items=types.Schema(type=types.Type.STRING),
                description="Optional arguments to pass to the Python file",
            ),
        },
        required=["file_path"],
    ),
)
