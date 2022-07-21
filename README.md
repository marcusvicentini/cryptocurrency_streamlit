# cryptocurrency_streamlit


OBJETIVO DO PROJETO 

 

Atualmente as criptomoedas são temas de muita discussão e controvérsias. Há quem prefira investir em outra forma mais tradicional de aplicação como ouro, dólar, e ações de empresas também. 

Um dos fatores que torna as criptomoedas tão polemicas é sua alta volatilidade e instabilidade de preço. Para alguns essa volatilidade é boa se souberem medir isso e ganhar com a variação de preço 

O objetivo desse projeto é criar uma ferramenta que ajude investidores e também estudiosos das criptomoedas a analisar seu preço e variação, podendo assim ter mais segurança na sua decisão. 

 

SOLUÇÃO PROPOSTA 

 

Para solucionar esse problema vou criar um aplicativo no Streamlit que exiba algumas informações importantes das criptomoedas e que mostre também a predição dos valores 10 dias no futuro usando machine learning. 

A solução envolve coleta de dados usando Pandas Datareader, lendo dados do yahoo finance, banco de dados MySQL na AWS para armazenar nossos dados. Para o processamento desses dados foi usado a linguagem Python e algumas bibliotecas como Pandas, Prophet, Pickle dentre outras. 

 

O armazenamento dos dados começa com a coleta através do pandas datareader, que facilmente obtém os dados do yahoo finance e salva em um Dataframe. Com esse Dataframe salvamos os dados na AWS. 

 

Como os dados já estão disponíveis, agora entra a parte do processamento deles. Os preços de criptomoedas são uma séria temporal, ou seja, dados que variam no tempo de acordo com seu valor passado, podendo ou não depender de alguma outra variável. Nesse caso não incluirei nenhuma outra variável, só será a analisado o preço passado. 

Foi criado um modelo de baseline com média móvel de 3 dias para previsão de preço. Esse modelo serve de base para que possamos avaliar outros modelos, que devem ser melhores que esse de baseline. A métrica para avaliar o resultado será a RMSE, já que é uma métrica que usa a própria unidade de medida, no nosso caso o dólar americano. 

A partir dessa referência podemos fazer testes com alguns algoritmos e ver sua performance.  O algoritmo escolhido foi o Prophet do Facebook por sua simplicidade e grande robustez. Mas é preciso fazer um tuning desse algoritmo para ter um resultado melhor.  

Criei uma função grid_search que faz o teste com um vetor de vários valores para os parâmetros do Prophet. Com o tunning, a performance do algoritmo aumentou muito, dando um resultado satisfatório. 

Com o modelo e parâmetros definidos, precisamos persistir os modelos no disco (um modelo para cada criptomoeda) para poder usar esse modelo na solução final. 

O produto final do projeto é o aplicativo no streamlit, então carregamos os modelos para o código do streamlit. Além da previsão de preço também tem a opção de ver os candlesticks das moedas, o preço histórico e também algumas médias móveis que são muito usadas pelos analistas. 

 

RESULTADOS 

O aplicativo criado no Streamlit cumpro o que promete. O usuário pode facilmente visualizar os preços históricos da moeda em escolha, ver candlesticks, plotar medias moveis em cima do preço e principalmente ver a previsão de preços dos proximos 10 dias. 

Além dessas opções ele mostra se a recomendação é de compra ou venda, comparando a previsao de preço futuro com o ultimo preço registrado. 

 

Link para o aplicativo no Streamlit: 

https://marcusvicentini-cryptocurrency-streamlit-main-2dq8y6.streamlitapp.com/ 
