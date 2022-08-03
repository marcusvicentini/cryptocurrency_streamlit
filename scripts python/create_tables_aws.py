import pandas_datareader.data as pdr
from datetime import datetime
from sqlalchemy import create_engine
import json

#Carregando dados da AWS do arquivo json
with open("aws_mysql_key.json") as aws_keys:
    keys = json.load(aws_keys)
    username = keys['user']
    password = keys['password']
    endpoint = keys['endpoint']
    database_name = keys['databasename']

#Lista com os nomes das criptomoedas que serão armazenadas
crypto_names = ['BTC', 'ETH', 'LTC', 'DAI', 'ETC', 'ETP', 'NEO', 'REP', 'XLM', 'XMR', 'XVG']

engine = create_engine("mysql+pymysql://{user}:{pw}@{host}/{db}"
				.format(host=endpoint, db=database_name, user=username, pw=password))

#Data final como hoje
end = datetime.today()

#Data inicial como 3 anos atras
start = datetime(end.year-3, end.month, end.day)

#escolhendo a moeda:
currency = 'USD'

#lista para armazenar os DF de cada cryptomoeda
crypto_df_list = []

#Armazenando os dados na lista criada anteriormente
for crypto in crypto_names:
    crypto_df_list.append(pdr.DataReader(f"{crypto}-{currency}",'yahoo',start,end))

#Laço que vai criar tabelas na AWS com os dados
try:
    for crypto_name, crypto_df in zip(crypto_names, crypto_df_list):
        crypto_df.to_sql(crypto_name, engine, if_exists='replace')
except:
        print("Erro ao tentar gravar no banco de dados!")
else:
        print("Dados gravados com sucesso!")
