import pandas as pd

file_path = 'divorce+predictors+data+set/divorce/divorce.csv'

try:
    df = pd.read_csv(file_path, sep=';')
    
    print(f"Data loaded. Shape: {df.shape}")
    
    missing_values = df.isnull().sum().sum()
    print(f"Nulls: {missing_values}")
    
    print("Stats:")
    print(df.describe())
    
    print("Classes:")
    print(df['Class'].value_counts())
    
    print("Types:")
    print(df.dtypes.unique())

except FileNotFoundError:
    print(f"Error: File not found at {file_path}")
except Exception as e:
    print(f"Error: {e}")
