import yfinance as yf
import pandas as pd

def get_public_company_data(ticker):
    """
    Fetch financial data for a public company using yfinance.
    """
    try:
        company = yf.Ticker(ticker)
        info = company.info
        financials = company.financials
        
        # Calculate key metrics
        market_cap = info.get('marketCap', 0) / 1e9  # Convert to billions
        revenue = financials.loc['Total Revenue'].iloc[0] / 1e9  # Convert to billions
        net_income = financials.loc['Net Income'].iloc[0] / 1e9  # Convert to billions
        
        # Calculate growth rates
        revenue_growth = ((financials.loc['Total Revenue'].iloc[0] / 
                         financials.loc['Total Revenue'].iloc[1]) - 1) * 100
        
        profit_margin = (net_income / revenue) * 100
        pe_ratio = info.get('forwardPE', info.get('trailingPE', 0))
        
        return {
            'name': info.get('longName', ticker),
            'industry': info.get('industry', 'N/A'),
            'market_cap': market_cap,
            'revenue': revenue,
            'net_income': net_income,
            'revenue_growth': revenue_growth,
            'profit_margin': profit_margin,
            'pe_ratio': pe_ratio,
            'description': info.get('longBusinessSummary', ''),
            'competitors': info.get('companyOfficers', [])
        }
    
    except Exception as e:
        print(f"Error fetching data for {ticker}: {str(e)}")
        return None

def process_private_company_data(data):
    """
    Process and validate private company data.
    """
    processed_data = data.copy()
    
    # Convert revenue to billions for consistency
    processed_data['revenue'] = processed_data['revenue'] / 1000  # Convert millions to billions
    
    # Calculate net income from revenue and profit margin
    processed_data['net_income'] = (processed_data['revenue'] * 
                                  processed_data['profit_margin'] / 100)
    
    # Convert competitors string to list
    if isinstance(processed_data['competitors'], str):
        processed_data['competitors'] = [comp.strip() for comp in 
                                       processed_data['competitors'].split(',')]
    
    return processed_data
