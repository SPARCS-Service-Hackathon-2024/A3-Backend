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
        "content": "이 AI는 사용자의 답변을 토대로 사용자의 경험과 감정에 공감하며, 대화에 대한 마무리 멘트를 제공합니다. 답변은 간결하며 2 문장을 넘어가지 않습니다."
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

        reply = completion.choices[0].message.content
        return reply
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

# Example input
input_messages = [
    {"speaker": "ai", "text": "가장 기억에 남는 일은 무엇인가요?"},
    {"speaker": "user", "text": "첫째 아이가 태어난 날이 가장 기억에 남아. 와이프가 아이를 낳고 나서 아이를 보여줬을 때, 정말 감동적이었어."},
     {"speaker": "ai", "text": "그 순간의 감정을 상상할 수 있어요. 가족이 함께한 특별한 순간이었겠네요. 다른 기억에 남는 일도 있나요?"},
    {"speaker": "user", "text": "네, 결혼식 날도 정말 기억에 남아요. 모든 사람들이 우리를 축복해주러 왔고, 정말 행복했어요."},
    {"speaker": "ai", "text": "정말 아름다운 순간이었겠어요. 그날의 분위기는 어땠나요?"},
    {"speaker": "user", "text": "모두가 웃고 즐기는 분위기였어요. 사랑하는 사람들과 함께해서 더욱 뜻깊었죠."},
    {"speaker": "ai", "text": "사랑하는 사람들과의 시간은 언제나 특별하죠. 가족과 함께 보낸 또 다른 소중한 시간이 있을까요?"},
    {"speaker": "user", "text": "아이들과 함께한 첫 가족 여행도 정말 잊을 수 없어요. 함께 해변에서 놀고, 저녁에는 바베큐를 했죠."},
    {"speaker": "ai", "text": "가족 여행은 정말 좋은 추억을 만들기에 완벽한 순간이죠. 여행에서 가장 인상 깊었던 일은 무엇인가요?"},
    {"speaker": "user", "text": "해변에서 아이들이 처음으로 파도를 만끽하는 모습을 본 것이에요. 그들의 웃음소리가 아직도 귀에 생생해요."},
]

# Generate and print the response
response = generate_response(input_messages)
print("GPT-4 Response:", response)
