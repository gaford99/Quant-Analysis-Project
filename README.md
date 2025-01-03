# TSM Quantitative Analysis Project 

## Overview
A comprehensive quantitative analysis tool for Taiwan Semiconductor (TSM) stock, combining traditional financial metrics with AI-powered insights using Claude API. The project provides investment analysis, risk assessment, and market context through both quantitative calculations and AI interpretation.

### Features
Historical price data analysis
Technical indicators calculation
Risk metrics assessment
AI-powered market analysis
Investment recommendations
Interactive analysis capabilities

## Project Structure

TSM_Quant_Analysis/

 data/
   raw/            
   processed/        

src/
 data_collection.py  
 data_processing.py
 investment_analysis.py
 anthropic_analysis.py

requirements.txt

## Features Breakdown
### Quantitative Analysis
- Daily returns calculation
- Volatility metrics
- Technical indicators (RSI, MACD)
- Moving averages
- Volume analysis
- Price pattern recognition
### Risk Assessment
- Maximum historical loss
- Value at Risk (VaR)
- Annual volatility
- Risk-adjusted returns
### AI Analysis
- Market context interpretation
- Risk factor identification
- Investment recommendations
- Industry trend analysis

## Sample Output

Investment Analysis for $10,000.00

### Projected Scenarios (1 Year):
Conservative: $9,871.93

Expected: $10,009.81

Optimistic: $10,133.01

### Risk Assessment:
Maximum Historical Loss: $-1,849.19

95% Value at Risk: $-402.99

Annual Volatility: 43.67%

## Dependencies
- pandas
- numpy
- yfinance
- anthropic
- matplotlib
- statsmodels
  
### Contributing
1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request
   
### Future Enhancements
- Additional technical indicators
- Portfolio optimization
- Real-time data updates
- Enhanced AI analysis
- Comparative industry analysis
## License
[]
