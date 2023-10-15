import numpy as np
import time
from finance_data_utils.stock_information import STOCK_INFO_OBTAINER

class ADVANCED_ANALYSIS:
    def __init__(self, stock_code):
        self.stock = STOCK_INFO_OBTAINER(stock_code)

    def _get_working_capital_ratio(self):
        """Get working capital ratio trend"""
        balanceSheet = self.stock.get_balance_sheet()
        trend_of_wcr = []
        for i in range(20):
            if i >= len(balanceSheet["data"]["list"]):
                break
            currentAssets = float(balanceSheet["data"]["list"][i]["currentAssets"])
            currentLiabilities = float(balanceSheet["data"]["list"][i]["currentLiabilities"])
            if currentAssets != 0:
                trend_of_wcr.append(round(((currentAssets - currentLiabilities)/currentAssets)*100,2))
            else:
                trend_of_wcr.append(0)
        wcr = np.array(trend_of_wcr)
        mean_wcr = np.mean(wcr)
        std_wcr = np.std(wcr)
        if mean_wcr == 0 and std_wcr == 0:
            return None
        return [mean_wcr,std_wcr]

    
    def _get_longTerm_debt_ratio(self):
        """get long-term debt ratio"""
        balanceSheet = self.stock.get_balance_sheet()
        longTermLiabilities = float(balanceSheet["data"]["list"][0]["longTermLiabilities"])
        equity = float(balanceSheet["data"]["list"][0]["equity"])
        res = round((longTermLiabilities/equity)*100,2) if equity != 0 else float('inf')
        if res == 0 or res == float('inf'):
            return None
        return res
        

    def _get_current_ratio(self):
        """Get current ratio"""
        balanceSheet = self.stock.get_balance_sheet()
        currentAssets = float(balanceSheet["data"]["list"][0]["currentAssets"])
        currentLiabilities = float(balanceSheet["data"]["list"][0]["currentLiabilities"])
        res = round(currentAssets / currentLiabilities,2) if currentLiabilities != 0 else float('inf')
        if res == 0 or res == float('inf'):
            return None
        return res

    def _get_quick_ratio(self):
        """Get quick ratio"""
        balanceSheet = self.stock.get_balance_sheet()
        currentAssets = float(balanceSheet["data"]["list"][0]["currentAssets"])
        currentLiabilities = float(balanceSheet["data"]["list"][0]["currentLiabilities"])
        inventory = float(balanceSheet["data"]["list"][0]["inventory"])
        res = round((currentAssets-inventory) / currentLiabilities,2) if currentLiabilities != 0 else float('inf')
        if res == 0 or res == float('inf'):
            return None
        return res

    def _get_equity_ratio(self):
        """Get equity ratio"""
        balanceSheet = self.stock.get_balance_sheet()
        equity = float(balanceSheet["data"]["list"][0]["equity"])
        totalAssets = float(balanceSheet["data"]["list"][0]["totalAssets"])
        res = round((equity/totalAssets)*100,2) if totalAssets != 0 else float('inf')
        if res == 0 or res == float('inf'):
            return None
        return res

    
    def _get_liquidation_value(self):
        """Get liquidation value"""
        balanceSheet = self.stock.get_balance_sheet()
        basicInfo = self.stock.get_basic_info()
        currentAssets = float(balanceSheet["data"]["list"][0]["currentAssets"])
        totalLiabilities = float(balanceSheet["data"]["list"][0]["totalLiabilities"])
        num_share = int(basicInfo[16].replace(",",""))
        res = round((currentAssets-totalLiabilities)/num_share,2) if num_share != 0 else float('inf')
        if res == 0 or res == float('inf'):
            return None
        return res
    
    def _get_net_working_capital(self):
        """Get net working capital"""
        balanceSheet = self.stock.get_balance_sheet()
        basicInfo = self.stock.get_basic_info()
        currentAssets = float(balanceSheet["data"]["list"][0]["currentAssets"])
        currentLiabilities = float(balanceSheet["data"]["list"][0]["currentLiabilities"])
        num_share = int(basicInfo[16].replace(",",""))
        res = round((currentAssets-currentLiabilities)/num_share,2) if num_share != 0 else float('inf')
        if res == 0 or res == float('inf'):
            return None
        return res
    
    def _get_days_sales_of_inventory(self):
        """Get days sales of inventory"""
        balanceSheet = self.stock.get_balance_sheet()
        incomeStatement = self.stock.get_income_statement()
        cogs = 0
        for i in range(4):
            season_revenue = float(incomeStatement["data"]["incomeStatementsList"][i]["revenue"])
            season_grossProfit = float(incomeStatement["data"]["incomeStatementsList"][i]["grossProfit"])
            cogs += season_revenue - season_grossProfit
        inventory = 0
        for i in range(4):
            sub_inventory = float(balanceSheet["data"]["list"][i]["inventory"])
            inventory += sub_inventory
        inventory = inventory / 4
        res = round((inventory/cogs)*360,2) if cogs != 0 else float('inf')
        if res == 0 or res == float('inf'):
            return None
        return res
    
    def _get_days_sales_outstanding(self):
        """Get days sales outstanding"""
        balanceSheet = self.stock.get_balance_sheet()
        incomeStatement = self.stock.get_income_statement()
        revenue = 0
        for i in range(4):
            season_revenue = float(incomeStatement["data"]["incomeStatementsList"][i]["revenue"])
            revenue += season_revenue
        
        accountReceivable = 0
        for i in range(4):
            sub_accountReceivable = float(balanceSheet["data"]["list"][i]["accountsReceivable"])
            accountReceivable += sub_accountReceivable
        accountReceivable = accountReceivable/4
        res = round((accountReceivable/revenue)*360,2) if revenue != 0 else float('inf')
        if res == 0 or res == float('inf'):
            return None
        return res
    
    def _get_days_payable_outstanding(self):
        """Get days payable"""
        balanceSheet = self.stock.get_balance_sheet()
        incomeStatement = self.stock.get_income_statement()
        revenue = 0
        for i in range(4):
            season_revenue = float(incomeStatement["data"]["incomeStatementsList"][i]["revenue"])
            revenue += season_revenue
        
        accountsPayable = 0
        for i in range(4):
            sub_accountsPayable = float(balanceSheet["data"]["list"][i]["accountsPayable"])
            accountsPayable += sub_accountsPayable
        accountsPayable = accountsPayable/4
        res = round((accountsPayable/revenue)*360,2) if revenue != 0 else float('inf')
        if res == 0 or res == float('inf'):
            return None
        return res
    
    def _get_revenue_growth(self):
        """Get revenue growth Yoy and AccYoy"""
        revenue_eps = self.stock.get_revenue_eps()
        acc = float(revenue_eps["data"]["data"]["result"]["revenues"][0]["revenueYoYAcc"])
        yoy = float(revenue_eps["data"]["data"]["result"]["revenues"][0]["revenueYoY"])
        return [yoy,acc]

    def _get_operating_profit_margin(self):
        """Get operating profit margin"""
        incomeStatement = self.stock.get_income_statement()
        revenue = 0
        for i in range(4):
            season_revenue = float(incomeStatement["data"]["incomeStatementsList"][i]["revenue"])
            revenue += season_revenue
        netIncome = 0
        for i in range(4):
            season_netIncome = float(incomeStatement["data"]["incomeStatementsList"][i]["netIncome"])
            netIncome += season_netIncome
        res = round((netIncome/revenue)*100,2) if revenue != 0 else float('inf')
        if res == float('inf'):
            return None
        return res
    
    def _get_eps_record(self):
        """Get 5 year's eps record and up or not"""
        eps_info = self.stock.get_eps_rank()
        trend_list = list(eps_info["data"]["list"][0].values())[:5]
        analyze_res = None
        try:
            if trend_list[0] > trend_list[-1]:
                analyze_res = False
            else:
                analyze_res = True
        except TypeError:
            pass
        return [trend_list,analyze_res]

    
    def _get_dividend_record(self):
        """Get dividend record"""
        info = self.stock.get_etf_ingredient()
        dividend_info = info["data"]["dividend"]["historical"]
        dividend_list = []
        for item in dividend_info:
            if item['dividend'] == '':
                break
            dividend_list.append(float(item['dividend']))
        dividend_list
        if len(dividend_list) == 0:
            period = 0
        else:
            index = len(dividend_list) - 1
            end = int(dividend_info[0]["date"].split('/')[0])
            start = int(dividend_info[index]["date"].split('/')[0])
            period = end - start
        return [dividend_list, period]

    def _check_input(self):
        """Classify what the hell input is"""
        for _ in range(3):
            res = self.stock.get_basic_info()
            if res:
                return len(res)
            else:
                time.sleep(5)
        return 0

    def get_all_intelligent_info(self):
        """Subscript sequence: 
        0. working capital ratio
        1. long-term debt ratio
        2. current ratio
        3. quick ratio
        4. days sales of inventory
        5. days sales outstanding
        6. days payable outstanding
        7. equity ratio
        8. liquidation value
        9. net working capital
        10. revenue growth
        11. operating profit margin
        12. eps record
        13. dividend record
        """
        return [
            self._get_working_capital_ratio(),
            self._get_longTerm_debt_ratio(),
            self._get_current_ratio(),
            self._get_quick_ratio(),
            self._get_days_sales_of_inventory(),
            self._get_days_sales_outstanding(),
            self._get_days_payable_outstanding(),
            self._get_equity_ratio(),
            self._get_liquidation_value(),
            self._get_net_working_capital(),
            self._get_revenue_growth(),
            self._get_operating_profit_margin(),
            self._get_eps_record(),
            self._get_dividend_record()         
        ]
    