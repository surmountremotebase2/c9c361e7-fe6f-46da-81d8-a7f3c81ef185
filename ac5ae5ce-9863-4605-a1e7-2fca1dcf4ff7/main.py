from surmount.base_class import Strategy, TargetAllocation
from surmount.data import OHLCV
from surmount.technical_indicators import ATR
from surmount.logging import log

class TradingStrategy(Strategy):
    def __init__(self):
        self.ticker = "SPY"  # Adjust this to trade a different asset

    @property
    def assets(self):
        return [self.ticker]

    @property
    def interval(self):
        # '1day' interval for daily volatility analysis
        return "1day"

    def run(self, data):
        # Extracting data for the asset
        asset_data = data["ohlcv"]
        
        # Check if there is enough data to calculate ATR
        if len(asset_data) < 15:
            log("Not enough data to evaluate ATR")
            return TargetAllocation({self.ticker: 0})  # No position if insufficient data
        
        # Calculate 14-day ATR for the asset
        atr_values = ATR(self.ticker, asset_data, 14)
        
        # Determine trading signal
        if atr_values[-1] > atr_values[-2]:
            # If current ATR is greater than the previous, assume increased volatility and buy
            allocation = {self.ticker: 1}  # Full allocation to this asset
            log(f"Buying {self.ticker}- Increased Volatility detected")
        else:
            # If current ATR is not greater than the previous, reduce or hold no position
            allocation = {self.ticker: 0}  # No allocation to this asset
            log(f"Selling {self.ticker}- Decreased Volatility detected")

        return TargetAllocation(allocation)