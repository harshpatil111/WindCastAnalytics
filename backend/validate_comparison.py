import requests
import pandas as pd

API_URL = "http://127.0.0.1:8000/api/comparison/"

params = {
    "start_date": "2026-01-01",
    "end_date": "2026-01-31",
}

response = requests.get(API_URL, params=params, timeout=120)
response.raise_for_status()

payload = response.json()
records = payload.get("results", [])

df = pd.DataFrame(records)

print("\n========== WINDCAST DATA VALIDATION ==========")

print("API status:", payload.get("status"))
print("API count:", payload.get("count"))
print("Records received:", len(df))

if df.empty:
    print("No records returned. Cannot continue validation.")
    raise SystemExit(1)

required_columns = [
    "delivery_time",
    "forecast_publish_time",
    "lead_hours",
    "forecast_mw",
    "actual_mw",
    "error_mw",
    "absolute_error_mw",
]

missing_columns = [
    column for column in required_columns
    if column not in df.columns
]

print("\nMissing columns:", missing_columns)

if missing_columns:
    raise SystemExit("Required fields are missing.")

df["delivery_time"] = pd.to_datetime(
    df["delivery_time"], utc=True, errors="coerce"
)

df["forecast_publish_time"] = pd.to_datetime(
    df["forecast_publish_time"], utc=True, errors="coerce"
)

numeric_columns = [
    "lead_hours",
    "forecast_mw",
    "actual_mw",
    "error_mw",
    "absolute_error_mw",
]

for column in numeric_columns:
    df[column] = pd.to_numeric(df[column], errors="coerce")

print("\nDuplicate delivery timestamps:",
      int(df["delivery_time"].duplicated().sum()))

print("Missing values by column:")
print(df[required_columns].isna().sum().to_string())

actual_lead_hours = (
    df["delivery_time"] - df["forecast_publish_time"]
).dt.total_seconds() / 3600

print("\nMinimum lead hours:", round(actual_lead_hours.min(), 2))
print("Maximum lead hours:", round(actual_lead_hours.max(), 2))

print(
    "Records meeting 24-hour rule:",
    int((actual_lead_hours >= 24).sum()),
)

error_difference = (
    df["error_mw"] - (df["forecast_mw"] - df["actual_mw"])
).abs()

absolute_error_difference = (
    df["absolute_error_mw"] - df["error_mw"].abs()
).abs()

print(
    "\nIncorrect signed error calculations:",
    int((error_difference > 0.02).sum()),
)

print(
    "Incorrect absolute error calculations:",
    int((absolute_error_difference > 0.02).sum()),
)

expected_hours = pd.date_range(
    "2026-01-01",
    "2026-02-01",
    inclusive="left",
    freq="h",
    tz="UTC",
)

actual_hours = pd.DatetimeIndex(
    df["delivery_time"].dropna().unique()
).sort_values()

missing_hours = expected_hours.difference(actual_hours)
unexpected_hours = actual_hours.difference(expected_hours)

print("\nExpected January hours:", len(expected_hours))
print("Unique delivery timestamps:", len(actual_hours))
print("Missing delivery hours:", len(missing_hours))
print("Unexpected delivery timestamps:", len(unexpected_hours))

print("\nFirst 5 records:")
print(df[required_columns].head().to_string(index=False))

print("\n========== VALIDATION COMPLETE ==========")