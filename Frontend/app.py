import streamlit as st
import pandas as pd
import numpy as np
import sys
import os


# Add project root to Python path
sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
)


from src.fetch_today_data import fetch_today_market_data
from src.data_processing import load_and_clean_data, pivot_close_prices
from src.optimization import monte_carlo_simulation

# =========================
# SIMPLE PREMIUM STYLING
# =========================
st.markdown("""
<style>

/* Background image with overlay */
[data-testid="stAppViewContainer"] {
    background: linear-gradient(rgba(0,0,0,0.65), rgba(0,0,0,0.65)),
                url("https://images.unsplash.com/photo-1611974789855-9c2a0a7236a3");
    background-size: cover;
    background-position: center;
    background-attachment: fixed;
}

/* Hide Streamlit header */
[data-testid="stHeader"] {
    visibility: hidden;
}

/* Style the real Streamlit container */
.block-container {
    max-width: 900px;
    margin: 60px auto;
    padding: 40px;
    border-radius: 25px;
    background: rgba(20, 30, 60, 0.75);
    box-shadow: 0 20px 60px rgba(0, 0, 0, 0.6);
    backdrop-filter: blur(15px);
    animation: float 5s ease-in-out infinite;

}

@keyframes float {
    0% { transform: translateY(0px); }
    50% { transform: translateY(-6px); }
    100% { transform: translateY(0px); }
}


/* Title style */
h1 {
    text-align: center;
    color: white;
}

/* Button style */
div.stButton > button {
    background: linear-gradient(90deg, #00c6ff, #0072ff);
    color: white;
    font-weight: bold;
    border-radius: 12px;
    height: 3em;
    width: 100%;
    transition: 0.3s;
}

div.stButton > button:hover {
    transform: scale(1.05);
}

</style>
""", unsafe_allow_html=True)


st.title("📈 Stock Portfolio Optimizer")
st.write(
    "Enter stocks you are interested in. "
    "The system will recommend optimal investment weights."
)


# -------------------------------
# USER INPUT
# -------------------------------
stock_input = st.text_input(
    "Enter NSE stock symbols (comma-separated)",
    placeholder="RELIANCE, TCS, HDFCBANK, SBIN,etc..."
)

investment_amount = st.number_input(
    "Total Investment Amount (₹)",
    min_value=1000,
    step=1000,
    value=100000
)

optimize_btn = st.button("Optimize Portfolio")

# -------------------------------
# MAIN LOGIC
# -------------------------------
if optimize_btn:

    user_selected_stocks = [
        s.strip().upper()
        for s in stock_input.split(",")
        if s.strip()
    ]

    if len(user_selected_stocks) < 2:
        st.error("Please enter at least 2 valid stock symbols.")
        st.stop()
    
    
    user_selected_stocks = [
    s.strip().upper()
    for s in stock_input.split(",")
    if s.strip()
    ]

    st.info(f"Selected Stocks: {user_selected_stocks}")

    # Fetch latest data
    with st.spinner("Fetching market data..."):
        fetch_today_market_data(
            user_selected_stocks,
            "data/stock_prices.csv"
        )

    # Load & process data
    df = load_and_clean_data("data/")
    price_matrix = pivot_close_prices(
        df,
        selected_stocks=user_selected_stocks
    )

    if price_matrix.shape[1] < 2:
        st.error("Insufficient data for optimization.")


    # Returns & covariance
    daily_returns = price_matrix.pct_change().dropna()
    annual_returns = daily_returns.mean() * 252
    annual_cov = daily_returns.cov() * 252

    # Optimization
    results, weights = monte_carlo_simulation(
        annual_returns.values,
        annual_cov.values,
        num_portfolios=5000
    )

    sharpe_ratios = results[2]
    best_idx = np.argmax(sharpe_ratios)
    best_weights = weights[best_idx]

    # Output table
    result_df = pd.DataFrame({
        "Stock": user_selected_stocks,
        "Weight (%)": np.round(best_weights * 100, 2),
        "Investment (₹)": np.round(best_weights * investment_amount, 2)
    })

    st.success("✅ Optimal Portfolio Generated")
    st.dataframe(result_df)

    st.download_button(
        "Download Portfolio Allocation",
        result_df.to_csv(index=False),
        file_name="optimal_portfolio.csv",
        mime="text/csv"
    )
    
    

