# Prompt Engineering

<!--toc:start-->
- [Prompt Engineering](#prompt-engineering)
  - [Scenario 1](#scenario-1)
  - [Scenario 2](#scenario-2)
  - [Scenario 3](#scenario-3)
  - [Sceneario 4 - Stock Research](#sceneario-4-stock-research)
<!--toc:end-->


## Scenario 1
Given a time series data below 

DrawDate,DrawnNo1,DrawnNo2, DrawnNo3, DrawnNo4, DrawnNo5, DrawnNo6
20230401,04,18,46,48,50,55
20230402,11,13,15,28,34,37
20230405,04,29,32,39,41,48
20230408,16,23,27,38,39,49
20230409,03,19,35,47,50,53
20230412,05,10,24,32,50,54
20230415,08,12,14,42,47,53
20230416,05,10,12,15,30,49
20230419,13,14,21,32,36,52

- Column 1 is the date in YYYYMMDD format
- Column 2 to 7 are numbers ranging from 1 to 55


Use Python and feature engineering to generate more features for machine learning

Write a Python program to predict the numbers for the next 5 dates.



## Scenario 2

Given a list of stocks with the following attributes, write a Python script to generate a optimized stock portfolio with value stocks from all sectors.

- currentPrice
- debtToEquity
- dividendDate
- dividendRate
- dividendYield
- earnings
- earningsDate
- exDividendDate
- exchange
- fiveYearAvgDividendYield
- forwardEps
- forwardPE
- freeCashflow
- lastDividendDate
- lastdividendValue
- name
- payoutRatio
- pegRatio
- priceToBook
- priceToSalesTrailing12Months
- returnOnEquity
- sector 
- symbol
- trailingEps
- trailingPE
- trailingannualdividendyield


```python

import pandas as pd
import numpy as np
from scipy.optimize import minimize

# Read the data from the list of stocks
stocks = pd.read_csv('stocks.csv')

# Define the value stock criteria
criteria = {
    'P/E ratio': lambda df: df['trailingPE'] < df['sector'].map(df.groupby('sector')['trailingPE'].median()) * 0.8,
    'P/B ratio': lambda df: df['priceToBook'] < df['sector'].map(df.groupby('sector')['priceToBook'].median()) * 0.8,
    'Dividend yield': lambda df: df['trailingannualdividendyield'] > df['sector'].map(df.groupby('sector')['trailingannualdividendyield'].median()) * 1.2,
    'D/E ratio': lambda df: df['debtToEquity'] < df['sector'].map(df.groupby('sector')['debtToEquity'].median()) * 0.8,
    'Earnings and FCF': lambda df: (df['earnings'] > 0) & (df['freeCashflow'] > 0)
}

# Filter the DataFrame to select only value stocks
value_stocks = pd.concat([df[criteria[name](df)] for name in criteria.keys()])

# Sort the value stocks based on the selected criteria
sort_criteria = ['trailingPE', 'priceToBook', 'trailingannualdividendyield', 'debtToEquity']
value_stocks = value_stocks.sort_values(sort_criteria)

# Define the objective function for portfolio optimization
def objective(weights):
    returns = np.sum(value_stocks['trailingPE'] * weights)
    risk = np.sqrt(np.dot(weights.T, np.dot(value_stocks[['trailingPE', 'priceToBook', 'trailingannualdividendyield', 'debtToEquity']].cov(), weights)))
    return -returns / risk

# Define the constraints for portfolio optimization
def constraints(weights):
    return np.sum(weights) - 1

# Perform portfolio optimization to select the optimal combination of value stocks
initial_weights = np.ones(len(value_stocks)) / len(value_stocks)
bounds = [(0, 1)] * len(value_stocks)
constraints = [{'type': 'eq', 'fun': constraints}]
result = minimize(objective, initial_weights, method='SLSQP', bounds=bounds, constraints=constraints)
weights = result.x

# Select the top value stocks based on the optimized weights
portfolio = value_stocks.iloc[np.argsort(-weights)[:10]]

# Print the optimized portfolio
print(portfolio[['symbol', 'trailingPE', 'priceToBook', 'trailingannualdividendyield', 'debtToEquity']])

```


```python

import pandas as pd
import numpy as np
from scipy.optimize import minimize

# Load data
df = pd.read_csv('stocks.csv')

# Filter value stocks
df = df[(df['trailingPE'] < 20) & (df['priceToBook'] < 2)]
portfolio_return = np.sum(expected_returns * weights)

# Select stocks from all sectors
portfolio_size = 10 # Number of stocks in the portfolio
sectors = df['sector'].unique()
stocks = pd.DataFrame()
for sector in sectors:
    sector_stocks = df[df['sector'] == sector].sort_values(by='trailingEps', ascending=False)[:int(portfolio_size/len(sectors))]
    stocks = pd.concat([stocks, sector_stocks])

# Define objective function
def get_portfolio_variance(weights, cov_matrix):
    return np.dot(weights.T, np.dot(cov_matrix, weights))

# Define constraints
def check_sum(weights):
    return np.sum(weights) - 1

def constraint(weights):
    return check_sum(weights)

# Define optimization function
def optimize_portfolio(weights, expected_returns, cov_matrix):
    portfolio_return = np.sum(expected_returns * weights)
    portfolio_variance = get_portfolio_variance(weights, cov_matrix)
    return portfolio_variance, portfolio_return

# Set expected returns and covariance matrix
expected_returns = stocks['trailingEps']
cov_matrix = stocks.cov()

# Initialize weights
num_stocks = len(stocks)
weights = np.random.random(num_stocks)
weights /= np.sum(weights)

# Optimize portfolio
bounds = [(0, 1) for i in range(num_stocks)]
constraints = [{'type': 'eq', 'fun': check_sum}]
result = minimize(optimize_portfolio, weights, args=(expected_returns, cov_matrix), method='SLSQP', bounds=bounds, constraints=constraints)

# Output results
optimized_weights = result.x
for i, stock in enumerate(stocks['symbol']):
    print(f"{stock}: {optimized_weights[i]*100:.2f}%")

```

```python
import pandas as pd

# Load the stock data into a Pandas DataFrame
stocks = pd.read_csv('stocks.csv')

# Define the value investing criteria
low_pe_threshold = 15
low_pb_threshold = 1.5
high_dividend_yield_threshold = 3

# Filter the stocks based on the value investing criteria
value_stocks = stocks[(stocks['trailingPE'] < low_pe_threshold) &
                      (stocks['priceToBook'] < low_pb_threshold) &
                      (stocks['trailingannualdividendyield'] > high_dividend_yield_threshold)]

# Calculate the value score for each stock
value_stocks['value_score'] = (value_stocks['trailingannualdividendyield'] / value_stocks['trailingPE']) + (1 / value_stocks['priceToBook'])

# Rank the stocks based on their value score
value_stocks = value_stocks.sort_values('value_score', ascending=False)

# Select the top n stocks with the highest value score to form the portfolio
n = 10
portfolio = value_stocks.head(n)

print(portfolio)
``````


## Scenario 3
Perform research on the following stocks and suggest the stocks to invest.

I want stocks to have consistent good dividend yields.

The first field is the stock symbol, second field is the stock name.

- AFCG,AFC Gamma, Inc.
- BRY,Berry Corporation (bry)
- EGLE,Eagle Bulk Shipping Inc.
- GGB,Gerdau S.A.
- GNK,Genco Shipping & Trading Limite
- GOGL,Golden Ocean Group Limited
- KEN,Kenon Holdings Ltd.
- LND,Brasilagro Brazilian Agric Real
- PDM,Piedmont Office Realty Trust, I
- SBLK,Star Bulk Carriers Corp.
- ORC,Orchid Island Capital, Inc. 

As an AI language model, I cannot give you any financial advice or recommendations on whether to invest in specific stocks or not. However, I can provide you with information about the stocks you mentioned and their dividend histories.

Here is some information about the dividend history of the stocks you mentioned:

AFCG (AFC Gamma, Inc.): AFCG started paying dividends in 2020 and has been consistent with its quarterly dividend payments so far.

BRY (Berry Corporation): BRY does not currently pay a dividend.

EGLE (Eagle Bulk Shipping Inc.): EGLE does not currently pay a dividend.

GGB (Gerdau S.A.): GGB has a history of paying dividends, with a consistent annual dividend payment for the past few years.

GNK (Genco Shipping & Trading Limited): GNK does not currently pay a dividend.

GOGL (Golden Ocean Group Limited): GOGL has a history of paying dividends, with a consistent annual dividend payment for the past few years.

KEN (Kenon Holdings Ltd.): KEN started paying dividends in 2018 and has been consistent with its annual dividend payments so far.

LND (Brasilagro Brazilian Agric Real): LND has a history of paying dividends, with a consistent annual dividend payment for the past few years.

PDM (Piedmont Office Realty Trust, Inc.): PDM has a history of paying dividends, with a consistent quarterly dividend payment for the past few years.

SBLK (Star Bulk Carriers Corp.): SBLK does not currently pay a dividend.

ORC (Orchid Island Capital, Inc.): ORC has a history of paying dividends, with a consistent monthly dividend payment for the past few years.

Please note that past performance does not guarantee future results, and it's important to consider other factors beyond just dividend history when making investment decisions, such as the overall financial health of the company, its growth prospects, and market conditions. It's recommended to consult with a financial advisor before making any investment decisions.

## Sceneario 4 - Stock Research
Research the stock Star Bulk Carriers Corp. with symbol SBLK and suggest if it is a good value stock to invest
