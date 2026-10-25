
import pandas as pd

from analytics.services.elexon_client import fetch_elexon_data


def main():
    params = {
        "publishDateTimeFrom": "2026-01-15T00:00:00Z",
        "publishDateTimeTo": "2026-01-16T00:00:00Z",
    }

    records = fetch_elexon_data(
        "datasets/WINDFOR/stream",
        params=params,
    )

    if not records:
        print("No forecast records found.")
        return

    df = pd.DataFrame(records)

    df["publishTime"] = pd.to_datetime(
        df["publishTime"], utc=True
    )

    df["startTime"] = pd.to_datetime(
        df["startTime"], utc=True
    )

    # Calculate how many hours before delivery
    # each forecast was published.
    df["lead_hours"] = (
        df["startTime"] - df["publishTime"]
    ).dt.total_seconds() / 3600

    # Keep forecasts published at least 24 hours
    # before their delivery intervals.
    eligible = df[df["lead_hours"] >= 24].copy()

    print("Total forecast records:", len(df))
    print("Eligible day-ahead records:", len(eligible))

    if eligible.empty:
        print("No forecasts meet the 24-hour cutoff.")
        return

    # Select the latest eligible forecast for each
    # delivery interval.
    selected = (
        eligible.sort_values("publishTime")
        .drop_duplicates(
            subset=["startTime"],
            keep="last",
        )
        .sort_values("startTime")
    )

    print(
        "Unique eligible delivery intervals:",
        selected["startTime"].nunique(),
    )

    print("\nSelected forecast examples:")

    print(
        selected[
            [
                "startTime",
                "publishTime",
                "generation",
                "lead_hours",
            ]
        ].head(15).to_string(index=False)
    )

    print("\nDelivery interval range:")
    print("First:", selected["startTime"].min())
    print("Last:", selected["startTime"].max())


if __name__ == "__main__":
    main()

