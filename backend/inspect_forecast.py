
from pprint import pprint
from analytics.services.elexon_client import fetch_elexon_data


def main():
    endpoint = "datasets/WINDFOR/stream"

    params = {
        "publishDateTimeFrom": "2026-01-15T00:00:00Z",
        "publishDateTimeTo": "2026-01-16T00:00:00Z",
    }

    try:
        data = fetch_elexon_data(endpoint, params=params)

        print("Response type:", type(data).__name__)
        print("Number of records:", len(data))

        if data:
            print("\nFirst record:")
            pprint(data[0])

            print("\nLast record:")
            pprint(data[-1])

            print("\nFirst startTime:", data[0].get("startTime"))
            print("Last startTime:", data[-1].get("startTime"))

            print("\nFirst publishTime:", data[0].get("publishTime"))
            print("Last publishTime:", data[-1].get("publishTime"))
        else:
            print("No records returned for the selected period.")

    except Exception as error:
        print("Error:", error)


if __name__ == "__main__":
    main()

