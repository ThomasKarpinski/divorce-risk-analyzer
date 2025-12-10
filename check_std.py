import pandas as pd

file_path = 'divorce+predictors+data+set/divorce/divorce.csv'

try:
    df = pd.read_csv(file_path, sep=';')
    
    std_devs = df.std()
    
    zero_std_cols = std_devs[std_devs == 0]
    
    if len(zero_std_cols) > 0:
        print("Columns with 0 std dev:")
        print(zero_std_cols.index.tolist())
    else:
        print("No constant columns.")

except Exception as e:
    print(f"Error: {e}")
