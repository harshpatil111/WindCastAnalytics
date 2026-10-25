
import pandas as pd

from analytics.services.elexon_client import fetch_elexon_data


def main():
    endpoint = "datasets/WINDFOR/stream"

    params = {
        "publishDateTimeFrom": "2026-01-15T00:00:00Z",
        "publishDateTimeTo": "2026-01-16T00:00:00Z",
    }

    records = fetch_elexon_data(endpoint, params=params)

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

    print("\nTotal records:", len(df))

    print("\nUnique delivery intervals:", df["startTime"].nunique())

    print("\nUnique publication timestamps:", df["publishTime"].nunique())

    print("\nForecasts published before their delivery intervals:")

    eligible = df[df["publishTime"] <= df["startTime"]]

    print("Count:", len(eligible))

    print("\nFirst 10 records sorted by publication time:")

    print(
        df.sort_values("publishTime")[
            ["startTime", "publishTime", "generation"]
        ].head(10).to_string(index=False)
    )

    print("\nFirst 10 records sorted by delivery interval:")

    print(
        df.sort_values("startTime")[
            ["startTime", "publishTime", "generation"]
        ].head(10).to_string(index=False)
    )


if __name__ == "__main__":
    main()

