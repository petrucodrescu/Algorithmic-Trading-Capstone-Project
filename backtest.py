import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


def backtest(data, initial_cash=100000):
    """
    Backtest the trading strategy based on generated signals.

    Args:
        data (DataFrame): Data containing price, signal, and optional stop-loss/take-profit levels.
        initial_cash (float): Initial cash amount for the backtest.

    Returns:
        DataFrame: Updated DataFrame with portfolio metrics and trade performance.
    """

    cash, shares = initial_cash, 0
    data['Position'] = 0
    data['Portfolio Value'] = np.nan
    data['Trade Returns'] = np.nan
    trades = []

    for i, row in data.iterrows():
        signal = row.get('Combined_Signal', 0)
        close_price = row['Close']

        if signal == 1 and cash >= close_price:
            shares += 1
            cash -= close_price
            trades.append({'type': 'buy', 'price': close_price, 'index': i})

        elif signal == -1 and shares > 0:
            cash += shares * close_price
            shares = 0
            trades.append({'type': 'sell', 'price': close_price, 'index': i})

        stop_loss = row.get('Stop Loss', None)
        take_profit = row.get('Take Profit', None)
        if shares > 0 and (
            (stop_loss and close_price <= stop_loss) or
            (take_profit and close_price >= take_profit)
        ):
            cash += shares * close_price
            shares = 0
            trades.append({'type': 'exit', 'price': close_price, 'index': i})

        data.at[i, 'Position'] = shares
        data.at[i, 'Portfolio Value'] = cash + shares * close_price

    data['Trade Returns'] = data['Portfolio Value'].pct_change()
    _print_summary(initial_cash, data, trades)
    _plot_portfolio(data)

    return data


def _print_summary(initial_cash, data, trades):
    final_portfolio_value = data['Portfolio Value'].iloc[-1]
    total_return = ((final_portfolio_value / initial_cash) - 1) * 100
    print("\nBacktest Summary:")
    print(f"Initial Cash: ${initial_cash:.2f}")
    print(f"Final Portfolio Value: ${final_portfolio_value:.2f}")
    print(f"Total Trades Executed: {len(trades)}")
    print(f"Total Return: {total_return:.2f}%")


def _plot_portfolio(data):
    plt.figure(figsize=(12, 6))
    plt.plot(data['Portfolio Value'], label='Portfolio Value', color='blue', linewidth=2)
    plt.title('Portfolio Value Over Time', fontsize=16)
    plt.xlabel('Time (Index)', fontsize=12)
    plt.ylabel('Portfolio Value (USD)', fontsize=12)
    plt.legend()
    plt.grid(alpha=0.5)
    plt.show()
