# Optimal Stock Portfolio Allocation Using Modern Portfolio Theory (MPT)

## Project Overview
This project applies Modern Portfolio Theory to Indian stock market data
to construct an optimal investment portfolio that maximizes return while minimizing risk.

## Business Problem
Investors want to allocate capital efficiently across multiple stocks to achieve
the best risk-adjusted returns rather than relying on intuition.

## Dataset
- Source: Kaggle (NIFTY 50 / NSE historical stock prices)
- Columns: Date, Symbol, Open, High, Low, Close, Volume

## Methodology
Modern Portfolio Theory (MPT) states that:
- Risk can be reduced through diversification
- Portfolio risk depends on how stocks move together (covariance)
- The Efficient Frontier shows optimal portfolios

Monte Carlo simulation is used to generate thousands of random portfolios.

## Results
- Maximum Sharpe Ratio portfolio identified
- Minimum volatility portfolio identified
- Efficient Frontier plotted
- Equal-weight portfolio compared

## Technologies Used
- Python
- NumPy
- Pandas
- Matplotlib
- Seaborn
- SciPy

## How to Run
1. Install dependencies:
