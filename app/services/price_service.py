import httpx

COINGECKO_URL = "https://api.coingecko.com/api/v3/simple/price"

SYMBOL_MAP = {
    "BTC": "bitcoin",
    "ETH": "ethereum",
    "SOL": "solana",
    "DOGE": "dogecoin"}

async def fetch_price(symbol: str) -> float:
    """
    Fetch the current price of a cryptocurrency by its symbol.
    
    Args:
        symbol (str): The symbol of the cryptocurrency (e.g., 'BTC', 'ETH').
    
    Returns:
        float: The current price of the cryptocurrency in USD.
    
    Raises:
        ValueError: If the symbol is not recognized.
        httpx.HTTPStatusError: If the API request fails.
    """
    coin_id = SYMBOL_MAP.get(symbol.upper())
    if not coin_id:
        raise ValueError(f"不支援的幣別：{symbol}")

    params = {"ids": coin_id, "vs_currencies": "usd"}
    
    async with httpx.AsyncClient() as client:
        response = await client.get(COINGECKO_URL, params=params)
        response.raise_for_status()
        data = response.json()
        return data[coin_id]['usd']