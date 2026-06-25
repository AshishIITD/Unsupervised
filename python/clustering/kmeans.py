import numpy as np
import matplotlib.pyplot as plt
import os

class CustomKMeans:
    """
    A clean, from-scratch implementation of the K-Means clustering algorithm
    designed for educational clarity.
    """
    def __init__(self, k=3, max_iters=100, tol=1e-4, random_state=42):
        self.k = k
        self.max_iters = max_iters
        self.tol = tol
        self.random_state = random_state
        self.centroids = None
        self.labels = None
        self.inertia_ = None

    def fit(self, X):
        # Set random seed for reproducibility
        np.random.seed(self.random_state)
        
        # 1. Initialize centroids using K-Means++ style for faster convergence
        n_samples, n_features = X.shape
        self.centroids = np.zeros((self.k, n_features))
        
        # Select first centroid randomly
        self.centroids[0] = X[np.random.choice(n_samples)]
        
        # Select remaining centroids based on distance
        for i in range(1, self.k):
            distances = np.min([np.sum((X - c) ** 2, axis=1) for c in self.centroids[:i]], axis=0)
            probabilities = distances / np.sum(distances)
            self.centroids[i] = X[np.random.choice(n_samples, p=probabilities)]

        # Optimization loop
        for iteration in range(self.max_iters):
            old_centroids = self.centroids.copy()
            
            # 2. Assign Phase: Assign each data point to the closest centroid
            # Compute Euclidean distances: shape (n_samples, k)
            distances = np.linalg.norm(X[:, np.newaxis] - self.centroids, axis=2)
            self.labels = np.argmin(distances, axis=1)
            
            # 3. Update Phase: Recompute centroids as the mean of assigned points
            for center_idx in range(self.k):
                points_in_cluster = X[self.labels == center_idx]
                if len(points_in_cluster) > 0:
                    self.centroids[center_idx] = np.mean(points_in_cluster, axis=0)
            
            # Check for convergence (if centroids didn't move much)
            centroid_shift = np.sum((self.centroids - old_centroids) ** 2)
            if centroid_shift < self.tol:
                break
                
        # Calculate Inertia (Sum of squared distances of samples to their closest centroid)
        self.inertia_ = 0
        for center_idx in range(self.k):
            points_in_cluster = X[self.labels == center_idx]
            if len(points_in_cluster) > 0:
                self.inertia_ += np.sum((points_in_cluster - self.centroids[center_idx]) ** 2)
                
        return self

    def predict(self, X):
        distances = np.linalg.norm(X[:, np.newaxis] - self.centroids, axis=2)
        return np.argmin(distances, axis=1)

def calculate_silhouette_score_simple(X, labels):
    """
    Computes a simplified silhouette score to assess clustering quality.
    For each point:
      a = mean distance to other points in the same cluster
      b = mean distance to points in the nearest neighboring cluster
      s = (b - a) / max(a, b)
    """
    n_samples = X.shape[0]
    silhouette_vals = np.zeros(n_samples)
    unique_labels = np.unique(labels)
    
    if len(unique_labels) < 2:
        return 0.0
        
    for i in range(n_samples):
        curr_label = labels[i]
        curr_point = X[i]
        
        # 1. Compute 'a' (intra-cluster distance)
        same_cluster_mask = (labels == curr_label)
        same_cluster_mask[i] = False # Exclude current point
        same_cluster_points = X[same_cluster_mask]
        
        if len(same_cluster_points) == 0:
            a = 0.0
        else:
            a = np.mean(np.linalg.norm(same_cluster_points - curr_point, axis=1))
            
        # 2. Compute 'b' (nearest-cluster distance)
        b = float('inf')
        for other_label in unique_labels:
            if other_label == curr_label:
                continue
            other_cluster_points = X[labels == other_label]
            mean_dist = np.mean(np.linalg.norm(other_cluster_points - curr_point, axis=1))
            b = min(b, mean_dist)
            
        # 3. Compute silhouette coefficient for this point
        if max(a, b) == 0:
            silhouette_vals[i] = 0
        else:
            silhouette_vals[i] = (b - a) / max(a, b)
            
    return np.mean(silhouette_vals)

def generate_demo_dataset():
    """
    Generates a synthetic 2D customer dataset representing:
    - Feature 1: Age (scaled 18 to 70)
    - Feature 2: Spending Score (scaled 1 to 100)
    """
    np.random.seed(42)
    
    # Create 3 distinct segments
    # Segment 1: Young & High Spenders (Age: 20-35, Spending: 70-95)
    s1_age = np.random.normal(28, 4, 50)
    s1_spending = np.random.normal(82, 6, 50)
    
    # Segment 2: Middle Aged & Moderate Spenders (Age: 40-55, Spending: 40-60)
    s2_age = np.random.normal(48, 5, 60)
    s2_spending = np.random.normal(50, 8, 60)
    
    # Segment 3: Older & Conservative Spenders (Age: 55-70, Spending: 10-30)
    s3_age = np.random.normal(62, 4, 40)
    s3_spending = np.random.normal(20, 5, 40)
    
    ages = np.concatenate([s1_age, s2_age, s3_age])
    spendings = np.concatenate([s1_spending, s2_spending, s3_spending])
    
    # Clip values to realistic ranges
    ages = np.clip(ages, 18, 75)
    spendings = np.clip(spendings, 1, 100)
    
    X = np.column_stack((ages, spendings))
    return X

def main():
    print("=" * 70)
    print("   UNSUPERVISED LEARNING: K-MEANS CUSTOMER SEGMENTATION DEMO")
    print("=" * 70)
    
    # 1. Generate data
    X = generate_demo_dataset()
    print(f"[*] Generated synthetic dataset: {X.shape[0]} customers with 2 features:")
    print("    - Age (Years)")
    print("    - Spending Score (1-100 scale of purchase frequency/volume)")
    
    # 2. Fit Custom KMeans (k=3)
    k = 3
    kmeans = CustomKMeans(k=k, random_state=42)
    kmeans.fit(X)
    
    # 3. Evaluate results
    silhouette = calculate_silhouette_score_simple(X, kmeans.labels)
    
    # 4. Generate Layman Explanations
    print("\n" + "-" * 50)
    print("📊 ALGORITHM RESULTS (TECHNICAL & LAYMAN TRANSATION)")
    print("-" * 50)
    print(f"Centroids Found: \n{kmeans.centroids}")
    print(f"Inertia (Total Squared Error): {kmeans.inertia_:.2f}")
    print(f"Average Silhouette Score: {silhouette:.3f}")
    
    print("\n📢 Layman Narrative Interpretation:")
    if silhouette > 0.7:
        quality_str = "EXCELLENT. The customer groups are highly distinct and do not overlap."
    elif silhouette > 0.5:
        quality_str = "GOOD. The groups are clear, though some borderline customers exist."
    elif silhouette > 0.25:
        quality_str = "WEAK. The groups overlap significantly; boundaries are blurry."
    else:
        quality_str = "POOR. The data does not have natural clusters, or we chose the wrong 'k'."
        
    print(f"-> Clustering Quality: {quality_str}")
    
    # Describe the clusters in plain English based on their centroid coordinates
    print("\n🔍 What do these groups actually mean?")
    for i, centroid in enumerate(kmeans.centroids):
        age_val, spend_val = centroid
        size = np.sum(kmeans.labels == i)
        
        # Labeling logic based on centroid position
        if age_val < 38 and spend_val > 65:
            label = "🚀 'Young Trendsetters' (Younger age, high spending rate)"
            desc = "These are high-value younger customers. Target them with new arrivals, modern trends, and digital campaigns."
        elif age_val > 50 and spend_val < 35:
            label = "🏡 'Conservative Seniors' (Older age, low spending rate)"
            desc = "These customers are highly budget-conscious. Target them with discount loyalty programs and classic items."
        else:
            label = "💼 'Middle-of-the-Road' (Moderate age, moderate spending)"
            desc = "These represent the stable core. They make regular, predictable purchases. Target with standard newsletter updates."
            
        print(f"\nGroup {i+1}: {label}")
        print(f"   - Size: {size} customers ({size/len(X)*100:.1f}% of base)")
        print(f"   - Average Profile: Age {age_val:.1f} years, Spending Score {spend_val:.1f}/100")
        print(f"   - Business Action: {desc}")

    # 5. Plot and save
    os.makedirs("/home/gaian/Unsupervised/python/clustering", exist_ok=True)
    plt.figure(figsize=(10, 6), facecolor='#121214')
    ax = plt.axes()
    ax.set_facecolor('#1e1e24')
    
    colors = ['#ff4d6d', '#3a86c8', '#00f5d4']
    for i in range(k):
        cluster_data = X[kmeans.labels == i]
        plt.scatter(cluster_data[:, 0], cluster_data[:, 1], s=50, c=colors[i], label=f'Group {i+1}', alpha=0.8, edgecolors='none')
    
    # Plot centroids
    plt.scatter(kmeans.centroids[:, 0], kmeans.centroids[:, 1], s=250, marker='*', c='#ffffff', 
                edgecolors='#000000', linewidths=1.5, label='Group Centroids', zorder=10)
    
    plt.title('K-Means Customer Segmentation Map', fontsize=14, color='#ffffff', pad=15)
    plt.xlabel('Customer Age (Years)', fontsize=11, color='#cccccc')
    plt.ylabel('Spending Score (1-100)', fontsize=11, color='#cccccc')
    
    # Style legend & axes
    legend = plt.legend(facecolor='#1e1e24', edgecolor='#333333', labelcolor='#ffffff')
    ax.tick_params(colors='#cccccc')
    ax.spines['bottom'].set_color('#333333')
    ax.spines['left'].set_color('#333333')
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    plt.grid(color='#333333', linestyle='--', alpha=0.3)
    
    output_path = "/home/gaian/Unsupervised/python/clustering/kmeans_result.png"
    plt.savefig(output_path, dpi=150, bbox_inches='tight')
    plt.close()
    
    print(f"\n[+] Visualization successfully saved to: {output_path}")
    print("=" * 70)

if __name__ == '__main__':
    main()
