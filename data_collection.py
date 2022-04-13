"""
    需获取数据：
    1. 股票列表  --> stock_list
    2. 个股日线行情  --> pro_bar
    3. 三大报表数据  --> income_sheet, balance_sheet, cash_flow
    4. financial ratio数据 --> finance_ratio
"""
import pandas as pd

from MyPackages.Tushare.TusharePro import TushareData
from MyPackages.SQL.YZsql import MySQL

yzsql = MySQL()
td = TushareData()
# back test time period
start_date = '20141231'
end_date = '20211231'

failure_df = []


# get stock list from tushare
def get_stock_list():
    stock_list = td.stock_list()
    yzsql.save_data(df=stock_list, df_name='stock_list', method='replace')


# get stock list from sql
def get_stock_list_from_sql():
    return yzsql.get_data(sql='stock_list')


# get daily price
def daily_data(stock_list):
    for ts_code in stock_list['ts_code']:
        try:
            print(f'get daily bar of {ts_code} ...')
            daily_bar = td.daily_bar(ts_code=ts_code, start_date=start_date, end_date=end_date)
            yzsql.save_data(df=daily_bar, df_name='daily_bar', method='append')
        except:
            print('fail, continue to next item')
            failure_df.append(f'{ts_code} daily bar')
            continue


# get adj daily price
def daily_data_hfq(stock_list):
    for ts_code in stock_list['ts_code']:
        try:
            print(f'get hfq adj daily bar of {ts_code} ...')
            daily_bar = td.pro_bar(ts_code=ts_code, start_date=start_date, end_date=end_date)
            yzsql.save_data(df=daily_bar, df_name='daily_bar_hfq', method='append')
        except:
            print('fail, continue to next item')
            failure_df.append(f'{ts_code} hfq adj daily bar')
            continue


# get balance sheet
def balance_sheet(stock_list):
    for ts_code in stock_list['ts_code']:
        try:
            print(f'get balance_sheet of {ts_code} ...')
            balance_sheet = td.balance_sheet(ts_code=ts_code, start_date=start_date, end_date=end_date)
            yzsql.save_data(df=balance_sheet, df_name='balace_sheet', method='append')
        except:
            print('fail, continue to next item')
            failure_df.append(f'{ts_code} balance_sheet')
            continue


def income_sheet(stock_list):
    for ts_code in stock_list['ts_code']:
        try:
            print(f'get income_sheet of {ts_code} ...')
            income_sheet = td.income_sheet(ts_code=ts_code, start_date=start_date, end_date=end_date)
            yzsql.save_data(df=income_sheet, df_name='income_sheet', method='append')
        except:
            print('fail, continue to next item')
            failure_df.append(f'{ts_code} income_sheet')
            continue


def cash_flow(stock_list):
    for ts_code in stock_list['ts_code']:
        try:
            print(f'get cash_flow of {ts_code} ...')
            cash_flow = td.cash_flow(ts_code=ts_code, start_date=start_date, end_date=end_date)
            yzsql.save_data(df=cash_flow, df_name='cash_flow', method='append')
        except:
            print('fail, continue to next item')
            failure_df.append(f'{ts_code} cash_flow')
            continue


def financial_ratio(stock_list):
    for ts_code in stock_list['ts_code']:
        try:
            print(f'get financial_ratio of {ts_code} ...')
            financial_ratio = td.finance_ratio(ts_code=ts_code, start_date=start_date, end_date=end_date)
            yzsql.save_data(df=financial_ratio, df_name='cash_flow', method='append')
        except:
            print('fail, continue to next item')
            failure_df.append(f'{ts_code} financial_ratio')
            continue


def main():
    # get stock list
    try:
        stock_list = get_stock_list_from_sql()
    except:
        get_stock_list()
        stock_list = get_stock_list_from_sql()

    # get daily price
    daily_data(stock_list)

    # get balance sheet
    balance_sheet(stock_list)

    # get income sheet
    income_sheet(stock_list)

    # get cash flow
    cash_flow(stock_list)

    # get financial ratio
    financial_ratio(stock_list)

    # get hfq adj daily price
    daily_data_hfq(stock_list)


if __name__ == '__main__':
    main()

    failure_df = pd.DataFrame(failure_df)
    failure_df.to_csv('failure_1.csv')
