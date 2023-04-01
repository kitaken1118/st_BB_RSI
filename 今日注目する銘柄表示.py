import streamlit as st
import pandas as pd
import numpy as np
import requests
import re
import yfinance as yf

st.title('テクニカル分析による注目銘柄表示')
option_1 = st.selectbox('検索する銘柄群を選択してください',
                        ('日経225','1~2Kで買える出来高が多い銘柄','両方'))
st.write('You selected: 'option_1')
