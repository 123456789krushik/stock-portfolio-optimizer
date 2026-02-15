import numpy as np

def portfolio_return(weights, mean_returns):
    """
    Calculate expected portfolio return
    """
    return np.dot(weights, mean_returns)


def portfolio_volatility(weights, cov_matrix):
    """
    Calculate portfolio volatility (standard deviation)
    """
    return np.sqrt(np.dot(weights.T, np.dot(cov_matrix, weights)))


def sharpe_ratio(weights, mean_returns, cov_matrix, risk_free_rate=0.0):
    """
    Calculate Sharpe Ratio
    """
    port_return = portfolio_return(weights, mean_returns)
    port_vol = portfolio_volatility(weights, cov_matrix)

    return (port_return - risk_free_rate) / port_vol
