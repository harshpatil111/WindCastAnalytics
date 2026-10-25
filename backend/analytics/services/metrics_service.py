import numpy as np


def calculate_accuracy_metrics(comparison):
    """
    Calculate forecast accuracy metrics from matched records.

    Error convention:
        error = forecast - actual

    Positive bias means overforecasting.
    Negative bias means underforecasting.
    """

    if comparison.empty:
        return {
            "sample_count": 0,
            "mae_mw": None,
            "rmse_mw": None,
            "bias_mw": None,
        }

    errors = comparison["error_mw"].to_numpy(dtype=float)

    mae = np.mean(np.abs(errors))
    rmse = np.sqrt(np.mean(np.square(errors)))
    bias = np.mean(errors)

    return {
        "sample_count": int(len(errors)),
        "mae_mw": round(float(mae), 2),
        "rmse_mw": round(float(rmse), 2),
        "bias_mw": round(float(bias), 2),
    }