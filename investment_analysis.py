# investment_analysis.py
from tsm_data_collection import get_tsm_data
from Data_processing import create_features, generate_signals
import numpy as np
import pandas as pd

def calculate_investment_scenarios(df, investment_amount):
    try:
        returns_dist = df['returns'].dropna()
        
        optimistic = np.percentile(returns_dist, 75)
        expected = returns_dist.mean()
        conservative = np.percentile(returns_dist, 25)
        
        scenarios = {
            'Conservative': investment_amount * (1 + conservative),
            'Expected': investment_amount * (1 + expected),
            'Optimistic': investment_amount * (1 + optimistic)
        }
        
        return scenarios
    except Exception as e:
        print(f"Error calculating scenarios: {e}")
        return None

def calculate_risk_metrics(df, investment_amount):
    try:
        # Clean the returns data
        returns = df['returns'].dropna()
        
        # Maximum drawdown
        max_loss = returns.min() * investment_amount
        
        # Value at Risk (95% confidence)
        var_95 = np.nanpercentile(returns, 5) * investment_amount  # Using nanpercentile
        
        # Add more metrics
        annual_volatility = returns.std() * np.sqrt(252)  # Annualized volatility
        
        return {
            'Maximum_Historical_Loss': max_loss,
            'Value_at_Risk_95': var_95,
            'Annual_Volatility': annual_volatility
        }
    except Exception as e:
        print(f"Error calculating risk metrics: {e}")
        return None

# Main execution
if __name__ == "__main__":
    investment = 10000
    
    print("Fetching data...")
    tsm = get_tsm_data()
    
    print("Processing data...")
    processed_data = create_features(tsm)
    
    print("Calculating scenarios...")
    scenarios = calculate_investment_scenarios(processed_data, investment)
    risk_metrics = calculate_risk_metrics(processed_data, investment)
    
    if scenarios and risk_metrics:
        print(f"\nInvestment Analysis for ${investment:,.2f}")
        
        print("\nProjected Scenarios (1 Year):")
        print(f"Conservative: ${scenarios['Conservative']:,.2f}")
        print(f"Expected: ${scenarios['Expected']:,.2f}")
        print(f"Optimistic: ${scenarios['Optimistic']:,.2f}")
        
        print("\nRisk Assessment:")
        print(f"Maximum Historical Loss: ${risk_metrics['Maximum_Historical_Loss']:,.2f}")
        print(f"95% Value at Risk: ${risk_metrics['Value_at_Risk_95']:,.2f}")
        print(f"Annual Volatility: {risk_metrics['Annual_Volatility']*100:.2f}%")
        
        # Add interpretation
        print("\nInterpretation:")
        print(f"- There is a 95% chance that you won't lose more than ${abs(risk_metrics['Value_at_Risk_95']):,.2f} in a day")
        print(f"- The worst historical daily loss would have been ${abs(risk_metrics['Maximum_Historical_Loss']):,.2f}")
        print(f"- Expected annual volatility is {risk_metrics['Annual_Volatility']*100:.2f}%")
    else:
        print("Error occurred during calculations")
