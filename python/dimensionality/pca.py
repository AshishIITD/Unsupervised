import numpy as np
import matplotlib.pyplot as plt
import os

class CustomPCA:
    """
    A clean, from-scratch implementation of Principal Component Analysis (PCA)
    designed for educational clarity.
    """
    def __init__(self, n_components=2):
        self.n_components = n_components
        self.components = None      # Eigenvectors (Principal Directions)
        self.mean = None            # Feature means for centering
        self.eigenvalues = None     # Variance along each component
        self.explained_variance_ratio_ = None

    def fit(self, X):
        # 1. Center the data (subtract the mean of each feature)
        self.mean = np.mean(X, axis=0)
        X_centered = X - self.mean
        
        # 2. Compute the Covariance Matrix
        # Covariance represents how features vary together. Formula: 1/(N-1) * (X^T * X)
        n_samples = X.shape[0]
        covariance_matrix = np.dot(X_centered.T, X_centered) / (n_samples - 1)
        
        # 3. Compute Eigenvalues and Eigenvectors of the Covariance Matrix
        # We use np.linalg.eigh because covariance matrices are symmetric.
        # eigh returns eigenvalues in ascending order, along with their eigenvectors.
        eigenvalues, eigenvectors = np.linalg.eigh(covariance_matrix)
        
        # 4. Sort eigenvalues and eigenvectors in descending order (highest variance first)
        sorted_indices = np.argsort(eigenvalues)[::-1]
        self.eigenvalues = eigenvalues[sorted_indices]
        self.components = eigenvectors[:, sorted_indices].T # Shape (n_features, n_features)
        
        # 5. Calculate Explained Variance Ratio
        total_variance = np.sum(self.eigenvalues)
        self.explained_variance_ratio_ = self.eigenvalues / total_variance
        
        # 6. Keep only the top n_components
        self.components = self.components[:self.n_components]
        
        return self

    def transform(self, X):
        # Center the data using the mean computed during fit
        X_centered = X - self.mean
        # Project the centered data onto the principal components
        # Formula: X_projected = X_centered * W (where W is the matrix of selected eigenvectors)
        return np.dot(X_centered, self.components.T)

    def fit_transform(self, X):
        self.fit(X)
        return self.transform(X)

def generate_tilted_3d_sheet():
    """
    Generates a 3D dataset where points lie on a heavily tilted, flat 2D plane
    with a small amount of orthogonal noise. This represents high-dimensional data
    that is structurally 2D, making it ideal for PCA compression.
    """
    np.random.seed(42)
    n_samples = 200
    
    # Generate two independent coordinates (internal 2D structure)
    u = np.random.uniform(-5, 5, n_samples)
    v = np.random.uniform(-5, 5, n_samples)
    
    # Map them to 3D space with a tilt
    # X = u, Y = v, Z = 0.8*u - 1.2*v + small noise
    x = u
    y = v
    z = 0.8 * u - 1.2 * v + np.random.normal(0, 0.2, n_samples)
    
    X = np.column_stack((x, y, z))
    return X

def main():
    print("=" * 70)
    print("   UNSUPERVISED LEARNING: PCA DIMENSIONALITY REDUCTION DEMO")
    print("=" * 70)
    
    # 1. Generate data
    X = generate_tilted_3d_sheet()
    print(f"[*] Generated synthetic 3D dataset: {X.shape[0]} samples with 3 features (X, Y, Z).")
    print("    Structural properties: The points are spread out along a flat, tilted plane.")
    print("    Although described in 3D, it is essentially a 2D shape floating in space.")
    
    # 2. Fit and Transform Custom PCA
    pca = CustomPCA(n_components=2)
    X_projected = pca.fit_transform(X)
    
    # 3. Analyze results
    print("\n" + "-" * 50)
    print("📊 ALGORITHM RESULTS (TECHNICAL & LAYMAN TRANSATION)")
    print("-" * 50)
    print("Eigenvalues (Variance per component):")
    for idx, val in enumerate(pca.eigenvalues):
        print(f"  - Component {idx+1}: {val:.4f}")
        
    print("\nExplained Variance Ratio (Percentage of information kept):")
    for idx, ratio in enumerate(pca.explained_variance_ratio_):
        print(f"  - Component {idx+1}: {ratio*100:.2f}% of total data variance")
        
    cumulative_variance = np.sum(pca.explained_variance_ratio_[:2]) * 100
    print(f"\nTotal variance retained in 2D projection: {cumulative_variance:.2f}%")
    
    print("\n📢 Layman Narrative Interpretation:")
    print("-> How PCA thinks:")
    print("   Imagine holding a 3D sculpture in front of a flashlight and looking at its 2D shadow on the wall.")
    print("   If you turn the sculpture, the shadow changes. Some angles compress the shadow into a line, losing detail.")
    print("   Other angles show a wide, detailed silhouette that captures the sculpture's true shape.")
    print("   PCA rotates the data to find the absolute best shadow—the one that spreads out the points as much as possible,")
    print("   retaining the maximum amount of original detail (variance).")
    
    print(f"\n🔍 What do these results tell us?")
    print(f"   - Component 1 captures {pca.explained_variance_ratio_[0]*100:.1f}% of the variance. It points in the direction")
    print("     of the longest axis of our tilted sheet.")
    print(f"   - Component 2 captures {pca.explained_variance_ratio_[1]*100:.1f}% of the variance. It points along the secondary")
    print("     wide axis of the sheet.")
    print(f"   - Together, they capture {cumulative_variance:.1f}% of the information. The remaining {100-cumulative_variance:.1f}%")
    print("     was just tiny random noise perpendicular to the sheet, which we successfully discarded!")
    print("     We compressed a 3-feature dataset to 2-features with virtually zero loss of useful structure.")

    # 4. Plot and save
    os.makedirs("/home/gaian/Unsupervised/python/dimensionality", exist_ok=True)
    fig = plt.figure(figsize=(14, 6), facecolor='#121214')
    
    # Left subplot: Original 3D Data
    ax1 = fig.add_subplot(1, 2, 1, projection='3d')
    ax1.set_facecolor('#121214')
    ax1.scatter(X[:, 0], X[:, 1], X[:, 2], c=X[:, 2], cmap='cool', s=25, alpha=0.8)
    
    # Draw the principal components as lines in 3D
    mean = pca.mean
    for i, component in enumerate(pca.components):
        # Scale component vector for visualization
        scaled_comp = component * np.sqrt(pca.eigenvalues[i]) * 2
        ax1.plot([mean[0], mean[0] + scaled_comp[0]],
                 [mean[1], mean[1] + scaled_comp[1]],
                 [mean[2], mean[2] + scaled_comp[2]],
                 color='#ffffff', linewidth=3, zorder=15, 
                 label=f'PC {i+1} Vector' if i < 2 else '')
                 
    ax1.set_title('Original 3D Data & Principal Axes', fontsize=12, color='#ffffff')
    ax1.set_xlabel('X Axis', color='#cccccc')
    ax1.set_ylabel('Y Axis', color='#cccccc')
    ax1.set_zlabel('Z Axis', color='#cccccc')
    ax1.tick_params(colors='#cccccc')
    ax1.xaxis.label.set_color('#cccccc')
    ax1.yaxis.label.set_color('#cccccc')
    ax1.zaxis.label.set_color('#cccccc')
    ax1.xaxis.pane.set_facecolor((0.1, 0.1, 0.12, 1.0))
    ax1.yaxis.pane.set_facecolor((0.1, 0.1, 0.12, 1.0))
    ax1.zaxis.pane.set_facecolor((0.1, 0.1, 0.12, 1.0))
    
    # Right subplot: Projected 2D Data
    ax2 = fig.add_subplot(1, 2, 2)
    ax2.set_facecolor('#1e1e24')
    scatter = ax2.scatter(X_projected[:, 0], X_projected[:, 1], c=X[:, 2], cmap='cool', s=40, alpha=0.8, edgecolors='none')
    
    ax2.set_title('PCA Projected 2D Compressed Data', fontsize=12, color='#ffffff')
    ax2.set_xlabel('Principal Component 1 (PC1)', color='#cccccc')
    ax2.set_ylabel('Principal Component 2 (PC2)', color='#cccccc')
    ax2.tick_params(colors='#cccccc')
    ax2.spines['bottom'].set_color('#333333')
    ax2.spines['left'].set_color('#333333')
    ax2.spines['top'].set_visible(False)
    ax2.spines['right'].set_visible(False)
    ax2.grid(color='#333333', linestyle='--', alpha=0.3)
    
    # Add colorbar
    cbar = fig.colorbar(scatter, ax=[ax1, ax2], shrink=0.7, label='Original Z Value')
    cbar.ax.yaxis.set_tick_params(color='#cccccc')
    cbar.ax.yaxis.label.set_color('#cccccc')
    plt.setp(plt.getp(cbar.ax.axes, 'yticklabels'), color='#cccccc')
    
    output_path = "/home/gaian/Unsupervised/python/dimensionality/pca_result.png"
    plt.savefig(output_path, dpi=150, bbox_inches='tight')
    plt.close()
    
    print(f"\n[+] Visualization successfully saved to: {output_path}")
    print("=" * 70)

if __name__ == '__main__':
    main()
