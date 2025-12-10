import pandas as pd
import numpy as np
import xgboost as xgb
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
import seaborn as sns

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

    print("Avg scores by class:")
    top_features = ['Atr11', 'Atr17', 'Atr40']
    
    means = df.groupby('Class')[top_features].mean()
    print(means)
    
    plt.figure(figsize=(12, 5))
    df_melted = df.melt(id_vars='Class', value_vars=top_features, var_name='Question', value_name='Response')
    sns.boxplot(x='Question', y='Response', hue='Class', data=df_melted, palette={0: 'tab:blue', 1: 'tab:red'})
    plt.title('How Responses Differ: Married (0) vs Divorced (1)')
    plt.ylabel('Response Score (0=Never ... 4=Always)')
    plt.savefig('top_features_distribution.png')
    print("Saved plots.")

    plt.figure(figsize=(8, 6))
    sns.scatterplot(data=df, x='Atr11', y='Atr17', hue='Class', palette={0: 'tab:blue', 1: 'tab:red'}, alpha=0.6, s=100)
    plt.title('Interaction: Atr11 vs Atr17')
    plt.xlabel('Atr11 (Harmony)')
    plt.ylabel('Atr17 (Shared Views on Happiness)')
    plt.grid(True, alpha=0.3)
    plt.savefig('feature_interaction.png')

    test_results = X_test.copy()
    test_results['Actual'] = y_test
    test_results['Predicted'] = y_pred
    
    errors = test_results[test_results['Actual'] != test_results['Predicted']]
    
    if not errors.empty:
        print(f"Misclassified ({len(errors)}):")
        print(errors[['Actual', 'Predicted'] + top_features])
    else:
        print("No errors.")

except Exception as e:
    print(f"Error: {e}")
