from finance_data_utils.analyst import get_indicator_data, analyze_company_stocks

def main():
    stock = "2330"
    price, data = get_indicator_data(stock_code=stock)
    res = analyze_company_stocks(stock_code=stock, price=price, data=data)
    print(res)

if __name__ == "__main__":
    main()
