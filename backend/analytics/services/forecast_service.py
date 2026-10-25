import logging

import pandas as pd

from analytics.services.elexon_client import fetch_elexon_data


logger = logging.getLogger(__name__)

FORECAST_ENDPOINT = "datasets/WINDFOR/stream"
ACTUAL_ENDPOINT = "datasets/FUELHH/stream"


def _fetch_records(endpoint, publish_from, publish_to, fuel_type=None):
    """
    Retrieve records from Elexon using publication-time filters.
    """
    params = {
        "publishDateTimeFrom": publish_from,
        "publishDateTimeTo": publish_to,
    }

    if fuel_type:
        params["fuelType"] = fuel_type

    records = fetch_elexon_data(endpoint, params=params)

    if not isinstance(records, list):
        raise ValueError(
            f"Unexpected response from Elexon endpoint: {endpoint}"
        )

    return records


def _prepare_dataframe(records):
    """
    Convert API records into a clean DataFrame.
    """
    if not records:
        return pd.DataFrame(
            columns=["startTime", "publishTime", "generation"]
        )

    df = pd.DataFrame(records)

    required_columns = {"startTime", "publishTime", "generation"}
    missing_columns = required_columns - set(df.columns)

    if missing_columns:
        raise ValueError(
            f"Missing required data columns: {sorted(missing_columns)}"
        )

    df["startTime"] = pd.to_datetime(
        df["startTime"], utc=True, errors="coerce"
    )

    df["publishTime"] = pd.to_datetime(
        df["publishTime"], utc=True, errors="coerce"
    )

    df["generation"] = pd.to_numeric(
        df["generation"], errors="coerce"
    )

    df = df.dropna(
        subset=["startTime", "publishTime", "generation"]
    )

    return df


def build_forecast_comparison(start_date, end_date):
    """
    Compare day-ahead wind forecasts with actual wind generation.

    start_date and end_date are inclusive UTC delivery dates.

    Forecast rule:
        Select the latest forecast published at least 24 hours
        before its delivery interval.

    Actual rule:
        Keep the latest published version of each half-hourly
        actual interval, then calculate hourly average generation
        using complete hours containing two half-hour intervals.
    """

    start = pd.Timestamp(start_date, tz="UTC")
    end_exclusive = pd.Timestamp(end_date, tz="UTC") + pd.Timedelta(days=1)

    if start > end_exclusive:
        raise ValueError("Invalid delivery date range.")

    # Fetch earlier publications so day-ahead forecasts are available
    # for the beginning of the requested delivery period.
    forecast_publish_from = (
        start - pd.Timedelta(days=3)
    ).strftime("%Y-%m-%dT%H:%M:%SZ")

    forecast_publish_to = end_exclusive.strftime(
        "%Y-%m-%dT%H:%M:%SZ"
    )

    # Actual records can be published after their delivery intervals.
    # Fetch a wider publication window to capture later revisions.
    actual_publish_from = (
        start - pd.Timedelta(days=2)
    ).strftime("%Y-%m-%dT%H:%M:%SZ")

    actual_publish_to = (
        end_exclusive + pd.Timedelta(days=2)
    ).strftime("%Y-%m-%dT%H:%M:%SZ")

    logger.info(
        "Fetching wind data for delivery dates %s through %s",
        start_date,
        end_date,
    )

    forecast_records = _fetch_records(
        FORECAST_ENDPOINT,
        forecast_publish_from,
        forecast_publish_to,
    )

    actual_records = _fetch_records(
        ACTUAL_ENDPOINT,
        actual_publish_from,
        actual_publish_to,
        fuel_type="WIND",
    )

    forecasts = _prepare_dataframe(forecast_records)
    actuals = _prepare_dataframe(actual_records)

    if forecasts.empty:
        raise ValueError("Elexon returned no forecast records.")

    if actuals.empty:
        raise ValueError("Elexon returned no actual generation records.")

    # Keep forecasts whose DELIVERY timestamps fall within the
    # requested date range.
    forecasts = forecasts[
        (forecasts["startTime"] >= start)
        & (forecasts["startTime"] < end_exclusive)
    ].copy()

    # Select forecasts available at least 24 hours before delivery.
    forecasts["lead_hours"] = (
        forecasts["startTime"] - forecasts["publishTime"]
    ).dt.total_seconds() / 3600

    eligible = forecasts[
        forecasts["lead_hours"] >= 24
    ].copy()

    if eligible.empty:
        raise ValueError(
            "No forecasts satisfy the 24-hour day-ahead rule "
            "for the selected delivery dates."
        )

    # Keep the latest eligible publication for each delivery interval.
    selected_forecasts = (
        eligible
        .sort_values("publishTime")
        .drop_duplicates(subset=["startTime"], keep="last")
        [
            [
                "startTime",
                "publishTime",
                "generation",
                "lead_hours",
            ]
        ]
        .rename(
            columns={
                "publishTime": "forecast_publish_time",
                "generation": "forecast_mw",
            }
        )
    )

    # Keep the latest published version of each actual interval.
    actuals = (
        actuals
        .sort_values("publishTime")
        .drop_duplicates(subset=["startTime"], keep="last")
    )

    # Restrict actual delivery intervals to the requested dates.
    actuals = actuals[
        (actuals["startTime"] >= start)
        & (actuals["startTime"] < end_exclusive)
    ].copy()

    # FUELHH data is half-hourly. Calculate hourly average generation.
    # Require exactly two half-hour intervals per hour to avoid
    # silently treating incomplete hours as complete.
    actuals = actuals.set_index("startTime").sort_index()

    hourly_actuals = (
        actuals["generation"]
        .resample("1h")
        .agg(["mean", "count"])
    )

    hourly_actuals = hourly_actuals[
        hourly_actuals["count"] == 2
    ]

    hourly_actuals = (
        hourly_actuals[["mean"]]
        .rename(columns={"mean": "actual_mw"})
        .reset_index()
    )

    # Match forecast and actual using delivery time.
    comparison = selected_forecasts.merge(
        hourly_actuals,
        on="startTime",
        how="inner",
        validate="one_to_one",
    )

    if comparison.empty:
        raise ValueError(
            "No matching forecast and actual delivery intervals "
            "were found for these dates."
        )

    comparison["error_mw"] = (
        comparison["forecast_mw"] - comparison["actual_mw"]
    )

    comparison["absolute_error_mw"] = comparison["error_mw"].abs()

    comparison = comparison.sort_values("startTime").reset_index(
        drop=True
    )

    logger.info(
        "Comparison completed: %s matched delivery intervals",
        len(comparison),
    )

    return comparison