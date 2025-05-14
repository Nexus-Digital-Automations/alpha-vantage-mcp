"""
Handlers for Alpha Vantage MCP tools.

This package provides handler functions for various financial data tools
from the Alpha Vantage API.
"""

# Import stock-related handlers
from .stocks import (
    handle_stock_quote, handle_company_info, handle_time_series,
    handle_time_series_weekly, handle_time_series_monthly,
    handle_time_series_daily_adjusted, handle_time_series_weekly_adjusted,
    handle_time_series_monthly_adjusted, handle_market_status,
    handle_listing_status, handle_historical_options,
    handle_intraday_time_series, handle_symbol_search,
    handle_etf_profile, handle_ipo_calendar,
    handle_earnings_calendar, handle_earnings_call_transcript,
    handle_insider_transactions, handle_gainers_losers
)

# Import cryptocurrency-related handlers
from .crypto import (
    handle_crypto_exchange_rate, handle_crypto_daily,
    handle_crypto_weekly, handle_crypto_monthly,
    handle_fx_rate, handle_fx_daily,
    handle_fx_weekly, handle_fx_monthly
)

# Import technical indicator handlers
from .technical import (
    handle_sma, handle_ema, handle_wma,
    handle_dema, handle_tema, handle_macd,
    handle_rsi, handle_bbands, handle_stoch,
    handle_stochf, handle_willr, handle_adx,
    handle_stochrsi, handle_adxr, handle_apo,
    handle_ppo, handle_mom, handle_bop, handle_cci,
    handle_cmo, handle_roc, handle_rocr, handle_aroon,
    handle_aroonosc, handle_mfi, handle_trix, handle_ultosc,
    handle_dx
)

# Import economic/fundamental data handlers
from .economic import (
    handle_real_gdp, handle_cpi, handle_inflation,
    handle_treasury_yield, handle_income_statement,
    handle_balance_sheet, handle_cash_flow,
    handle_earnings, handle_news_sentiment,
    handle_wti, handle_brent, handle_natural_gas,
    handle_copper, handle_wheat, handle_corn,
    handle_real_gdp_per_capita, handle_federal_funds_rate, 
    handle_aluminum, handle_retail_sales, handle_durables,
    handle_unemployment, handle_nonfarm_payroll, handle_cotton,
    handle_sugar, handle_coffee, handle_all_commodities
)

# Export all handlers
__all__ = [
    # Stock-related handlers
    'handle_stock_quote', 'handle_company_info', 'handle_time_series',
    'handle_time_series_weekly', 'handle_time_series_monthly',
    'handle_time_series_daily_adjusted', 'handle_time_series_weekly_adjusted',
    'handle_time_series_monthly_adjusted', 'handle_market_status',
    'handle_listing_status', 'handle_historical_options',
    'handle_intraday_time_series', 'handle_symbol_search',
    'handle_etf_profile', 'handle_ipo_calendar',
    'handle_earnings_calendar', 'handle_earnings_call_transcript',
    'handle_insider_transactions', 'handle_gainers_losers',
    
    # Cryptocurrency-related handlers
    'handle_crypto_exchange_rate', 'handle_crypto_daily',
    'handle_crypto_weekly', 'handle_crypto_monthly',
    'handle_fx_rate', 'handle_fx_daily',
    'handle_fx_weekly', 'handle_fx_monthly',
    
    # Technical indicator handlers
    'handle_sma', 'handle_ema', 'handle_wma',
    'handle_dema', 'handle_tema', 'handle_macd',
    'handle_rsi', 'handle_bbands', 'handle_stoch',
    'handle_stochf', 'handle_willr', 'handle_adx',
    'handle_stochrsi', 'handle_adxr', 'handle_apo',
    'handle_ppo', 'handle_mom', 'handle_bop', 'handle_cci',
    'handle_cmo', 'handle_roc', 'handle_rocr', 'handle_aroon',
    'handle_aroonosc', 'handle_mfi', 'handle_trix', 'handle_ultosc',
    'handle_dx',
    
    # Economic/fundamental data handlers
    'handle_real_gdp', 'handle_cpi', 'handle_inflation',
    'handle_treasury_yield', 'handle_income_statement',
    'handle_balance_sheet', 'handle_cash_flow',
    'handle_earnings', 'handle_news_sentiment',
    'handle_wti', 'handle_brent', 'handle_natural_gas',
    'handle_copper', 'handle_wheat', 'handle_corn',
    'handle_real_gdp_per_capita', 'handle_federal_funds_rate', 
    'handle_aluminum', 'handle_retail_sales', 'handle_durables',
    'handle_unemployment', 'handle_nonfarm_payroll', 'handle_cotton',
    'handle_sugar', 'handle_coffee', 'handle_all_commodities'
]

# Handler mapping dict for quick function lookup by tool name
HANDLER_MAPPING = {
    # Stock-related handlers
    'get-stock-quote': handle_stock_quote,
    'get-company-info': handle_company_info,
    'get-time-series': handle_time_series,
    'get-weekly-time-series': handle_time_series_weekly,
    'get-monthly-time-series': handle_time_series_monthly,
    'get-daily-adjusted-time-series': handle_time_series_daily_adjusted,
    'get-weekly-adjusted-time-series': handle_time_series_weekly_adjusted,
    'get-monthly-adjusted-time-series': handle_time_series_monthly_adjusted,
    'get-market-status': handle_market_status,
    'get-listing-status': handle_listing_status,
    'get-historical-options': handle_historical_options,
    'get-intraday-time-series': handle_intraday_time_series,
    'get-symbol-search': handle_symbol_search,
    'get-etf-profile': handle_etf_profile,
    'get-ipo-calendar': handle_ipo_calendar,
    'get-earnings-calendar': handle_earnings_calendar,
    'get-earnings-call-transcript': handle_earnings_call_transcript,
    'get-insider-transactions': handle_insider_transactions,
    'get-top-gainers-losers': handle_gainers_losers,
    
    # Cryptocurrency-related handlers
    'get-crypto-exchange-rate': handle_crypto_exchange_rate,
    'get-crypto-daily': handle_crypto_daily,
    'get-crypto-weekly': handle_crypto_weekly,
    'get-crypto-monthly': handle_crypto_monthly,
    'get-fx-rate': handle_fx_rate,
    'get-fx-daily': handle_fx_daily,
    'get-fx-weekly': handle_fx_weekly,
    'get-fx-monthly': handle_fx_monthly,
    
    # Technical indicator handlers
    'get-sma': handle_sma,
    'get-ema': handle_ema,
    'get-wma': handle_wma,
    'get-dema': handle_dema,
    'get-tema': handle_tema,
    'get-macd': handle_macd,
    'get-rsi': handle_rsi,
    'get-bbands': handle_bbands,
    'get-stoch': handle_stoch,
    'get-stochf': handle_stochf,
    'get-willr': handle_willr,
    'get-adx': handle_adx,
    'get-stochrsi': handle_stochrsi,
    'get-adxr': handle_adxr,
    'get-apo': handle_apo,
    'get-ppo': handle_ppo,
    'get-mom': handle_mom,
    'get-bop': handle_bop,
    'get-cci': handle_cci,
    'get-cmo': handle_cmo,
    'get-roc': handle_roc,
    'get-rocr': handle_rocr,
    'get-aroon': handle_aroon,
    'get-aroonosc': handle_aroonosc,
    'get-mfi': handle_mfi,
    'get-trix': handle_trix,
    'get-ultosc': handle_ultosc,
    'get-dx': handle_dx,
    
    # Economic/fundamental data handlers
    'get-real-gdp': handle_real_gdp,
    'get-cpi': handle_cpi,
    'get-inflation': handle_inflation,
    'get-treasury-yield': handle_treasury_yield,
    'get-income-statement': handle_income_statement,
    'get-balance-sheet': handle_balance_sheet,
    'get-cash-flow': handle_cash_flow,
    'get-earnings': handle_earnings,
    'get-news-sentiment': handle_news_sentiment,
    'get-wti': handle_wti,
    'get-brent': handle_brent,
    'get-natural-gas': handle_natural_gas,
    'get-copper': handle_copper,
    'get-wheat': handle_wheat,
    'get-corn': handle_corn,
    'get-real-gdp-per-capita': handle_real_gdp_per_capita,
    'get-federal-funds-rate': handle_federal_funds_rate,
    'get-aluminum': handle_aluminum,
    'get-retail-sales': handle_retail_sales,
    'get-durables': handle_durables,
    'get-unemployment': handle_unemployment,
    'get-nonfarm-payroll': handle_nonfarm_payroll,
    'get-cotton': handle_cotton,
    'get-sugar': handle_sugar,
    'get-coffee': handle_coffee,
    'get-all-commodities': handle_all_commodities
}