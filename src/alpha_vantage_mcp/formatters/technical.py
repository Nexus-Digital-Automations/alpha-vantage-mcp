"""
Formatters for technical indicator Alpha Vantage API responses.

This module provides functions for formatting technical indicators like
SMA, MACD, BBANDS, STOCH, and others.
"""

from typing import Any, Dict, List, Optional
from ..config.settings import MAX_DISPLAY_ITEMS
from .common import (
    format_number, format_percentage, format_date, 
    truncate_list, clean_key, extract_metadata,
    format_error_message
)

def format_technical_indicator(indicator_data: Dict[str, Any], indicator_name: str) -> str:
    """
    Format generic technical indicator data into a readable string.
    
    Args:
        indicator_data: The response data from Alpha Vantage Technical Indicator endpoints
        indicator_name: The name of the technical indicator (e.g., SMA, EMA)
        
    Returns:
        A formatted string containing the technical indicator information
    """
    try:
        # Find the main technical indicator data
        metadata = extract_metadata(indicator_data)
        indicator_key = next((k for k in indicator_data.keys() if "Technical Analysis" in k), None)
        
        if not indicator_key or not indicator_data[indicator_key]:
            return f"No {indicator_name} data available for this symbol."
            
        # Get indicator data and sort by date (most recent first)
        indicator_values = indicator_data[indicator_key]
        dates = sorted(indicator_values.keys(), reverse=True)
        
        # Create header
        symbol = metadata.get("symbol", "Unknown")
        interval = metadata.get("interval", "Unknown")
        time_period = metadata.get("time_period", "Unknown")
        series_type = metadata.get("series_type", "Unknown")
        last_refreshed = metadata.get("last_refreshed", "Unknown")
        
        output = f"Technical Indicator: {indicator_name} for {symbol}\n"
        output += f"Interval: {interval}, Time Period: {time_period}, Series Type: {series_type}\n"
        output += f"Last Refreshed: {last_refreshed}\n\n"
        
        # Add data points (limited to MAX_DISPLAY_ITEMS)
        for date in dates[:MAX_DISPLAY_ITEMS]:
            data_point = indicator_values[date]
            
            # For most technical indicators, there's just one value with the indicator name as the key
            indicator_value = data_point.get(indicator_name, "N/A")
            output += f"Date: {date}, {indicator_name}: {indicator_value}\n"
            
        # Add a note if there are more data points
        if len(dates) > MAX_DISPLAY_ITEMS:
            output += f"\n... and {len(dates) - MAX_DISPLAY_ITEMS} more data points."
            
        return output
    except Exception as e:
        return format_error_message(f"Error formatting {indicator_name} data: {str(e)}")

def format_bbands(indicator_data: Dict[str, Any]) -> str:
    """
    Format Bollinger Bands indicator data into a readable string.
    
    Args:
        indicator_data: The response data from the Alpha Vantage BBANDS endpoint
        
    Returns:
        A formatted string containing the Bollinger Bands information
    """
    try:
        # Find the main technical indicator data
        metadata = extract_metadata(indicator_data)
        indicator_key = next((k for k in indicator_data.keys() if "Technical Analysis" in k), None)
        
        if not indicator_key or not indicator_data[indicator_key]:
            return "No Bollinger Bands data available for this symbol."
            
        # Get indicator data and sort by date (most recent first)
        indicator_values = indicator_data[indicator_key]
        dates = sorted(indicator_values.keys(), reverse=True)
        
        # Create header
        symbol = metadata.get("symbol", "Unknown")
        interval = metadata.get("interval", "Unknown")
        time_period = metadata.get("time_period", "Unknown")
        series_type = metadata.get("series_type", "Unknown")
        last_refreshed = metadata.get("last_refreshed", "Unknown")
        
        output = f"Bollinger Bands (BBANDS) for {symbol}\n"
        output += f"Interval: {interval}, Time Period: {time_period}, Series Type: {series_type}\n"
        output += f"Last Refreshed: {last_refreshed}\n\n"
        
        # Add data points (limited to MAX_DISPLAY_ITEMS)
        for date in dates[:MAX_DISPLAY_ITEMS]:
            data_point = indicator_values[date]
            
            # Bollinger Bands have three values: upper, middle, and lower
            upper_band = data_point.get("Real Upper Band", "N/A")
            middle_band = data_point.get("Real Middle Band", "N/A")
            lower_band = data_point.get("Real Lower Band", "N/A")
            
            output += f"Date: {date}\n"
            output += f"  Upper Band: {upper_band}\n"
            output += f"  Middle Band: {middle_band}\n"
            output += f"  Lower Band: {lower_band}\n\n"
            
        # Add a note if there are more data points
        if len(dates) > MAX_DISPLAY_ITEMS:
            output += f"... and {len(dates) - MAX_DISPLAY_ITEMS} more data points."
            
        return output
    except Exception as e:
        return format_error_message(f"Error formatting Bollinger Bands data: {str(e)}")

def format_macd(indicator_data: Dict[str, Any]) -> str:
    """
    Format MACD indicator data into a readable string.
    
    Args:
        indicator_data: The response data from the Alpha Vantage MACD endpoint
        
    Returns:
        A formatted string containing the MACD information
    """
    try:
        # Find the main technical indicator data
        metadata = extract_metadata(indicator_data)
        indicator_key = next((k for k in indicator_data.keys() if "Technical Analysis" in k), None)
        
        if not indicator_key or not indicator_data[indicator_key]:
            return "No MACD data available for this symbol."
            
        # Get indicator data and sort by date (most recent first)
        indicator_values = indicator_data[indicator_key]
        dates = sorted(indicator_values.keys(), reverse=True)
        
        # Create header
        symbol = metadata.get("symbol", "Unknown")
        interval = metadata.get("interval", "Unknown")
        series_type = metadata.get("series_type", "Unknown")
        fast_period = metadata.get("fastperiod", "12")
        slow_period = metadata.get("slowperiod", "26")
        signal_period = metadata.get("signalperiod", "9")
        last_refreshed = metadata.get("last_refreshed", "Unknown")
        
        output = f"Moving Average Convergence/Divergence (MACD) for {symbol}\n"
        output += f"Interval: {interval}, FastP: {fast_period}, SlowP: {slow_period}, SignalP: {signal_period}\n"
        output += f"Last Refreshed: {last_refreshed}\n---\n"
        
        # Add data points (limited to MAX_DISPLAY_ITEMS)
        for date in dates[:MAX_DISPLAY_ITEMS]:
            data_point = indicator_values[date]
            
            # MACD has three values: MACD, MACD_Signal, and MACD_Hist
            macd_value = data_point.get("MACD", "N/A")
            macd_signal = data_point.get("MACD_Signal", "N/A")
            macd_hist = data_point.get("MACD_Hist", "N/A")
            
            output += f"Date: {date} -> MACD: {macd_value}, Signal: {macd_signal}, Hist: {macd_hist}\n"
            
        # Add a note if there are more data points
        if len(dates) > MAX_DISPLAY_ITEMS:
            output += f"\n... and {len(dates) - MAX_DISPLAY_ITEMS} more data points."
            
        return output
    except Exception as e:
        return format_error_message(f"Error formatting MACD data: {str(e)}")

def format_stoch(indicator_data: Dict[str, Any]) -> str:
    """
    Format Stochastic Oscillator (STOCH) indicator data into a readable string.
    
    Args:
        indicator_data: The response data from the Alpha Vantage STOCH endpoint
        
    Returns:
        A formatted string containing the Stochastic Oscillator information
    """
    try:
        # Find the main technical indicator data
        metadata = extract_metadata(indicator_data)
        indicator_key = next((k for k in indicator_data.keys() if "Technical Analysis" in k), None)
        
        if not indicator_key or not indicator_data[indicator_key]:
            return "No Stochastic Oscillator data available for this symbol."
            
        # Get indicator data and sort by date (most recent first)
        indicator_values = indicator_data[indicator_key]
        dates = sorted(indicator_values.keys(), reverse=True)
        
        # Create header
        symbol = metadata.get("symbol", "Unknown")
        interval = metadata.get("interval", "Unknown")
        fastkperiod = metadata.get("fastkperiod", "5")
        slowkperiod = metadata.get("slowkperiod", "3")
        slowdperiod = metadata.get("slowdperiod", "3")
        last_refreshed = metadata.get("last_refreshed", "Unknown")
        
        output = f"Stochastic Oscillator (STOCH) for {symbol}:\n\n"
        output += f"Technical Indicator: STOCH for {symbol}\n"
        output += f"Interval: {interval}, FastK: {fastkperiod}, SlowK: {slowkperiod}, SlowD: {slowdperiod}\n"
        output += f"Last Refreshed: {last_refreshed}\n\n"
        
        # Add data points (limited to MAX_DISPLAY_ITEMS)
        for date in dates[:MAX_DISPLAY_ITEMS]:
            data_point = indicator_values[date]
            
            # Stochastic Oscillator has two values: SlowK and SlowD
            slowk = data_point.get("SlowK", "N/A")
            slowd = data_point.get("SlowD", "N/A")
            
            output += f"Date: {date} -> SlowK: {slowk}, SlowD: {slowd}\n"
            
        # Add a note if there are more data points
        if len(dates) > MAX_DISPLAY_ITEMS:
            output += f"\n... and {len(dates) - MAX_DISPLAY_ITEMS} more data points."
            
        return output
    except Exception as e:
        return format_error_message(f"Error formatting Stochastic Oscillator data: {str(e)}")

def format_stochf(indicator_data: Dict[str, Any]) -> str:
    """
    Format Stochastic Fast (STOCHF) indicator data into a readable string.
    
    Args:
        indicator_data: The response data from the Alpha Vantage STOCHF endpoint
        
    Returns:
        A formatted string containing the Stochastic Fast information
    """
    try:
        # Find the main technical indicator data
        metadata = extract_metadata(indicator_data)
        indicator_key = next((k for k in indicator_data.keys() if "Technical Analysis" in k), None)
        
        if not indicator_key or not indicator_data[indicator_key]:
            return "No Stochastic Fast data available for this symbol."
            
        # Get indicator data and sort by date (most recent first)
        indicator_values = indicator_data[indicator_key]
        dates = sorted(indicator_values.keys(), reverse=True)
        
        # Create header
        symbol = metadata.get("symbol", "Unknown")
        interval = metadata.get("interval", "Unknown")
        fastkperiod = metadata.get("fastkperiod", "5")
        fastdperiod = metadata.get("fastdperiod", "3")
        last_refreshed = metadata.get("last_refreshed", "Unknown")
        
        output = f"Stochastic Fast (STOCHF) for {symbol}:\n\n"
        output += f"Technical Indicator: STOCHF for {symbol}\n"
        output += f"Interval: {interval}, FastK Period: {fastkperiod}, FastD Period: {fastdperiod}\n"
        output += f"Last Refreshed: {last_refreshed}\n\n"
        
        # Add data points (limited to MAX_DISPLAY_ITEMS)
        for date in dates[:MAX_DISPLAY_ITEMS]:
            data_point = indicator_values[date]
            
            # Stochastic Fast has two values: FastK and FastD
            fastk = data_point.get("FastK", "N/A")
            fastd = data_point.get("FastD", "N/A")
            
            output += f"Date: {date} -> FastK: {fastk}, FastD: {fastd}\n"
            
        # Add a note if there are more data points
        if len(dates) > MAX_DISPLAY_ITEMS:
            output += f"\n... and {len(dates) - MAX_DISPLAY_ITEMS} more data points."
            
        return output
    except Exception as e:
        return format_error_message(f"Error formatting Stochastic Fast data: {str(e)}")

def format_willr(indicator_data: Dict[str, Any]) -> str:
    """
    Format Williams' %R (WILLR) indicator data into a readable string.
    
    Args:
        indicator_data: The response data from the Alpha Vantage WILLR endpoint
        
    Returns:
        A formatted string containing the Williams' %R information
    """
    try:
        # Find the main technical indicator data
        metadata = extract_metadata(indicator_data)
        indicator_key = next((k for k in indicator_data.keys() if "Technical Analysis" in k), None)
        
        if not indicator_key or not indicator_data[indicator_key]:
            return "No Williams' %R data available for this symbol."
            
        # Get indicator data and sort by date (most recent first)
        indicator_values = indicator_data[indicator_key]
        dates = sorted(indicator_values.keys(), reverse=True)
        
        # Create header
        symbol = metadata.get("symbol", "Unknown")
        interval = metadata.get("interval", "Unknown")
        time_period = metadata.get("time_period", "14")
        last_refreshed = metadata.get("last_refreshed", "Unknown")
        
        output = f"Williams' %R (WILLR) for {symbol}:\n\n"
        output += f"Technical Indicator: WILLR for {symbol}\n"
        output += f"Interval: {interval}, Time Period: {time_period}\n"
        output += f"Last Refreshed: {last_refreshed}\n\n"
        
        # Add data points (limited to MAX_DISPLAY_ITEMS)
        for date in dates[:MAX_DISPLAY_ITEMS]:
            data_point = indicator_values[date]
            
            # Williams' %R has one value: WILLR
            willr = data_point.get("WILLR", "N/A")
            
            output += f"Date: {date} -> WILLR: {willr}\n"
            
        # Add a note if there are more data points
        if len(dates) > MAX_DISPLAY_ITEMS:
            output += f"\n... and {len(dates) - MAX_DISPLAY_ITEMS} more data points."
            
        return output
    except Exception as e:
        return format_error_message(f"Error formatting Williams' %R data: {str(e)}")

def format_adx(indicator_data: Dict[str, Any]) -> str:
    """
    Format Average Directional Movement Index (ADX) indicator data into a readable string.
    
    Args:
        indicator_data: The response data from the Alpha Vantage ADX endpoint
        
    Returns:
        A formatted string containing the ADX information
    """
    try:
        # Find the main technical indicator data
        metadata = extract_metadata(indicator_data)
        indicator_key = next((k for k in indicator_data.keys() if "Technical Analysis" in k), None)
        
        if not indicator_key or not indicator_data[indicator_key]:
            return "No ADX data available for this symbol."
            
        # Get indicator data and sort by date (most recent first)
        indicator_values = indicator_data[indicator_key]
        dates = sorted(indicator_values.keys(), reverse=True)
        
        # Create header
        symbol = metadata.get("symbol", "Unknown")
        interval = metadata.get("interval", "Unknown")
        time_period = metadata.get("time_period", "14")
        last_refreshed = metadata.get("last_refreshed", "Unknown")
        
        output = f"Average Directional Movement Index (ADX) for {symbol}:\n\n"
        output += f"Technical Indicator: ADX for {symbol}\n"
        output += f"Interval: {interval}, Time Period: {time_period}\n"
        output += f"Last Refreshed: {last_refreshed}\n\n"
        
        # Add data points (limited to MAX_DISPLAY_ITEMS)
        for date in dates[:MAX_DISPLAY_ITEMS]:
            data_point = indicator_values[date]
            
            # ADX has one value: ADX
            adx = data_point.get("ADX", "N/A")
            
            output += f"Date: {date} -> ADX: {adx}\n"
            
        # Add a note if there are more data points
        if len(dates) > MAX_DISPLAY_ITEMS:
            output += f"\n... and {len(dates) - MAX_DISPLAY_ITEMS} more data points."
            
        return output
    except Exception as e:
        return format_error_message(f"Error formatting ADX data: {str(e)}")

def format_stochrsi(indicator_data: Dict[str, Any]) -> str:
    """
    Format Stochastic Relative Strength Index (STOCHRSI) indicator data into a readable string.
    
    Args:
        indicator_data: The response data from the Alpha Vantage STOCHRSI endpoint
        
    Returns:
        A formatted string containing the STOCHRSI information
    """
    try:
        # Find the main technical indicator data
        metadata = extract_metadata(indicator_data)
        indicator_key = next((k for k in indicator_data.keys() if "Technical Analysis" in k), None)
        
        if not indicator_key or not indicator_data[indicator_key]:
            return "No Stochastic RSI data available for this symbol."
            
        # Get indicator data and sort by date (most recent first)
        indicator_values = indicator_data[indicator_key]
        dates = sorted(indicator_values.keys(), reverse=True)
        
        # Create header
        symbol = metadata.get("symbol", "Unknown")
        interval = metadata.get("interval", "Unknown")
        time_period = metadata.get("time_period", "14")
        series_type = metadata.get("series_type", "close")
        fastkperiod = metadata.get("fastkperiod", "5")
        fastdperiod = metadata.get("fastdperiod", "3")
        fastdmatype = metadata.get("fastdmatype", "0")
        last_refreshed = metadata.get("last_refreshed", "Unknown")
        
        # Get MA type name
        ma_types = {
            "0": "Simple Moving Average (SMA)",
            "1": "Exponential Moving Average (EMA)",
            "2": "Weighted Moving Average (WMA)",
            "3": "Double Exponential Moving Average (DEMA)",
            "4": "Triple Exponential Moving Average (TEMA)",
            "5": "Triangular Moving Average (TRIMA)",
            "6": "T3 Moving Average",
            "7": "Kaufman Adaptive Moving Average (KAMA)",
            "8": "MESA Adaptive Moving Average (MAMA)"
        }
        
        fastdmatype_name = ma_types.get(str(fastdmatype), f"MA Type {fastdmatype}")
        
        output = f"Stochastic Relative Strength Index (STOCHRSI) for {symbol}\n\n"
        output += f"Interval: {interval}, Time Period: {time_period}, Series Type: {series_type}\n"
        output += f"FastK Period: {fastkperiod}, FastD Period: {fastdperiod}, FastD MA Type: {fastdmatype_name}\n"
        output += f"Last Refreshed: {last_refreshed}\n\n"
        
        # Add data points (limited to MAX_DISPLAY_ITEMS)
        for date in dates[:MAX_DISPLAY_ITEMS]:
            data_point = indicator_values[date]
            
            # STOCHRSI typically has two values: FastK and FastD
            fastk = data_point.get("FastK", "N/A")
            fastd = data_point.get("FastD", "N/A")
            
            output += f"Date: {date}\n"
            output += f"  FastK: {fastk}\n"
            output += f"  FastD: {fastd}\n"
            
        # Add a note if there are more data points
        if len(dates) > MAX_DISPLAY_ITEMS:
            output += f"\n... and {len(dates) - MAX_DISPLAY_ITEMS} more data points."
            
        return output
    except Exception as e:
        return format_error_message(f"Error formatting STOCHRSI data: {str(e)}")

def format_adxr(indicator_data: Dict[str, Any]) -> str:
    """
    Format Average Directional Movement Index Rating (ADXR) indicator data into a readable string.
    
    Args:
        indicator_data: The response data from the Alpha Vantage ADXR endpoint
        
    Returns:
        A formatted string containing the ADXR information
    """
    try:
        # Find the main technical indicator data
        metadata = extract_metadata(indicator_data)
        indicator_key = next((k for k in indicator_data.keys() if "Technical Analysis" in k), None)
        
        if not indicator_key or not indicator_data[indicator_key]:
            return "No ADXR data available for this symbol."
            
        # Get indicator data and sort by date (most recent first)
        indicator_values = indicator_data[indicator_key]
        dates = sorted(indicator_values.keys(), reverse=True)
        
        # Create header
        symbol = metadata.get("symbol", "Unknown")
        interval = metadata.get("interval", "Unknown")
        time_period = metadata.get("time_period", "14")
        last_refreshed = metadata.get("last_refreshed", "Unknown")
        
        output = f"Average Directional Movement Index Rating (ADXR) for {symbol}\n\n"
        output += f"Interval: {interval}, Time Period: {time_period}\n"
        output += f"Last Refreshed: {last_refreshed}\n\n"
        
        # Add data points (limited to MAX_DISPLAY_ITEMS)
        for date in dates[:MAX_DISPLAY_ITEMS]:
            data_point = indicator_values[date]
            
            # ADXR has one value: ADXR
            adxr = data_point.get("ADXR", "N/A")
            
            output += f"Date: {date} -> ADXR: {adxr}\n"
            
        # Add a note if there are more data points
        if len(dates) > MAX_DISPLAY_ITEMS:
            output += f"\n... and {len(dates) - MAX_DISPLAY_ITEMS} more data points."
            
        return output
    except Exception as e:
        return format_error_message(f"Error formatting ADXR data: {str(e)}")

def format_apo(indicator_data: Dict[str, Any]) -> str:
    """
    Format Absolute Price Oscillator (APO) indicator data into a readable string.
    
    Args:
        indicator_data: The response data from the Alpha Vantage APO endpoint
        
    Returns:
        A formatted string containing the APO information
    """
    try:
        # Find the main technical indicator data
        metadata = extract_metadata(indicator_data)
        indicator_key = next((k for k in indicator_data.keys() if "Technical Analysis" in k), None)
        
        if not indicator_key or not indicator_data[indicator_key]:
            return "No APO data available for this symbol."
            
        # Get indicator data and sort by date (most recent first)
        indicator_values = indicator_data[indicator_key]
        dates = sorted(indicator_values.keys(), reverse=True)
        
        # Create header
        symbol = metadata.get("symbol", "Unknown")
        interval = metadata.get("interval", "Unknown")
        series_type = metadata.get("series_type", "close")
        fastperiod = metadata.get("fastperiod", "12")
        slowperiod = metadata.get("slowperiod", "26")
        matype = metadata.get("matype", "0")
        last_refreshed = metadata.get("last_refreshed", "Unknown")
        
        # Get MA type name
        ma_types = {
            "0": "Simple Moving Average (SMA)",
            "1": "Exponential Moving Average (EMA)",
            "2": "Weighted Moving Average (WMA)",
            "3": "Double Exponential Moving Average (DEMA)",
            "4": "Triple Exponential Moving Average (TEMA)",
            "5": "Triangular Moving Average (TRIMA)",
            "6": "T3 Moving Average",
            "7": "Kaufman Adaptive Moving Average (KAMA)",
            "8": "MESA Adaptive Moving Average (MAMA)"
        }
        
        matype_name = ma_types.get(str(matype), f"MA Type {matype}")
        
        output = f"Absolute Price Oscillator (APO) for {symbol}\n\n"
        output += f"Interval: {interval}, Series Type: {series_type}\n"
        output += f"Fast Period: {fastperiod}, Slow Period: {slowperiod}, MA Type: {matype_name}\n"
        output += f"Last Refreshed: {last_refreshed}\n\n"
        
        # Add data points (limited to MAX_DISPLAY_ITEMS)
        for date in dates[:MAX_DISPLAY_ITEMS]:
            data_point = indicator_values[date]
            
            # APO has one value: APO
            apo = data_point.get("APO", "N/A")
            
            output += f"Date: {date} -> APO: {apo}\n"
            
        # Add a note if there are more data points
        if len(dates) > MAX_DISPLAY_ITEMS:
            output += f"\n... and {len(dates) - MAX_DISPLAY_ITEMS} more data points."
            
        return output
    except Exception as e:
        return format_error_message(f"Error formatting APO data: {str(e)}")

def format_ppo(indicator_data: Dict[str, Any]) -> str:
    """
    Format Percentage Price Oscillator (PPO) indicator data into a readable string.
    
    Args:
        indicator_data: The response data from the Alpha Vantage PPO endpoint
        
    Returns:
        A formatted string containing the PPO information
    """
    try:
        # Find the main technical indicator data
        metadata = extract_metadata(indicator_data)
        indicator_key = next((k for k in indicator_data.keys() if "Technical Analysis" in k), None)
        
        if not indicator_key or not indicator_data[indicator_key]:
            return "No PPO data available for this symbol."
            
        # Get indicator data and sort by date (most recent first)
        indicator_values = indicator_data[indicator_key]
        dates = sorted(indicator_values.keys(), reverse=True)
        
        # Create header
        symbol = metadata.get("symbol", "Unknown")
        interval = metadata.get("interval", "Unknown")
        series_type = metadata.get("series_type", "close")
        fastperiod = metadata.get("fastperiod", "12")
        slowperiod = metadata.get("slowperiod", "26")
        matype = metadata.get("matype", "0")
        last_refreshed = metadata.get("last_refreshed", "Unknown")
        
        # Get MA type name
        ma_types = {
            "0": "Simple Moving Average (SMA)",
            "1": "Exponential Moving Average (EMA)",
            "2": "Weighted Moving Average (WMA)",
            "3": "Double Exponential Moving Average (DEMA)",
            "4": "Triple Exponential Moving Average (TEMA)",
            "5": "Triangular Moving Average (TRIMA)",
            "6": "T3 Moving Average",
            "7": "Kaufman Adaptive Moving Average (KAMA)",
            "8": "MESA Adaptive Moving Average (MAMA)"
        }
        
        matype_name = ma_types.get(str(matype), f"MA Type {matype}")
        
        output = f"Percentage Price Oscillator (PPO) for {symbol}\n\n"
        output += f"Interval: {interval}, Series Type: {series_type}\n"
        output += f"Fast Period: {fastperiod}, Slow Period: {slowperiod}, MA Type: {matype_name}\n"
        output += f"Last Refreshed: {last_refreshed}\n\n"
        
        # Add data points (limited to MAX_DISPLAY_ITEMS)
        for date in dates[:MAX_DISPLAY_ITEMS]:
            data_point = indicator_values[date]
            
            # PPO has one value: PPO
            ppo = data_point.get("PPO", "N/A")
            
            output += f"Date: {date} -> PPO: {ppo}\n"
            
        # Add a note if there are more data points
        if len(dates) > MAX_DISPLAY_ITEMS:
            output += f"\n... and {len(dates) - MAX_DISPLAY_ITEMS} more data points."
            
        return output
    except Exception as e:
        return format_error_message(f"Error formatting PPO data: {str(e)}")

def format_mom(indicator_data: Dict[str, Any]) -> str:
    """
    Format Momentum (MOM) indicator data into a readable string.
    
    Args:
        indicator_data: The response data from the Alpha Vantage MOM endpoint
        
    Returns:
        A formatted string containing the Momentum information
    """
    try:
        # Find the main technical indicator data
        metadata = extract_metadata(indicator_data)
        indicator_key = next((k for k in indicator_data.keys() if "Technical Analysis" in k), None)
        
        if not indicator_key or not indicator_data[indicator_key]:
            return "No Momentum data available for this symbol."
            
        # Get indicator data and sort by date (most recent first)
        indicator_values = indicator_data[indicator_key]
        dates = sorted(indicator_values.keys(), reverse=True)
        
        # Create header
        symbol = metadata.get("symbol", "Unknown")
        interval = metadata.get("interval", "Unknown")
        time_period = metadata.get("time_period", "10")
        series_type = metadata.get("series_type", "close")
        last_refreshed = metadata.get("last_refreshed", "Unknown")
        
        output = f"Momentum (MOM) for {symbol}\n\n"
        output += f"Interval: {interval}, Time Period: {time_period}, Series Type: {series_type}\n"
        output += f"Last Refreshed: {last_refreshed}\n\n"
        
        # Add data points (limited to MAX_DISPLAY_ITEMS)
        for date in dates[:MAX_DISPLAY_ITEMS]:
            data_point = indicator_values[date]
            
            # MOM has one value: MOM
            mom = data_point.get("MOM", "N/A")
            
            output += f"Date: {date} -> MOM: {mom}\n"
            
        # Add a note if there are more data points
        if len(dates) > MAX_DISPLAY_ITEMS:
            output += f"\n... and {len(dates) - MAX_DISPLAY_ITEMS} more data points."
            
        return output
    except Exception as e:
        return format_error_message(f"Error formatting MOM data: {str(e)}")

def format_bop(indicator_data: Dict[str, Any]) -> str:
    """
    Format Balance Of Power (BOP) indicator data into a readable string.
    
    Args:
        indicator_data: The response data from the Alpha Vantage BOP endpoint
        
    Returns:
        A formatted string containing the BOP information
    """
    try:
        # Find the main technical indicator data
        metadata = extract_metadata(indicator_data)
        indicator_key = next((k for k in indicator_data.keys() if "Technical Analysis" in k), None)
        
        if not indicator_key or not indicator_data[indicator_key]:
            return "No Balance Of Power data available for this symbol."
            
        # Get indicator data and sort by date (most recent first)
        indicator_values = indicator_data[indicator_key]
        dates = sorted(indicator_values.keys(), reverse=True)
        
        # Create header
        symbol = metadata.get("symbol", "Unknown")
        interval = metadata.get("interval", "Unknown")
        last_refreshed = metadata.get("last_refreshed", "Unknown")
        
        output = f"Balance Of Power (BOP) for {symbol}\n\n"
        output += f"Interval: {interval}\n"
        output += f"Last Refreshed: {last_refreshed}\n\n"
        
        # Add data points (limited to MAX_DISPLAY_ITEMS)
        for date in dates[:MAX_DISPLAY_ITEMS]:
            data_point = indicator_values[date]
            
            # BOP has one value: BOP
            bop = data_point.get("BOP", "N/A")
            
            output += f"Date: {date} -> BOP: {bop}\n"
            
        # Add a note if there are more data points
        if len(dates) > MAX_DISPLAY_ITEMS:
            output += f"\n... and {len(dates) - MAX_DISPLAY_ITEMS} more data points."
            
        return output
    except Exception as e:
        return format_error_message(f"Error formatting BOP data: {str(e)}")

def format_cci(indicator_data: Dict[str, Any]) -> str:
    """
    Format Commodity Channel Index (CCI) indicator data into a readable string.
    
    Args:
        indicator_data: The response data from the Alpha Vantage CCI endpoint
        
    Returns:
        A formatted string containing the CCI information
    """
    try:
        # Find the main technical indicator data
        metadata = extract_metadata(indicator_data)
        indicator_key = next((k for k in indicator_data.keys() if "Technical Analysis" in k), None)
        
        if not indicator_key or not indicator_data[indicator_key]:
            return "No Commodity Channel Index data available for this symbol."
            
        # Get indicator data and sort by date (most recent first)
        indicator_values = indicator_data[indicator_key]
        dates = sorted(indicator_values.keys(), reverse=True)
        
        # Create header
        symbol = metadata.get("symbol", "Unknown")
        interval = metadata.get("interval", "Unknown")
        time_period = metadata.get("time_period", "20")
        last_refreshed = metadata.get("last_refreshed", "Unknown")
        
        output = f"Commodity Channel Index (CCI) for {symbol}\n\n"
        output += f"Interval: {interval}, Time Period: {time_period}\n"
        output += f"Last Refreshed: {last_refreshed}\n\n"
        
        # Add data points (limited to MAX_DISPLAY_ITEMS)
        for date in dates[:MAX_DISPLAY_ITEMS]:
            data_point = indicator_values[date]
            
            # CCI has one value: CCI
            cci = data_point.get("CCI", "N/A")
            
            output += f"Date: {date} -> CCI: {cci}\n"
            
        # Add a note if there are more data points
        if len(dates) > MAX_DISPLAY_ITEMS:
            output += f"\n... and {len(dates) - MAX_DISPLAY_ITEMS} more data points."
            
        return output
    except Exception as e:
        return format_error_message(f"Error formatting CCI data: {str(e)}")

def format_cmo(indicator_data: Dict[str, Any]) -> str:
    """
    Format Chande Momentum Oscillator (CMO) data into a readable string.
    
    Args:
        indicator_data: The response data from the Alpha Vantage CMO endpoint
        
    Returns:
        A formatted string containing the CMO information
    """
    try:
        # Find the main technical indicator data
        metadata = extract_metadata(indicator_data)
        indicator_key = next((k for k in indicator_data.keys() if "Technical Analysis" in k), None)
        
        if not indicator_key or not indicator_data[indicator_key]:
            return "No CMO data available for this symbol."
            
        # Get indicator data and sort by date (most recent first)
        indicator_values = indicator_data[indicator_key]
        dates = sorted(indicator_values.keys(), reverse=True)
        
        # Create header
        symbol = metadata.get("symbol", "Unknown")
        interval = metadata.get("interval", "Unknown")
        time_period = metadata.get("time_period", "Unknown")
        series_type = metadata.get("series_type", "Unknown")
        last_refreshed = metadata.get("last_refreshed", "Unknown")
        
        output = f"Chande Momentum Oscillator (CMO) for {symbol}\n\n"
        output += f"Interval: {interval}, Time Period: {time_period}, Series Type: {series_type}\n"
        output += f"Last Refreshed: {last_refreshed}\n\n"
        
        # Add data points (limited to MAX_DISPLAY_ITEMS)
        for date in dates[:MAX_DISPLAY_ITEMS]:
            point_data = indicator_values[date]
            cmo_value = point_data.get("CMO", "N/A")
            
            # Format as number
            try:
                cmo_float = float(cmo_value)
                cmo_value = f"{cmo_float:.4f}"
            except (ValueError, TypeError):
                pass
                
            output += f"Date: {date} -> CMO: {cmo_value}\n"
            
        # Add a note if there are more data points
        if len(dates) > MAX_DISPLAY_ITEMS:
            output += f"\n... and {len(dates) - MAX_DISPLAY_ITEMS} more data points."
            
        return output
    except Exception as e:
        return format_error_message(f"Error formatting CMO data: {str(e)}")

def format_roc(indicator_data: Dict[str, Any]) -> str:
    """
    Format Rate of Change (ROC) data into a readable string.
    
    Args:
        indicator_data: The response data from the Alpha Vantage ROC endpoint
        
    Returns:
        A formatted string containing the ROC information
    """
    try:
        # Find the main technical indicator data
        metadata = extract_metadata(indicator_data)
        indicator_key = next((k for k in indicator_data.keys() if "Technical Analysis" in k), None)
        
        if not indicator_key or not indicator_data[indicator_key]:
            return "No ROC data available for this symbol."
            
        # Get indicator data and sort by date (most recent first)
        indicator_values = indicator_data[indicator_key]
        dates = sorted(indicator_values.keys(), reverse=True)
        
        # Create header
        symbol = metadata.get("symbol", "Unknown")
        interval = metadata.get("interval", "Unknown")
        time_period = metadata.get("time_period", "Unknown")
        series_type = metadata.get("series_type", "Unknown")
        last_refreshed = metadata.get("last_refreshed", "Unknown")
        
        output = f"Rate of Change (ROC) for {symbol}\n\n"
        output += f"Interval: {interval}, Time Period: {time_period}, Series Type: {series_type}\n"
        output += f"Last Refreshed: {last_refreshed}\n\n"
        
        # Add data points (limited to MAX_DISPLAY_ITEMS)
        for date in dates[:MAX_DISPLAY_ITEMS]:
            point_data = indicator_values[date]
            roc_value = point_data.get("ROC", "N/A")
            
            # Format as percentage
            try:
                roc_float = float(roc_value)
                roc_value = f"{roc_float:.4f}%"
            except (ValueError, TypeError):
                pass
                
            output += f"Date: {date} -> ROC: {roc_value}\n"
            
        # Add a note if there are more data points
        if len(dates) > MAX_DISPLAY_ITEMS:
            output += f"\n... and {len(dates) - MAX_DISPLAY_ITEMS} more data points."
            
        return output
    except Exception as e:
        return format_error_message(f"Error formatting ROC data: {str(e)}")

def format_rocr(indicator_data: Dict[str, Any]) -> str:
    """
    Format Rate of Change Ratio (ROCR) data into a readable string.
    
    Args:
        indicator_data: The response data from the Alpha Vantage ROCR endpoint
        
    Returns:
        A formatted string containing the ROCR information
    """
    try:
        # Find the main technical indicator data
        metadata = extract_metadata(indicator_data)
        indicator_key = next((k for k in indicator_data.keys() if "Technical Analysis" in k), None)
        
        if not indicator_key or not indicator_data[indicator_key]:
            return "No ROCR data available for this symbol."
            
        # Get indicator data and sort by date (most recent first)
        indicator_values = indicator_data[indicator_key]
        dates = sorted(indicator_values.keys(), reverse=True)
        
        # Create header
        symbol = metadata.get("symbol", "Unknown")
        interval = metadata.get("interval", "Unknown")
        time_period = metadata.get("time_period", "Unknown")
        series_type = metadata.get("series_type", "Unknown")
        last_refreshed = metadata.get("last_refreshed", "Unknown")
        
        output = f"Rate of Change Ratio (ROCR) for {symbol}\n\n"
        output += f"Interval: {interval}, Time Period: {time_period}, Series Type: {series_type}\n"
        output += f"Last Refreshed: {last_refreshed}\n\n"
        
        # Add data points (limited to MAX_DISPLAY_ITEMS)
        for date in dates[:MAX_DISPLAY_ITEMS]:
            point_data = indicator_values[date]
            rocr_value = point_data.get("ROCR", "N/A")
            
            # Format as ratio
            try:
                rocr_float = float(rocr_value)
                rocr_value = f"{rocr_float:.4f}"
            except (ValueError, TypeError):
                pass
                
            output += f"Date: {date} -> ROCR: {rocr_value}\n"
            
        # Add a note if there are more data points
        if len(dates) > MAX_DISPLAY_ITEMS:
            output += f"\n... and {len(dates) - MAX_DISPLAY_ITEMS} more data points."
            
        return output
    except Exception as e:
        return format_error_message(f"Error formatting ROCR data: {str(e)}")

def format_aroon(indicator_data: Dict[str, Any]) -> str:
    """
    Format Aroon indicator data into a readable string.
    
    Args:
        indicator_data: The response data from the Alpha Vantage AROON endpoint
        
    Returns:
        A formatted string containing the Aroon information
    """
    try:
        # Find the main technical indicator data
        metadata = extract_metadata(indicator_data)
        indicator_key = next((k for k in indicator_data.keys() if "Technical Analysis" in k), None)
        
        if not indicator_key or not indicator_data[indicator_key]:
            return "No Aroon data available for this symbol."
            
        # Get indicator data and sort by date (most recent first)
        indicator_values = indicator_data[indicator_key]
        dates = sorted(indicator_values.keys(), reverse=True)
        
        # Create header
        symbol = metadata.get("symbol", "Unknown")
        interval = metadata.get("interval", "Unknown")
        time_period = metadata.get("time_period", "Unknown")
        last_refreshed = metadata.get("last_refreshed", "Unknown")
        
        output = f"Aroon Indicator for {symbol}\n\n"
        output += f"Interval: {interval}, Time Period: {time_period}\n"
        output += f"Last Refreshed: {last_refreshed}\n\n"
        
        # Add data points (limited to MAX_DISPLAY_ITEMS)
        for date in dates[:MAX_DISPLAY_ITEMS]:
            point_data = indicator_values[date]
            aroon_up = point_data.get("Aroon Up", "N/A")
            aroon_down = point_data.get("Aroon Down", "N/A")
            
            # Format as percentage
            try:
                aroon_up_float = float(aroon_up)
                aroon_up = f"{aroon_up_float:.2f}"
            except (ValueError, TypeError):
                pass
                
            try:
                aroon_down_float = float(aroon_down)
                aroon_down = f"{aroon_down_float:.2f}"
            except (ValueError, TypeError):
                pass
                
            output += f"Date: {date}\n"
            output += f"  Aroon Up: {aroon_up}\n"
            output += f"  Aroon Down: {aroon_down}\n"
            
        # Add a note if there are more data points
        if len(dates) > MAX_DISPLAY_ITEMS:
            output += f"\n... and {len(dates) - MAX_DISPLAY_ITEMS} more data points."
            
        return output
    except Exception as e:
        return format_error_message(f"Error formatting Aroon data: {str(e)}")

def format_aroonosc(indicator_data: Dict[str, Any]) -> str:
    """
    Format Aroon Oscillator data into a readable string.
    
    Args:
        indicator_data: The response data from the Alpha Vantage AROONOSC endpoint
        
    Returns:
        A formatted string containing the Aroon Oscillator information
    """
    try:
        # Find the main technical indicator data
        metadata = extract_metadata(indicator_data)
        indicator_key = next((k for k in indicator_data.keys() if "Technical Analysis" in k), None)
        
        if not indicator_key or not indicator_data[indicator_key]:
            return "No Aroon Oscillator data available for this symbol."
            
        # Get indicator data and sort by date (most recent first)
        indicator_values = indicator_data[indicator_key]
        dates = sorted(indicator_values.keys(), reverse=True)
        
        # Create header
        symbol = metadata.get("symbol", "Unknown")
        interval = metadata.get("interval", "Unknown")
        time_period = metadata.get("time_period", "Unknown")
        last_refreshed = metadata.get("last_refreshed", "Unknown")
        
        output = f"Aroon Oscillator for {symbol}\n\n"
        output += f"Interval: {interval}, Time Period: {time_period}\n"
        output += f"Last Refreshed: {last_refreshed}\n\n"
        
        # Add data points (limited to MAX_DISPLAY_ITEMS)
        for date in dates[:MAX_DISPLAY_ITEMS]:
            point_data = indicator_values[date]
            aroonosc = point_data.get("AROONOSC", "N/A")
            
            # Format as float
            try:
                aroonosc_float = float(aroonosc)
                aroonosc = f"{aroonosc_float:.2f}"
            except (ValueError, TypeError):
                pass
                
            output += f"Date: {date} -> AROONOSC: {aroonosc}\n"
            
        # Add a note if there are more data points
        if len(dates) > MAX_DISPLAY_ITEMS:
            output += f"\n... and {len(dates) - MAX_DISPLAY_ITEMS} more data points."
            
        return output
    except Exception as e:
        return format_error_message(f"Error formatting Aroon Oscillator data: {str(e)}")

def format_mfi(indicator_data: Dict[str, Any]) -> str:
    """
    Format Money Flow Index (MFI) indicator data into a readable string.
    
    Args:
        indicator_data: The response data from the Alpha Vantage MFI endpoint
        
    Returns:
        A formatted string containing the Money Flow Index information
    """
    try:
        # Find the main technical indicator data
        metadata = extract_metadata(indicator_data)
        indicator_key = next((k for k in indicator_data.keys() if "Technical Analysis" in k), None)
        
        if not indicator_key or not indicator_data[indicator_key]:
            return "No Money Flow Index data available for this symbol."
            
        # Get indicator data and sort by date (most recent first)
        indicator_values = indicator_data[indicator_key]
        dates = sorted(indicator_values.keys(), reverse=True)
        
        # Create header
        symbol = metadata.get("symbol", "Unknown")
        interval = metadata.get("interval", "Unknown")
        time_period = metadata.get("time_period", "Unknown")
        last_refreshed = metadata.get("last_refreshed", "Unknown")
        
        output = f"Money Flow Index (MFI) for {symbol}\n\n"
        output += f"Interval: {interval}, Time Period: {time_period}\n"
        output += f"Last Refreshed: {last_refreshed}\n\n"
        
        # Add data points (limited to MAX_DISPLAY_ITEMS)
        for date in dates[:MAX_DISPLAY_ITEMS]:
            point_data = indicator_values[date]
            mfi = point_data.get("MFI", "N/A")
            
            # Format as float
            try:
                mfi_float = float(mfi)
                mfi = f"{mfi_float:.2f}"
            except (ValueError, TypeError):
                pass
                
            output += f"Date: {date} -> MFI: {mfi}\n"
            
        # Add a note if there are more data points
        if len(dates) > MAX_DISPLAY_ITEMS:
            output += f"\n... and {len(dates) - MAX_DISPLAY_ITEMS} more data points."
            
        return output
    except Exception as e:
        return format_error_message(f"Error formatting Money Flow Index data: {str(e)}")

def format_trix(indicator_data: Dict[str, Any]) -> str:
    """
    Format Triple Exponential Moving Average (TRIX) indicator data into a readable string.
    
    Args:
        indicator_data: The response data from the Alpha Vantage TRIX endpoint
        
    Returns:
        A formatted string containing the TRIX information
    """
    try:
        # Find the main technical indicator data
        metadata = extract_metadata(indicator_data)
        indicator_key = next((k for k in indicator_data.keys() if "Technical Analysis" in k), None)
        
        if not indicator_key or not indicator_data[indicator_key]:
            return "No TRIX data available for this symbol."
            
        # Get indicator data and sort by date (most recent first)
        indicator_values = indicator_data[indicator_key]
        dates = sorted(indicator_values.keys(), reverse=True)
        
        # Create header
        symbol = metadata.get("symbol", "Unknown")
        interval = metadata.get("interval", "Unknown")
        time_period = metadata.get("time_period", "Unknown")
        series_type = metadata.get("series_type", "Unknown")
        last_refreshed = metadata.get("last_refreshed", "Unknown")
        
        output = f"Triple Exponential Moving Average (TRIX) for {symbol}\n\n"
        output += f"Interval: {interval}, Time Period: {time_period}, Series Type: {series_type}\n"
        output += f"Last Refreshed: {last_refreshed}\n\n"
        
        # Add data points (limited to MAX_DISPLAY_ITEMS)
        for date in dates[:MAX_DISPLAY_ITEMS]:
            point_data = indicator_values[date]
            trix = point_data.get("TRIX", "N/A")
            
            # Format as float with 6 decimal places since TRIX values are typically small decimals
            try:
                trix_float = float(trix)
                trix = f"{trix_float:.6f}"
            except (ValueError, TypeError):
                pass
                
            output += f"Date: {date} -> TRIX: {trix}\n"
            
        # Add a note if there are more data points
        if len(dates) > MAX_DISPLAY_ITEMS:
            output += f"\n... and {len(dates) - MAX_DISPLAY_ITEMS} more data points."
            
        return output
    except Exception as e:
        return format_error_message(f"Error formatting TRIX data: {str(e)}")

def format_ultosc(indicator_data: Dict[str, Any]) -> str:
    """
    Format Ultimate Oscillator (ULTOSC) indicator data into a readable string.
    
    Args:
        indicator_data: The response data from the Alpha Vantage ULTOSC endpoint
        
    Returns:
        A formatted string containing the Ultimate Oscillator information
    """
    try:
        # Find the main technical indicator data
        metadata = extract_metadata(indicator_data)
        indicator_key = next((k for k in indicator_data.keys() if "Technical Analysis" in k), None)
        
        if not indicator_key or not indicator_data[indicator_key]:
            return "No Ultimate Oscillator data available for this symbol."
            
        # Get indicator data and sort by date (most recent first)
        indicator_values = indicator_data[indicator_key]
        dates = sorted(indicator_values.keys(), reverse=True)
        
        # Create header
        symbol = metadata.get("symbol", "Unknown")
        interval = metadata.get("interval", "Unknown")
        timeperiod1 = metadata.get("timeperiod1", "7")
        timeperiod2 = metadata.get("timeperiod2", "14")
        timeperiod3 = metadata.get("timeperiod3", "28")
        last_refreshed = metadata.get("last_refreshed", "Unknown")
        
        output = f"Ultimate Oscillator (ULTOSC) for {symbol}\n\n"
        output += f"Interval: {interval}, Time Periods: {timeperiod1}/{timeperiod2}/{timeperiod3}\n"
        output += f"Last Refreshed: {last_refreshed}\n\n"
        
        # Add data points (limited to MAX_DISPLAY_ITEMS)
        for date in dates[:MAX_DISPLAY_ITEMS]:
            point_data = indicator_values[date]
            ultosc = point_data.get("ULTOSC", "N/A")
            
            # Format as float with 2 decimal places
            try:
                ultosc_float = float(ultosc)
                ultosc = f"{ultosc_float:.2f}"
            except (ValueError, TypeError):
                pass
                
            output += f"Date: {date} -> ULTOSC: {ultosc}\n"
            
        # Add a note if there are more data points
        if len(dates) > MAX_DISPLAY_ITEMS:
            output += f"\n... and {len(dates) - MAX_DISPLAY_ITEMS} more data points."
            
        return output
    except Exception as e:
        return format_error_message(f"Error formatting Ultimate Oscillator data: {str(e)}")

def format_dx(indicator_data: Dict[str, Any]) -> str:
    """
    Format Directional Movement Index (DX) indicator data into a readable string.
    
    Args:
        indicator_data: The response data from the Alpha Vantage DX endpoint
        
    Returns:
        A formatted string containing the DX information
    """
    try:
        # Find the main technical indicator data
        metadata = extract_metadata(indicator_data)
        indicator_key = next((k for k in indicator_data.keys() if "Technical Analysis" in k), None)
        
        if not indicator_key or not indicator_data[indicator_key]:
            return "No DX data available for this symbol."
            
        # Get indicator data and sort by date (most recent first)
        indicator_values = indicator_data[indicator_key]
        dates = sorted(indicator_values.keys(), reverse=True)
        
        # Create header
        symbol = metadata.get("symbol", "Unknown")
        interval = metadata.get("interval", "Unknown")
        time_period = metadata.get("time_period", "14")
        last_refreshed = metadata.get("last_refreshed", "Unknown")
        
        output = f"Directional Movement Index (DX) for {symbol}\n\n"
        output += f"Interval: {interval}, Time Period: {time_period}\n"
        output += f"Last Refreshed: {last_refreshed}\n\n"
        
        # Add data points (limited to MAX_DISPLAY_ITEMS)
        for date in dates[:MAX_DISPLAY_ITEMS]:
            point_data = indicator_values[date]
            dx = point_data.get("DX", "N/A")
            
            # Format as float with 2 decimal places
            try:
                dx_float = float(dx)
                dx = f"{dx_float:.2f}"
            except (ValueError, TypeError):
                pass
                
            output += f"Date: {date} -> DX: {dx}\n"
            
        # Add a note if there are more data points
        if len(dates) > MAX_DISPLAY_ITEMS:
            output += f"\n... and {len(dates) - MAX_DISPLAY_ITEMS} more data points."
            
        return output
    except Exception as e:
        return format_error_message(f"Error formatting DX data: {str(e)}")

# Export all formatters
__all__ = [
    'format_technical_indicator',
    'format_bbands',
    'format_macd',
    'format_stoch',
    'format_stochf',
    'format_willr',
    'format_adx',
    'format_stochrsi',
    'format_adxr',
    'format_apo',
    'format_ppo',
    'format_mom',
    'format_bop',
    'format_cci',
    'format_cmo',
    'format_roc',
    'format_rocr',
    'format_aroon',
    'format_aroonosc',
    'format_mfi',
    'format_trix',
    'format_ultosc',
    'format_dx'
]