from django.urls import path

from analytics.views import (
    health_check,
    summary,
    comparison_data,
)


urlpatterns = [
    path("health/", health_check, name="health-check"),
    path("summary/", summary, name="summary"),
    path(
        "comparison/",
        comparison_data,
        name="comparison-data",
    ),
]