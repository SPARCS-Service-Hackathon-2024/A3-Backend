import openai
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

def generate_summary(input_messages):

    system_message = {
        "role": "system",
        "content": "이 AI는 사용자의 이야기를 듣고, 존댓말을 사용하여 약간의 요약하고 정리하는 작가입니다. 자연스러우면서도 진정성 있는 요약을 제공하는 것이 목표입니다. 본문은 자서전 형식에 맞게 1인칭 시점을 유지하며, 부가적인 설명은 최소화합니다('이렇게 정리해볼게요'와 같은 표현은 사용하지 않습니다). 사용자의 경험과 감정을 정확히 반영하여 요약하되, 내용을 과장하지 않습니다. 요약은 충분한 세부 정보를 포함하여 사용자의 원래 의도와 감정을 표현합니다. 요약은 존댓말(예: '했습니다', '되었습니다', '있었습니다')로 적어주세요."
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
        )


        summary_response = completion.choices[0].message.content

        # Prepare the output
        output = [
            {"speaker": "ai", "text": input_messages[0]["text"]},  # The first AI question
            {"speaker": "user", "text": summary_response}  # The GPT-generated summary
        ]
        return output
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

response = generate_summary(input_messages)
if response:
    for message in response:
        print(f"{message['speaker']} says: {message['text']}")
else:
    print("No response generated.")