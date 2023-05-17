import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

portfolio_file = "portfolio.csv"

# Read stock data from CSVasdfasdfasdfasdf
try:
    stock_data = pd.read_csv('stock_data.csv', encoding='utf-8')
except UnicodeDecodeError:
    st.error("Error: Unable to read the CSV file. Please check the file encoding and try again.")
    st.stop()

# Load the portfolio data from CSV file or create an empty dictionary
if st.sidebar.checkbox("Load Portfolio"):
    try:
        portfolio = pd.read_csv(portfolio_file).set_index('Stock').to_dict(orient='index')
    except FileNotFoundError:
        portfolio = {}
else:
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
        current_price = stock_data[stock_data['Symbol'] == stock_symbol]['Currentprice'].values[0]
        performance = (current_price - (stock_info['Amount'] / stock_info['Quantity'])) / (stock_info['Amount'] / stock_info['Quantity'])
        portfolio_performance.append({'Stock': stock_symbol, 'Performance': performance})
    return portfolio_performance

def save_portfolio():
    """Save the portfolio data to a CSV file."""
    portfolio_df = pd.DataFrame.from_dict(portfolio, orient='index').reset_index()
    portfolio_df.columns = ['Stock', 'Quantity', 'Amount']
    portfolio_df.to_csv(portfolio_file, index=False)

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
        st.subheader("Portfolio Value")
        portfolio_value = sum(stock_info['Amount'] for stock_info in portfolio.values())
        st.write(f"The total value of your portfolio is: ${portfolio_value:.2f}")

        st.subheader("Portfolio Composition")
        composition_data = pd.DataFrame.from_dict(portfolio, orient='index')
        composition_data['Percentage'] = composition_data['Amount'] / portfolio_value * 100
        st.bar_chart(composition_data['Percentage'])

        st.subheader("Portfolio Performance")
        performance_data = calculate_performance()
        performance_df = pd.DataFrame(performance_data)
        st.bar_chart(performance_df.set_index('Stock'))

    # Save the portfolio data when the application stops
    save_portfolio()

if __name__ == '__main__':
    main()
