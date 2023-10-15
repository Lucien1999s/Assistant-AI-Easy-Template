import requests
from bs4 import BeautifulSoup

class STOCK_INFO_OBTAINER:
    def __init__(self, stock_code):
        self.stock_code = stock_code

    def get_basic_info(self):
        url = f"https://tw.stock.yahoo.com/quote/{self.stock_code}.TW/profile"
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        divs = soup.find_all('div', class_='Py(8px) Pstart(12px) Bxz(bb)')
        return [div.text for div in divs]
        
    def get_overview_info(self):
        url = f"https://tw.stock.yahoo.com/_td-stock/api/resource/StockServices.stockList;autoRefresh=1695117188379;fields=avgPrice%2Corderbook;symbols={self.stock_code}.TW?bkt=stock_dt_feature&device=desktop&ecma=modern&feature=useNewQuoteTabColor&intl=tw&lang=zh-Hant-TW&partner=none&prid=111nkipigirq7&region=TW&site=finance&tz=Asia%2FTaipei&ver=1.2.2007&returnMeta=true"
        response = requests.get(url)
        return response.json()

    def get_price(self):
        url = f"https://tw.stock.yahoo.com/_td-stock/api/resource/FinanceChartService.ApacLibraCharts;autoRefresh=1695117188377;symbols=%5B%22{self.stock_code}.TW%22%5D;type=tick?bkt=stock_dt_feature&device=desktop&ecma=modern&feature=useNewQuoteTabColor&intl=tw&lang=zh-Hant-TW&partner=none&prid=111nkipigirq7&region=TW&site=finance&tz=Asia%2FTaipei&ver=1.2.2007&returnMeta=true"
        response = requests.get(url)
        return response.json()

    def get_balance_sheet(self):
        url = f"https://tw.stock.yahoo.com/_td-stock/api/resource/StockServices.balanceSheets;limit=20;period=quarter;sortBy=-date;symbol={self.stock_code}.TW?bkt=stock_dt_feature&device=desktop&ecma=modern&feature=useNewQuoteTabColor&intl=tw&lang=zh-Hant-TW&partner=none&prid=3k8g7ttigisj9&region=TW&site=finance&tz=Asia%2FTaipei&ver=1.2.2007&returnMeta=true"
        response = requests.get(url)
        return response.json()

    def get_income_statement(self):
        url = f"https://tw.stock.yahoo.com/_td-stock/api/resource/StockServices.incomeStatements-growthAnalyses;limit=20;period=quarter;sortBy=-date;symbol={self.stock_code}.TW?bkt=stock_dt_feature&device=desktop&ecma=modern&feature=useNewQuoteTabColor&intl=tw&lang=zh-Hant-TW&partner=none&prid=3k8g7ttigisj9&region=TW&site=finance&tz=Asia%2FTaipei&ver=1.2.2007&returnMeta=true"
        response = requests.get(url)
        return response.json()

    def get_cashflow_statement(self):
        url = f"https://tw.stock.yahoo.com/_td-stock/api/resource/StockServices.cashFlowStatements;limit=20;period=quarter;sortBy=-date;symbol={self.stock_code}.TW?bkt=stock_dt_feature&device=desktop&ecma=modern&feature=useNewQuoteTabColor&intl=tw&lang=zh-Hant-TW&partner=none&prid=3k8g7ttigisj9&region=TW&site=finance&tz=Asia%2FTaipei&ver=1.2.2007&returnMeta=true"
        response = requests.get(url)
        return response.json()

    def get_revenue_eps(self):
        url = f"https://tw.stock.yahoo.com/_td-stock/api/resource/StockServices.revenues;period=month;symbol={self.stock_code}.TW?bkt=stock_dt_feature&device=desktop&ecma=modern&feature=useNewQuoteTabColor&intl=tw&lang=zh-Hant-TW&partner=none&prid=3k8g7ttigisj9&region=TW&site=finance&tz=Asia%2FTaipei&ver=1.2.2007&returnMeta=true"
        response = requests.get(url)
        return response.json()

    def get_dividends(self):
        url = f"https://tw.stock.yahoo.com/_td-stock/api/resource/StockServices.dividends;action=combineCashAndStock;date=;limit=100;showUpcoming=true;sortBy=-date;symbol={self.stock_code}.TW?bkt=stock_dt_feature&device=desktop&ecma=modern&feature=useNewQuoteTabColor&intl=tw&lang=zh-Hant-TW&partner=none&prid=3k8g7ttigisj9&region=TW&site=finance&tz=Asia%2FTaipei&ver=1.2.2007&returnMeta=true"
        response = requests.get(url)
        return response.json()

    def get_etf_ingredient(self):
        url = f"https://tw.stock.yahoo.com/_td-stock/api/resource/ApacFinanceServices.etfInfo;etfRegion=tw;etfSymbol={self.stock_code}.TW?bkt=stock_dt_feature&device=desktop&ecma=modern&feature=useNewQuoteTabColor&intl=tw&lang=zh-Hant-TW&partner=none&prid=4ekm4e5igj9iq&region=TW&site=finance&tz=Asia%2FTaipei&ver=1.2.2017&returnMeta=true"
        response = requests.get(url)
        return response.json()

    def get_recommend_tickers(self):
        url = f"https://tw.stock.yahoo.com/_td-stock/api/resource/StockServices.recommendedTickers;autoRefresh=1695117188379;id=recommendedTickers;sortBy=-changePercent;symbol={self.stock_code}.TW?bkt=stock_dt_feature&device=desktop&ecma=modern&feature=useNewQuoteTabColor&intl=tw&lang=zh-Hant-TW&partner=none&prid=111nkipigirq7&region=TW&site=finance&tz=Asia%2FTaipei&ver=1.2.2007&returnMeta=true"
        response = requests.get(url)
        return response.json()

    def get_sector_rank(self):
        url = f"https://tw.stock.yahoo.com/_td-stock/api/resource/StockServices.stockList;autoRefresh=1695117188379;fields=avgPrice%2Corderbook;symbols={self.stock_code}.TW?bkt=stock_dt_feature&device=desktop&ecma=modern&feature=useNewQuoteTabColor&intl=tw&lang=zh-Hant-TW&partner=none&prid=111nkipigirq7&region=TW&site=finance&tz=Asia%2FTaipei&ver=1.2.2007&returnMeta=true"
        response = requests.get(url)
        sector_id = response.json()["data"][0]["sectorId"]
        url = f"https://tw.stock.yahoo.com/_td-stock/api/resource/StockServices.sectorRanks;autoRefresh=1695117188380;id=sectorRanks;sectorId={sector_id};sortBy=-changePercent?bkt=stock_dt_feature&device=desktop&ecma=modern&feature=useNewQuoteTabColor&intl=tw&lang=zh-Hant-TW&partner=none&prid=111nkipigirq7&region=TW&site=finance&tz=Asia%2FTaipei&ver=1.2.2007&returnMeta=true"
        response = requests.get(url)
        return response.json()

    def get_categories_rank(self):
        url = f"https://tw.stock.yahoo.com/_td-stock/api/resource/StockServices.categoryRanks;id=categoryRanks;label=%E6%A6%82%E5%BF%B5%E8%82%A1;sortBy=-changePercent;symbol={self.stock_code}.TW?bkt=stock_dt_feature&device=desktop&ecma=modern&feature=useNewQuoteTabColor&intl=tw&lang=zh-Hant-TW&partner=none&prid=111nkipigirq7&region=TW&site=finance&tz=Asia%2FTaipei&ver=1.2.2007&returnMeta=true"
        response = requests.get(url)
        return response.json()

    def get_change_rank(self):
        url = f"https://tw.stock.yahoo.com/_td-stock/api/resource/StockServices.changePercentHistory;symbol={self.stock_code}.TW?bkt=stock_dt_feature&device=desktop&ecma=modern&feature=useNewQuoteTabColor&intl=tw&lang=zh-Hant-TW&partner=none&prid=5mtggftigjab0&region=TW&site=finance&tz=Asia%2FTaipei&ver=1.2.2017&returnMeta=true"
        response = requests.get(url)
        return response.json()

    def get_eps_rank(self):
        url = f"https://tw.stock.yahoo.com/_td-stock/api/resource/StockServices.epsHistory;symbol={self.stock_code}.TW?bkt=stock_dt_feature&device=desktop&ecma=modern&feature=useNewQuoteTabColor&intl=tw&lang=zh-Hant-TW&partner=none&prid=5mtggftigjab0&region=TW&site=finance&tz=Asia%2FTaipei&ver=1.2.2017&returnMeta=true"
        response = requests.get(url)
        return response.json()

    def get_ytm_cash(self):
        url = f"https://tw.stock.yahoo.com/_td-stock/api/resource/StockServices.ytmCashSectorRanks;symbol={self.stock_code}.TW?bkt=stock_dt_feature&device=desktop&ecma=modern&feature=useNewQuoteTabColor&intl=tw&lang=zh-Hant-TW&partner=none&prid=5mtggftigjab0&region=TW&site=finance&tz=Asia%2FTaipei&ver=1.2.2017&returnMeta=true"
        response = requests.get(url)
        return response.json()

    def get_same_sector(self):
        url = f"https://tw.stock.yahoo.com/_td-stock/api/resource/StockServices.stockList;autoRefresh=1695117188379;fields=avgPrice%2Corderbook;symbols={self.stock_code}.TW?bkt=stock_dt_feature&device=desktop&ecma=modern&feature=useNewQuoteTabColor&intl=tw&lang=zh-Hant-TW&partner=none&prid=111nkipigirq7&region=TW&site=finance&tz=Asia%2FTaipei&ver=1.2.2007&returnMeta=true"
        response = requests.get(url)
        sector_id = response.json()["data"][0]["sectorId"]
        offset = 0
        res = []
        while True:
            url = f"https://tw.stock.yahoo.com/_td-stock/api/resource/StockServices.getClassQuoteHolders;exchange=TAI;offset={offset};sectorId={sector_id}?bkt=twstock-dt-gam-migration-1&device=desktop&ecma=modern&feature=useNewQuoteTabColor%2CenableHeaderBidding%2CenableStyleTW%2CenableGAMAds%2CenableGAMEdgeToEdge&intl=tw&lang=zh-Hant-TW&partner=none&prid=4nh85uhihfg5k&region=TW&site=finance&tz=Asia%2FTaipei&ver=1.2.2021&returnMeta=true"
            response = requests.get(url).json()
            ids_in_response = [str(item["id"]).replace(".TW","") for item in response["data"]["list"]]
            res.extend(ids_in_response)
            if response["data"]["pagination"]["nextOffset"] is None:
                break
            offset += 30
        return res

if __name__ == "__main__":
    s=STOCK_INFO_OBTAINER("2330")
    res = s.get_price()
    print(res["data"][0]["chart"]["meta"]["regularMarketPrice"])