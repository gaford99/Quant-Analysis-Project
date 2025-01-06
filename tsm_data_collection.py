# tsm_data_collection.py
import yfinance as yf

def get_tsm_data(start_date='1997-10-09'):
    """Get TSM data"""
    try:
        # Download data
        tsm = yf.download('TSM', start=start_date)
        
       
        return tsm
    except Exception as e:
        print(f"Error fetching data: {e}")
        return None
