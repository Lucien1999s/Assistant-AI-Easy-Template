import re
import requests
from bs4 import BeautifulSoup
from langchain.document_loaders import WebBaseLoader

class Climber:
    def __init__(self, stock_code):
        self.stock_code = stock_code

    def get_stock_name(self):
        url = f'https://tw.stock.yahoo.com/quote/{self.stock_code}.TW'
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        name = soup.find('h1', {'class': 'C($c-link-text) Fw(b) Fz(24px) Mend(8px)'}).text
        return name

    def get_basic_info(self):
        url = f'https://www.google.com/finance/quote/{self.stock_code}:TPE'
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        price = soup.find('div', {'class': 'YMlKec fxKbKc'}).text
        elements = soup.find_all('div', {'class': 'P6K39c'})
        result = f"現價:{price}\n昨日收盤價:{elements[0].text}\n日價格區間:{elements[1].text}\n年價格區間:{elements[2].text}\n總市值:{elements[3].text}\
            \n本益比:{elements[4].text}\n股息收益率:{elements[5].text}"
        return result

    def get_finance_report(self):
        url = f'https://www.google.com/finance/quote/{self.stock_code}:TPE'
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        titles = soup.find_all('div', {'class': 'rsPbEe'})
        values = soup.find_all('td', {'class': 'QXDnM'})
        td_elements = soup.find_all('td', {'class': 'gEUVJe'})
        changes = []
        for td_element in td_elements:
            span_element = td_element.find('span', {'class': ['JwB6zf Ez2Ioe CnzlGc', 'JwB6zf Ebnabc CnzlGc']})
            if span_element is not None:
                changes.append(span_element.text)
            else:
                changes.append("-")
        res = ""
        for title,value,change in zip(titles,values,changes):
            res += title.text+"："+value.text+" 與上季的變化："+change+"\n"
        return res

    def get_recent_info(self):
        query = f"台股{self.stock_code}近期新聞"
        i = 1
        url = f"https://www.google.com/search?q={query}&start={i}0"
        loader = WebBaseLoader(url)
        data = loader.load()
        avg_words = 300
        content = self._preprocess(data[0].page_content,avg_words)
        return content
    
    def _preprocess(self,data, avg_words):
        target1 = "一字不差"
        target2 = "下一頁 >"

        index = data.find(target1)
        if index != -1:
            data = data[index + len(target1):]

        next_page_index = data.find(target2)
        if next_page_index != -1:
            data = data[:next_page_index]

        data = re.sub(r'\s{2,}', ' ', data)

        data_parts = data.split("›")
        data = "".join(part for part in data_parts if part != "")

        if avg_words is not None:
            data = data[:avg_words]

        return data

if __name__ == "__main__":
    c = Climber("3008")
    name = c.get_stock_name()
    basic_info = c.get_basic_info()
    finance_report = c.get_finance_report()
    recent_info = c.get_recent_info()
    print("股票：",name,"\n","基本資訊：\n",basic_info,"\n最新一季財報：\n",finance_report,"\n相關資訊：\n",recent_info)
    # print("股票：",name,"\n","基本資訊：\n",basic_info,"\n相關資訊：\n",recent_info)