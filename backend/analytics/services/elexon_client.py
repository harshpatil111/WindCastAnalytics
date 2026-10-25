from typing import Any

import requests


ELEXON_API_BASE_URL = "https://data.elexon.co.uk/bmrs/api/v1"
DEFAULT_TIMEOUT_SECONDS = 30


def fetch_elexon_data(
    endpoint: str,
    params: dict[str, Any] | None = None,
    *,
    timeout: int = DEFAULT_TIMEOUT_SECONDS,
) -> Any:
    """Fetch and decode a JSON response from the Elexon BMRS API."""
    normalized_endpoint = endpoint.strip().lstrip("/")
    if not normalized_endpoint:
        raise ValueError("The Elexon endpoint must not be empty.")
    if timeout <= 0:
        raise ValueError("The request timeout must be greater than zero.")

    response = requests.get(
        f"{ELEXON_API_BASE_URL}/{normalized_endpoint}",
        params=params,
        timeout=timeout,
    )
    response.raise_for_status()
    return response.json()