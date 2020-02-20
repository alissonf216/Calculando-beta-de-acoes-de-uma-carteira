
import numpy as np
from datetime import date
import quandl


# In[15]:


# Faz a consulta de dados históricos do Quandl e retorna um array Numpy
def get_prices(stock, startDate, endDate):
    # Retorna os Ãºltimos 252 registros de cotações
    data = quandl.get(
        stock, trim_start=startDate,
        trim_end=endDate,
        returns="numpy"
    )

    return data


# In[16]:


# Verifica se existe datas faltando entre dados históricos da ação e de mercado
def check_missing_date_prices(stock_prices, market_prices):
    # transforma os dados históricos num array com de datas de preços
    stock_dates = get_datas_by_prices(stock_prices)
    # transforma os dados históricos num array com de datas de mercdo
    market_dates = get_datas_by_prices(market_prices)

    for stock_date in stock_dates:
        if stock_date not in market_dates:
            print('Data não existe nos dados de mercado: ', stock_date)

    for market_date in market_dates:
        if market_date not in stock_dates:
            print('Data não existe nos dados da ação: ', market_date)

    return False


# In[17]:


# Transforma o array de preços retornados pelo Quantl num array de datas
def get_datas_by_prices(prices):

    # array com as datas que serão armazenadas
    datas = []

    # Percorre cada linha (ou seja, dia a dia)
    for price in prices:
        # Adiciona o elemento data no array
        datas.append(price[0])

    # Retorna os resultados
    return datas


# In[18]:


# Transforma o array de preços retornados pelo Quantl
# num array Numpy somente com os preços de fechamento (index)
def get_closing_prices(prices, index):

    # preços de fechamento que serão os preços de fechamento diÃ¡rios
    closing_prices = []

    # Percorre cada linha (ou seja, dia a dia)
    for price in prices:
        # Adiciona o elemento preço de fechamento no array, depois
        # de convertÃª-lo para float
        closing_prices.append(float(price[index]))

    # Retorna os resultados como um array Numpy
    return np.array(closing_prices)


# In[19]:


# Transforma o array de preços de fechamento num array de retornos
# (preço atual / preço dia anterior - 1)
def get_returns_prices(closing_prices, lenght):

    # Cria arrays zerados que serão preenchidos com os retornos dos preços.
    # Os dados de retorno sempre serão uma unidade menor do que os arrays
    # originais
    returns = np.zeros(lenght - 1)

    # Percorre cada preço dado
    for i in range(lenght - 1):
        # O retorno é igual ao preço atual dividido pelo preço anterior menos 1.
        # Devido a isso, vamos sempre começar com o segundo preço
        returns[i] = (closing_prices[i + 1] / closing_prices[i]) - 1

    # Retorna os resultados como um array Numpy
    return np.array(returns)


# In[20]:


# Calcula o beta de uma ação dados os preços bem como os preços para o mercado
# como um todo (como um índice, Bovespa por exemplo).
# Os dois arrays devem ter o mesmo tamanho.
# O resultado é o beta arredondado com duas casas decimais
def calc_beta(prices_stock, prices_market):

    # Calcula e armazena o tamanho dos arrays porque eles serão usados várias
    # vezes
    stock_len = len(prices_stock)
    market_len = len(prices_market)

    # Decide qual o conjunto de dados tem menos itens, pois para calcular o
    # beta é necessário que os dados da ação e de mercado tenha a mesma
    # quantidade de registros
    smallest = market_len
    if stock_len < market_len:
        smallest = stock_len

    # Cria os arrays de retornos dos preços
    # Os dados de retorno sempre serão uma unidade menor do que os arrays
    # originais
    stock_ret = get_returns_prices(prices_stock, smallest)
    market_ret = get_returns_prices(prices_market, smallest)

    # Calcula a covariância entre a ação e o mercado
    # http://docs.scipy.org/doc/numpy/reference/generated/numpy.cov.html
    covar_stock_market = np.cov(stock_ret, market_ret, ddof=0)[0, 1]
    print('Covariância ação/mercado: ', covar_stock_market)

    # Calcula a variância dos retornos do mercado
    # http://docs.scipy.org/doc/numpy/reference/generated/numpy.var.html
    var_market = np.var(market_ret)
    print('Variância mercado: ', var_market)

    # Beta é igual a covariância entre os retornos do ativo e retornos
    # do mercado dividido pela variância dos retornos do mercado.
    # Além disso, estamos arredondado o beta para duas casas decimais.
    return np.around(covar_stock_market / var_market, decimals=2)


# In[21]:


# data atual
today = date.today()
# data de início para pegar os dados de mercado - 5 anos
startDate = date(today.year - 3, today.month, today.day)
# a data final é a data de hoje
endDate = today

# pega os dados do índice Bovespa
stock = 'YAHOO/INDEX_BVSP'
market_prices = get_prices(stock, startDate, endDate)
print('Mercado:', stock[stock.find('/')+1:])

# para os dados do YAHOO o índice de preço de fechamento ajustado é o 6
# ["Date","Open","High","Low","Close","Volume","Adjusted Close"]
closing_prices_market = get_closing_prices(market_prices, 6)

# pega os dados da ação PETR4
stock = 'GOOG/BVMF_PETR4'
stock_prices = get_prices(stock, startDate, endDate)
print('Ação:', stock[stock.find('/')+1:])

# para os dados do GOOGLE o índice de preço de fechamento é o 4
# ["Date","Open","High","Low","Close","Volume"]
closing_prices_stock = get_closing_prices(stock_prices, 4)

beta = calc_beta(closing_prices_stock, closing_prices_market)
print('O beta é = ', beta)

