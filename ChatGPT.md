# ChatGPT Prompt

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
