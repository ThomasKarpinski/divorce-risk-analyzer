import pandas as pd
import numpy as np
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
import seaborn as sns
file_path = 'divorce+predictors+data+set/divorce/divorce.csv'
try:
    df = pd.read_csv(file_path, sep=';')
    X = df.drop('Class', axis=1)
    y = df['Class']
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    pca = PCA(n_components=2)
    X_pca = pca.fit_transform(X_scaled)
    explained_variance = pca.explained_variance_ratio_
    total_var_2d = sum(explained_variance) * 100
    print("PCA Variance:")
    print(f"PC1: {explained_variance[0]:.2%}")
    print(f"PC2: {explained_variance[1]:.2%}")
    print(f"Total (2D): {total_var_2d:.2f}%")
    plt.figure(figsize=(10, 6))
    scatter = plt.scatter(X_pca[:, 0], X_pca[:, 1], c=y, cmap='viridis', alpha=0.7, edgecolor='k')
    plt.title(f'PCA: Divorce Dataset (2 Components, {total_var_2d:.1f}% Variance)')
    plt.xlabel(f'Principal Component 1 ({explained_variance[0]:.1%} var)')
    plt.ylabel(f'Principal Component 2 ({explained_variance[1]:.1%} var)')
    plt.colorbar(scatter, label='Class (0=No Divorce, 1=Divorce)')
    plt.grid(True, alpha=0.3)
    plt.savefig('pca_plot.png')
    print("Saved pca_plot.png")
    print("\nCorrelations:")
    corr_matrix = df.corr().abs()
    upper = corr_matrix.where(np.triu(np.ones(corr_matrix.shape), k=1).astype(bool))
    to_drop = [column for column in upper.columns if any(upper[column] > 0.90)]
    print(f"Pairs > 0.90: {len(to_drop)}")
    if len(to_drop) > 0:
        print("Examples:")
        print(to_drop[:10])
    print("Top target correlations:")
    target_corr = df.corrwith(df['Class']).abs().sort_values(ascending=False)
    print(target_corr.head(6))
except Exception as e:
    print(f"Error: {e}")
