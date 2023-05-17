import streamlit as st
import pandas as pd

# Read stock data from CSV
stock_data = pd.read_csv('stock_data.csv')

# Create an empty portfolio dictionary to store stock information
portfolio = {}

def add_to_portfolio(stock_symbol, quantity, amount):
    """Add a stock to the portfolio."""
    if stock_symbol in portfolio:
        # Update existing stock quantity and amount
        portfolio[stock_symbol]['Quantity'] += quantity
        portfolio[stock_symbol]['Amount'] += amount
    else:
        # Add new stock to the portfolio
        portfolio[stock_symbol] = {'Quantity': quantity, 'Amount': amount}

def calculate_performance():
    """Calculate performance of stocks in the portfolio."""
    portfolio_performance = []
    for stock_symbol, stock_info in portfolio.items():
        # Get the current price of the stock from the stock_data DataFrame
        current_price = stock_data[stock_data['Symbol'] == stock_symbol]['Price'].values[0]
        performance = (current_price - (stock_info['Amount'] / stock_info['Quantity'])) / (stock_info['Amount'] / stock_info['Quantity'])
        portfolio_performance.append({'Stock': stock_symbol, 'Performance': performance})
    return portfolio_performance

def main():
    st.title("Financial Portfolio Dashboard")

    # Stock selection and buying section
    st.header("Buy Stocks")
    stock_options = stock_data['Symbol'].tolist()
    selected_stock = st.selectbox('Select a stock:', stock_options)
    quantity = st.number_input('Quantity:', value=1, min_value=1)
    amount = st.number_input('Amount:', value=0.0, min_value=0.0)
    if st.button("Add to Portfolio"):
        add_to_portfolio(selected_stock, quantity, amount)
        st.success(f"{quantity} shares of {selected_stock} have been added to the portfolio!")

    # Portfolio section
    st.header("Portfolio")
    if not portfolio:
        st.info("Your portfolio is currently empty.")
    else:
        st.write("Stocks in your portfolio:")
        for stock_symbol, stock_info in portfolio.items():
            st.write(f"Stock: {stock_symbol}, Quantity: {stock_info['Quantity']}, Amount: {stock_info['Amount']}")

    # Performance analysis section
    st.header("Performance Analysis")
    if not portfolio:
        st.info("Add stocks to the portfolio to calculate performance.")
    else:
        performance_data = calculate_performance()
        performance_df = pd.DataFrame(performance_data)
        st.write("Portfolio Performance:")
        st.dataframe(performance_df)

    # Portfolio dashboard
    st.header("Portfolio Dashboard")
    if not portfolio:
        st.info("Add stocks to the portfolio to generate the dashboard.")
    else:
        st.write("Portfolio Dashboard will be displayed here.")

if __name__ == '__main__':
    main()
