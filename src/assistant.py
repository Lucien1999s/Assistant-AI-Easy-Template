from src.knowledge_base import KnowledgeBase
import os
import openai
from dotenv import load_dotenv

load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")


class Assistant:
    def __init__(self):
        self.prompt = KnowledgeBase()
        self.model = os.getenv("OPENAI_MODEL", default="gpt-3.5-turbo-16k")
        self.temperature = float(os.getenv("OPENAI_TEMPERATURE", default=0.2))
        self.max_tokens = int(os.getenv("OPENAI_MAX_TOKENS", default=2000))

    def get_response(self):
        response = openai.ChatCompletion.create(
            model=self.model,
            messages=self.prompt.generate_prompt(),
            temperature=self.temperature,
            max_tokens=self.max_tokens,
        )
        return response["choices"][0]["message"]["content"]

    def add_msg(self, text, role):
        if role == "ai":
            self.prompt.add_ai_msg(text)
        else:
            self.prompt.add_user_msg(text)

    def check_field(self,user_input):
        check_prompt = f"""
        你是一個領域審查者，你會查看使用者的訊息是否和金融投資相關
        使用者訊息：
        [
        {user_input}
        ]
        請問該訊息是否和金融相關?
        回答相關或不相關
        你的回答：
        """
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": check_prompt}],
            temperature=0.1,
            max_tokens=5,
        )
        return response["choices"][0]["message"]["content"]

if __name__ == "__main__":
    a = Assistant()
    res=a.check_field("金融好棒對吧")
    print(res)