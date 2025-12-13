import pandas as pd
import numpy as np
import xgboost as xgb
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import matplotlib.pyplot as plt
import seaborn as sns
import joblib
import os
os.makedirs('models', exist_ok=True)
os.makedirs('results', exist_ok=True)
file_path = 'divorce+predictors+data+set/divorce/divorce.csv'
try:
    print("Loading data...")
    df = pd.read_csv(file_path, sep=';')
    X = df.drop('Class', axis=1)
    y = df['Class']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
    print("Starting hyperparameter tuning...")
    param_grid = {
        'n_estimators': [50, 100, 200],
        'learning_rate': [0.01, 0.1, 0.2],
        'max_depth': [3, 5, 7],
        'eval_metric': ['logloss'],
        'use_label_encoder': [False]
    }
    xgb_model = xgb.XGBClassifier(random_state=42)
    grid_search = GridSearchCV(estimator=xgb_model, param_grid=param_grid, cv=3, scoring='accuracy', verbose=1)
    grid_search.fit(X_train, y_train)
    best_model = grid_search.best_estimator_
    print(f"Best parameters: {grid_search.best_params_}")
    y_pred = best_model.predict(X_test)
    acc = accuracy_score(y_test, y_pred)
    report = classification_report(y_test, y_pred)
    conf_matrix = confusion_matrix(y_test, y_pred)
    print(f"Test Accuracy: {acc:.4f}")
    model_path = 'models/divorce_model.pkl'
    joblib.dump(best_model, model_path)
    print(f"Model saved to {model_path}")
    metrics_path = 'results/metrics.txt'
    with open(metrics_path, 'w') as f:
        f.write(f"Best Parameters: {grid_search.best_params_}\n")
        f.write(f"Test Accuracy: {acc:.4f}\n\n")
        f.write("Classification Report:\n")
        f.write(report)
        f.write("\nConfusion Matrix:\n")
        f.write(str(conf_matrix))
    print(f"Metrics saved to {metrics_path}")
    plt.figure(figsize=(12, 10))
    sns.heatmap(df.corr(), cmap='coolwarm', linewidths=0.5)
    plt.title('Feature Correlation Heatmap')
    plt.tight_layout()
    plt.savefig('results/correlation_heatmap.png')
    plt.close()
    print("Saved results/correlation_heatmap.png")
    importances = best_model.feature_importances_
    feature_imp_df = pd.DataFrame({'Feature': X.columns, 'Importance': importances})
    top_3_features = feature_imp_df.sort_values(by='Importance', ascending=False).head(3)['Feature'].tolist()
    print(f"Top 3 Features: {top_3_features}")
    pairplot_data = df[top_3_features + ['Class']]
    sns.pairplot(pairplot_data, hue='Class', palette='viridis')
    plt.savefig('results/top3_pairplot.png')
    plt.close()
    print("Saved results/top3_pairplot.png")
except Exception as e:
    print(f"An error occurred: {e}")
    raise e
