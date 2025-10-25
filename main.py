import os
from dotenv import load_dotenv
from google import genai

load_dotenv()


def main():
    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)
    response = client.models.generate_content(
        model="gemini-2.0-flash-001",
        contents="Why is Boot.dev such a great place to learn backend development? Use one paragraph maximum.",
    )
    usage_metadata = response.usage_metadata

    print(response.text)
    print(f"Prompt tokens: {usage_metadata.prompt_token_count}")
    print(f"Response tokens: {usage_metadata.candidates_token_count}")


if __name__ == "__main__":
    main()
