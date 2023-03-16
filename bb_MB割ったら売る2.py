import streamlit as st
import pandas as pd
import numpy as np
import requests
import re
import yfinance as yf

# st.set_page_config(layout="wide")
 
# st.title('銘柄スキャン')
# days = st.selectbox(
#     '何日間の取引を想定していますか？',
#     (5,1,3,10))



all_profit = []
all_count_buy = []
all_count_win = []

#古山選定株（1000円台で出来高が多い）
#codes = ['5901','6810','6804','6779','6770','6754','6753','6752','6750','6724','6723','5727','5802','5805','5929','5943','6013','6055','6058','6062','6070','6101','6113','6141','6208','6250','6269','6287','6298','6338','6395','6407','6463','6513','6630','6641','6666','6871','6925','6937','6941','6952','6962','6995','6999','7202','7261','7270','7296','7313','7254','7414','7421','7453','7532','7545','7575','7606','7613','7616','7718','7730','7732','7731','7752','7760','7867','7906','7915','7965','7970','7981','7984','7994','8020','8086','8129','8130','8133','8174','8233','8253','8282','8341','8411','8699','8795','8802','8804','8909','8920','8923','8929','8934','9005','9007','9076','9308','9401','9409','9503','9511','9513','9625','9692','9832','1712','1808','1826','1944','1969','2002','2154','2158','2160','2301','2309','2389','2395','2427','2432','2433','2438','2471','2503','2531','2579','2607','2613','2678','2681','2685','2730','2784','2792','2910','2929','3003','3048','3076','3086','3099','3105','3107','3161','3254','3319','3377','3405','3407','3433','3436','3591','3604','3632','3657','3661','3675','4028','4042','4045','4080','4095','4204','4331']
#日経平均の銘柄(過去5年でエラーになる銘柄は除く)
codes = ['1332','1605','1801']#,'1808','1802','1803','1721','1812','1925','1963','1928','2801','2269','2802','2501','2282','2502','2503','2914','2002','2531','2871','3401','3402','3101','3861','3863','4063','4911','6988','4021','4452','4901','4004','4061','4042','4631','4183','4188','4208','3407','3405','4005','4043','4502','4578','4507','4519','4151','4503','4568','4523','5020','5108','5101','5201','5214','5232','5332','5301','5333','5233','5202','5541','5411','5401','5406','5801','5713','5711','5714','5803','5706','3436','5707','5802','5703','6273','7011','6367','5631','6361','6305','6326','7013','6301','6103','6113','6473','6471','7004','6472','6302','8035','6861','6857','7735','6954','6702','6758','6762','6981','6594','6976','6504','6645','6501','6902','6971','6506','6479','6503','6701','6674','7751','6770','6952','7752','6753','6724','6841','6752','7021','7003','7203','7202','7205','7261','7201','7211','7267','7270','7272','7269','7741','4543','7733','7731','4902','7762','7951','7832','7912','7911','8015','8001','8031','2768','8058','8053','8002','9983','3382','8267','3099','3086','8233','8252','8306','8316','8411','8331','8309','7186','8601']#'8604','8628','8795','8630','8750','8725','8766','8591','8697','8253','8801','8802','3289','8830','9022','9020','9005','9007','9001','9009','9008','9021','9147','9064','9107','9101','9104','9202','9301','9984','9432','9613','9433','9434','9503','9501','9502','9532','9531','9766','6098','3659','2413','4324','9602','2432','4751','4704','7974','4755','6178','4689','9735']

for code in codes:
    option = code
    ticker = str(option) + '.T'
    tkr = yf.Ticker(ticker)
    hist = tkr.history(period='3y')
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

    #RSI
    # 前日との差分を計算
    df_diff = source["Close"].diff(1)

    # 計算用のDataFrameを定義
    df_up, df_down = df_diff.copy(), df_diff.copy()

    # df_upはマイナス値を0に変換
    # df_downはプラス値を0に変換して正負反転
    df_up[df_up < 0] = 0
    df_down[df_down > 0] = 0

    df_up_14 = df_up.rolling(window = 14, center = False).mean()
    df_down_14 = abs(df_down.rolling(window = 14, center = False).mean())
    
    # RSIを算出
    source["RSI"] = 100.0 * (df_up_14 / (df_up_14 + df_down_14))


    #ボリンジャーバンド
    # 標準偏差
    source["std"] = source["Close"].rolling(window=20).std()
    
    # ボリンジャーバンド
    source["2upper"] = source["sma20"] + (2 * source["std"])
    source["2lower"] = source["sma20"] - (2 * source["std"])
    source["3upper"] = source["sma20"] + (3 * source["std"])
    source["3lower"] = source["sma20"] - (3 * source["std"])

    count_up, count_down, count_buy, count_win = 0, 0, 0, 0
    profit = 0

    for i in source:
      price = source['Close'][i]
      tomorrow_price = source['Close'][i+1]
      open = source['Open'][i]
      volume = source['Volume'][i]
      sma05 = source['sma05'][i]
      sma25 = source['sma25'][i]
      sma75 = source['sma75'][i]
      rsi = source['RSI'][i]

     #sma25とsma75より終値が高いときカウントアップ
      if price>sma25 and price>sma75:

        count_up = count_up + 1
        count_down = 0
      
       #終値がsma5,25,75のいずれかより低いときはカウントダウン
      elif price<sma05 or price<sma25 or price<sma75:
        count_down = count_down + 1

        if count_down == 3:  #カウントダウンが3以上でカウントアップを初期化
          count_up = 0
       
       #半年間上昇トレンドが続き、rsiが65以下の時買いシグナル
      if count_up>=130 and rsi<=65:
        buy = tomorrow_price
        all_buy = all_buy + buy
        coount_buy = count_buy + 1

         #買いシグナル点灯後の売りタイミングを見つける
        if buy != 0:
          count_up = count_up - 20
          for n in range(i+1, i+100):
            close = source['Close'][n]
            tomorrow_close = source['Close'][n+1]
            sma05 = source['sma05'][n]
            sma25 = source['sma25'][n]
            sma75 = source['sma75'][n]
            rsi = source['RSI'][n]

             #買値の110%で利益確定
            if close>(1.1*buy):
              sell = tomorrow_close
              count_win = count_win + 1
              profit = profit + sell - buy
              break

             #終値がsma25,75を下回るか、rsiが70以上で売り
            if close<sma25 or close<sma75 or rsi>70:
              sell = tomorrow_close
              profit = profit + sell - buy
              if sell>buy:
                count_win = count_win + 1
              break
               
             #損切は5%  
            if close<(0.95*buy):
              sell = tomorrow_close
              profit = profit + sell - buy
              break

       





    all_profit.append(profit)
    all_count_buy.append(count_buy)
    all_count_win.append(count_win)
 
    print(all_profit)
    
                
                        
                            
                            
                        
                        
                           
                           
                           
                           
          
    
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
