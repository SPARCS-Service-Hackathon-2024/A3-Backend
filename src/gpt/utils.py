import openai
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

def generate_response(input_messages):
    # Initial system message describing the role and behavior of the GPT
    system_message = {
        "role": "system",
        "content": "이 AI는 노인분들을 잘 이해하며, 진정성이 느껴지는 짧은 답변(한 마디에서 세 마디 사이)과 질문을 한국어로 생성합니다. 공감을 표현하거나 바로 질문하는 형식으로 응답해주세요. 답변을 하는 도중 중간에 끊기지 않게 해주세요. 각 문장 끝에는 \n으로 줄바꿈을 표시합니다."
    }
    
    # Format the input for the OpenAI API, starting with the system message
    messages = [system_message]
    for msg in input_messages:
        role = "system" if msg["speaker"] == "ai" else "user"
        messages.append({"role": role, "content": msg["text"]})

    try:
        completion = openai.chat.completions.create(
            model="gpt-4",
            messages=messages,
            temperature=0.7,  # Adjust for creativity; lower for more precise responses
            # max_tokens=200,  # Adjust based on the length of response you expect; keep it short for 1-3 phrases
        )

        replies = completion.choices[0].message.content
        return replies
    except Exception as e:
        print(f"An error occurred: {e}")
        return None