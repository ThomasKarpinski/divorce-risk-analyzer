import os
import joblib
import numpy as np

def test_model_loading_and_prediction():
    MODEL_PATH = os.path.join(
        os.path.dirname(os.path.dirname(__file__)),
        "predictions",
        "ml_models",
        "model.pkl"
    )

    assert os.path.exists(MODEL_PATH), f"Model file does not exist: {MODEL_PATH}"

    model = joblib.load(MODEL_PATH)
    assert model is not None, "Failed to load the model"

    dummy_input = np.zeros((1, 54))
    prediction = model.predict(dummy_input)
    proba = model.predict_proba(dummy_input)

    assert prediction.shape[0] == 1, "Prediction output shape incorrect"
    assert proba.shape == (1, 2), "Probability output shape incorrect"
