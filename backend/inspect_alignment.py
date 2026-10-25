
import pandas as pd

from analytics.services.elexon_client import fetch_elexon_data


def main():
    # Fetch forecasts published during January 15.
    forecasts = fetch_elexon_data(
        "datasets/WINDFOR/stream",
        params={
            "publishDateTimeFrom": "2026-01-15T00:00:00Z",
            "publishDateTimeTo": "2026-01-16T00:00:00Z",
        },
    )

    # Fetch actuals covering the delivery dates in the forecast data.
    actuals = fetch_elexon_data(
        "datasets/FUELHH/stream",
        params={
            "publishDateTimeFrom": "2026-01-14T00:00:00Z",
            "publishDateTimeTo": "2026-01-19T00:00:00Z",
            "fuelType": "WIND",
        },
    )

    forecast_df = pd.DataFrame(forecasts)
    actual_df = pd.DataFrame(actuals)

    if forecast_df.empty or actual_df.empty:
        print("Forecast or actual data is empty.")
        return

    for df in (forecast_df, actual_df):
        df["startTime"] = pd.to_datetime(df["startTime"], utc=True)
        df["publishTime"] = pd.to_datetime(df["publishTime"], utc=True)
        df["generation"] = pd.to_numeric(df["generation"], errors="coerce")

    # Inspect the time coverage before joining.
    print("Forecast records:", len(forecast_df))
    print("Actual records:", len(actual_df))

    print("\nForecast delivery range:")
    print(forecast_df["startTime"].min(), "to", forecast_df["startTime"].max())

    print("\nActual delivery range:")
    print(actual_df["startTime"].min(), "to", actual_df["startTime"].max())

    # Select forecasts published at least 24 hours before delivery.
    forecast_df["lead_hours"] = (
        forecast_df["startTime"] - forecast_df["publishTime"]
    ).dt.total_seconds() / 3600

    eligible = forecast_df[forecast_df["lead_hours"] >= 24].copy()

    # Choose the latest eligible forecast for each delivery interval.
    selected = (
        eligible.sort_values("publishTime")
        .drop_duplicates(subset=["startTime"], keep="last")
        [["startTime", "publishTime", "generation"]]
        .rename(columns={
            "publishTime": "forecast_publish_time",
            "generation": "forecast_mw",
        })
    )

    # Remove duplicate actual versions, keeping the latest publication.
    actual_df = (
        actual_df.sort_values("publishTime")
        .drop_duplicates(subset=["startTime"], keep="last")
    )

    # Convert the half-hourly actual data to hourly averages.
    actual_df = actual_df.set_index("startTime").sort_index()

    hourly_actuals = (
        actual_df["generation"]
        .resample("1h")
        .mean()
        .dropna()
        .rename("actual_mw")
        .reset_index()
    )

    # Match forecasts and actuals using delivery time.
    comparison = selected.merge(
        hourly_actuals,
        on="startTime",
        how="inner",
    )

    print("\nSelected forecasts:", len(selected))
    print("Hourly actual intervals:", len(hourly_actuals))
    print("Matched delivery intervals:", len(comparison))

    if not comparison.empty:
        comparison["error_mw"] = (
            comparison["forecast_mw"] - comparison["actual_mw"]
        )

        print("\nFirst 10 matched intervals:")
        print(comparison.head(10).to_string(index=False))

        print("\nMean absolute error (MW):",
              comparison["error_mw"].abs().mean())
    else:
        print(
            "\nNo matching delivery intervals found. "
            "Check the actual data coverage and endpoint filters."
        )


if __name__ == "__main__":
    main()

