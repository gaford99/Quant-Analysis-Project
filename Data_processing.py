import yfinance as yf
import pandas as pd 
import numpy as np  
from scipy import stats
from statsmodels.nonparametric.smoothers_lowess  import lowess
from tsm_data_collection import get_tsm_data

#calculate RSI
def calculate_rsi(prices, periods=14):
    "Calculate Relative Strength Index"
    
    #Calculate daily price changes
    delta = prices.diff()
    
    #Separate gains and losses
    gain = (delta.where(delta>0, 0)).rolling(window=periods).mean()
    loss = (-delta.where(delta<0, 0)).rolling(window=periods).mean()
    
    #Calculate RS (relative strength index)``
    RS = gain/loss
    
    #Convert to RSI
    RSI = 100 - (100/(1+RS))
    
    return RSI

#feature engineering
def create_features (df):
    "Create technical indicators and features for the model"
    df = df.copy()
    
    #Calculate daily returns (percentage change)
    #price based features
    df['returns'] = df['Close'].pct_change()    
    #Calculate the log returns
    #More suitable for statistical modeling rather than simple returns
    df['log_returns'] = np.log(df['Close']/df['Close'].shift(1))
    
    #Lowess smoothing to remove noise from price data
    try: 
        #convert to numpy array
        y = df['Close'].values.squeeze() #convert to 1D array
        x = np.arange(len(y))
        
        #Apply Lowess smoothing
        smoothed = lowess(
            endog = y, #Price data
            exog = x, #Time points
            frac=0.1, #Smoothing parameter
            it = 0, #No iterations
            return_sorted = True 
            )
        
        #Add smooth values to dataframe 
        df['Close_smooth'] = smoothed[:,1]
        
    except Exception as e:  
        print(f"Error in smoothing: {e}")
        #Fallback: using simple smoothing if LOWESS fails
        df['Close_smooth'] = df['Close'].rolling(window=20).mean()  
    
    #Caculate indicators using smoothed price
    #Higher volumes mean more price swing 
    df['volatility'] = df['returns'].rolling(window=20).std()
    
    #Technical Indicators 
    #RSI (Relative Strength Index) - measures overbought/oversold conditions
    #Values range 0-100: >70 overbought, <30 potentially oversold
    df['RSI'] = calculate_rsi(df['Close'], periods=14) 
    
    #MACD (Moving Average Convergence Divergence)
    #Trend-following momentum indicator
    df['MACD'] = (df['Close'].ewm(span=12).mean()-
                  df['Close'].ewm(span=26).mean())
    
    #Moving Averages - smooth price data to show trends
    #50-day moving average (shorter term trend)
    df['MA50'] = df['Close_smooth'].rolling(window=50).mean()
    #200-day moving average (longer term trend)
    df['MA200'] = df['Close_smooth'].rolling(window=200).mean()
    
    #Trend indicator: 1 if uptrend (MA50 > MA200), -1 if downtrend 
    df['trend'] = np.where(df['MA50']>df['MA200'], 1, -1)
    
    #Volume Analysis 
    #20-day average volume
    volume_series = df['Volume'] if isinstance(df['Volume'], pd.Series) else df['Volume'].squeeze()
    #Current volume relative to average (>1 means higher than average)
    volume_ma = volume_series.rolling(window=20).mean()
    df['Volume_ratio'] = volume_series.div(volume_ma)
    
    # Add debug prints here
    print("\nDEBUG INFO:")
    print("Shape of Close_smooth:", df['Close_smooth'].shape)
    print("Shape of High:", df['High'].shape)
    print("Shape of Low:", df['Low'].shape)
    
    #Price pattern features 
    #Daily price range relative to closing 
    # Convert High and Low to 1D
    high_1d = df['High'].squeeze()  # Convert to 1D
    low_1d = df['Low'].squeeze()    # Convert to 1D
    
    df['High_Low_Range'] = (high_1d - low_1d).div(df['Close_smooth'])
    df['Price_Level'] = (df['Close_smooth'] - low_1d).div(high_1d - low_1d)
    
    return df

#generate trading signals
def generate_signals(df):
    "Generate trading signals based on technical indicators"
    conditions = {
        #strong buy when: RSI shows oversold + uptrend + high volume 
        'strong_buy':(
            (df['RSI']<30) & 
            (df['trend']==1) & 
            (df['Volume_ratio']>1.5)
        ),
        #Regular buy with less strict conditions
        'Buy':(
            (df['RSI'] < 40) &
            (df['trend'] == 1)
        ), 
        #Sell when: RSI shows overbought + downtrend
        'Sell': (
            (df['RSI'] > 60) &
            (df['trend'] == -1)
        ),
        #Strong sell with stricter conditions
        'Strong_Sell': (
            (df['RSI'] > 70) &
            (df['trend'] == -1) &
            (df['Volume_ratio'] > 1.5)
        )
    }
    return conditions 

#calculate performance of trading signals
def calculate_performance(df, signals):
    "Calculate performance of trading signals"
    #Initialize position column (0 = no position)
    df['Position'] = 0
    
    #Assign positions based on signals 
    #2 = strong buy, 1 = buy, -1 = sell, -2 = strong sell
    df.loc[signals['strong_buy'], 'Position'] = 2
    df.loc[signals['Buy'], 'Position'] = 1
    df.loc[signals['Sell'], 'Position'] = -1
    df.loc[signals['Strong_Sell'], 'Position'] = -2
    
    #calculate strategy returns 
    #Multiply position by next day's return
    df['Strategy_Returns'] = df['Position']*df['returns'].shift(-1) 
    
    return df

#main function
def main():
    # Get and process data
    tsm = get_tsm_data()
    tsm_processed = create_features(tsm)
    signals = generate_signals(tsm_processed)
    tsm_processed = calculate_performance(tsm_processed, signals)
    return tsm_processed

#run main function
if __name__ == "__main__":
    processed_data = main()
    # Print metrics
    print("\nStrategy Performance Metrics:")
    print(f"Total Returns: {processed_data['Strategy_Returns'].sum()*100:.2f}%")
    print(f"Sharpe Ratio: {processed_data['Strategy_Returns'].mean()/processed_data['Strategy_Returns'].std()*np.sqrt(252):.2f}")
