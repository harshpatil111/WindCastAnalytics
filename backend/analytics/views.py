import logging
from datetime import timedelta

import requests

from django.utils.dateparse import parse_date
from django.utils import timezone

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from analytics.services.forecast_service import (
    build_forecast_comparison,
)
from analytics.services.metrics_service import (
    calculate_accuracy_metrics,
)


logger = logging.getLogger(__name__)


def get_date_range(request):
    """
    Read and validate inclusive delivery dates from query parameters.

    Defaults to January 2026, as required by the assignment.
    """

    start_value = request.query_params.get(
        "start_date", "2026-01-01"
    )

    end_value = request.query_params.get(
        "end_date", "2026-01-31"
    )

    start_date = parse_date(start_value)
    end_date = parse_date(end_value)

    if start_date is None or end_date is None:
        raise ValueError(
            "Dates must use YYYY-MM-DD format."
        )

    if start_date > end_date:
        raise ValueError(
            "start_date must be before or equal to end_date."
        )

    if end_date - start_date > timedelta(days=30):
        raise ValueError(
            "The maximum supported delivery range is 31 days."
        )

    return start_date, end_date


def get_comparison_or_error(request):
    """
    Shared data-loading and error-handling logic for API endpoints.
    """

    try:
        start_date, end_date = get_date_range(request)

        comparison = build_forecast_comparison(
            start_date=start_date,
            end_date=end_date,
        )

        return comparison, None

    except ValueError as exc:
        return None, Response(
            {"error": str(exc)},
            status=status.HTTP_400_BAD_REQUEST,
        )

    except requests.RequestException:
        logger.exception("Elexon API request failed.")

        return None, Response(
            {
                "error": (
                    "Unable to retrieve wind generation data "
                    "from Elexon. Please try again later."
                )
            },
            status=status.HTTP_503_SERVICE_UNAVAILABLE,
        )

    except Exception:
        logger.exception("Unexpected error processing wind data.")

        return None, Response(
            {
                "error": (
                    "An unexpected error occurred while processing "
                    "wind generation data."
                )
            },
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


@api_view(["GET"])
def health_check(request):
    return Response(
        {
            "status": "success",
            "message": "WindCast Analytics API is running",
            "application": "WindCast Analytics",
        }
    )


@api_view(["GET"])
def summary(request):
    comparison, error_response = get_comparison_or_error(request)

    if error_response:
        return error_response

    metrics = calculate_accuracy_metrics(comparison)

    return Response(
        {
            "status": "success",
            "delivery_period": {
                "start_date": str(
                    comparison["startTime"].min().date()
                ),
                "end_date": str(
                    comparison["startTime"].max().date()
                ),
            },
            "forecast_rule": (
                "Latest forecast published at least 24 hours "
                "before delivery"
            ),
            "metrics": metrics,
        }
    )


@api_view(["GET"])
def comparison_data(request):
    comparison, error_response = get_comparison_or_error(request)

    if error_response:
        return error_response

    # Convert pandas timestamps and numeric values into JSON-safe types.
    records = []

    for _, row in comparison.iterrows():
        records.append(
            {
                "delivery_time": row["startTime"].isoformat(),
                "forecast_publish_time": (
                    row["forecast_publish_time"].isoformat()
                ),
                "lead_hours": round(float(row["lead_hours"]), 2),
                "forecast_mw": round(float(row["forecast_mw"]), 2),
                "actual_mw": round(float(row["actual_mw"]), 2),
                "error_mw": round(float(row["error_mw"]), 2),
                "absolute_error_mw": round(
                    float(row["absolute_error_mw"]), 2
                ),
            }
        )

    return Response(
        {
            "status": "success",
            "count": len(records),
            "results": records,
        }
    )