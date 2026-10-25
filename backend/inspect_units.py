
import pandas as pd

from analytics.services.elexon_client import fetch_elexon_data


def main():
    params = {
        "publishDateTimeFrom": "2026-01-15T00:00:00Z",
        "publishDateTimeTo": "2026-01-16T00:00:00Z",
    }

    forecast_records = fetch_elexon_data(
        "datasets/WINDFOR/stream",
        params=params,
    )

    actual_records = fetch_elexon_data(
        "datasets/FUELHH/stream",
        params={
            "publishDateTimeFrom": "2026-01-15T00:00:00Z",
            "publishDateTimeTo": "2026-01-16T00:00:00Z",
            "fuelType": "WIND",
        },
    )

    forecast_df = pd.DataFrame(forecast_records)
    actual_df = pd.DataFrame(actual_records)

    print("\n--- WINDFOR ---")
    print("Rows:", len(forecast_df))

    if not forecast_df.empty:
        print("Generation minimum:", forecast_df["generation"].min())
        print("Generation maximum:", forecast_df["generation"].max())
        print("Generation mean:", forecast_df["generation"].mean())
        print("\nSample:")
        print(
            forecast_df[
                ["startTime", "publishTime", "generation"]
            ].head(5).to_string(index=False)
        )

    print("\n--- FUELHH ---")
    print("Rows:", len(actual_df))

    if not actual_df.empty:
        print("Generation minimum:", actual_df["generation"].min())
        print("Generation maximum:", actual_df["generation"].max())
        print("Generation mean:", actual_df["generation"].mean())
        print("\nSample:")
        print(
            actual_df[
                ["startTime", "publishTime", "generation"]
            ].head(5).to_string(index=False)
        )


if __name__ == "__main__":
    main()

