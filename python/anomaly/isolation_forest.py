import numpy as np
import matplotlib.pyplot as plt
import os

class IsolationNode:
    """
    A node in an Isolation Tree.
    """
    def __init__(self, left=None, right=None, split_feature=None, split_value=None, size=0, is_leaf=False):
        self.left = left
        self.right = right
        self.split_feature = split_feature
        self.split_value = split_value
        self.size = size
        self.is_leaf = is_leaf

class IsolationTree:
    """
    An individual tree in the Isolation Forest that recursively partitions data.
    """
    def __init__(self, max_depth):
        self.max_depth = max_depth
        self.root = None

    def fit(self, X, current_depth=0):
        n_samples = X.shape[0]
        
        # Base case: Leaf node reached
        if n_samples <= 1 or current_depth >= self.max_depth:
            return IsolationNode(size=n_samples, is_leaf=True)
            
        # Select a random feature to split on
        n_features = X.shape[1]
        split_feature = np.random.choice(n_features)
        
        # Find min and max of that feature
        feat_min = np.min(X[:, split_feature])
        feat_max = np.max(X[:, split_feature])
        
        # If all values are identical, we cannot split further
        if feat_min == feat_max:
            return IsolationNode(size=n_samples, is_leaf=True)
            
        # Select a random split point between min and max
        split_value = np.random.uniform(feat_min, feat_max)
        
        # Partition the data
        left_mask = X[:, split_feature] < split_value
        X_left = X[left_mask]
        X_right = X[~left_mask]
        
        # Recursively build left and right children
        left_node = self.fit(X_left, current_depth + 1)
        right_node = self.fit(X_right, current_depth + 1)
        
        return IsolationNode(left=left_node, right=right_node, 
                             split_feature=split_feature, split_value=split_value, 
                             size=n_samples)

    def path_length(self, x, node, current_depth=0):
        """
        Computes the path length h(x) to isolate point x.
        """
        if node.is_leaf:
            return current_depth + self._c(node.size)
            
        split_feat = node.split_feature
        split_val = node.split_value
        
        if x[split_feat] < split_val:
            return self.path_length(x, node.left, current_depth + 1)
        else:
            return self.path_length(x, node.right, current_depth + 1)

    def _c(self, n):
        """
        Average path length of an unsuccessful search in a Binary Search Tree (BST).
        Used as a normalizing factor.
        """
        if n <= 1:
            return 0
        if n == 2:
            return 1
        # Euler's constant approximation: 0.5772156649
        return 2 * (np.log(n - 1) + 0.5772156649) - (2 * (n - 1) / n)

class CustomIsolationForest:
    """
    A clean, from-scratch implementation of the Isolation Forest ensemble.
    """
    def __init__(self, n_estimators=100, max_samples=256, random_state=42):
        self.n_estimators = n_estimators
        self.max_samples = max_samples
        self.random_state = random_state
        self.trees = []
        
    def fit(self, X):
        np.random.seed(self.random_state)
        n_samples = X.shape[0]
        self.trees = []
        
        # Calculate maximum tree depth based on sample limit: log2(max_samples)
        subsample_size = min(n_samples, self.max_samples)
        max_depth = int(np.ceil(np.log2(self.max_samples)))
        
        for _ in range(self.n_estimators):
            # Draw a random subsample without replacement
            indices = np.random.choice(n_samples, size=subsample_size, replace=False)
            X_sub = X[indices]
            
            # Train an individual tree
            tree = IsolationTree(max_depth=max_depth)
            tree.root = tree.fit(X_sub)
            self.trees.append(tree)
            
        return self

    def _c(self, n):
        """
        BST normalizing factor.
        """
        if n <= 1:
            return 0
        if n == 2:
            return 1
        return 2 * (np.log(n - 1) + 0.5772156649) - (2 * (n - 1) / n)

    def compute_anomaly_score(self, X):
        n_samples = X.shape[0]
        paths = np.zeros((n_samples, self.n_estimators))
        
        # Compute path length for each point across all trees
        for tree_idx, tree in enumerate(self.trees):
            for sample_idx in range(n_samples):
                paths[sample_idx, tree_idx] = tree.path_length(X[sample_idx], tree.root)
                
        # Average path length E(h(x))
        mean_paths = np.mean(paths, axis=1)
        
        # Normalize: s(x, n) = 2^(-E(h(x)) / c(n))
        # c(max_samples) is the average path length of trees of size max_samples
        c_factor = self._c(min(X.shape[0], self.max_samples))
        
        scores = 2 ** (-mean_paths / c_factor)
        return scores

def generate_transaction_data():
    """
    Generates a 2D synthetic dataset representing credit card transactions:
    - Feature 1: Transaction Amount ($)
    - Feature 2: Transaction Frequency (Purchases per week)
    """
    np.random.seed(42)
    
    # 1. Normal Transactions: Small/moderate amount, moderate frequency
    n_normal = 200
    normal_amounts = np.random.normal(45, 12, n_normal)
    normal_freq = np.random.normal(8, 2, n_normal)
    
    # 2. Fraud Anomalies: Very high amounts (single large purchases) or insane frequency (bot card-testing)
    n_anomalies = 12
    # Anomalies type A: Huge purchases ($300 - $500), normal frequency
    anom_a_amounts = np.random.uniform(300, 450, n_anomalies // 2)
    anom_a_freq = np.random.normal(5, 1, n_anomalies // 2)
    
    # Anomalies type B: Moderate purchases ($100), but extremely high frequency (35-45 purchases/week)
    anom_b_amounts = np.random.normal(110, 15, n_anomalies - n_anomalies // 2)
    anom_b_freq = np.random.uniform(35, 45, n_anomalies - n_anomalies // 2)
    
    amounts = np.concatenate([normal_amounts, anom_a_amounts, anom_b_amounts])
    frequencies = np.concatenate([normal_freq, anom_a_freq, anom_b_freq])
    
    # Clip values to ensure positive numbers
    amounts = np.clip(amounts, 1, 500)
    frequencies = np.clip(frequencies, 0.5, 50)
    
    X = np.column_stack((amounts, frequencies))
    return X

def main():
    print("=" * 70)
    print("   UNSUPERVISED LEARNING: ISOLATION FOREST ANOMALY DETECTION DEMO")
    print("=" * 70)
    
    # 1. Generate data
    X = generate_transaction_data()
    n_total = X.shape[0]
    print(f"[*] Generated synthetic transaction dataset: {n_total} records with 2 features:")
    print("    - Transaction Amount ($)")
    print("    - Weekly Transaction Frequency (Purchases/Week)")
    print("    This dataset contains mostly normal habits, plus a few hidden suspicious anomalies.")
    
    # 2. Fit Custom Isolation Forest
    forest = CustomIsolationForest(n_estimators=100, max_samples=128, random_state=42)
    forest.fit(X)
    
    # 3. Calculate Anomaly Scores
    scores = forest.compute_anomaly_score(X)
    
    # Classify as anomaly if score > 0.6
    anomaly_threshold = 0.6
    anomalies_detected = np.where(scores > anomaly_threshold)[0]
    
    # 4. Show results and layman narrative
    print("\n" + "-" * 50)
    print("📊 ALGORITHM RESULTS (TECHNICAL & LAYMAN TRANSATION)")
    print("-" * 50)
    print(f"Total Transactions Audited: {n_total}")
    print(f"Anomalies Detected (Score > {anomaly_threshold}): {len(anomalies_detected)}")
    print(f"Maximum Anomaly Score in Data: {np.max(scores):.3f}")
    print(f"Average Normal Score: {np.mean(scores[scores <= anomaly_threshold]):.3f}")
    
    print("\n📢 Layman Narrative Interpretation:")
    print("-> How Isolation Forest thinks:")
    print("   Imagine trying to locate a specific person in a crowded city center vs. someone standing in the middle")
    print("   of an empty desert. To find the person in the desert, you just need to ask one simple question:")
    print("   'Are they east of the highway?' Boom, they are isolated.")
    print("   To find the person in the crowded city, you must ask dozens of questions: 'Which district? Which street?")
    print("   Which building? Which floor? Which apartment?'")
    print("   Isolation Forest cuts up space randomly. Anomalies, being isolated in empty space, get separated")
    print("   very quickly (short path length). Normal points in dense clusters take many cuts to separate.")
    
    print("\n🔍 What do these results tell us?")
    print("   We have flagged suspicious transactions. Here are a few notable anomalies:")
    
    # Print the top 5 most anomalous points
    sorted_anom_indices = np.argsort(scores)[::-1][:5]
    for idx in sorted_anom_indices:
        amount, freq = X[idx]
        score = scores[idx]
        
        # Labeling behavior
        if amount > 250:
            reason = "⚠️ 'High-Value Outlier' (Extremely large single purchase, potential card theft)"
        elif freq > 30:
            reason = "🤖 'High-Frequency Outlier' (Rapid-fire card testing, typical of automated bot fraud)"
        else:
            reason = "❓ 'Mild Outlier' (Outside of the dense cluster of normal transactions)"
            
        print(f"   - Index {idx:3d}: Amount = ${amount:6.2f}, Freq = {freq:4.1f}/wk, Anomaly Score = {score:.3f}")
        print(f"     Flag Reason: {reason}")

    # 5. Plot and save (Heatmap + Scatter)
    os.makedirs("/home/gaian/Unsupervised/python/anomaly", exist_ok=True)
    plt.figure(figsize=(11, 8), facecolor='#121214')
    ax = plt.axes()
    ax.set_facecolor('#1e1e24')
    
    # Generate a grid to plot the decision boundary heatmap
    x_min, x_max = 0, 500
    y_min, y_max = 0, 50
    xx, yy = np.meshgrid(np.linspace(x_min, x_max, 150),
                         np.linspace(y_min, y_max, 100))
    
    grid_points = np.c_[xx.ravel(), yy.ravel()]
    grid_scores = forest.compute_anomaly_score(grid_points)
    grid_scores = grid_scores.reshape(xx.shape)
    
    # Plot heatmap of anomaly scores
    contour = plt.contourf(xx, yy, grid_scores, levels=15, cmap='plasma', alpha=0.85)
    cbar = plt.colorbar(contour, shrink=0.8)
    cbar.ax.yaxis.set_tick_params(color='#cccccc')
    cbar.ax.yaxis.label.set_color('#cccccc')
    plt.setp(plt.getp(cbar.ax.axes, 'yticklabels'), color='#cccccc')
    cbar.set_label('Anomaly Score (Closer to 1 = More Suspicious)', fontsize=11, color='#cccccc', labelpad=10)
    
    # Plot normal points
    normal_idx = np.where(scores <= anomaly_threshold)[0]
    plt.scatter(X[normal_idx, 0], X[normal_idx, 1], s=40, c='#00ffcc', 
                edgecolors='#111111', linewidths=0.5, label='Normal Transactions', alpha=0.8)
    
    # Plot anomalies
    plt.scatter(X[anomalies_detected, 0], X[anomalies_detected, 1], s=80, c='#ff0055', 
                edgecolors='#ffffff', linewidths=1.0, label='FLAGGED Fraud Suspicion', marker='o')
    
    # Highlight highest risk transaction
    highest_risk_idx = sorted_anom_indices[0]
    plt.annotate('HIGHEST RISK', xy=(X[highest_risk_idx, 0], X[highest_risk_idx, 1]), 
                 xytext=(X[highest_risk_idx, 0] - 80, X[highest_risk_idx, 1] + 4),
                 arrowprops=dict(facecolor='#ffffff', shrink=0.08, width=1, headwidth=6, headlength=6),
                 color='#ffffff', fontweight='bold', fontsize=9, bbox=dict(boxstyle="round,pad=0.3", fc="#ff0055", ec="white", lw=1))
    
    plt.title('Isolation Forest Fraud Detection Heatmap', fontsize=14, color='#ffffff', pad=15)
    plt.xlabel('Transaction Amount ($)', fontsize=11, color='#cccccc')
    plt.ylabel('Transaction Frequency (Purchases per Week)', fontsize=11, color='#cccccc')
    
    plt.legend(facecolor='#1e1e24', edgecolor='#333333', labelcolor='#ffffff', loc='lower right')
    
    ax.tick_params(colors='#cccccc')
    ax.spines['bottom'].set_color('#333333')
    ax.spines['left'].set_color('#333333')
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    plt.xlim(x_min, x_max)
    plt.ylim(y_min, y_max)
    
    output_path = "/home/gaian/Unsupervised/python/anomaly/isolation_forest_result.png"
    plt.savefig(output_path, dpi=150, bbox_inches='tight')
    plt.close()
    
    print(f"\n[+] Visualization successfully saved to: {output_path}")
    print("=" * 70)

if __name__ == '__main__':
    main()
