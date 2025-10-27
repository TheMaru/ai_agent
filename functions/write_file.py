import os


def write_file(working_directory, file_path, content):
    base_dir = os.path.abspath(working_directory)
    full_path = os.path.abspath(os.path.join(working_directory, file_path))

    if not full_path.startswith(base_dir + os.sep) and full_path != base_dir:
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'

    try:
        file_directory = os.path.dirname(full_path)
        os.makedirs(file_directory, exist_ok=True)
        with open(full_path, "w") as f:
            f.write(content)

        return (
            f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
        )

    except Exception as e:
        return f"Error: {e}"
