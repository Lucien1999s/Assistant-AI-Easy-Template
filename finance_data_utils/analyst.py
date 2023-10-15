from finance_data_utils.intelligent_investor_information import ADVANCED_ANALYSIS
from finance_data_utils.stock_information import STOCK_INFO_OBTAINER
from finance_data_utils.database import fetch_data_from_db, check_table_columns, update_data, insert_data_to_db
from tqdm import tqdm
import time

def _climb_and_analyze(same_sector_stocks):
    data = []
    for stock in tqdm(same_sector_stocks):
        for _ in range(3):
            result = [stock, None]
            try:
                advance = ADVANCED_ANALYSIS(stock_code=stock)
                advance_info = advance.get_all_intelligent_info()
                result = [stock, advance_info]
            except Exception:
                print(f"Retrying in 1 min...")
                time.sleep(65)
        data.append(result)
    return data

def get_indicator_data(stock_code, update=False):
    root_basic = STOCK_INFO_OBTAINER(stock_code=stock_code)
    price = root_basic.get_price()["data"][0]["chart"]["meta"]["regularMarketPrice"]
    same_sector_stocks = root_basic.get_same_sector()
    sectorId = root_basic.get_overview_info()["data"][0]["sectorId"]
    column_name = f"sector{sectorId}"
    sector_list = check_table_columns()
    if column_name in sector_list:
        if update:
            data = _climb_and_analyze(same_sector_stocks=same_sector_stocks)
            update_data(sectorId=sectorId, new_value=data)
            return price, data
        else:
            return price, fetch_data_from_db(sectorId=sectorId)
    data = _climb_and_analyze(same_sector_stocks=same_sector_stocks)
    insert_data_to_db(sectorId=sectorId,data=data)
    return price, data

def analyze_company_stocks(stock_code, price, data):
    # 取得有用的分析指標
    for i, item in enumerate(data):
        if item[0] == stock_code:
            index = i
            break
    useful_items = []
    for i in range(len(data[index][1])):
        if data[index][1][i] != None:
            useful_items.append(i)

    result = {}
    # 營運資金比率分析
    if 0 in useful_items:
        # counting
        work_capital_ratio1_list = []
        work_capital_ratio2_list = []
        stock_list = []
        for item in data:
            if item[1] is not None and item[1][0] is not None:
                stock_list.append(item[0])
                work_capital_ratio1_list.append(round(item[1][0][0],3))
                work_capital_ratio2_list.append(round(item[1][0][1],3))
                
        mean = sum(work_capital_ratio1_list)/len(work_capital_ratio1_list)
        std = sum(work_capital_ratio2_list)/len(work_capital_ratio2_list)
        target_mean = data[index][1][0][0]
        target_std = data[index][1][0][1]

        # Filter
        working_capital_ratio_comment = ""
        if target_mean > mean:
            working_capital_ratio_comment += f"該公司的營運資金比率歷年均值為{round(target_mean,2)} 高於同業水平的{round(mean,2)}，意味著公司有足夠的流動資產來支付其流動負債，這反映了公司的財務健康和靈活性。但此值也不能過高，過高可能表示公司沒有有效利用流動資產。"
        else:
            working_capital_ratio_comment += f"該公司的營運資金比率歷年均值為{round(target_mean,2)} 低於同業水平的{round(mean,2)}，可能意味著公司在特殊情況下可能會在支付其短期債務上有困難。"
        
        if target_std > std:
            working_capital_ratio_comment += f"該公司的營運資金比率歷年變異數為{round(target_std,2)} 高於同業水平的{round(std,2)}，可能顯示公司的經營不穩定和風險高"
        else:
            working_capital_ratio_comment += f"該公司的營運資金比率歷年變異數為{round(target_std,2)} 低於同業水平的{round(std,2)}，表示公司的經營較為穩定，風險管理好"
        
        # Ranking
        mean_rank_list = dict(sorted(dict(zip(stock_list, work_capital_ratio1_list)).items(), key=lambda item: item[1], reverse=True))
        if stock_code in mean_rank_list:
            mean_rank = list(mean_rank_list.keys()).index(stock_code) + 1
            mean_percentage = (mean_rank / len(mean_rank_list)) * 100

        std_rank_list = dict(sorted(dict(zip(stock_list, work_capital_ratio2_list)).items(), key=lambda item: item[1]))
        if stock_code in std_rank_list:
            std_rank = list(std_rank_list.keys()).index(stock_code) + 1
            std_percentage = (std_rank / len(std_rank_list)) * 100
        mean_rank_list = [[key, value] for key, value in mean_rank_list.items()]
        std_rank_list = [[key, value] for key, value in std_rank_list.items()]
        working_capital_ratio_info = [working_capital_ratio_comment, [mean_rank, round(mean_percentage,2), mean_rank_list], [std_rank, round(std_percentage,2), std_rank_list]]
        result["working capital ratio"] = working_capital_ratio_info
    # 長期負債比率分析
    if 1 in useful_items:
        longterm_debt_list = []
        stock_list = []
        for item in data:
            if item[1] is not None and item[1][1] is not None:
                stock_list.append(item[0])
                longterm_debt_list.append(item[1][1])
        # mean = sum(longterm_debt_list)/len(longterm_debt_list)
        target_longterm_debt = data[index][1][1]

        # Filter
        longterm_debt_comment = ""
        if target_longterm_debt < 50:
            longterm_debt_comment += f"長期負債比率為{round(target_longterm_debt,2)}% 低於50%，50%是一個標準門檻，顯示不會有過度依賴借款之現象。"
        else:
            longterm_debt_comment += f"長期負債比率為{round(target_longterm_debt,2)}% 高於50%，這可能顯示該公司有過度依賴借款來維持營運的問題。"
        
        # Ranking
        combined_list = list(zip(stock_list, longterm_debt_list))
        sorted_combined_list = sorted(combined_list, key=lambda item: item[1])
        if any(stock_code in sublist for sublist in sorted_combined_list):
            rank = next(i for i, v in enumerate(sorted_combined_list) if v[0] == stock_code) + 1
            percentage = (rank / len(sorted_combined_list)) * 100
        longterm_debt_rank_list = [[item[0], item[1]] for item in sorted_combined_list]
        longterm_debt_info = [longterm_debt_comment, [rank, round(percentage,2), longterm_debt_rank_list]]
        result["longterm debt ratio"] = longterm_debt_info
    # 流動比率分析
    if 2 in useful_items:
        current_ratio_list = []
        stock_list = []
        for item in data:
            if item[1] is not None and item[1][2] is not None:
                current_ratio_list.append(item[1][2])
                stock_list.append(item[0])
        # mean = sum(current_ratio_list)/len(current_ratio_list)
        target_current_ratio = data[index][1][2]
        # filter
        current_ratio_comment = ""
        if target_current_ratio > 2:
            current_ratio_comment += f"該公司流動比率為{round(target_current_ratio,2)} 高於2，表示公司有充足的流動性，這表明公司在到期時處理其流動債務將沒有困難。"
        else:
            current_ratio_comment += f"該公司流動比率為{round(target_current_ratio,2)} 低於2，表示公司沒有充足的流動性，這表明公司在到期時處理其流動債務會較困難。"
        
        # Ranking
        combined_list = list(zip(stock_list, current_ratio_list))
        sorted_combined_list = sorted(combined_list, key=lambda item: item[1], reverse=True)
        if any(stock_code in sublist for sublist in sorted_combined_list):
            rank = next(i for i, v in enumerate(sorted_combined_list) if v[0] == stock_code) + 1
            percentage = (rank / len(sorted_combined_list)) * 100
        current_ratio_rank_list = [[item[0], item[1]] for item in sorted_combined_list]
        current_ratio_info = [current_ratio_comment, [rank, round(percentage,2), current_ratio_rank_list]]
        result["current ratio"] = current_ratio_info
    # 速動比率分析
    if 3 in useful_items:
        quick_ratio_list = []
        stock_list = []
        for item in data:
            if item[1] is not None and item[1][3] is not None:
                quick_ratio_list.append(item[1][3])
                stock_list.append(item[0])
        # mean = sum(quick_ratio_list)/len(quick_ratio_list)
        target_quick_ratio = data[index][1][3]
        # Filter
        quick_ratio_comment = ""
        if target_quick_ratio > 1:
            quick_ratio_comment += f"該公司速動比率為{round(target_quick_ratio,2)} 大於1，一般認為該數值大於1是一個標準，表示公司的現金和應收帳款能應付及時的債務"
        else:
            quick_ratio_comment += f"該公司速動比率為{round(target_quick_ratio,2)} 小於1，一般認為該數值大於1是一個標準，因此表示公司的現金和應收帳款較難應付及時的債務"
        
        # Ranking
        combined_list = list(zip(stock_list, quick_ratio_list))
        sorted_combined_list = sorted(combined_list, key=lambda item: item[1], reverse=True)
        if any(stock_code in sublist for sublist in sorted_combined_list):
            rank = next(i for i, v in enumerate(sorted_combined_list) if v[0] == stock_code) + 1
            percentage = (rank / len(sorted_combined_list)) * 100
        quick_ratio_rank_list = [[item[0], item[1]] for item in sorted_combined_list]
        quick_ratio_info = [quick_ratio_comment, [rank, round(percentage,2), quick_ratio_rank_list]]
        result["quick ratio"] = quick_ratio_info
    # 存貨週轉天數分析
    if 4 in useful_items:
        days_sale_inventory_list = []
        stock_list = []
        for item in data:
            if item[1] is not None and item[1][4] is not None:
                days_sale_inventory_list.append(item[1][4])
                stock_list.append(item[0])
        mean = sum(days_sale_inventory_list)/len(days_sale_inventory_list)
        target_days_sale_inventory = data[index][1][4]
        # Filter
        days_sale_inventory_comment = ""
        if target_days_sale_inventory < mean:
            days_sale_inventory_comment += f"該公司的存貨週轉天數為{round(target_days_sale_inventory,2)}天 低於同業平均水平的{round(mean, 2)}天，表示公司有良好的存貨管理能力，公司將資產轉化為利潤的實力較好。"
        else:
            days_sale_inventory_comment += f"該公司的存貨週轉天數為{round(target_days_sale_inventory, 2)}天 高於同業平均水平的{round(mean, 2)}天，表示公司在存貨管理能力方面較同業公司的差，公司將資產轉化為利潤的實力較差。"
        
        # Ranking
        combined_list = list(zip(stock_list, days_sale_inventory_list))
        sorted_combined_list = sorted(combined_list, key=lambda item: item[1])
        if any(stock_code in sublist for sublist in sorted_combined_list):
            rank = next(i for i, v in enumerate(sorted_combined_list) if v[0] == stock_code) + 1
            percentage = (rank / len(sorted_combined_list)) * 100
        days_sale_inventory_rank_list = [[item[0], item[1]] for item in sorted_combined_list]
        days_sale_inventory_info = [days_sale_inventory_comment, [rank, round(percentage,2), days_sale_inventory_rank_list]]
        result["days sale inventory"] = days_sale_inventory_info
    # 應收帳款天數分析
    if 5 in useful_items:
        days_sale_outstanding_list = []
        stock_list = []
        for item in data:
            if item[1] is not None and item[1][5] is not None:
                days_sale_outstanding_list.append(item[1][5])
                stock_list.append(item[0])
        mean = sum(days_sale_outstanding_list)/len(days_sale_outstanding_list)
        target_days_sale_outstanding = data[index][1][5]
        # Filter
        days_sale_outstanding_comment = ""
        if target_days_sale_outstanding < mean:
            days_sale_outstanding_comment += f"該公司的應收帳款天數為{round(target_days_sale_outstanding,2)}天 低於同業平均水平的{round(mean, 2)}天，表示公司相較同業公司能夠更快地轉化賬款為現金，顯現較好的管理能力。"
        else:
            days_sale_outstanding_comment += f"該公司的應收帳款天數為{round(target_days_sale_outstanding, 2)}天 高於同業平均水平的{round(mean, 2)}天，表示公司相較同業公司轉化賬款為現金的能力較差。"
        
        # Ranking
        combined_list = list(zip(stock_list, days_sale_outstanding_list))
        sorted_combined_list = sorted(combined_list, key=lambda item: item[1])
        if any(stock_code in sublist for sublist in sorted_combined_list):
            rank = next(i for i, v in enumerate(sorted_combined_list) if v[0] == stock_code) + 1
            percentage = (rank / len(sorted_combined_list)) * 100
        days_sale_outstanding_rank_list = [[item[0], item[1]] for item in sorted_combined_list]
        days_sale_outstanding_info = [days_sale_outstanding_comment, [rank, round(percentage, 2), days_sale_outstanding_rank_list]]
        result["days sale outstanding"] = days_sale_outstanding_info
    # 應付帳款天數分析
    if 6 in useful_items:
        days_payable_outstanding_list = []
        stock_list = []
        for item in data:
            if item[1] is not None and item[1][6] is not None:
                days_payable_outstanding_list.append(item[1][6])
                stock_list.append(item[0])
        mean = sum(days_payable_outstanding_list)/len(days_payable_outstanding_list)
        target_days_payable_outstanding = data[index][1][6]
        # Filter
        days_payable_outstanding_comment = ""
        if target_days_payable_outstanding < mean:
            days_payable_outstanding_comment += f"該公司的應收帳款天數為{round(target_days_payable_outstanding, 2)}天 低於同業平均水平的{round(mean, 2)}天，表示公司相較同業公司能夠更快地轉化賬款為現金，顯現較好的管理能力。"
        else:
            days_payable_outstanding_comment += f"該公司的應收帳款天數為{round(target_days_payable_outstanding, 2)}高於同業平均水平的{round(mean, 2)}，表示公司相較同業公司轉化賬款為現金的能力較差。"
        
        # Ranking
        combined_list = list(zip(stock_list, days_payable_outstanding_list))
        sorted_combined_list = sorted(combined_list, key=lambda item: item[1])
        if any(stock_code in sublist for sublist in sorted_combined_list):
            rank = next(i for i, v in enumerate(sorted_combined_list) if v[0] == stock_code) + 1
            percentage = (rank / len(sorted_combined_list)) * 100
        days_payable_outstanding_rank_list = [[item[0], item[1]] for item in sorted_combined_list]
        days_payable_outstanding_info = [days_payable_outstanding_comment, [rank, round(percentage, 2), days_payable_outstanding_rank_list]]
        result["days payable outstanding"] = days_payable_outstanding_info
    # 股本比例分析
    if 7 in useful_items:
        equity_ratio_list = []
        stock_list = []
        for item in data:
            if item[1] is not None and item[1][7] is not None:
                equity_ratio_list.append(item[1][7])
                stock_list.append(item[0])
        # mean = sum(equity_ratio_list)/len(equity_ratio_list)
        target_equity_ratio = data[index][1][7]
        # Filter
        equity_ratio_comment = ""
        if target_equity_ratio > 50:
            equity_ratio_comment += f"該公司的股本比例為{round(target_equity_ratio, 2)}% 高於50%，這顯示公司使用的自有資金程度過半，也能表示該公司的財務結構是穩健的"
        else:
            equity_ratio_comment += f"該公司的股本比例為{round(target_equity_ratio, 2)}% 低於50%，這顯示公司使用的自有資金程度未過半，也能表示該公司的財務結構較差"
        
        # Ranking
        combined_list = list(zip(stock_list, equity_ratio_list))
        sorted_combined_list = sorted(combined_list, key=lambda item: item[1],reverse=True)
        if any(stock_code in sublist for sublist in sorted_combined_list):
            rank = next(i for i, v in enumerate(sorted_combined_list) if v[0] == stock_code) + 1
            percentage = (rank / len(sorted_combined_list)) * 100
        equity_ratio_rank_list = [[item[0], item[1]] for item in sorted_combined_list]
        equity_ratio_info = [equity_ratio_comment, [rank, round(percentage, 2), equity_ratio_rank_list]]
        result["equity ratio"] = equity_ratio_info
    if 8 in useful_items:
        liquidation_list = []
        stock_list = []
        for item in data:
            if item[1] is not None and item[1][8] is not None:
                liquidation_list.append(item[1][8])
                stock_list.append(item[0])
        target_liquidation = data[index][1][8]
        # Filter
        liquidation_comment = ""
        if price > target_liquidation:
            liquidation_comment += f"該公司的清算價值除以總股數為{round(target_liquidation, 2)}元 低於其現價{price}元，這很可能表示該公司股票價值被高估，但也要看產業類型。"
        else:
            liquidation_comment += f"該公司的清算價值除以總股數為{round(target_liquidation, 2)}元 高於其現價{price}元，這很可能表示該公司股票價值被低估。"

        # Ranking
        combined_list = list(zip(stock_list, liquidation_list))
        sorted_combined_list = sorted(combined_list, key=lambda item: item[1],reverse=True)
        if any(stock_code in sublist for sublist in sorted_combined_list):
            rank = next(i for i, v in enumerate(sorted_combined_list) if v[0] == stock_code) + 1
            percentage = (rank / len(sorted_combined_list)) * 100
        liquidation_rank_list = [[item[0], item[1]] for item in sorted_combined_list]
        liquidation_info = [liquidation_comment, [rank, round(percentage,2), liquidation_rank_list]]
        result["liquidation value"] = liquidation_info
    
    # 淨營運資本分析
    if 9 in useful_items:
        net_working_capital_list = []
        stock_list = []
        for item in data:
            if item[1] is not None and item[1][9] is not None:
                net_working_capital_list.append(item[1][9])
                stock_list.append(item[0])
        target_net_working_capital = data[index][1][9]
        # Filter
        net_working_capital_comment = ""
        if price > target_net_working_capital:
            net_working_capital_comment += f"該公司的每股淨營運資本為{round(target_net_working_capital, 2)}元 低於其現價{price}元，這很可能表示該公司股票價值被高估。"
        else:
            net_working_capital_comment += f"該公司的每股淨營運資本為{round(target_net_working_capital, 2)}元 高於其現價{price}元，這很可能表示該公司股票價值被低估，是投資的好機會。"

        # Ranking
        combined_list = list(zip(stock_list, net_working_capital_list))
        sorted_combined_list = sorted(combined_list, key=lambda item: item[1],reverse=True)
        if any(stock_code in sublist for sublist in sorted_combined_list):
            rank = next(i for i, v in enumerate(sorted_combined_list) if v[0] == stock_code) + 1
            percentage = (rank / len(sorted_combined_list)) * 100
        net_working_capital_rank_list = [[item[0], item[1]] for item in sorted_combined_list]
        net_working_capital_info = [net_working_capital_comment, [rank, round(percentage,2), net_working_capital_rank_list]]
        result["net working capital"] = net_working_capital_info

    # 營收成長性分析
    if 10 in useful_items:
        revenue_growth_list = []
        stock_list = []
        for item in data:
            if item[1] is not None and item[1][10] is not None:
                revenue_growth_list.append(item[1][10][1])
                stock_list.append(item[0])
        mean = sum(revenue_growth_list)/len(revenue_growth_list)
        target_revenue_growth = data[index][1][10][1]
        # Filter
        revenue_growth_comment = ""
        if target_revenue_growth > mean and target_revenue_growth > 0:
            revenue_growth_comment += f"該公司的營收累積成長率為{round(target_revenue_growth, 2)}% 高於同業平均的{round(mean, 2)}%，表示相較同業公司，有更為穩定的營收成長表現，且期間內營收有穩定成長。"
        elif target_revenue_growth > mean and target_revenue_growth < 0:
            revenue_growth_comment += f"該公司的營收累積成長率為{round(target_revenue_growth, 2)}% 高於同業平均的{round(mean, 2)}%，表示相較同業公司，有更為穩定的營收成長表現，但營收累積成長率為負值，表示營收並未穩定成長。"
        elif target_revenue_growth < mean and target_revenue_growth > 0:
            revenue_growth_comment += f"該公司的營收累積成長率為{round(target_revenue_growth, 2)}% 低於同業平均的{round(mean, 2)}%，表示相較同業公司，營收成長表現較差，但營收累積成長率為正值，表示營收還是有穩定成長。"
        else:
            revenue_growth_comment += f"該公司的營收累積成長率為{round(target_revenue_growth, 2)}% 低於同業平均的{round(mean, 2)}%，表示相較同業公司，營收成長表現較差，而營收累積成長率為負值，表示營收也並未穩定成長。"
        
        # Ranking
        combined_list = list(zip(stock_list, revenue_growth_list))
        sorted_combined_list = sorted(combined_list, key=lambda item: item[1],reverse=True)
        if any(stock_code in sublist for sublist in sorted_combined_list):
            rank = next(i for i, v in enumerate(sorted_combined_list) if v[0] == stock_code) + 1
            percentage = (rank / len(sorted_combined_list)) * 100
        revenue_growth_rank_list = [[item[0], item[1]] for item in sorted_combined_list]
        revenue_growth_info = [revenue_growth_comment, [rank, round(percentage,2), revenue_growth_rank_list]]
        result["revenue growth"] = revenue_growth_info
    # 營業利益率分析
    if 11 in useful_items:
        operating_profit_margin_list = []
        stock_list = []
        for item in data:
            if item[1] is not None and item[1][11] is not None:
                operating_profit_margin_list.append(item[1][11])
                stock_list.append(item[0])
        mean = sum(operating_profit_margin_list)/len(operating_profit_margin_list)
        target_operating_profit_margin = data[index][1][11]
        # Filter
        operating_profit_margin_comment = ""
        if target_operating_profit_margin > mean:
            operating_profit_margin_comment += f"該公司的營業利益率為{round(target_operating_profit_margin, 2)}% 高於同業平均水平的{round(mean, 2)}%，表示相較同業有較優秀且高效的經營管理能力"
        else:
            operating_profit_margin_comment += f"該公司的營業利益率為{round(target_operating_profit_margin, 2)}% 低於同業平均水平的{round(mean, 2)}%，表示相較同業有較差的經營管理能力"
        
        # Ranking
        combined_list = list(zip(stock_list, operating_profit_margin_list))
        sorted_combined_list = sorted(combined_list, key=lambda item: item[1],reverse=True)
        if any(stock_code in sublist for sublist in sorted_combined_list):
            rank = next(i for i, v in enumerate(sorted_combined_list) if v[0] == stock_code) + 1
            percentage = (rank / len(sorted_combined_list)) * 100
        operating_profit_margin_rank_list = [[item[0], item[1]] for item in sorted_combined_list]
        operating_profit_margin_info = [operating_profit_margin_comment, [rank, round(percentage,2), operating_profit_margin_rank_list]]
        result["operating profit margin"] = operating_profit_margin_info
    # 每股盈餘分析
    if 12 in useful_items:
        stock_list = []
        for item in data:
            if item[1] is not None and item[1][12][1] is not None:
                stock_list.append(item[0])
        target_eps = data[index][1][12][1]
        eps_data = data[index][1][12][0]
        # Filter
        eps_comment = ""
        if target_eps is True:
            eps_comment += f"該公司的每股盈餘在幾年內有穩定增長，表示公司有持續創造價值的能力"
        else:
            eps_comment += f"該公司的每股盈餘在幾年內未穩定增長，公司是否有持續創造價值的能力，需要進一步分析"
        eps_info = [eps_comment, target_eps, eps_data]
        result["eps"] = eps_info
    # 股息政策分析
    if 13 in useful_items:
        stock_strategy_list = []
        stock_list = []
        for item in data:
            if item[1] is not None and item[1][13][1] is not None:
                stock_strategy_list.append(item[1][13][1])
                stock_list.append(item[0])
        mean = sum(stock_strategy_list)/len(stock_strategy_list)
        target_stock_strategy = data[index][1][13][1]
        # Filter
        stock_strategy_comment = ""
        if target_stock_strategy > mean:
            stock_strategy_comment += f"該公司的持續發股時間為{round(target_stock_strategy, 2)}年 高於同業水平的{round(mean, 2)}年"
        else:
            stock_strategy_comment += f"該公司的持續發股時間為{round(target_stock_strategy, 2)}年 低於同業水平的{round(mean, 2)}年"

        # Ranking
        combined_list = list(zip(stock_list, stock_strategy_list))
        sorted_combined_list = sorted(combined_list, key=lambda item: item[1],reverse=True)
        if any(stock_code in sublist for sublist in sorted_combined_list):
            rank = next(i for i, v in enumerate(sorted_combined_list) if v[0] == stock_code) + 1
            percentage = (rank / len(sorted_combined_list)) * 100
        stock_strategy_rank_list = [[item[0], item[1]] for item in sorted_combined_list]
        stock_strategy_info = [stock_strategy_comment, [rank, round(percentage,2), stock_strategy_rank_list]]
        result["stock strategy"] = stock_strategy_info
    return result
