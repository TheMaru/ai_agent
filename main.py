import sys
import os
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()


def main():
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
    response = client.models.generate_content(
        model="gemini-2.0-flash-001",
        contents=messages,
    )
    usage_metadata = response.usage_metadata

    if verbose_mode:
        print(f"User prompt: {user_promt}")
        print(f"Prompt tokens: {usage_metadata.prompt_token_count}")
        print(f"Response tokens: {usage_metadata.candidates_token_count}")

    print(response.text)


if __name__ == "__main__":
    main()
