import numpy as np

def monte_carlo_simulation(
    mean_returns,
    cov_matrix,
    num_portfolios=5000,
    risk_free_rate=0.0
):
    """
    Run Monte Carlo simulation to generate random portfolios
    """

    num_assets = len(mean_returns)

    results = np.zeros((3, num_portfolios))
    weights_record = []

    for i in range(num_portfolios):
        # Generate random weights
        weights = np.random.random(num_assets)
        weights /= np.sum(weights)
        weights_record.append(weights)

        # Portfolio return
        portfolio_return = np.dot(weights, mean_returns)

        # Portfolio volatility
        portfolio_volatility = np.sqrt(
            np.dot(weights.T, np.dot(cov_matrix, weights))
        )

        # Sharpe Ratio
        sharpe_ratio = (portfolio_return - risk_free_rate) / portfolio_volatility

        results[0, i] = portfolio_return
        results[1, i] = portfolio_volatility
        results[2, i] = sharpe_ratio

    return results, weights_record
