from src.knowledge_base import KnowledgeBase
from src.stock_info_grabber import Climber
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
    
    def check_analysis(self,user_input):
        check_prompt = f"""
        你是一個資訊審查者，你會查看使用者的訊息是否要求分析股票
        使用者訊息：
        [
        {user_input}
        ]
        請問該訊息是否要求分析股票？
        回答是或不是
        你的回答：
        """
        extraction_prompt = f"""
        你是一個萃取器，你會從文本中萃取出股票代碼，如果沒有你會回覆None
        文本：
        [
        {user_input}
        ]
        回答股票代碼或None
        你的回答：
        """
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": check_prompt}],
            temperature=0.1,
            max_tokens=5,
        )
        check = response["choices"][0]["message"]["content"]
        if check == "是":
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": extraction_prompt}],
                temperature=0.1,
                max_tokens=7,
            )
            return response["choices"][0]["message"]["content"]
        else:
            return None
    
    def analysis_stock(self,stock_code):
        climber = Climber(stock_code)
        name = climber.get_stock_name()
        basic_info = climber.get_basic_info()
        finance_report = climber.get_finance_report()
        recent_info = climber.get_recent_info()
        info = "股票："+name+"\n"+"基本資訊：\n"+basic_info+"\n最新一季財報：\n"+finance_report+"\n相關資訊：\n"+recent_info
        prompt = f"""
        你是一個股票分析師，你將閱讀完以下股票的資訊並撰寫一個分析結果
        股票相關資訊：
        [
        {info}
        ]
        你報告的內容要有：
        該股票的本益比來看是否被低估？(本益比低於12便宜，15合理，大於15就是不合理)
        以年範圍來看現價是否值得投資？(假如年範圍是15-25，現價=23，中值計算:25-((25-15)/2)=20，而現價23>中值20，所以目前不值得投資，應該再等一陣子，如果小於中值表示相對便宜可以買進)
        從財務報表來看此公司是否財務結構健全？詳細分析，可以提到負債比率和成本等等的
        該股票的整體資訊和你分析結果來看是否值得投資？
        股票分析結果報告：
        """
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo-16k",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.1,
            max_tokens=2000,
        )
        return response["choices"][0]["message"]["content"]

if __name__ == "__main__":
    a = Assistant()
    res=a.analysis_stock("2330")
    print(res)