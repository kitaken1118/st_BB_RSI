import streamlit as st
import pandas as pd
import numpy as np
import requests
import re
import yfinance as yf

codes = []
st.title('テクニカル分析による注目銘柄表示')
options_1 = st.multiselect('検索する銘柄群を選択してください',
                        ['日経225','1~2Kで買える出来高が多い銘柄'])
st.write('You selected:', options_1)


if '日経225' in options_1:
  codes.append(['5901','6810','6804','6779','6770','6754','6753','6752','6750','6724','6723','5727','5802','5805','5929','5943','6013','6055','6058','6062','6070','6101','6113','6141','6208','6250','6269','6287','6298','6338','6395','6407','6463','6513','6630','6641','6666','6871','6925','6937','6941','6952','6962','6995','6999','7202','7261','7270','7296','7313','7254','7414','7421','7453','7532','7545','7575','7606','7613','7616','7718','7730','7732','7731','7752','7760','7867','7906','7915','7965','7970','7981','7984','7994','8020','8086','8129','8130','8133','8174','8233','8253','8282','8341','8411','8699','8795','8802','8804','8920','8923','8929','8934','9005','9007','9076','9308','9401','9409','9503','9511','9513','9625','9692','9832','1712','1808','1826','1944','1969','2002','2154','2158','2160','2301','2309','2389','2395','2427','2432','2433','2438','2471','2503','2531','2579','2607','2613','2678','2681','2685','2730','2784','2792','2910','2929','3003','3048','3076','3086','3099','3105','3107','3161','3254','3319','3377','3405','3407','3433','3436','3591','3604','3632','3657','3661','3675','4028','4042','4045','4080','4095','4204','4331'])
if '1~2Kで買える出来高が多い銘柄' in options_1:
  codes.append('1332','1605','1801', '1808','1802','1803','1721','1812','1925','1963','1928','2801','2269','2802','2501','2282','2502','2503','2914','2002','2531','2871','3401','3402','3101','3861','3863','4063','4911','6988','4021','4452','4901','4004','4061','4042','4631','4183','4188','4208','3407','3405','4005','4043','4502','4578','4507','4519','4151','4503','4568','4523','5020','5108','5101','5201','5214','5232','5332','5301','5333','5233','5202','5541','5411','5401','5406','5801','5713','5711','5714','5803','5706','3436','5707','5802','5703','6273','7011','6367','5631','6361','6305','6326','7013','6301','6103','6113','6473','6471','7004','6472','6302','8035','6861','6857','7735','6954','6702','6758','6762','6981','6594','6976','6504','6645','6501','6902','6971','6506','6479','6503','6701','6674','7751','6770','6952','7752','6753','6724','6841','6752','7021','7003','7203','7202','7205','7261','7201','7211','7267','7270','7272','7269','7741','4543','7733','7731','4902','7762','7951','7832','7912','7911','8015','8001','8031','2768','8058','8053','8002','9983','3382','8267','3099','3086','8233','8252','8306','8316','8411','8331','8309','7186','8604')

st.write(codes)
options_2 = st.multiselect('使用するテクニカル指標を選択してください',
                       ['陽線によるカウントアップ方式(日経225推奨)','ボリンジャーバンド','両方'])
st.write('You selected:', options_2)


if options_2 == '陽線によるカウントアップ方式(日経225推奨)':
  for code in codes:
    option = code
    ticker = str(option) + '.T'
    tkr = yf.Ticker(ticker)
    start_date = '2022-04-01' # 開始日
    source = yf.download(ticker, start=start_date, interval='1d')
    source2 = yf.download(ticker, start=start_date, interval='1wk')
    source3 = yf.download(ticker, start=start_date, interval='1mo')

    #移動平均
    span01=5
    span02=25
    span03=50
    span04=20
    span05=75

    source['sma05'] = source['Close'].rolling(window=span01).mean()
    source['sma25'] = source['Close'].rolling(window=span02).mean()
    source['sma50'] = source['Close'].rolling(window=span03).mean()
    source['sma20'] = source['Close'].rolling(window=span04).mean()
    source['sma75'] = source['Close'].rolling(window=span05).mean()

    source2['sma04'] = source2['Close'].rolling(window=4).mean()
    source2['sma08'] = source2['Close'].rolling(window=8).mean()
    source2['sma12'] = source2['Close'].rolling(window=12).mean()
