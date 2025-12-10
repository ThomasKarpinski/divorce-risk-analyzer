import pandas as pd
import numpy as np
import xgboost as xgb
import matplotlib.pyplot as plt
import seaborn as sns

file_path = 'divorce+predictors+data+set/divorce/divorce.csv'

try:
    # Load and Train
    df = pd.read_csv(file_path, sep=';')
    X = df.drop('Class', axis=1)
    y = df['Class']
    
    # Train high-quality model
    model = xgb.XGBClassifier(n_estimators=100, max_depth=3, eval_metric='logloss', use_label_encoder=False)
    model.fit(X, y)

    # --- Scenario 1: The "One Red Flag" Test ---
    # Perfect couple (all 0s) but we increase ONE feature (Atr11 - Harmony) from 0 to 4
    print("\n--- Test 1: The 'One Red Flag' Impact ---")
    print("Baseline: Perfect Couple (All 0s)")
    print("Varying 'Atr11' (Harmony) from 0 to 4...")
    
    red_flag_data = []
    for val in range(5):
        row = np.zeros(54) # All zeros
        row[10] = val      # Set Atr11 (index 10) to val
        red_flag_data.append(row)
    
    probs = model.predict_proba(pd.DataFrame(red_flag_data, columns=X.columns))[:, 1]
    
    for val, prob in zip(range(5), probs):
        print(f"Atr11 Score {val}: {prob*100:.1f}% Divorce Risk")

    # --- Scenario 2: Heatmap of the 'Danger Zone' ---
    # We vary Atr11 (Harmony) and Atr17 (Happiness) from 0 to 4 in 0.1 increments.
    # Other values set to "Average" (2) to simulate a normal, messy life.
    
    print("\n--- Test 2: Generating Decision Boundary Heatmap ---")
    
    x_range = np.linspace(0, 4, 50) # Atr11
    y_range = np.linspace(0, 4, 50) # Atr17
    
    heatmap_data = np.zeros((50, 50))
    
    # We need to construct a batch of 2500 samples
    batch_data = []
    
    for i, val_x in enumerate(x_range):
        for j, val_y in enumerate(y_range):
            # Base row: Mostly 1s (Low conflict background)
            # If we set background to 0, it's too easy. 
            # If we set to 2 (Average), we saw earlier that risk is already high.
            # Let's set background to 0.5 (Very good relationship) to isolate the impact of top 2 features.
            row = np.full(54, 0.5) 
            
            row[10] = val_x # Atr11
            row[16] = val_y # Atr17
            batch_data.append(row)
            
    # Predict in bulk
    batch_df = pd.DataFrame(batch_data, columns=X.columns)
    batch_probs = model.predict_proba(batch_df)[:, 1]
    
    # Reshape for heatmap
    # Note: We need to map the 1D array back to 50x50
    # x is rows here, y is cols? 
    # Let's fill carefully.
    
    k = 0
    for i in range(50):
        for j in range(50):
            heatmap_data[i, j] = batch_probs[k]
            k += 1
            
    # Plot
    plt.figure(figsize=(10, 8))
    # Flip Y axis so 0 is at bottom
    ax = sns.heatmap(heatmap_data.T, cmap='RdYlGn_r', xticklabels=False, yticklabels=False, vmin=0, vmax=1)
    
    # Add custom labels
    plt.title("Divorce Risk Heatmap: Harmony (Atr11) vs Happiness (Atr17)")
    plt.xlabel(f"Atr11: Harmony (Left=0/Never, Right=4/Always)")
    plt.ylabel(f"Atr17: Shared Happiness (Bottom=0/Never, Top=4/Always)")
    
    # Add simple markers for 0, 2, 4
    plt.xticks([0, 25, 49], ['0', '2', '4'])
    plt.yticks([0, 25, 49], ['0', '2', '4'])
    
    plt.savefig('boundary_heatmap.png')
    print("Saved boundary_heatmap.png")

except Exception as e:
    print(f"Error: {e}")
