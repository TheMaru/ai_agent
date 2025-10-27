import os

from google.genai import types


def get_files_info(working_directory, directory="."):
    return_str = ""
    try:
        base_dir = os.path.abspath(working_directory)
        full_path = os.path.abspath(os.path.join(working_directory, directory))

        if not full_path.startswith(base_dir + os.sep) and full_path != base_dir:
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'

        if not os.path.isdir(full_path):
            return f'Error: "{directory}" is not a directory'

        dir_contents = os.listdir(full_path)

        for content in dir_contents:
            path = os.path.join(full_path, content)
            return_str += f"- {content}: file_size={os.path.getsize(path)} is_dir={os.path.isdir(path)}\n"

        return return_str
    except Exception as e:
        return f"Error: {e}"


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
