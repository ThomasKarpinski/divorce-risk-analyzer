import pandas as pd
import numpy as np
import xgboost as xgb
import matplotlib.pyplot as plt
import seaborn as sns

file_path = 'divorce+predictors+data+set/divorce/divorce.csv'

try:
                    
    df = pd.read_csv(file_path, sep=';')
    X = df.drop('Class', axis=1)
    y = df['Class']
    
                              
    model = xgb.XGBClassifier(n_estimators=100, max_depth=3, eval_metric='logloss', use_label_encoder=False)
    model.fit(X, y)

                                                 
                                                                                       
    print("\n--- Test 1: The 'One Red Flag' Impact ---")
    print("Baseline: Perfect Couple (All 0s)")
    print("Varying 'Atr11' (Harmony) from 0 to 4...")
    
    red_flag_data = []
    for val in range(5):
        row = np.zeros(54)            
        row[10] = val                                   
        red_flag_data.append(row)
    
    probs = model.predict_proba(pd.DataFrame(red_flag_data, columns=X.columns))[:, 1]
    
    for val, prob in zip(range(5), probs):
        print(f"Atr11 Score {val}: {prob*100:.1f}% Divorce Risk")

                                                      
                                                                                  
                                                                         
    
    print("\n--- Test 2: Generating Decision Boundary Heatmap ---")
    
    x_range = np.linspace(0, 4, 50)        
    y_range = np.linspace(0, 4, 50)        
    
    heatmap_data = np.zeros((50, 50))
    
                                                  
    batch_data = []
    
    for i, val_x in enumerate(x_range):
        for j, val_y in enumerate(y_range):
                                                           
                                                        
                                                                                 
                                                                                                           
            row = np.full(54, 0.5) 
            
            row[10] = val_x        
            row[16] = val_y        
            batch_data.append(row)
            
                     
    batch_df = pd.DataFrame(batch_data, columns=X.columns)
    batch_probs = model.predict_proba(batch_df)[:, 1]
    
                         
                                                     
                                 
                           
    
    k = 0
    for i in range(50):
        for j in range(50):
            heatmap_data[i, j] = batch_probs[k]
            k += 1
            
          
    plt.figure(figsize=(10, 8))
                                   
    ax = sns.heatmap(heatmap_data.T, cmap='RdYlGn_r', xticklabels=False, yticklabels=False, vmin=0, vmax=1)
    
                       
    plt.title("Divorce Risk Heatmap: Harmony (Atr11) vs Happiness (Atr17)")
    plt.xlabel(f"Atr11: Harmony (Left=0/Never, Right=4/Always)")
    plt.ylabel(f"Atr17: Shared Happiness (Bottom=0/Never, Top=4/Always)")
    
                                    
    plt.xticks([0, 25, 49], ['0', '2', '4'])
    plt.yticks([0, 25, 49], ['0', '2', '4'])
    
    plt.savefig('boundary_heatmap.png')
    print("Saved boundary_heatmap.png")

except Exception as e:
    print(f"Error: {e}")
