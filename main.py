import sys
import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
from functions.call_function import call_function
from functions.get_files_info import schema_get_files_info
from functions.get_file_content import schema_get_file_content
from functions.run_python_file import schema_run_python_file
from functions.write_file import schema_write_file

load_dotenv()


def main():
    system_prompt = """
You are a helpful AI coding agent.

When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

- List files and directories
- Read file contents
- Execute Python files with optional arguments
- Write or overwrite files

All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
"""
    available_functions = types.Tool(
        function_declarations=[
            schema_get_files_info,
            schema_get_file_content,
            schema_run_python_file,
            schema_write_file,
        ]
    )

    verbose_mode = "--verbose" in sys.argv
    args = []
    for arg in sys.argv[1:]:
        if not arg.startswith("--"):
            args.append(arg)

    if not args:
        print("AI Code Assistant")
        print('\nUsage: python main.py "your prompt here" [--verbose]')
        print('Example: python main.py "What is the meaning of life?"')
        sys.exit(1)

    user_promt = " ".join(args)

    messages = [
        types.Content(role="user", parts=[types.Part(text=user_promt)]),
    ]
    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)

    MAX_ITERRATIONS = 20
    counter = 1
    while counter <= MAX_ITERRATIONS:
        counter += 1
        try:
            response = client.models.generate_content(
                model="gemini-2.0-flash-001",
                contents=messages,
                config=types.GenerateContentConfig(
                    tools=[available_functions], system_instruction=system_prompt
                ),
            )
            usage_metadata = response.usage_metadata

            if verbose_mode:
                print(f"User prompt: {user_promt}")
                print(f"Prompt tokens: {usage_metadata.prompt_token_count}")
                print(f"Response tokens: {usage_metadata.candidates_token_count}")

            if response.function_calls is not None and len(response.function_calls) > 0:
                if response.candidates is not None and len(response.candidates) > 0:
                    for candidate in response.candidates:
                        if candidate.content is not None:
                            messages.append(candidate.content)

                for call in response.function_calls:
                    verbose = False
                    function_call_result = call_function(
                        {"name": call.name, "args": call.args}, verbose=verbose
                    )
                    messages.append(
                        types.Content(role="user", parts=function_call_result.parts)
                    )
                    if verbose:
                        print(
                            f"-> {function_call_result.parts[0].function_response.response}"
                        )
            elif response.text is not None:
                print(response.text)
                break
        except Exception as e:
            print(f"Error: {e}")


if __name__ == "__main__":
    main()
