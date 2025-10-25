import sys
import os
from dotenv import load_dotenv
from google import genai

load_dotenv()


def main():
    if len(sys.argv) != 2:
        print('Usage: uv run main.py "<Question to AI>"')
        sys.exit(1)

    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)
    response = client.models.generate_content(
        model="gemini-2.0-flash-001",
        contents=sys.argv[1],
    )
    usage_metadata = response.usage_metadata

    print(response.text)
    print(f"Prompt tokens: {usage_metadata.prompt_token_count}")
    print(f"Response tokens: {usage_metadata.candidates_token_count}")


if __name__ == "__main__":
    main()
