import os
import joblib
import numpy as np

def test_model_sanity():
    BASE_DIR = os.path.dirname(os.path.dirname(__file__))

    MODEL_PATH = os.path.join(
        BASE_DIR,
        "predictions",
        "ml_models",
        "model.pkl"
    )

    model = joblib.load(MODEL_PATH)

    good_rel = np.zeros((1, 54))
    good_rel[0, 0:30] = 4
    good_rel[0, 30:54] = 0
    prob_good = model.predict_proba(good_rel)[0][1]

    bad_rel = np.zeros((1, 54))
    bad_rel[0, 0:30] = 0
    bad_rel[0, 30:54] = 4
    prob_bad = model.predict_proba(bad_rel)[0][1]

    assert prob_good > prob_bad, "Model does not distinguish good vs bad relationship"


