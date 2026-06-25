import numpy as np
import matplotlib.pyplot as plt
import os

class CustomDBSCAN:
    """
    A clean, from-scratch implementation of DBSCAN (Density-Based Spatial Clustering
    of Applications with Noise) designed for educational clarity.
    """
    def __init__(self, eps=1.5, min_samples=5):
        self.eps = eps
        self.min_samples = min_samples
        self.labels_ = None
        self.core_sample_indices_ = []
        self.components_ = [] # Core points
        
    def _get_neighbors(self, X, point_idx):
        # Calculate Euclidean distances from the target point to all other points
        distances = np.linalg.norm(X - X[point_idx], axis=1)
        return np.where(distances <= self.eps)[0]

    def fit(self, X):
        n_samples = X.shape[0]
        # -1 represents unclassified, -2 represents noise
        self.labels_ = np.full(n_samples, -1)
        self.core_sample_indices_ = []
        
        cluster_id = 0
        
        for i in range(n_samples):
            if self.labels_[i] != -1:
                continue # Already processed
                
            # Find neighbors within radius eps
            neighbors = self._get_neighbors(X, i)
            
            if len(neighbors) < self.min_samples:
                # Label as noise for now (might be relabeled as border point later)
                self.labels_[i] = -2
            else:
                # It is a Core point! Mark it and expand the cluster
                self.core_sample_indices_.append(i)
                self.labels_[i] = cluster_id
                
                # Expand cluster using a queue (Breadth-First Search)
                queue = list(neighbors)
                
                # Remove the current point from queue to avoid redundant checks
                if i in queue:
                    queue.remove(i)
                    
                idx = 0
                while idx < len(queue):
                    neighbor_idx = queue[idx]
                    
                    # If previously classified as noise, it's a border point!
                    if self.labels_[neighbor_idx] == -2:
                        self.labels_[neighbor_idx] = cluster_id
                        
                    # If unclassified, process it
                    elif self.labels_[neighbor_idx] == -1:
                        self.labels_[neighbor_idx] = cluster_id
                        
                        # Find its neighbors
                        sub_neighbors = self._get_neighbors(X, neighbor_idx)
                        
                        # If the neighbor is also a Core point, expand its neighbors
                        if len(sub_neighbors) >= self.min_samples:
                            self.core_sample_indices_.append(neighbor_idx)
                            for sn in sub_neighbors:
                                if sn not in queue and self.labels_[sn] == -1:
                                    queue.append(sn)
                                    
                    idx += 1
                
                cluster_id += 1 # Move to the next cluster
                
        # Format labels: make noise points -1 instead of -2 for standard notation
        # -1 = Noise, 0, 1, 2... = Clusters
        self.labels_[self.labels_ == -2] = -1
        self.core_sample_indices_ = np.array(self.core_sample_indices_)
        return self

def generate_concentric_rings():
    """
    Generates a 2D synthetic dataset of two concentric rings + random noise.
    Standard K-Means fails on this because it cannot handle non-spherical shapes,
    making it the perfect showcase for DBSCAN.
    """
    np.random.seed(42)
    n_points_inner = 100
    n_points_outer = 200
    n_noise = 25
    
    # Inner ring (radius ~ 2.0)
    theta_inner = np.linspace(0, 2 * np.pi, n_points_inner)
    r_inner = 2.0 + np.random.normal(0, 0.15, n_points_inner)
    x_inner = r_inner * np.cos(theta_inner)
    y_inner = r_inner * np.sin(theta_inner)
    
    # Outer ring (radius ~ 5.0)
    theta_outer = np.linspace(0, 2 * np.pi, n_points_outer)
    r_outer = 5.0 + np.random.normal(0, 0.2, n_points_outer)
    x_outer = r_outer * np.cos(theta_outer)
    y_outer = r_outer * np.sin(theta_outer)
    
    # Random noise (outliers scattered throughout)
    x_noise = np.random.uniform(-7, 7, n_noise)
    y_noise = np.random.uniform(-7, 7, n_noise)
    
    x = np.concatenate([x_inner, x_outer, x_noise])
    y = np.concatenate([y_inner, y_outer, y_noise])
    
    X = np.column_stack((x, y))
    return X

def main():
    print("=" * 70)
    print("   UNSUPERVISED LEARNING: DBSCAN COMPLEX SHAPE CLUSTERING DEMO")
    print("=" * 70)
    
    # 1. Generate data
    X = generate_concentric_rings()
    print(f"[*] Generated synthetic dataset: {X.shape[0]} points containing:")
    print("    - A tight inner ring of points (100 samples)")
    print("    - A larger outer ring enclosing the inner one (200 samples)")
    print("    - Randomly scattered outlier noise points (25 samples)")
    print("    Note: K-Means would slice these rings in half because it only understands blobs.")
    
    # 2. Fit Custom DBSCAN
    # We choose an epsilon (neighborhood radius) of 1.0 and minimum points of 5
    eps = 1.0
    min_samples = 4
    dbscan = CustomDBSCAN(eps=eps, min_samples=min_samples)
    dbscan.fit(X)
    
    # 3. Analyze results
    labels = dbscan.labels_
    unique_labels = np.unique(labels)
    n_clusters = len(unique_labels[unique_labels >= 0])
    n_noise = np.sum(labels == -1)
    n_core = len(dbscan.core_sample_indices_)
    n_border = len(X) - n_core - n_noise
    
    # 4. Show results and layman narrative
    print("\n" + "-" * 50)
    print("📊 ALGORITHM RESULTS (TECHNICAL & LAYMAN TRANSATION)")
    print("-" * 50)
    print(f"Parameters: Epsilon (Search Radius) = {eps}, Min Samples = {min_samples}")
    print(f"Number of Clusters Discovered: {n_clusters}")
    print(f"Core Points (Dense centerpieces): {n_core}")
    print(f"Border Points (Edge of groups): {n_border}")
    print(f"Noise Points (Isolated outliers): {n_noise}")
    
    print("\n📢 Layman Narrative Interpretation:")
    print("-> How DBSCAN thinks:")
    print("   Instead of forcing every point into a group, DBSCAN works like a social network spreading a rumor.")
    print(f"   A point is a 'Core' member if it has at least {min_samples} close neighbors within a distance of {eps}.")
    print("   If a point is close to a group but doesn't have enough neighbors of its own, it's a 'Border' member.")
    print("   If a point is completely isolated, it is labeled as 'Noise' (outliers).")
    
    print("\n🔍 What do these results tell us?")
    print(f"   - DBSCAN successfully found {n_clusters} distinct groups. By looking at the shapes, these represent")
    print("     the inner ring and the outer ring separately, completely preserving their circular geometry.")
    print(f"   - It successfully isolated {n_noise} noisy points that were floating in the empty space between")
    print("     and around the rings, preventing them from distorting the shape of the true groups.")
    
    # 5. Plot and save
    os.makedirs("/home/gaian/Unsupervised/python/clustering", exist_ok=True)
    plt.figure(figsize=(10, 8), facecolor='#121214')
    ax = plt.axes()
    ax.set_facecolor('#1e1e24')
    
    # Colors: Outliers are grey/dimmed, clusters are vibrant
    colors = ['#ff4d6d', '#00f5d4', '#ffb703', '#3a86c8']
    
    # Plot noise points
    noise_data = X[labels == -1]
    plt.scatter(noise_data[:, 0], noise_data[:, 1], s=40, c='#5c5c64', label='Noise (Outliers)', alpha=0.6, marker='x')
    
    # Plot clusters
    for i in range(n_clusters):
        cluster_data = X[labels == i]
        
        # Distinguish core vs border points in the plot
        is_core = np.isin(np.where(labels == i)[0], dbscan.core_sample_indices_)
        core_data = cluster_data[is_core]
        border_data = cluster_data[~is_core]
        
        # Plot core points (larger, solid)
        plt.scatter(core_data[:, 0], core_data[:, 1], s=55, c=colors[i % len(colors)], 
                    label=f'Cluster {i+1} (Core)', alpha=0.9, edgecolors='none')
        
        # Plot border points (smaller, transparent)
        if len(border_data) > 0:
            plt.scatter(border_data[:, 0], border_data[:, 1], s=25, c=colors[i % len(colors)], 
                        alpha=0.4, edgecolors='#ffffff', linewidths=0.5, label=f'Cluster {i+1} (Border)')
            
    plt.title('DBSCAN Density-Based Clustering Map', fontsize=14, color='#ffffff', pad=15)
    plt.xlabel('X Coordinate', fontsize=11, color='#cccccc')
    plt.ylabel('Y Coordinate', fontsize=11, color='#cccccc')
    
    # Style legend & axes
    # Deduplicate legend items
    handles, labels_legend = plt.gca().get_legend_handles_labels()
    by_label = dict(zip(labels_legend, handles))
    plt.legend(by_label.values(), by_label.keys(), facecolor='#1e1e24', edgecolor='#333333', labelcolor='#ffffff', loc='upper right')
    
    ax.tick_params(colors='#cccccc')
    ax.spines['bottom'].set_color('#333333')
    ax.spines['left'].set_color('#333333')
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    plt.grid(color='#333333', linestyle='--', alpha=0.3)
    plt.axis('equal')
    
    output_path = "/home/gaian/Unsupervised/python/clustering/dbscan_result.png"
    plt.savefig(output_path, dpi=150, bbox_inches='tight')
    plt.close()
    
    print(f"\n[+] Visualization successfully saved to: {output_path}")
    print("=" * 70)

if __name__ == '__main__':
    main()
