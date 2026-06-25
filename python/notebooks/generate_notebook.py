import json
import os

def create_notebook():
    notebook = {
        "cells": [
            {
                "cell_type": "markdown",
                "metadata": {},
                "source": [
                    "# 🎓 Unsupervised Learning Masterclass: Core Pillars & Visual Implementations\n",
                    "\n",
                    "Welcome to the **Unsupervised Learning Masterclass**! Unsupervised learning is the branch of machine learning that discovers hidden patterns, structures, or relationships in data without the guidance of pre-assigned labels or answers.\n",
                    "\n",
                    "This notebook acts as an interactive, educational workbook. We will walk through the **four key pillars of unsupervised learning** using our custom, from-scratch implementations located in the parent directory:\n",
                    "\n",
                    "1. **Clustering**: Grouping similar items (K-Means & DBSCAN)\n",
                    "2. **Dimensionality Reduction**: Simplifying complex, high-dimensional data (PCA)\n",
                    "3. **Anomaly Detection**: Identifying rare outliers (Isolation Forest)\n",
                    "4. **Association Rule Mining**: Discovering purchase patterns (Apriori)\n",
                    "\n",
                    "Let's add the parent directory to the Python path so we can import our custom modules, and then dive right in!"
                ]
            },
            {
                "cell_type": "code",
                "execution_count": None,
                "metadata": {},
                "outputs": [],
                "source": [
                    "import sys\n",
                    "import os\n",
                    "import numpy as np\n",
                    "import matplotlib.pyplot as plt\n",
                    "\n",
                    "# Add parent directory to sys.path so we can import our custom engines\n",
                    "sys.path.append(os.path.abspath('..'))\n",
                    "\n",
                    "print(\"[+] Libraries loaded and custom path configured successfully.\")"
                ]
            },
            {
                "cell_type": "markdown",
                "metadata": {},
                "source": [
                    "--- \n",
                    "## 1. Clustering (Grouping Similar Items)\n",
                    "\n",
                    "Clustering is about dividing data points into groups (clusters) such that points in the same group are highly similar to each other, and highly different from points in other groups.\n",
                    "\n",
                    "### A. K-Means Clustering\n",
                    "* **Concept**: Partition-based clustering. It places $k$ points (centroids) randomly, groups data by nearest centroid, then shifts centroids to the center of those groups, repeating until they stop moving.\n",
                    "* **Layman Metaphor**: Think of $k$ politicians trying to position themselves in a crowd of voters to minimize the distance to their nearest supporters. As voters adjust their allegiance, politicians move their podiums to the center of their new voter base.\n",
                    "\n",
                    "Let's run our custom K-Means engine on a synthetic Customer Segmentation dataset (Age vs. Spending habits):"
                ]
            },
            {
                "cell_type": "code",
                "execution_count": None,
                "metadata": {},
                "outputs": [],
                "source": [
                    "from clustering.kmeans import CustomKMeans, generate_demo_dataset, calculate_silhouette_score_simple\n",
                    "\n",
                    "# 1. Generate customer data\n",
                    "X_kmeans = generate_demo_dataset()\n",
                    "\n",
                    "# 2. Fit K-Means (k=3)\n",
                    "kmeans = CustomKMeans(k=3, random_state=42)\n",
                    "kmeans.fit(X_kmeans)\n",
                    "\n",
                    "# 3. Evaluate using Silhouette Score\n",
                    "sil_score = calculate_silhouette_score_simple(X_kmeans, kmeans.labels)\n",
                    "\n",
                    "print(f\"Average Silhouette Score: {sil_score:.3f}\")\n",
                    "print(\"Centroids found:\")\n",
                    "for i, c in enumerate(kmeans.centroids):\n",
                    "    print(f\"  Group {i+1}: Age = {c[0]:.1f} years, Spending Score = {c[1]:.1f}/100\")"
                ]
            },
            {
                "cell_type": "code",
                "execution_count": None,
                "metadata": {},
                "outputs": [],
                "source": [
                    "# 4. Plot results\n",
                    "plt.figure(figsize=(9, 5), facecolor='#121214')\n",
                    "ax = plt.axes()\n",
                    "ax.set_facecolor('#1e1e24')\n",
                    "\n",
                    "colors = ['#ff4d6d', '#3a86c8', '#00f5d4']\n",
                    "for i in range(3):\n",
                    "    cluster_data = X_kmeans[kmeans.labels == i]\n",
                    "    plt.scatter(cluster_data[:, 0], cluster_data[:, 1], s=55, c=colors[i], label=f'Group {i+1}', alpha=0.8)\n",
                    "\n",
                    "plt.scatter(kmeans.centroids[:, 0], kmeans.centroids[:, 1], s=250, marker='*', c='#ffffff', \n",
                    "            edgecolors='#000000', linewidths=1.5, label='Centroids', zorder=10)\n",
                    "\n",
                    "plt.title('K-Means Customer Segments', color='#ffffff', fontsize=13)\n",
                    "plt.xlabel('Age (Years)', color='#cccccc')\n",
                    "plt.ylabel('Spending Score (1-100)', color='#cccccc')\n",
                    "ax.tick_params(colors='#cccccc')\n",
                    "plt.legend(facecolor='#1e1e24', edgecolor='#333333', labelcolor='#ffffff')\n",
                    "plt.grid(color='#333333', linestyle='--', alpha=0.3)\n",
                    "plt.show()"
                ]
            },
            {
                "cell_type": "markdown",
                "metadata": {},
                "source": [
                    "### B. DBSCAN Clustering\n",
                    "* **Concept**: Density-based clustering. Instead of assuming groups are round blobs (like K-Means), DBSCAN grows clusters like a rumor spreading in a social circle. It groups points that are close to many other points, and rejects isolated points as noise.\n",
                    "* **Layman Metaphor**: If you stand near 4 people at a party, you are part of a dense conversation circle. If you are standing far away in the corner alone, you are labeled as 'noise' (outliers).\n",
                    "\n",
                    "Let's see how DBSCAN handles concentric circles, which K-Means would fail to cluster correctly:"
                ]
            },
            {
                "cell_type": "code",
                "execution_count": None,
                "metadata": {},
                "outputs": [],
                "source": [
                    "from clustering.dbscan import CustomDBSCAN, generate_concentric_rings\n",
                    "\n",
                    "# 1. Generate non-linear ring data\n",
                    "X_dbscan = generate_concentric_rings()\n",
                    "\n",
                    "# 2. Fit DBSCAN\n",
                    "dbscan = CustomDBSCAN(eps=1.0, min_samples=4)\n",
                    "dbscan.fit(X_dbscan)\n",
                    "\n",
                    "labels = dbscan.labels_\n",
                    "n_clusters = len(np.unique(labels[labels >= 0]))\n",
                    "n_noise = np.sum(labels == -1)\n",
                    "print(f\"DBSCAN found {n_clusters} clusters and isolated {n_noise} noise points.\")"
                ]
            },
            {
                "cell_type": "code",
                "execution_count": None,
                "metadata": {},
                "outputs": [],
                "source": [
                    "# 3. Plot DBSCAN results\n",
                    "plt.figure(figsize=(8, 6), facecolor='#121214')\n",
                    "ax = plt.axes()\n",
                    "ax.set_facecolor('#1e1e24')\n",
                    "\n",
                    "# Plot Noise\n",
                    "noise = X_dbscan[labels == -1]\n",
                    "plt.scatter(noise[:, 0], noise[:, 1], s=35, c='#5c5c64', label='Noise (Outliers)', marker='x', alpha=0.6)\n",
                    "\n",
                    "# Plot Clusters\n",
                    "colors = ['#ff4d6d', '#00f5d4', '#ffb703', '#3a86c8']\n",
                    "for i in range(n_clusters):\n",
                    "    cluster_data = X_dbscan[labels == i]\n",
                    "    plt.scatter(cluster_data[:, 0], cluster_data[:, 1], s=45, c=colors[i % len(colors)], label=f'Cluster {i+1}', alpha=0.8)\n",
                    "\n",
                    "plt.title('DBSCAN Density-Based Rings', color='#ffffff', fontsize=13)\n",
                    "ax.tick_params(colors='#cccccc')\n",
                    "plt.legend(facecolor='#1e1e24', edgecolor='#333333', labelcolor='#ffffff')\n",
                    "plt.grid(color='#333333', linestyle='--', alpha=0.3)\n",
                    "plt.axis('equal')\n",
                    "plt.show()"
                ]
            },
            {
                "cell_type": "markdown",
                "metadata": {},
                "source": [
                    "--- \n",
                    "## 2. Dimensionality Reduction (Simplifying Complex Data)\n",
                    "\n",
                    "### PCA (Principal Component Analysis)\n",
                    "* **Concept**: Linear dimensionality reduction. It rotates and projects data to find the directions (Principal Components) along which the data varies the most. This lets us compress high-dimensional data (e.g., 10 features) down to 2D or 3D while keeping most of the original information.\n",
                    "* **Layman Metaphor**: Imagine taking a 2D photograph of a 3D teapot sculpture. If you photograph it from the top, it looks like a flat circle (bad angle). If you photograph it from the side, you see the spout, handle, and body clearly (good angle). PCA rotates the sculpture to find the angle that captures the maximum detail.\n",
                    "\n",
                    "Let's compress a tilted 3D flat sheet of points down to a 2D map using our custom PCA engine:"
                ]
            },
            {
                "cell_type": "code",
                "execution_count": None,
                "metadata": {},
                "outputs": [],
                "source": [
                    "from dimensionality.pca import CustomPCA, generate_tilted_3d_sheet\n",
                    "\n",
                    "# 1. Generate tilted 3D data\n",
                    "X_pca = generate_tilted_3d_sheet()\n",
                    "\n",
                    "# 2. Fit and transform to 2D\n",
                    "pca = CustomPCA(n_components=2)\n",
                    "X_projected = pca.fit_transform(X_pca)\n",
                    "\n",
                    "print(\"Explained Variance Ratio:\")\n",
                    "for idx, ratio in enumerate(pca.explained_variance_ratio_):\n",
                    "    print(f\"  Component {idx+1}: {ratio*100:.2f}%\")\n",
                    "print(f\"Total variance retained in 2D: {np.sum(pca.explained_variance_ratio_[:2])*100:.2f}%\")"
                ]
            },
            {
                "cell_type": "code",
                "execution_count": None,
                "metadata": {},
                "source": [
                    "# 3. Plot 3D original and 2D projected side-by-side\n",
                    "fig = plt.figure(figsize=(14, 6), facecolor='#121214')\n",
                    "\n",
                    "# Left Plot: 3D\n",
                    "ax1 = fig.add_subplot(1, 2, 1, projection='3d')\n",
                    "ax1.set_facecolor('#121214')\n",
                    "ax1.scatter(X_pca[:, 0], X_pca[:, 1], X_pca[:, 2], c=X_pca[:, 2], cmap='cool', s=25, alpha=0.8)\n",
                    "ax1.set_title('Original 3D Data (Flat Sheet)', color='#ffffff')\n",
                    "ax1.xaxis.pane.set_facecolor((0.1, 0.1, 0.12, 1.0))\n",
                    "ax1.yaxis.pane.set_facecolor((0.1, 0.1, 0.12, 1.0))\n",
                    "ax1.zaxis.pane.set_facecolor((0.1, 0.1, 0.12, 1.0))\n",
                    "ax1.tick_params(colors='#cccccc')\n",
                    "\n",
                    "# Right Plot: 2D Projection\n",
                    "ax2 = fig.add_subplot(1, 2, 2)\n",
                    "ax2.set_facecolor('#1e1e24')\n",
                    "ax2.scatter(X_projected[:, 0], X_projected[:, 1], c=X_pca[:, 2], cmap='cool', s=40, alpha=0.8)\n",
                    "ax2.set_title('PCA Projected 2D Shadow', color='#ffffff')\n",
                    "ax2.set_xlabel('Principal Component 1 (PC1)', color='#cccccc')\n",
                    "ax2.set_ylabel('Principal Component 2 (PC2)', color='#cccccc')\n",
                    "ax2.tick_params(colors='#cccccc')\n",
                    "ax2.grid(color='#333333', linestyle='--', alpha=0.3)\n",
                    "\n",
                    "plt.show()"
                ]
            },
            {
                "cell_type": "markdown",
                "metadata": {},
                "source": [
                    "--- \n",
                    "## 3. Anomaly Detection (Finding the Odd Ones Out)\n",
                    "\n",
                    "### Isolation Forest\n",
                    "* **Concept**: Tree-based outlier detection. It isolates points by randomly partitioning features. Outliers (anomalies) are located in sparse regions, so they get isolated in very few splits (near the root of the trees). Normal points require many splits to isolate.\n",
                    "* **Layman Metaphor**: Imagine a game of 20 Questions. If you are trying to guess a word that is extremely common (like 'apple'), it takes many specific questions to narrow it down. If you are guessing a highly unusual word (like 'quantum-teleportation'), a couple of broad questions immediately isolate it.\n",
                    "\n",
                    "Let's run our custom Isolation Forest on credit card transaction records to flag fraud:"
                ]
            },
            {
                "cell_type": "code",
                "execution_count": None,
                "metadata": {},
                "outputs": [],
                "source": [
                    "from anomaly.isolation_forest import CustomIsolationForest, generate_transaction_data\n",
                    "\n",
                    "# 1. Generate transaction data (normal vs fraud)\n",
                    "X_fraud = generate_transaction_data()\n",
                    "\n",
                    "# 2. Fit Isolation Forest\n",
                    "forest = CustomIsolationForest(n_estimators=100, max_samples=128, random_state=42)\n",
                    "forest.fit(X_fraud)\n",
                    "\n",
                    "# 3. Compute anomaly scores\n",
                    "scores = forest.compute_anomaly_score(X_fraud)\n",
                    "threshold = 0.6\n",
                    "flagged_idx = np.where(scores > threshold)[0]\n",
                    "print(f\"Audited {len(X_fraud)} transactions. Flagged {len(flagged_idx)} as high-risk anomalies.\")"
                ]
            },
            {
                "cell_type": "code",
                "execution_count": None,
                "metadata": {},
                "outputs": [],
                "source": [
                    "# 4. Plot decision boundary heatmap\n",
                    "plt.figure(figsize=(10, 6), facecolor='#121214')\n",
                    "ax = plt.axes()\n",
                    "ax.set_facecolor('#1e1e24')\n",
                    "\n",
                    "# Create grid to plot heatmap\n",
                    "xx, yy = np.meshgrid(np.linspace(0, 500, 100), np.linspace(0, 50, 80))\n",
                    "grid_points = np.c_[xx.ravel(), yy.ravel()]\n",
                    "grid_scores = forest.compute_anomaly_score(grid_points).reshape(xx.shape)\n",
                    "\n",
                    "# Plot heatmap\n",
                    "contour = plt.contourf(xx, yy, grid_scores, levels=15, cmap='plasma', alpha=0.8)\n",
                    "cbar = plt.colorbar(contour, shrink=0.8)\n",
                    "cbar.set_label('Anomaly Score (Closer to 1 = Outlier)', color='#cccccc', labelpad=10)\n",
                    "cbar.ax.yaxis.set_tick_params(color='#cccccc')\n",
                    "plt.setp(plt.getp(cbar.ax.axes, 'yticklabels'), color='#cccccc')\n",
                    "\n",
                    "# Plot normal points vs anomalies\n",
                    "normal_idx = np.where(scores <= threshold)[0]\n",
                    "plt.scatter(X_fraud[normal_idx, 0], X_fraud[normal_idx, 1], s=35, c='#00ffcc', edgecolors='none', label='Normal', alpha=0.7)\n",
                    "plt.scatter(X_fraud[flagged_idx, 0], X_fraud[flagged_idx, 1], s=70, c='#ff0055', edgecolors='#ffffff', label='Fraud Suspicion')\n",
                    "\n",
                    "plt.title('Isolation Forest Fraud Detection Heatmap', color='#ffffff', fontsize=13)\n",
                    "plt.xlabel('Transaction Amount ($)', color='#cccccc')\n",
                    "plt.ylabel('Purchase Frequency (per week)', color='#cccccc')\n",
                    "plt.legend(facecolor='#1e1e24', edgecolor='#333333', labelcolor='#ffffff')\n",
                    "ax.tick_params(colors='#cccccc')\n",
                    "plt.show()"
                ]
            },
            {
                "cell_type": "markdown",
                "metadata": {},
                "source": [
                    "--- \n",
                    "## 4. Association Rule Mining (Finding Hidden Relationships)\n",
                    "\n",
                    "### Apriori Algorithm\n",
                    "* **Concept**: Discovering 'if-then' relationships in transactional database. It looks at three main metrics:\n",
                    "  1. **Support**: How popular is the itemset? (e.g., fraction of all receipts containing Bread + Butter)\n",
                    "  2. **Confidence**: How reliable is the rule? (e.g., 'Of those who bought Bread, 80% also bought Butter')\n",
                    "  3. **Lift**: How much stronger is the rule than random chance? (e.g., 'If lift is 2, buying Bread makes a customer 2x more likely to buy Butter than a normal customer')\n",
                    "\n",
                    "Let's run our custom Apriori engine on a list of grocery transactions to find shopping associations:"
                ]
            },
            {
                "cell_type": "code",
                "execution_count": None,
                "metadata": {},
                "outputs": [],
                "source": [
                    "from association.apriori import CustomApriori, generate_grocery_transactions\n",
                    "\n",
                    "# 1. Load transactions\n",
                    "baskets = generate_grocery_transactions()\n",
                    "\n",
                    "# 2. Run Apriori\n",
                    "apriori = CustomApriori(min_support=0.25, min_confidence=0.6)\n",
                    "apriori.fit(baskets)\n",
                    "\n",
                    "print(f\"Discovered {len(apriori.rules)} strong association rules:\")\n",
                    "for idx, r in enumerate(sorted(apriori.rules, key=lambda x: x['lift'], reverse=True)[:5]):\n",
                    "    ant = \" + \".join(r['antecedent'])\n",
                    "    cons = \" + \".join(r['consequent'])\n",
                    "    print(f\"  Rule {idx+1}: [{ant}] ---> [{cons}]\")\n",
                    "    print(f\"    - Support: {r['support']*100:.1f}%  |  Confidence: {r['confidence']*100:.1f}%  |  Lift: {r['lift']:.2f}x\")"
                ]
            },
            {
                "cell_type": "code",
                "execution_count": None,
                "metadata": {},
                "outputs": [],
                "source": [
                    "# 3. Visualize rules using a bubble plot\n",
                    "rules = apriori.rules\n",
                    "supports = [r['support'] for r in rules]\n",
                    "confidences = [r['confidence'] for r in rules]\n",
                    "lifts = [r['lift'] for r in rules]\n",
                    "\n",
                    "plt.figure(figsize=(9, 5.5), facecolor='#121214')\n",
                    "ax = plt.axes()\n",
                    "ax.set_facecolor('#1e1e24')\n",
                    "\n",
                    "scatter = plt.scatter(supports, confidences, s=[l*130 for l in lifts], c=lifts, cmap='plasma', alpha=0.85, edgecolors='white', linewidths=0.5)\n",
                    "cbar = plt.colorbar(scatter, shrink=0.8)\n",
                    "cbar.set_label('Lift (Strength)', color='#cccccc', labelpad=10)\n",
                    "cbar.ax.yaxis.set_tick_params(color='#cccccc')\n",
                    "plt.setp(plt.getp(cbar.ax.axes, 'yticklabels'), color='#cccccc')\n",
                    "\n",
                    "plt.title('Discovered Association Rules (Apriori)', color='#ffffff', fontsize=13)\n",
                    "plt.xlabel('Support (Rule Popularity)', color='#cccccc')\n",
                    "plt.ylabel('Confidence (Rule Reliability)', color='#cccccc')\n",
                    "ax.tick_params(colors='#cccccc')\n",
                    "plt.grid(color='#333333', linestyle='--', alpha=0.3)\n",
                    "plt.show()"
                ]
            },
            {
                "cell_type": "markdown",
                "metadata": {},
                "source": [
                    "--- \n",
                    "## Conclusion\n",
                    "\n",
                    "Congratulations! You have completed the **Unsupervised Learning Masterclass**. \n",
                    "\n",
                    "You have successfully:\n",
                    "1. Grouped customers using K-Means and circular paths using DBSCAN.\n",
                    "2. Simplified complex 3D sheets to a flat 2D projection using PCA.\n",
                    "3. Isolated high-risk transactions from normal records using Isolation Forest.\n",
                    "4. Mined grocery receipts to find strong cross-selling bundles using Apriori.\n",
                    "\n",
                    "These tools form the backbone of exploratory data analysis, allowing you to extract structure, find outliers, and uncover relationships from unlabeled datasets in any domain. \n",
                    "\n",
                    "Feel free to experiment by changing the parameters (like `k`, `eps`, `min_samples`, `min_support`, or `min_confidence`) in the code cells above and running them again to see how the shapes and explanations change!"
                ]
            }
        ],
        "metadata": {
            "kernelspec": {
                "display_name": "Python 3",
                "language": "python",
                "name": "python3"
            },
            "language_info": {
                "name": "python"
            }
        },
        "nbformat": 4,
        "nbformat_minor": 2
    }
    
    os.makedirs("/home/gaian/Unsupervised/python/notebooks", exist_ok=True)
    output_path = "/home/gaian/Unsupervised/python/notebooks/unsupervised_masterclass.ipynb"
    with open(output_path, "w") as f:
        json.dump(notebook, f, indent=2)
        
    print(f"[+] Jupyter Notebook successfully generated at: {output_path}")

if __name__ == "__main__":
    create_notebook()
