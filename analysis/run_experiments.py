import pandas as pd
import numpy as np
import xgboost as xgb
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix, roc_curve, auc
import matplotlib.pyplot as plt
import seaborn as sns
import joblib
import os
import shutil
configs = [
    {
        'name': 'baseline_default',
        'params': {
            'n_estimators': 100,
            'max_depth': 3,
            'learning_rate': 0.1,
            'use_label_encoder': False,
            'eval_metric': 'logloss',
            'random_state': 42
        }
    },
    {
        'name': 'deep_trees',
        'params': {
            'n_estimators': 200,
            'max_depth': 10,
            'learning_rate': 0.05,
            'use_label_encoder': False,
            'eval_metric': 'logloss',
            'random_state': 42
        }
    },
    {
        'name': 'conservative_regularized',
        'params': {
            'n_estimators': 300,
            'max_depth': 2,
            'learning_rate': 0.01,
            'reg_alpha': 0.1,
            'reg_lambda': 0.1,
            'use_label_encoder': False,
            'eval_metric': 'logloss',
            'random_state': 42
        }
    },
     {
        'name': 'high_variance_fast',
        'params': {
            'n_estimators': 50,
            'max_depth': 6,
            'learning_rate': 0.3,
            'use_label_encoder': False,
            'eval_metric': 'logloss',
            'random_state': 42
        }
    }
]
file_path = 'divorce+predictors+data+set/divorce/divorce.csv'
def run_experiment(config, X_train, X_test, y_train, y_test, X, y):
    name = config['name']
    params = config['params']
    print(f"\nRunning Experiment: {name}")
    output_dir = f'results/{name}'
    if os.path.exists(output_dir):
        shutil.rmtree(output_dir)
    os.makedirs(output_dir)
    model = xgb.XGBClassifier(**params)
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    y_proba = model.predict_proba(X_test)[:, 1]
    acc = accuracy_score(y_test, y_pred)
    cm = confusion_matrix(y_test, y_pred)
    report = classification_report(y_test, y_pred)
    cv_scores = cross_val_score(model, X, y, cv=5)
    print(f"  Accuracy: {acc:.4f}")
    print(f"  CV Mean Score: {cv_scores.mean():.4f}")
    with open(f'{output_dir}/metrics.txt', 'w') as f:
        f.write(f"Configuration: {name}\n")
        f.write(f"Parameters: {params}\n\n")
        f.write(f"Test Accuracy: {acc:.4f}\n")
        f.write(f"CV Scores: {cv_scores}\n")
        f.write(f"CV Mean: {cv_scores.mean():.4f}\n\n")
        f.write("Classification Report:\n")
        f.write(report)
        f.write("\nConfusion Matrix:\n")
        f.write(str(cm))
    joblib.dump(model, f'{output_dir}/model.pkl')
    plt.figure(figsize=(6, 5))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', cbar=False)
    plt.title(f'Confusion Matrix - {name}')
    plt.ylabel('True Label')
    plt.xlabel('Predicted Label')
    plt.savefig(f'{output_dir}/confusion_matrix.png')
    plt.close()
    fpr, tpr, _ = roc_curve(y_test, y_proba)
    roc_auc = auc(fpr, tpr)
    plt.figure(figsize=(6, 5))
    plt.plot(fpr, tpr, color='darkorange', lw=2, label=f'ROC curve (area = {roc_auc:.2f})')
    plt.plot([0, 1], [0, 1], color='navy', lw=2, linestyle='--')
    plt.xlim([0.0, 1.0])
    plt.ylim([0.0, 1.05])
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    plt.title(f'ROC Curve - {name}')
    plt.legend(loc="lower right")
    plt.savefig(f'{output_dir}/roc_curve.png')
    plt.close()
    importances = model.feature_importances_
    feature_imp_df = pd.DataFrame({'Feature': X.columns, 'Importance': importances})
    feature_imp_df = feature_imp_df.sort_values(by='Importance', ascending=False).head(10)
    plt.figure(figsize=(8, 6))
    sns.barplot(x='Importance', y='Feature', data=feature_imp_df, palette='viridis')
    plt.title(f'Top 10 Features - {name}')
    plt.tight_layout()
    plt.savefig(f'{output_dir}/feature_importance.png')
    plt.close()
    print(f"  Results saved to {output_dir}/")
def main():
    try:
        df = pd.read_csv(file_path, sep=';')
        X = df.drop('Class', axis=1)
        y = df['Class']
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
        for config in configs:
            run_experiment(config, X_train, X_test, y_train, y_test, X, y)
    except Exception as e:
        print(f"Error: {e}")
if __name__ == "__main__":
    main()
