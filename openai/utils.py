from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Retrieve the OPENAI_API_KEY from the .env file

def generate_response(input):
    # Format the input for the OpenAI API
    messages = []
    for msg in input:
        role = "system" if msg["speaker"] == "ai" else "user"
        messages.append({"role": role, "content": msg["text"]})

    try:
        completion = client.chat.completions.create(model="gpt-4",
        messages=messages)

        reply = completion.choices[0].message.content
        return reply
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

# Example input
input_messages = [
    {"speaker": "ai", "text": "가장 기억에 남는 일은 무엇인가요?"},
    {"speaker": "user", "text": "첫째 아이가 태어난 날이 가장 기억에 남아. 와이프가 아이를 낳고 나서 아이를 보여줬을 때, 정말 감동적이었어."}
]

# Generate and print the response
response = generate_response(input_messages)
print("GPT-4 Response:", response)
