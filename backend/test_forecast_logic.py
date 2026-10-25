import pandas as pd

from analytics.services.metrics_service import calculate_accuracy_metrics


def test_forecast_selection_and_accuracy():
    comparison = pd.DataFrame({
        "error_mw": [500, -200, 300],
    })

    metrics = calculate_accuracy_metrics(comparison)

    # Three comparison records should be counted.
    assert metrics["sample_count"] == 3

    # MAE = (500 + 200 + 300) / 3
    assert metrics["mae_mw"] == 333.33

    # RMSE = sqrt((500² + 200² + 300²) / 3)
    assert metrics["rmse_mw"] == 355.90

    # Bias = (500 - 200 + 300) / 3
    assert metrics["bias_mw"] == 200.00