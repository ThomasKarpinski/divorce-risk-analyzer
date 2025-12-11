import pandas as pd
import numpy as np
import xgboost as xgb
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score

file_path = 'divorce+predictors+data+set/divorce/divorce.csv'

try:
    df = pd.read_csv(file_path, sep=';')
    X = df.drop('Class', axis=1)
    y = df['Class']

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

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
    f1 = f1_score(y_test, y_pred)
    prec = precision_score(y_test, y_pred)
    rec = recall_score(y_test, y_pred)

    data = {
        'Metric_Name': ['Accuracy', 'F1_Score', 'Precision', 'Recall'],
        'Value': [acc, f1, prec, rec]
    }

                                
    importances = model.feature_importances_
    feature_names = X.columns
    
    feat_df = pd.DataFrame({'Feature': feature_names, 'Importance': importances})
    feat_df = feat_df.sort_values(by='Importance', ascending=False).head(10)
    
                                     
    for index, row in feat_df.iterrows():
        data['Metric_Name'].append(f"Feature_Importance_{row['Feature']}")
        data['Value'].append(row['Importance'])

                    
    results_df = pd.DataFrame(data)
    csv_filename = 'model_metrics_and_features.csv'
    results_df.to_csv(csv_filename, index=False)
    
    print(f"Metrics and features saved to {csv_filename}")
    print(results_df)

except Exception as e:
    print(f"Error: {e}")
