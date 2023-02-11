from math import nan
import streamlit as st
from PIL import Image
import pandas as pd
import numpy as np
import requests

import yfinance as yf

def RCI(x):
    n = len(x)
    d = ((np.arange(1,n+1)-np.array(pd.Series(x).rank()))**2).sum()
    rci = 1-6*d/(n*(n**2-1))
    return rci*100
days = 5
# st.set_page_config(layout="wide")
 
# st.title('銘柄スキャン')
# days = st.selectbox(
#     '何日間の取引を想定していますか？',
#     (5,1,3,10))


chance1_all = []
percent_list = []
win = []
win_price = []

chance2_all = []
percent_list2 = []
win2 = []
win_price2 = []

chance3_all = []
percent_list3 = []
win3 = []
win_price3 = []
day3 = []

chance4_all = []
percent_list4 = []
win4 = []
win_price4 = []
day4 = []

chance5_all = []
percent_list5 = []
win5 = []
win_price5 = []
day5 = []

chance6_all = []
percent_list6 = []
win6 = []
win_price6 = []
day6 = []

chance7_all = []
percent_list7 = []
win7 = []
win_price7 = []
day7 = []

chance8_all = []
percent_list8 = []
win8 = []
win_price8 = []
day8 = []

chance9_all = []
percent_list9 = []
win9 = []
win_price9 = []
day9 = []

all_profit = []
all_decrease_profit = []
all_count_1 = []
all_count_2 = []
all_count_3 = []
all_count_4 = []

#codes = ['5901','6810','6804','6779','6770','6754','6753','6752','6750','6724','6723','5727','5802','5805','5929','5943','6013','6055','6058','6062','6070','6101','6113','6141','6208','6250','6269','6287','6298','6338','6395','6407','6463','6513','6630','6641','6666','6871','6925','6937','6941','6952','6962','6995','6999','7202','7261','7270','7296','7313','7254','7414','7421','7453','7532','7545','7575','7606','7613','7616','7718','7730','7732','7731','7752','7760','7867','7906','7915','7965','7970','7981','7984','7994','8020','8086','8129','8130','8133','8174','8233','8253','8282','8341','8411','8699','8795','8802','8804','8909','8920','8923','8929','8934','9005','9007','9076','9308','9401','9409','9503','9511','9513','9625','9692','9832','1712','1808','1826','1944','1969','2002','2154','2158','2160','2301','2309','2389','2395','2427','2432','2433','2438','2471','2503','2531','2579','2607','2613','2678','2681','2685','2730','2784','2792','2910','2929','3003','3048','3076','3086','3099','3105','3107','3161','3254','3319','3377','3405','3407','3433','3436','3591','3604','3632','3657','3661','3675','4028','4042','4045','4080','4095','4204','4331']
codes = ['1332','1605','1801','1808','1802','1803','1721','1812','1925','1963','1928','2801','2269','2802','2501','2282','2502','2503','2914','2002','2531','2871','3401','3402','3101','3861','3863','4063','4911','6988','4021','4452','4901','4004','4061','4042','4631','4183','4188','4208','3407','3405','4005','4043','4502','4578','4507','4519','4151','4503','4568','4523','5020','5108','5101','5201','5214','5232','5332','5301','5333','5233','5202','5541','5411','5401','5406','5801','5713','5711','5714','5803','5706','3436','5707','5802','5703','6273','7011','6367','5631','6361','6305','6326','7013','6301','6103','6113','6473','6471','7004','6472','6302','8035','6861','6857','7735','6954','6702','6758','6762','6981','6594','6976','6504','6645','6501','6902','6971','6506','6479','6503','6701','6674','7751','6770','6952','7752','6753','6724','6841','6752','7021','7003','7203','7202','7205','7261','7201','7211','7267','7270','7272','7269','7741','4543','7733','7731','4902','7762','7951','7832','7912','7911','8015','8001','8031','2768','8058','8053','8002','9983','3382','8267','3099','3086','8233','8252','8306','8316','8411','8331','8309','7186','8601']#'8604','8628','8795','8630','8750','8725','8766','8591','8697','8253','8801','8802','3289','8830','9022','9020','9005','9007','9001','9009','9008','9021','9147','9064','9107','9101','9104','9202','9301','9984','9432','9613','9433','9434','9503','9501','9502','9532','9531','9766','6098','3659','2413','4324','9602','2432','4751','4704','7974','4755','6178','4689','9735']

for code in codes:
    option = code
    ticker = str(option) + '.T'
    tkr = yf.Ticker(ticker)
    hist = tkr.history(period='5y')
    hist = hist.reset_index()
    hist = hist.set_index(['Date'])
    hist = hist.rename_axis('Date').reset_index()
    hist = hist.T
    a = hist.to_dict()

    for items in a.values():
            time = items['Date']
            items['Date'] = time.strftime("%Y/%m/%d")

    b = [x for x in a.values()]

    source = pd.DataFrame(b)
    
    price = source['Close']

    #DMIの計算
    high = source['High']
    low = source['Low']
    close = source['Close']
    pDM = (high - high.shift(1))
    mDM = (low.shift(1) - low)
    pDM.loc[pDM<0] = 0
    pDM.loc[pDM-mDM < 0] = 0
    mDM.loc[mDM<0] = 0
    mDM.loc[mDM-pDM < 0] = 0
    # trの計算
    a = (high - low).abs()
    b = (high - close.shift(1)).abs()
    c = (low - close.shift(1)).abs()
    tr = pd.concat([a, b, c], axis=1).max(axis=1)
    source['pDI'] = pDM.rolling(14).sum()/tr.rolling(14).sum() * 100
    source['mDI'] = mDM.rolling(14).sum()/tr.rolling(14).sum() * 100
    # ADXの計算
    DX = (source['pDI']-source['mDI']).abs()/(source['pDI']+source['mDI']) * 100
    DX = DX.fillna(0)
    source['ADX'] = DX.rolling(14).mean()

    #移動平均
    span01=5
    span02=25
    span03=50
    span04=20
    span05=75

    source['sma05'] = price.rolling(window=span01).mean()
    source['sma25'] = price.rolling(window=span02).mean()
    source['sma50'] = price.rolling(window=span03).mean()
    source['sma20'] = price.rolling(window=span04).mean()
    source['sma75'] = price.rolling(window=span05).mean()

    # 基準線
    high26 = source["High"].rolling(window=26).max()
    low26 = source["Low"].rolling(window=26).min()
    source["base_line"] = (high26 + low26) / 2
    
    # 転換線
    high9 = source["High"].rolling(window=9).max()
    low9 = source["Low"].rolling(window=9).min()
    source["conversion_line"] = (high9 + low9) / 2
    
    # 先行スパン1
    leading_span1 = (source["base_line"] + source["conversion_line"]) / 2
    source["leading_span1"] = leading_span1.shift(25)
    
    # 先行スパン2
    high52 = source["High"].rolling(window=52).max()
    low52 = source["Low"].rolling(window=52).min()
    leading_span2 = (high52 + low52) / 2
    source["leading_span2"] = leading_span2.shift(25)
    
    # 遅行スパン
    source["lagging_span"] = source["Close"].shift(-25)

    #RSI
    # 前日との差分を計算
    df_diff = source["Close"].diff(1)

    # 計算用のDataFrameを定義
    df_up, df_down = df_diff.copy(), df_diff.copy()

    # df_upはマイナス値を0に変換
    # df_downはプラス値を0に変換して正負反転
    df_up[df_up < 0] = 0
    df_down[df_down > 0] = 0
    df_down = df_down * -1

    
    # 期間14でそれぞれの平均を算出
    df_up_sma14 = df_up.rolling(window=14, center=False).mean()
    df_down_sma14 = df_down.rolling(window=14, center=False).mean()
    
    

    # RSIを算出
    source["RSI"] = 100.0 * (df_up_sma14 / (df_up_sma14 + df_down_sma14))

    #大循環macd
    exp5 = source['Close'].ewm(span=5, adjust=False).mean()
    exp20 = source['Close'].ewm(span=20, adjust=False).mean()
    source['MACD1'] = exp5 - exp20


    exp40 = source['Close'].ewm(span=40, adjust=False).mean()
    source['MACD2'] = exp5 - exp40

    source['MACD3'] = exp20 - exp40

    KDAY = 26  # K算定用期間
    MDAY = 3  # D算定用期間

    # stochasticks K
    source["sct_k_price"] = (
        100*
        (source["Close"] - source["Low"].rolling(window=KDAY, min_periods=KDAY).min())/
        (source["High"].rolling(window=KDAY, min_periods=KDAY).max() - source["Low"].rolling(window=KDAY, min_periods=KDAY).min())
    )

    # stochasticks D
    source["sct_d_price"] = (
        100*
        (source["Close"] - source["Low"].rolling(window=KDAY, min_periods=KDAY).min())
        .rolling(window=MDAY, min_periods=MDAY).sum()/
        (source["High"].rolling(window=KDAY, min_periods=KDAY).max() - source["Low"].rolling(window=KDAY, min_periods=KDAY).min())
        .rolling(window=MDAY, min_periods=MDAY).sum()
    )

    # slow stochasticks
    source["slow_sct_d_price"] = source["sct_d_price"].rolling(window=MDAY, min_periods=MDAY).mean()

    #GMMA
    exp3 = source['Close'].ewm(span=3, adjust=False).mean()
    exp8 = source['Close'].ewm(span=8, adjust=False).mean()
    exp10 = source['Close'].ewm(span=10, adjust=False).mean()
    exp12 = source['Close'].ewm(span=12, adjust=False).mean()
    exp15 = source['Close'].ewm(span=15, adjust=False).mean()
    source['EMA3'] = exp3
    source['EMA5'] = exp5
    source['EMA8'] = exp8
    source['EMA10'] = exp10
    source['EMA12'] = exp12
    source['EMA15'] = exp15


    exp20 = source['Close'].ewm(span=20, adjust=False).mean()
    exp30 = source['Close'].ewm(span=30, adjust=False).mean()
    exp35 = source['Close'].ewm(span=35, adjust=False).mean()
    exp40 = source['Close'].ewm(span=40, adjust=False).mean()
    exp45 = source['Close'].ewm(span=45, adjust=False).mean()
    exp50 = source['Close'].ewm(span=50, adjust=False).mean()
    exp60 = source['Close'].ewm(span=60, adjust=False).mean()
    source['EMA20'] = exp20
    source['EMA30'] = exp30
    source['EMA35'] = exp35
    source['EMA40'] = exp40
    source['EMA45'] = exp45
    source['EMA50'] = exp50
    source['EMA60'] = exp60

    #RCI
    source['RCI_short'] = source["Close"].rolling(9).apply(RCI)
    source['RCI_mid'] = source["Close"].rolling(14).apply(RCI)
    source['RCI_long'] = source["Close"].rolling(26).apply(RCI)

    #ボリンジャーバンド
    # 標準偏差
    source["std"] = source["Close"].rolling(window=20).std()
    
    # ボリンジャーバンド
    source["2upper"] = source["sma20"] + (2 * source["std"])
    source["2lower"] = source["sma20"] - (2 * source["std"])
    source["3upper"] = source["sma20"] + (3 * source["std"])
    source["3lower"] = source["sma20"] - (3 * source["std"])

#SMA(20日)を使用したボリンジャーバンド
    check7_all = []
    check7_up = []
    check7_down = []
    price_dif7 = []
    price7_win = []

    check8_all = []
    check8_up = []
    check8_down = []
    price_dif8 = []
    price8_win = []
    
    check9_all = []
    check9_up = []
    check9_down = []
    price_dif9 = []
    price9_win = []
    
#ボリンジャーバンドのグラフ表示
#     fig = make_subplots(rows = 2, cols = 1, shared_xaxes=False, subplot_titles=('ボリンジャーバンド'), vertical_spacing=0.1, row_width=[0.2, 0.7],)
#     fig.add_trace(go.Candlestick(x = source.index, open = source['Open'], high = source['High'], low = source['Low'], close = source['Close'], showlegend=False, name = 'candlestick'), row = 1, col = 1)
#     fig.add_trace(go.Scatter(x = source.index, y = source['sma20'], line_color = 'black', name = 'sma04'), row = 1, col = 1)
#     fig.add_trace(go.Scatter(x = source.index, y = source['sma20'] + (source['std'] * 2), line_color = 'gray', line = {'dash': 'dash'}, name = 'upper band', opacity = 0.5), row = 1, col = 1)
#     fig.add_trace(go.Scatter(x = source.index, y = source['sma20'] - (source['std'] * 2), line_color = 'gray', line = {'dash': 'dash'}, fill = 'tonexty', name = 'lower band', opacity = 0.5), row = 1, col = 1)
#     fig.add_trace(go.Scatter(x = source.index, y = source['RSI'], line_color = 'red', name = 'RSI'), row = 1, col = 1)
#     go.Figure(fig).show()
#     fig.update_layout(width = 900, height = 700)



    x, z= 0, 0
    width_array = []
    BBB_array = []
    BBB_direction = 0
    MB_direction = 0
    
    start = 60
    last = 600
    
    total_profit = 0
    total_decrease_profit = 0
    
    count_1, count_2, count_3, count_4 = 0, 0, 0, 0
    
    for i in range(start,last):
        price = source['Close'][i]
        price_high = source['High'][i]
        price_low = source['Low'][i]
        price_open = source['Open'][i]
        price_yesterday = source['Close'][i-1]
        price_direction = price - price_yesterday
        price_buy = source['Close'][i+1]
        price_days = source['Close'][i+days+1]
        price_days_before1 = source['Low'][i+days]
        price_days_before2 = source['Low'][i+days-1]
        price_days_before3 = source['Low'][i+days-2]
        price_days_before4 = source['Low'][i+days-3]
        price_high_before1 = source['High'][i+days]
        price_high_before2 = source['High'][i+days-1]
        price_high_before3 = source['High'][i+days-2]
        price_high_before4 = source['High'][i+days-3]
        price_buy_percent3 = source['Close'][i+1] * 0.03 * -1
        price_99 = source['Close'][i+1] * 0.97
        price_103 = source['Close'][i+1] * 1.03
        price_change = price_days - price_buy
        ema3 = source['EMA3'][i]
        ema5 = source['EMA5'][i]
        ema8 = source['EMA8'][i]
        ema12 = source['EMA12'][i]
        ema15 = source['EMA15'][i]
        ema20 = source['EMA20'][i]
        ema30 = source['EMA30'][i]
        ema35 = source['EMA35'][i]
        ema40 = source['EMA40'][i]
        ema40_yesterday = source['EMA40'][i-1]
        ema45 = source['EMA45'][i]
        ema50 = source['EMA50'][i]
        ema60 = source['EMA60'][i]
        ema10 = source['EMA10'][i]
        ema15_yesterday = source['EMA15'][i-1]
        width1 = ema3 - ema15
        width2 = ema30 - ema60
        width2_yesterday = source['EMA30'][i-1] - source['EMA60'][i-1]
        ema5_direction = source['EMA5'][i] - source['EMA5'][i-1]
        ema20_direction = source['EMA20'][i] - source['EMA20'][i-1]
        ema40_direction = source['EMA40'][i] - source['EMA40'][i-1]
        ema3_direction_yesterday = source['EMA3'][i-1] - source['EMA3'][i-2]
        slow_percentd = source['slow_sct_d_price'][i]
        percentk = source['sct_k_price'][i]
        ema30_direction = ema30 - source['EMA30'][i-1]
        ema20 = source['EMA20'][i]
        ema20_yesterday = source['EMA20'][i-1]
        obi1 = ema20 - ema40
        obi2 = source['EMA20'][i-3] - source['EMA40'][i-3]
        adx_direction = source['ADX'][i] - source['ADX'][i-1]
        percentk = source['sct_k_price'][i]
        percentk_direction = source['sct_k_price'][i] - source['sct_k_price'][i-1]
        slow_percentd = source['slow_sct_d_price'][i]
        slow_percentd_yesterday = source['slow_sct_d_price'][i-1]

        sma20 = source['sma20'][i]
        std20 = source['std'][i]
        upper_2 = source['2upper'][i]
        lower_2 = source['2lower'][i]
        upper_3 = source['3upper'][i]
        lower_3 = source['3lower'][i]
        rsi = source['RSI'][i]
        
        tomorrow_price = source['Close'][i+1]
        tomorrow_sma20 = source['sma20'][i+1]
        tomorrow_upper_2 = source['2upper'][i+1]
        tomorrow_lower_2 = source['2lower'][i+1]
        tomorrow_rsi = source['RSI'][i+1]
        
        dat_price = source['Close'][i+2]
        dat_sma20 = source['sma20'][i+2]
        dat_upper_2 = source['2upper'][i+2]
        dat_lower_2 = source['2lower'][i+2]
        dat_rsi = source['RSI'][i+2]
        
        d3l_price = source['Close'][i+3]
        d3l_sma20 = source['sma20'][i+3]
        d3l_upper_2 = source['2upper'][i+3]
        d3l_lower_2 = source['2lower'][i+3]
        d3l_rsi = source['RSI'][i+3]
        
        buy = 0
        decrease_buy = 0
        profit = 0
        decrease_profit = 0
       
        band_width = (upper_2 - lower_2)/sma20
        BB_B = (price-lower_2) / (upper_2-lower_2)
        
        tomorrow_band_width = (tomorrow_upper_2 - tomorrow_lower_2)/tomorrow_sma20
        tomorrow_BB_B = (tomorrow_price-tomorrow_lower_2)/(tomorrow_upper_2-tomorrow_lower_2)
        
        dat_band_width = (dat_upper_2-dat_lower_2)/dat_sma20
        dat_BB_B = (dat_price - dat_lower_2)/(dat_upper_2 - dat_lower_2)
        
        d3l_band_width = (d3l_upper_2-d3l_lower_2)/d3l_sma20
        d3l_BB_B = (d3l_price - d3l_lower_2)/(d3l_upper_2 - d3l_lower_2)
         
        width_array.append(band_width)
        BBB_array.append(BB_B)
        
        if i>start+3:
            MB_direction = (source['sma20'][i]-source['sma20'][i-1])# - (source['sma20'][i-2] + source[i-3])
            tomorrow_MB_direction = (source['sma20'][i+1] - source['sma20'][i])# - (source['sma20'][i-1] + source[i-2])
            dat_MB_direction = (source['sma20'][i+2] - source['sma20'][i])# - (source['sma20'][i] + source[i-1])
            d3l_MB_direction = (source['sma20'][i+3] - source['sma20'][i])
        z = z+1
        
        if z>130:#過去半年と比較するため、エラー回避のためにz>130とする
            min_band = min(width_array[z-130:])
            
            if min_band == band_width and rsi<58 and rsi>43 :#過去半年で今日が最小のバンド幅の時に注目
                #print('{}が半年で最小バンド幅'.format(source['Date'][i]))
                #print('i:'+str(i))
                
                if tomorrow_BB_B > 1.2 and tomorrow_MB_direction > 0 and tomorrow_band_width > (1.3*band_width) and 65>tomorrow_rsi>55:#注目した翌日に2σ以上になれば上昇トレンド発生と判断
                    #print('翌日上昇トレンド発生')
                    buy = source['Close'][i+1]#翌日発生したのでその一日後の終値で購入
                    count_1 = count_1 + 1
                    #print('購入額：'+str(buy))
                
                elif tomorrow_BB_B < -0.2 and tomorrow_MB_direction < 0 and tomorrow_band_width > (1.3*band_width) and 35<tomorrow_rsi<45:#注目した翌日に-2σを下回ったら下降トレンド発生と判断
                    #print('翌日下降トレンド発生')
                    decrease_buy = source['Close'][i+1]
                    count_3 = count_3 + 1
                    #print('購入額：'+str(decrease_buy))
                
                elif dat_BB_B > 1.2 and dat_MB_direction > 0 and dat_band_width > (1.3*band_width) and 65>dat_rsi>55:#2日後も同様
                    #print('2日後に上昇トレンド発生')
                    buy = source['Close'][i+2]#2日後にトレンド発生したのでその翌日の終値で購入
                    count_1 = count_1 + 1
                    #print('購入額：'+str(buy))
                           
                elif dat_BB_B < -0.2 and dat_MB_direction < 0 and dat_band_width > (1.3*band_width) and 35<dat_rsi<45:#2日後も同様
                    #print('2日後に下降トレンド発生')
                    decrease_buy = source['Close'][i+2]
                    count_3 = count_3 + 1
                    #print('購入額：'+str(decrease_buy))
                    
                elif d3l_BB_B > 1.2 and d3l_MB_direction > 0 and d3l_band_width > (1.3*band_width) and d3l_rsi>55:#2日後も同様
                    #print('2日後に上昇トレンド発生')
                    buy = source['Close'][i+3]#2日後にトレンド発生したのでその翌日の終値で購入
                    count_1 = count_1 + 1
                    #print('購入額：'+str(buy))
                           
                elif d3l_BB_B < -0.2 and d3l_MB_direction < 0 and d3l_band_width > (1.3*band_width) and d3l_rsi<45:#2日後も同様
                    #print('2日後に下降トレンド発生')
                    decrease_buy = source['Close'][i+3]
                    count_3 = count_3 + 1
                    #print('購入額：'+str(decrease_buy))
                           
                if buy != 0:
                    for n in range(i+4, last-1):#購入はi+2 or i+3であり、注目した翌日(i+1)に上昇トレンドが発生したときはi+2の終値で購入、i+3の終値からMBを下回る可能性があるからnはi+3から
                        #print('n:'+str(n))
                        MB = source['sma20'][n]
                        close = source['Close'][n]
                        
                        if close < MB:
                            sell = source['Close'][n]#MBを下回った翌日の終値で売却
                            #print('売却額：'+str(sell))
                            profit = 100*(sell - buy)
                            
                            if profit > 0:
                                count_2 = count_2 +1
                            break
                        
                        elif close < (0.95*buy):
                            sell = source['Close'][n]
                            profit = 100*(sell - buy)
                            break
                            
                        elif close == source['Close'][last]:
                            #print('現在もトレンド継続中')
                            break
                            
                elif decrease_buy != 0:
                    for n in range(i+4, last-1):
                        #print('n:'+str(n))
                        MB = source['sma20'][n]
                        close = source['Close'][n]
                        
                        if close > MB:
                            decrease_sell = source['Close'][n]
                            #print('売却額：'+str(decrease_sell))
                            decrease_profit = 100*(decrease_buy - decrease_sell)
                            #print('下降トレンドでの儲け：'+str(decrease_profit))
                            
                            if decrease_profit > 0:
                                count_4 = count_4 +1   
                            break
                            
                        elif close > (1.05*decrease_buy):
                            decrease_sell = source['Close'][n]
                            decrease_profit = 100*(decrease_buy - decrease_sell)
                            break
                            
                        elif close == source['Close'][last]:
                            #print('現在も下降トレンド発生中')
                            break
                if profit != 0 or decrease_profit != 0:
                    total_profit = total_profit + profit
                    total_decrease_profit = total_decrease_profit + decrease_profit
                    

    all_profit.append(total_profit)
    all_decrease_profit.append(total_decrease_profit)
    all_count_1.append(count_1)
    all_count_2.append(count_2)
    all_count_3.append(count_3)
    all_count_4.append(count_4)
    
    # print(all_profit)
    # print(all_decrease_profit)
    
sum_profit = sum(all_profit)
sum_decrease_profit = sum(all_decrease_profit)
sum_count_1 = sum(all_count_1)
sum_count_2 = sum(all_count_2)
sum_count_3 = sum(all_count_3)
sum_count_4 = sum(all_count_4)

percent_up = sum_count_2 / sum_count_1
percent_down = sum_count_4 / sum_count_3


st.write('上昇トレンドでの儲けは'+str(sum_profit))
st.write('下降トレンドでの儲けは'+str(sum_decrease_profit))
st.write('上昇トレンド発生回数：'+str(sum_count_1))
st.write('下降トレンド発生回数：'+str(sum_count_3))
st.write('勝率（上昇）：'+str(percent_up*100))
st.write('勝率（下降）：'+str(percent_down*100))
                
                        
                            
                            
                        
                        
                           
                           
                           
                           
          
    
# # #上昇に転換すると予想できる逆張り
#         if ema20<lower_2 and rsi_today<30 and BBB_direction>0 and source['Volume'][i-1]>(2.2*aource['Volume'][i-2]) and width_10ave>(2*width_5ave) and band_width >(1.7*width_5ave) and source['sma05']>source['sma25']:
#               print(code,source['Date'][i])
            
#         if price_days_before1>price_99 and price_days_before2>price_99 and price_days_before3>price_99 and price_days_before4>price_99  and price_days>price_buy:
#             check7_up.append(i)
                
#             price7_win.append(price_change)    
#         else:
#             check7_down.append(i)
#             price7_win.append(price_buy_percent3)
            
# # #下降に転換すると予想できる逆張り
#         if sma20>=upper_2 and rsi_today>70 and BBB_direction<0  :
#             print(code,source['Date'][i])
            
#         if price_high_before1<price_103 and price_high_before2<price_103 and price_high_before3<price_103 and price_high_before4<price_103  and price_days<price_buy:
#             check8_up.append(i)
                
#             price8_win.append(abs(price_change))    
#         else:
#             check8_down.append(i)
#             price8_win.append(price_buy_percent3)

# #均衡が崩れて上昇トレンドが発生するとき
#         if z<10:
#             width_5ave, width_10ave = 150, 150
#         else:
#             width_5ave = (width_array[z-1]+width_array[z-2]+width_array[z-3]+width_array[z-4]+width_array[z-5])/5
#             width_10ave = (width_array[z-1]+width_array[z-2]+width_array[z-3]+width_array[z-4]+width_array[z-5]+width_array[z-6]+width_array[z-7]+width_array[z-8]+width_array[z-9]+width_array[z-10])/10
          
#         if width_5ave<100 and width_10ave<130 and BB_B>1 and band_width>150 and BBB_direction>0 and price_direction>0 and source['Volume'][]:
#             print(code,source['Date'][i])
            
#             if price_days_before1>price_99 and price_days_before2>price_99 and price_days_before3>price_99 and price_days_before4>price_99  and price_days>price_buy:
#                 check9_up.append(i)
                
#                 price9_win.append(price_change)    
#             else:
#                 check9_down.append(i)
#                 price9_win.append(price_buy_percent3)
            
#     chance7 = len(check7_up) + len(check7_down)
#     chance7_all.append(chance7)
    
#     win7.append(len(check7_up))
#     win_price7.append(sum(price7_win))
    
#     chance8 = len(check8_up) + len(check8_down)
#     chance8_all.append(chance8)
    
#     win8.append(len(check8_up))
#     win_price8.append(sum(price8_win))
    
#     chance9 = len(check9_up) + len(check9_down)
#     chance9_all.append(chance9)
    
#     win9.append(len(check9_up))
#     win_price9.append(sum(price9_win))
#     # print(width_array)
#     #print(BBB_array)
#     # print(source['RSI'])











# #     #移動平均線大循環分析
#     exp20 = source['Close'].ewm(span=20, adjust=False).mean()
#     source['EMA20'] = exp20
#     source["sct_k_price2"] = (
#     100*
#     (source["Close"] - source["Low"].rolling(window=120, min_periods=120).min())/
#     (source["High"].rolling(window=120, min_periods=120).max() - source["Low"].rolling(window=120, min_periods=120).min())
# )

  





# #     check6_all = []
# #     check6_up = []
# #     check6_down = []
# #     price_dif6 = []
# #     price6_win = []

    
# # #     #移動平均線大循環分析
# #     for i in range(60,700):
# #         price = source['Close'][i]
# #         price_high = source['High'][i]
# #         price_low = source['Low'][i]
# #         price_yesterday = source['Close'][i-1]
# #         price_buy = source['Close'][i+1]
# #         price_days = source['Close'][i+days+1]
# #         price_days_before1 = source['Low'][i+days]
# #         price_days_before2 = source['Low'][i+days-1]
# #         price_days_before3 = source['Low'][i+days-2]
# #         price_days_before4 = source['Low'][i+days-3]
# #         price_buy_percent3 = source['Close'][i+1] * 0.03 * -1
# #         price_99 = source['Close'][i+1] * 0.95
# #         price_change = price_days - price_buy
# #         ema3 = source['EMA3'][i]
# #         ema5 = source['EMA5'][i]
# #         ema8 = source['EMA8'][i]
# #         ema12 = source['EMA12'][i]
# #         ema15 = source['EMA15'][i]
# #         ema30 = source['EMA30'][i]
# #         ema35 = source['EMA35'][i]
# #         ema40 = source['EMA40'][i]
# #         ema40_yesterday = source['EMA40'][i-1]
# #         ema45 = source['EMA45'][i]
# #         ema50 = source['EMA50'][i]
# #         ema60 = source['EMA60'][i]
# #         ema10 = source['EMA10'][i]
# #         ema15_yesterday = source['EMA15'][i-1]
# #         width1 = ema3 - ema15
# #         width2 = ema30 - ema60
# #         width2_yesterday = source['EMA30'][i-1] - source['EMA60'][i-1]
# #         ema5_direction = source['EMA5'][i] - source['EMA5'][i-1]
# #         ema20_direction = source['EMA20'][i] - source['EMA20'][i-1]
# #         ema40_direction = source['EMA40'][i] - source['EMA40'][i-1]
# #         ema3_direction_yesterday = source['EMA3'][i-1] - source['EMA3'][i-2]
# #         slow_percentd = source['slow_sct_d_price'][i]
# #         percentk = source['sct_k_price'][i]
# #         ema30_direction = ema30 - source['EMA30'][i-1]
# #         ema20 = source['EMA20'][i]
# #         ema20_yesterday = source['EMA20'][i-1]
# #         obi1 = ema20 - ema40
# #         obi2 = source['EMA20'][i-3] - source['EMA40'][i-3]
# #         adx_direction = source['ADX'][i] - source['ADX'][i-1]
# #         percentk = source['sct_k_price'][i]
# #         percentk_direction = source['sct_k_price'][i] - source['sct_k_price'][i-1]
# #         slow_percentd = source['slow_sct_d_price'][i]
# #         slow_percentd_yesterday = source['slow_sct_d_price'][i-1]


# #         if ema5>ema20>ema40 and ema5_direction>0 and ema20_direction>0 and ema40_direction>0 and obi1>obi2>5 and price_low<ema20<price_high and adx_direction>0 :
           
# #             print(code,source['Date'][i])
# #             if price_days_before1>price_99 and price_days_before2>price_99 and price_days_before3>price_99 and price_days_before4>price_99  and price_days>price_buy:
# #                 check6_up.append(i)
                
# #                 price6_win.append(price_change)    
# #             else:
# #                 check6_down.append(i)
# #                 price6_win.append(price_buy_percent3)
              
                


    
            
# #     chance6 = len(check6_up) + len(check6_down)
# #     chance6_all.append(chance6)
    
# #     win6.append(len(check6_up))
# #     win_price6.append(sum(price6_win))
        


# # win_probability6 = sum(win6) *100 / sum(chance6_all)
# # win6_1 = sum(win_price6) * 100
# # print('移動平均線大循環分析(押し目)')

# # print('勝率は:' + str(win_probability6))
# # print('起きた回数:' + str(sum(chance6_all)))
# # print('儲け:' + str(win6_1))

# win_probability7 = sum(win7) *100 / sum(chance7_all)
# win7_1 = sum(win_price7) * 100
# print('ボリンジャーバンド・RSI)上昇逆張り')

# print('勝率は:' + str(win_probability7))
# print('起きた回数:' + str(sum(chance7_all)))
# print('儲け:' + str(win7_1))
              
# win_probability8 = sum(win8) *100 / sum(chance8_all)
# win8_1 = sum(win_price8) * 100
# print('ボリンジャーバンド・RSI)下降逆張り')

# print('勝率は:' + str(win_probability8))
# print('起きた回数:' + str(sum(chance8_all)))
# print('儲け:' + str(win8_1))
# if sum(chance9_all) ==0:
#     win_probability9 =100
# else:
#     win_probability9 = sum(win9) *100 / sum(chance9_all)
    
# win9_1 = sum(win_price9) * 100
# print('ボリンジャーバンド順張り')

# print('勝率は:' + str(win_probability9))
# print('起きた回数:' + str(sum(chance9_all)))
# print('儲け:' + str(win9_1))
