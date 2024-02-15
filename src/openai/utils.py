import openai
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")


# Example input
input_messages = [
    {"speaker": "ai", "text": "가장 기억에 남는 일은 무엇인가요?"},
    {"speaker": "user", "text": "첫째 아이가 태어난 날이 가장 기억에 남아. 와이프가 아이를 낳고 나서 아이를 보여줬을 때, 정말 감동적이었어."}
]
# input_messages2 = [
#     {"speaker": "ai", "text":"노인 일자리에 참여하게 된 동기가 있나요?"},
#     {"speaker": "user", "text": "일자리에 참여하기 전까지 집에서 살림만 하면서 살았어요. 자식들을 다 키워놓고 남편과 집에만 있으니 할 일이 없잖아요. 그래서 무료함을 느끼던 차에 집 근처를 지나다니다가 군포시니어클럽 사무실이 보여서 무작정 들어가서 물어봤어요. 상담을 한 후에 실버급식도우미 자리가 있다고 해서 일을 시작하게 됐어요."}
# ]

def generate_response(input_messages):
    system_message = {
        "role": "system",
        "content": "당신은 노인분들을 잘 이해하며, 진정성이 느껴지는 짧은 답변(한 마디에서 세 마디 사이)과 질문을 한국어로 생성합니다. 공감을 표현하거나 바로 질문하는 형식으로 응답해주세요."
    }

    # Correctly format the input for the OpenAI API
    messages = [system_message] + input_messages  # This line combines the system message with the input messages

    try:
        completion = openai.ChatCompletion.create(
            model="gpt-4",
            messages=messages,
            temperature=0.7,  # Adjust for creativity; lower for more precise responses
            max_tokens=60,  # Adjust based on the length of response you expect; keep it short for 1-3 phrases
        )

        reply = completion.choices[0].message['content']
        return reply
    except Exception as e:
        print(f"An error occurred: {e}")
        return None
    
# Generate and print the response
response = generate_response(input_messages)
print("GPT-4 Response:", response)
