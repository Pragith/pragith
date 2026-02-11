import httpx
import os
from typing import Optional, Tuple

async def get_currency_from_ip(ip_address: str) -> str:
    """Get currency code based on IP address using ipapi.co (free tier: 1000 requests/day)"""
    # For local development, use CURRENCY env var if set
    if ip_address in ["127.0.0.1", "localhost"]:
        return os.getenv("CURRENCY", "USD")
    
    try:
        async with httpx.AsyncClient(timeout=2.0) as client:
            response = await client.get(f"https://ipapi.co/{ip_address}/currency/")
            if response.status_code == 200:
                currency = response.text.strip()
                # Validate it's a real currency code (3 letters)
                if len(currency) == 3 and currency.isalpha():
                    return currency.upper()
    except Exception:
        pass
    
    return "USD"  # Default fallback

async def get_exchange_rate(base_currency: str = "USD", target_currency: str = "USD") -> float:
    """Get exchange rate from USD to target currency using exchangerate-api.io (free tier)"""
    if base_currency == target_currency:
        return 1.0
    
    try:
        async with httpx.AsyncClient(timeout=2.0) as client:
            response = await client.get(f"https://api.exchangerate-api.com/v4/latest/{base_currency}")
            if response.status_code == 200:
                data = response.json()
                return data["rates"].get(target_currency, 1.0)
    except Exception:
        pass
    
    return 1.0  # Fallback to 1:1 if API fails

async def convert_rate(
    base_rate: float,
    ip_address: str
) -> Tuple[float, str, str]:
    """
    Convert base rate (USD) to user's local currency
    Returns: (converted_rate, currency_code, currency_symbol)
    """
    currency_code = await get_currency_from_ip(ip_address)
    exchange_rate = await get_exchange_rate("USD", currency_code)
    converted_rate = base_rate * exchange_rate
    
    # Currency symbols mapping
    currency_symbols = {
        "USD": "$",
        "EUR": "€",
        "GBP": "£",
        "JPY": "¥",
        "INR": "₹",
        "AUD": "A$",
        "CAD": "C$",
        "AED": "AED",
        "SAR": "SAR",
    }
    
    symbol = currency_symbols.get(currency_code, currency_code + " ")
    
    return (round(converted_rate, 2), currency_code, symbol)
