from optparse import Values
from turtle import title
from unicodedata import name
import streamlit as st
import mysql.connector
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import timedelta
import pickle

st.set_page_config(layout="wide")

crypto_names = {'BTC': 'Bitcoin', 
                'ETH': 'Ethereum', 
                'LTC': 'Litecoin', 
                }

#variaveis para armazenar previsao de 1 dia 
prev_btc = 0
prev_eth = 0
prev_ltc = 0


def select_model(cryptocurrency):
    """
    Carrega o modelo treinado de acordo com a escolha do usuario
    """
    global model
    if cryptocurrency == 'Bitcoin':
        model = pickle.load(open("models/btc_predictor.pkl", 'rb'))
    elif cryptocurrency == 'Ethereum':
        model = pickle.load(open("models/eth_predictor.pkl", 'rb'))
    else:
        model = pickle.load(open("models/ltc_predictor.pkl", 'rb'))
        

def init_connection():
    return mysql.connector.connect(**st.secrets["mysql"])



def run_query(db_name):

    query = "SELECT * FROM " + db_name
    with conn.cursor() as cur:
        cur.execute(query)
        data =  cur.fetchall()
        column_names = [column[0] for column in cur.description]
        db_data = []
        for record in data:
            db_data.append(dict(zip(column_names , record)))

        df = pd.DataFrame.from_dict(db_data)
        return df

# Criando dataframes das criptomoedas 
conn = init_connection()
btc_df = run_query("BTC")
eth_df = run_query("ETH")
ltc_df = run_query("LTC")

def create_phophet_dates(periods, crypto_df):
    """
    Cria um dataframe no formato que o Prophet usa com as datas
    """
    start_date = crypto_df['Date'].max() + timedelta(days=1)
    datelist = pd.date_range(start_date, periods=periods).tolist()

    return pd.DataFrame({'ds': datelist})

def predict_price(days, crypto_df):
    """
    Faz a previsao dos preços futuros
    """

    select_model(crypto)
    future_data = create_phophet_dates(days, crypto_df)
    predicted_values = model.predict(future_data)
    future_data['price'] = predicted_values['yhat']

    if crypto == 'Bitcoin':
        global prev_btc
        prev_btc = float(future_data.loc[0][['price']]) - float(crypto_df.iloc[-1][['Close']])
    if crypto == 'Ethereum':
        global prev_eth
        prev_eth = float(future_data.loc[0][['price']]) - float(crypto_df.iloc[-1][['Close']])
        print(prev_eth)
    if crypto == 'Litecoin':
        global prev_ltc
        prev_ltc = float(future_data.loc[0][['price']]) - float(crypto_df.iloc[-1][['Close']])
    return future_data


def plot_prediction(ndays, crypto_df):
    """
    Plota os dados historicos e ndays de previsão dos preços
    """
    prediction = predict_price(ndays,crypto_df)

    fig2 = go.Figure()
    fig2.add_trace(go.Scatter(x=crypto_df['Date'], y=crypto_df['Close'], mode='lines', line=dict(color='red'), name='Preço histórico'))
    fig2.add_trace(go.Scatter(x= prediction.ds, y=prediction.price, mode = 'lines', line=dict(color='green'), name='Preço previsto'))
    return fig2

st.title("Informações de criptomoedas")
st.sidebar.title("Escolha as informações desejadas")

crypto = st.sidebar.selectbox(
     'Criptomoeda:',
     crypto_names.values())

option = st.sidebar.selectbox(
     'Informação:',
     ('Preço Historico', 'Candlesticks', 'Previsão de preços'))



def select_criptp_df(cripto_option):
    """
    Retorna o dataframe da criptomoeda escolhida
    """

    if cripto_option == 'Bitcoin':
        return btc_df
    elif cripto_option == 'Ethereum':
        return eth_df
    else:
        return ltc_df


def select_plot(plot_type, crypto_df):
    """
    Função que plota o grafico de acordo com a escolha do usuario
    """

    if plot_type == 'Candlesticks':
        fig = go.Figure(data=[go.Candlestick(x=btc_df['Date'],
                open=crypto_df['Open'],
                high=crypto_df['High'],
                low=crypto_df['Low'],
                close=crypto_df['Close'])])

    elif plot_type == "Preço Historico":
        fig = px.line(crypto_df, x='Date', y='Close', title='Preço historico')

    elif plot_type == 'Previsão de preços':
        select_model(crypto)
        fig = plot_prediction(10, crypto_df)
    
    return fig


#Sugestão de comprar ou vender
previsao = st.text("")

show_fig = select_plot(option, select_criptp_df(crypto))
show_fig.update_layout(width=900, height=800, yaxis_title='Preço em USD', xaxis_title='Data')


#Checkboxes para plotar as medias junto com os preços
st.sidebar.text("Indicadores:")
sma14 = st.sidebar.checkbox("SMA 14")
sma21 = st.sidebar.checkbox("SMA 21")
sma55 = st.sidebar.checkbox("SMA 55")
sma100 = st.sidebar.checkbox("SMA 100")
if sma14:
    crypto_df = select_criptp_df(crypto)
    show_fig.add_trace(go.Scatter(x= crypto_df['Date'], y=crypto_df['Close'].rolling(14, min_periods=1).mean(), mode = 'lines', line=dict(color='yellow'), name='SMA 14'))
if sma21:
    crypto_df = select_criptp_df(crypto)
    show_fig.add_trace(go.Scatter(x= crypto_df['Date'], y=crypto_df['Close'].rolling(21, min_periods=1).mean(), mode = 'lines', line=dict(color='orange'), name='SMA 21'))
if sma55:
    crypto_df = select_criptp_df(crypto)
    show_fig.add_trace(go.Scatter(x= crypto_df['Date'], y=crypto_df['Close'].rolling(55, min_periods=1).mean(), mode = 'lines', line=dict(color='grey'), name='SMA 55'))
if sma100:
    crypto_df = select_criptp_df(crypto)
    show_fig.add_trace(go.Scatter(x= crypto_df['Date'], y=crypto_df['Close'].rolling(100, min_periods=1).mean(), mode = 'lines', line=dict(color='purple'), name='SMA 100'))

st.plotly_chart(show_fig)

if crypto == 'Bitcoin' and prev_btc != 0:
    if prev_btc > 0:
        previsao.text("Nossa sugestão é de comprar esta criptomoeda. De acordo com nossa previsao os preços vão subir")
    else:
        previsao.text("Nossa sugestão é de vender esta criptomoeda. De acordo com nossa previsao os preços vão cair")
        
if crypto == 'Ethereum' and prev_eth != 0:
    if prev_eth > 0:
        previsao.text("Nossa sugestão é de comprar esta criptomoeda. De acordo com nossa previsao os preços vão subir")
    else:
        previsao.text("Nossa sugestão é de vender esta criptomoeda. De acordo com nossa previsao os preços vão cair")

if crypto == 'Litecoin' and prev_ltc != 0:
    if prev_ltc > 0:
        previsao.text("Nossa sugestão é de comprar esta criptomoeda. De acordo com nossa previsao os preços vão subir")
    else:
        previsao.text("Nossa sugestão é de vender esta criptomoeda. De acordo com nossa previsao os preços vão cair")