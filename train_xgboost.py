import pandas as pd
import numpy as np
import xgboost as xgb
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import matplotlib.pyplot as plt
import seaborn as sns

file_path = 'divorce+predictors+data+set/divorce/divorce.csv'

try:
    df = pd.read_csv(file_path, sep=';')
    X = df.drop('Class', axis=1)
    y = df['Class']

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

    print(f"Train shape: {X_train.shape}")
    print(f"Test shape:  {X_test.shape}")

    model = xgb.XGBClassifier(
        n_estimators=100,
        learning_rate=0.1,
        max_depth=3,
        use_label_encoder=False,
        eval_metric='logloss',
        random_state=42
    )
    
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)

    acc = accuracy_score(y_test, y_pred)
    print(f"Accuracy: {acc:.4f}")
    
    print("Report:")
    print(classification_report(y_test, y_pred))

    print("Confusion Matrix:")
    print(confusion_matrix(y_test, y_pred))

    print("Top Features:")
    importances = model.feature_importances_
    feature_names = X.columns
    
    feature_imp_df = pd.DataFrame({'Feature': feature_names, 'Importance': importances})
    feature_imp_df = feature_imp_df.sort_values(by='Importance', ascending=False).head(10)
    
    print(feature_imp_df)

    plt.figure(figsize=(10, 6))
    sns.barplot(x='Importance', y='Feature', data=feature_imp_df, palette='viridis')
    plt.title('Top 10 Predictors of Divorce (XGBoost)')
    plt.xlabel('Importance Score')
    plt.ylabel('Question ID')
    plt.tight_layout()
    plt.savefig('feature_importance.png')
    print("Saved feature_importance.png")

except Exception as e:
    print(f"Error: {e}")
