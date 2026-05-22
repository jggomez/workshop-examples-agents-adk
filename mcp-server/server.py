import platform
import re
from fastmcp import FastMCP
import httpx
import psutil

# Initialize the FastMCP server
mcp = FastMCP("SystemAndCryptoMCP")


def is_alphanumeric_or_hyphen(text: str) -> bool:
    """Validate that the input contains only alphanumeric characters, hyphens, or underscores.

    Args:
        text (str): The input string to validate.

    Returns:
        bool: True if valid, False otherwise.
    """
    return bool(re.match(r"^[a-zA-Z0-9\-_]{1,50}$", text))


@mcp.tool()
def get_system_status() -> dict:
    """Get the current system status including operating system and CPU percentage.

    Returns:
        dict: A dictionary containing:
            - 'os_name': The operating system (e.g. Darwin, Windows, Linux).
            - 'os_release': The release version of the OS.
            - 'cpu_percentage': Current overall CPU usage percentage (measured over 0.5s).
            - 'ram_percentage': Physical memory usage percentage.
    """
    os_name = platform.system()
    os_release = platform.release()
    cpu_usage_percent = psutil.cpu_percent(interval=0.5)
    ram_usage_percent = psutil.virtual_memory().percent

    return {
        "os_name": os_name,
        "os_release": os_release,
        "cpu_percentage": cpu_usage_percent,
        "ram_percentage": ram_usage_percent,
    }


@mcp.tool()
async def get_crypto_price(crypto_id: str, vs_currency: str = "usd") -> dict:
    """Retrieve the current price of a cryptocurrency in a target currency using the CoinGecko public API.

    Args:
        crypto_id (str): The ID of the cryptocurrency on CoinGecko (e.g., 'bitcoin', 'ethereum').
        vs_currency (str): The target currency (e.g., 'usd', 'eur'). Defaults to 'usd'.

    Returns:
        dict: A dictionary containing the price details or error information.
    """
    clean_crypto_id = crypto_id.strip().lower()
    clean_vs_currency = vs_currency.strip().lower()

    # Input Validation (Zero Trust Policy)
    if not is_alphanumeric_or_hyphen(clean_crypto_id):
        raise ValueError(
            f"Invalid characters in crypto_id: '{crypto_id}'. "
            "Only alphanumeric characters, hyphens, and underscores are allowed (1-50 characters)."
        )

    if not is_alphanumeric_or_hyphen(clean_vs_currency):
        raise ValueError(
            f"Invalid characters in vs_currency: '{vs_currency}'. "
            "Only alphanumeric characters, hyphens, and underscores are allowed (1-50 characters)."
        )

    coingecko_api_url = "https://api.coingecko.com/api/v3/simple/price"
    query_parameters = {
        "ids": clean_crypto_id,
        "vs_currencies": clean_vs_currency,
    }
    request_headers = {"accept": "application/json"}

    async with httpx.AsyncClient(timeout=10.0) as http_client:
        response = await http_client.get(
            coingecko_api_url, params=query_parameters, headers=request_headers
        )

        if response.status_code != 200:
            return {
                "error": f"Failed to retrieve data from CoinGecko API. HTTP Status Code: {response.status_code}",
                "api_response_body": response.text,
            }

        price_results = response.json()

        if (
            clean_crypto_id not in price_results
            or clean_vs_currency not in price_results[clean_crypto_id]
        ):
            return {
                "error": (
                    f"Cryptocurrency '{crypto_id}' or target currency '{vs_currency}' "
                    "not found in CoinGecko API response."
                ),
                "api_response_body": price_results,
            }

        crypto_price = price_results[clean_crypto_id][clean_vs_currency]

        return {
            "cryptocurrency_id": clean_crypto_id,
            "target_currency": clean_vs_currency,
            "price": crypto_price,
        }


if __name__ == "__main__":
    import os

    # Cloud Run sets $PORT dynamically; fallback to 8000 for local development
    port = int(os.environ.get("PORT", 8080))
    mcp.run(transport="streamable-http", host="0.0.0.0", port=port)

