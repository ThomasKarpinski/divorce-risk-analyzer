import pandas as pd
import numpy as np
import xgboost as xgb
import matplotlib.pyplot as plt
import seaborn as sns
import joblib
file_path = 'divorce+predictors+data+set/divorce/divorce.csv'
model_path = 'models/divorce_model.pkl'
try:
    df = pd.read_csv(file_path, sep=';')
    X = df.drop('Class', axis=1)
    print(f"Loading model from {model_path}...")
    model = joblib.load(model_path)
    couples_data = []
    couple_names = [
        "Honeymooners (Perfect)", 
        "Occasional Arguers (Low)", 
        "Drifting Apart (Medium)", 
        "Toxic Volatile (High)",
        "The Broken (Certain)"
    ]
    base_scores = [0, 1, 2, 3, 4] 
    for base_score in base_scores:
        row = np.zeros(54)
        for i in range(54):
            val = int(np.random.normal(loc=base_score, scale=0.5))
            val = max(0, min(4, val))
            row[i] = val
        couples_data.append(row)
    new_couples_df = pd.DataFrame(couples_data, columns=X.columns)
    probs = model.predict_proba(new_couples_df)[:, 1]
    results_df = new_couples_df.copy()
    results_df['Couple_Name'] = couple_names
    results_df['Divorce_Risk_Percent'] = np.round(probs * 100, 2)
    csv_filename = 'synthetic_predictions.csv'
    results_df.to_csv(csv_filename, index=False)
    print(f"Saved data to {csv_filename}")
    plt.figure(figsize=(10, 6))
    ax = sns.barplot(x='Divorce_Risk_Percent', y='Couple_Name', data=results_df, palette='coolwarm')
    plt.title('Divorce Risk Prediction for Synthetic Couples')
    plt.xlabel('Probability of Divorce (%)')
    plt.xlim(0, 100)
    for i, v in enumerate(results_df['Divorce_Risk_Percent']):
        ax.text(v + 1, i, f"{v}%", color='black', va='center')
    plt.tight_layout()
    plt.savefig('synthetic_risk_plot.png')
    print("Saved plot to synthetic_risk_plot.png")
except Exception as e:
    print(f"Error: {e}")
