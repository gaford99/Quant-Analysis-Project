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

def project_future_scenarios(df, investment_amount, days=252):
    """Project future scenarios using Monte Carlo simulation"""
    try:
        returns = df['returns'].dropna()
        daily_return = returns.mean()
        daily_vol = returns.std()
        
        # Run simulations
        n_simulations = 1000
        simulated_returns = np.random.normal(
            daily_return, 
            daily_vol, 
            size=(n_simulations, days)
        )
        
        # Calculate future values
        future_values = investment_amount * np.cumprod(1 + simulated_returns, axis=1)
        final_values = future_values[:, -1]
        
        # Calculate projected scenarios
        projected_scenarios = {
            'Conservative': np.percentile(final_values, 25),
            'Expected': np.percentile(final_values, 50),
            'Optimistic': np.percentile(final_values, 75)
        }
        
        return projected_scenarios
    except Exception as e:
        print(f"Error in projections: {e}")
        return None

# Modify main execution
if __name__ == "__main__":
    investment = 10000
    
    print("Fetching data...")
    tsm = get_tsm_data()
    
    print("Processing data...")
    processed_data = create_features(tsm)
    
    print("Calculating scenarios...")
    historical_scenarios = calculate_investment_scenarios(processed_data, investment)
    risk_metrics = calculate_risk_metrics(processed_data, investment)
    future_scenarios = project_future_scenarios(processed_data, investment)
    
    if historical_scenarios and risk_metrics and future_scenarios:
        print(f"\nInvestment Analysis for ${investment:,.2f}")
        
        print("\nHistorical Scenarios:")
        print(f"Conservative: ${historical_scenarios['Conservative']:,.2f}")
        print(f"Expected: ${historical_scenarios['Expected']:,.2f}")
        print(f"Optimistic: ${historical_scenarios['Optimistic']:,.2f}")
        
        print("\nProjected Future Scenarios (1 Year):")
        print(f"Conservative: ${future_scenarios['Conservative']:,.2f}")
        print(f"Expected: ${future_scenarios['Expected']:,.2f}")
        print(f"Optimistic: ${future_scenarios['Optimistic']:,.2f}")
        
        print("\nRisk Assessment:")
        print(f"Maximum Historical Loss: ${risk_metrics['Maximum_Historical_Loss']:,.2f}")
        print(f"95% Value at Risk: ${risk_metrics['Value_at_Risk_95']:,.2f}")
        print(f"Annual Volatility: {risk_metrics['Annual_Volatility']*100:.2f}%")
        
        print("\nInterpretation:")
        print(f"- There is a 95% chance that you won't lose more than ${abs(risk_metrics['Value_at_Risk_95']):,.2f} in a day")
        print(f"- The worst historical daily loss would have been ${abs(risk_metrics['Maximum_Historical_Loss']):,.2f}")
        print(f"- Expected annual volatility is {risk_metrics['Annual_Volatility']*100:.2f}%")
    else:
        print("Error occurred during calculations")