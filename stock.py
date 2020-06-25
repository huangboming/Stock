from pandas.plotting import register_matplotlib_converters
import datetime, re, sys
import yfinance as yf
import pandas as pd
from matplotlib import pyplot as plt

def user_input():
    """
    功能：让用户按照格式输入起始日期和截止日期，且保证截止日期不得超过起始日期和使用当天的日期
    
    参数：无
    
    返回值：input_date: 数据类型——列表；包含六个数字，第一个数字到最后一个数字分别代表起始年月日，截止年月日
           如果用户输入quit，返回值为None
    """
    
    while True: 
        print("请输入起始日期，以year-mouth-day输入，如2020-06-01；输入quit退出程序")
        start = input()
        if start == 'quit':
            break
        print("请输入截止日期，以year-mouth-day输入，如2020-06-02；输入quit退出程序")
        end = input()
        if end == 'quit':
            break
        pttn = '\d\d\d\d-\d\d-\d\d|\d\d\d\d-\d\d-\d|\d\d\d\d-\d-\d\d|\d\d\d\d-\d-\d' ##利用正则表达式检测用户是否按照格式输入
    
        start_list = [int(i) for i in start.split('-')]
        end_list = [int(i) for i in end.split('-')]
    
        if re.findall(pttn, start) and re.findall(pttn, end): ## 用户按照格式输入日期
        
            start_year, start_mouth, start_day = start_list
            end_year, end_mouth, end_day = end_list
            
            start_day = datetime.date(start_year, start_mouth, start_day)
            end_day = datetime.date(end_year, end_mouth, end_day)
            
            if start_day > datetime.date.today() or start_day > end_day or end_day > datetime.date.today():
                print("输入日期不符合要求")
            else:
                input_date = start_list + end_list    
                return input_date                   
        else:
            print("请按照格式输入")

def get_data(input_date, tickers):
    
    """
    功能：利用yfinance从yahoo finance上抓取数据
    
    参数：input_date: 数据类型——列表或元组；包含六个数字，第一个数字到最后一个数字分别代表起始年月日，截止年月日
    
         tickers: 数据类型——字符串；包含用空格分隔的股票英文代码
         
    返回值：data: 数据类型——Pandas DataFrame；储存股票数据（包括开盘价，收盘价，当天最低价，最高价，交易量等等）
    """
    
    start_year, start_month, start_day, end_year, end_month, end_day = input_date
    print("正在下载数据，请稍后...")
    data = yf.download(tickers, start = f'{start_year}-{start_month}-{start_day}', end = f'{end_year}-{end_month}-{end_day}')
    return data

def plot_single_line_chart(input_date, tickers, data): 
    
    """
    功能：利用pyplot将输入的数据绘制成图，一支股票一张图
    
    参数：input_date: 数据类型——列表或元组；包含六个数字，第一个数字到最后一个数字分别代表起始年月日，截止年月日。
    
         tickers: 数据类型——字符串；包含用空格分隔的股票英文代码
         
         data: 数据类型——Pandas DataFrame；储存股票数据（包括开盘价，收盘价，当天最低价，最高价，交易量等等）
         
    返回值：None
    """
    
    start_year, start_month, start_day, end_year, end_month, end_day = input_date
    tickers_list = tickers.split()
    
    if len(tickers_list) == 1:
        register_matplotlib_converters()
        plt.figure(figsize = (20, 10))
        plt.title(f"Close Price of {tickers_list[0].upper()} ---- from {start_year}-{start_month}-{start_day} to {end_year}-{end_month}-{end_day}")
        plt.ylabel("Price/$")
        ## 插入最大值所在坐标
        ticker_max = data["Close"][data["Close"] == data["Close"].max()] 
        xmax = str(ticker_max.index[0])
        ymax = ticker_max[0]
        pttn = '\d\d\d\d-\d\d-\d\d'
        plt.annotate(s = f"{tickers_list[0].upper()}'s max close price = {ymax}, at {''.join(re.findall(pttn,xmax))}", xy = (xmax, ymax))
        ## 插入最小值所在坐标
        ticker_min = data["Close"][data["Close"] == data["Close"].min()]
        xmin = str(ticker_min.index[0])
        ymin = ticker_min[0]
        plt.annotate(s = f"{tickers_list[0].upper()}'s min close price = {ymin}, at {''.join(re.findall(pttn,xmin))}", xy = (xmin, ymin))
        
        plt.plot(data.Close, 'b')
        plt.show()
    else:   
        for item in tickers_list:
            register_matplotlib_converters()
            plt.figure(figsize = (20, 10))
            plt.title(f"Close Price of {item.upper()} ---- from {start_year}-{start_month}-{start_day} to {end_year}-{end_month}-{end_day}")
            plt.ylabel("Price/$")
            ## 插入最大值所在坐标
            item_max = data["Close"][f"{item.upper()}"][data["Close"][f"{item.upper()}"] == data["Close"][f"{item.upper()}"].max()]
            xmax = str(item_max.index[0])
            ymax = item_max[0]
            pttn = '\d\d\d\d-\d\d-\d\d'
            plt.annotate(s = f"{item.upper()}'s max close price = {ymax}, on {''.join(re.findall(pttn,xmax))}", xy = (xmax, ymax))
            ## 插入最小值所在坐标
            item_min = data["Close"][f"{item.upper()}"][data["Close"][f"{item.upper()}"] == data["Close"][f"{item.upper()}"].min()]
            xmin = str(item_min.index[0])
            ymin = item_min[0]
            plt.annotate(s = f"{item.upper()}'s min close price = {ymin}, on {''.join(re.findall(pttn,xmin))}", xy = (xmin, ymin))
            
            plt.plot(data.Close[item.upper()], 'b')
            plt.show()
            
def plot_all_line_chart(input_date, tickers, data):
    
    """
    功能：利用pyplot将输入的数据绘制成图，所有的股票汇集在一张图中
    
    参数：input_date: 数据类型——列表或元组；包含六个数字，第一个数字到最后一个数字分别代表起始年月日，截止年月日。
    
         tickers: 数据类型——字符串；包含用空格分隔的股票英文代码
         
         data: 数据类型——Pandas DataFrame；储存股票数据（包括开盘价，收盘价，当天最低价，最高价，交易量等等）
         
    返回值：None
    """
    
    tickers_list = tickers.split()
    start_year, start_month, start_day, end_year, end_month, end_day = input_date
    
    if len(tickers_list) == 1:
        plot_single_line_chart(input_date, tickers, data)
        
    else:
        register_matplotlib_converters()
        plt.figure(figsize = (20, 10))
        plt.title(f"Close Price of {tickers.upper()} ---- from {start_year}-{start_month}-{start_day} to {end_year}-{end_month}-{end_day}")
        plt.ylabel("Price/$")
        for item in tickers_list:
            ## 插入最大值所在坐标
            item_max = data["Close"][f"{item.upper()}"][data["Close"][f"{item.upper()}"] == data["Close"][f"{item.upper()}"].max()]
            xmax = str(item_max.index[0])
            ymax = item_max[0]
            pttn = '\d\d\d\d-\d\d-\d\d'
            plt.annotate(s = f"{item.upper()}'s max close price = {ymax}, at {''.join(re.findall(pttn,xmax))}", xy = (xmax, ymax))
            ## 插入最小值所在坐标
            item_min = data["Close"][f"{item.upper()}"][data["Close"][f"{item.upper()}"] == data["Close"][f"{item.upper()}"].min()]
            xmin = str(item_min.index[0])
            ymin = item_min[0]
            plt.annotate(s = f"{item.upper()}'s min close price = {ymin}, on {''.join(re.findall(pttn,xmin))}", xy = (xmin, ymin))
        
        plt.plot(data.Close)
        plt.show()

def to_excel_or_csv_file(data): 
    
    """
    功能：将所有数据写入excel或者csv文件，名称及格式由用户自行决定
    
    参数：data: 数据类型——Pandas DataFrame；储存股票数据（包括开盘价，收盘价，当天最低价，最高价，交易量等等）
    
    输出：无
    """
    
    while True:
        print("请输入输出格式，excel或者csv")
        file_format = input()
        print("请输入文件名称，不需要添加后缀")
        name = input()
        if file_format.lower() == 'excel':
            data.to_excel(f'{name}.xlsx')
            break
        elif file_format.lower() == 'csv':
            data.to_csv(f'{name}.csv')
            break
    
    
def main():
    
    print("请输入股票代码，如果有多个代码，请用空格隔开；输入quit退出程序")
    tickers = input()
    if tickers.lower() == 'quit':
        sys.exit()
    input_date = user_input()
    tickers_list = tickers.split()
    
    if input_date: 
        data = get_data(input_date, tickers)
    else:
        print("你已退出程序")
        sys.exit()
        
    while True:
        print("请输入输出模式，l表示折线图（每只股票一张图），al表示折线图（所有的股票在一张图内）")
        command = input()
        if command.lower() == "l":
            plot_single_line_chart(input_date, tickers, data)
        elif command.lower() == "al":
            plot_all_line_chart(input_date, tickers, data)
                
        print("需要重复上一个操作吗？(yes or no)")
        answer = input()
        if(answer.startswith('n')):
            break
            
    while True:
        print("需要将数据储存在excel或者csv文件中吗？(yes 或 no)")
        answer = input()
        if answer.startswith("y"):
            to_excel_or_csv_file(data)
        else:
            break
            
if __name__ == '__main__':
    main()