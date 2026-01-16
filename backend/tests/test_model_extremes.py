import os
import joblib
import numpy as np

def test_model_extreme_inputs():
    BASE_DIR = os.path.dirname(os.path.dirname(__file__))

    MODEL_PATH = os.path.join(
        BASE_DIR,
        "predictions",
        "ml_models",
        "model.pkl"
    )

    model = joblib.load(MODEL_PATH)

    # Scenario 1: All 0s
    input_zeros = np.zeros((1, 54))
    prob_zeros = model.predict_proba(input_zeros)[0][1]

    # Scenario 2: All 4s
    input_fours = np.full((1, 54), 4)
    prob_fours = model.predict_proba(input_fours)[0][1]

    # Sanity checks
    assert prob_zeros != prob_fours, "Model returns same probability for extreme inputs"
