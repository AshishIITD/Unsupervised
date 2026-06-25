# K-Means Clustering: Step-by-Step Educational Walkthrough

K-Means is a partition-based clustering algorithm. It groups data points into $K$ distinct clusters by minimizing the distance between points and their respective cluster centers (centroids). It runs in an iterative loop of **Assignment** (Expectation) and **Update** (Maximization) until the centroids stop shifting.

Here is a step-by-step trace using a tiny dataset.

---

## 📊 The Sample Dataset
Imagine we have 4 retail customers with two features: **Age** and **Spending Score (1-100)**:

* **Point A**: Age = 20, Spending = 80 (Young High Spender)
* **Point B**: Age = 22, Spending = 75 (Young High Spender)
* **Point C**: Age = 60, Spending = 20 (Senior Budget Shopper)
* **Point D**: Age = 62, Spending = 22 (Senior Budget Shopper)

We want to group them into **$K = 2$ clusters**.

---

## 🔁 Step-by-Step Clustering Loop

### 1️⃣ Step 1: Initial Centroid Placement
We randomly choose two points to act as our starting cluster centers (centroids):
* **Centroid 1 ($C_1$)**: Placed at Point A **(20, 80)** (Color Code: Pink)
* **Centroid 2 ($C_2$)**: Placed at Point C **(60, 20)** (Color Code: Blue)

---

### 2️⃣ Step 2: Distance & Cluster Assignment (Round 1)
We calculate the straight-line (Euclidean) distance from every point to both centroids:
$$\text{Distance} = \sqrt{(X_{\text{point}} - X_{\text{centroid}})^2 + (Y_{\text{point}} - Y_{\text{centroid}})^2}$$

* **Point A (20, 80)**:
  * Dist to $C_1 (20, 80) = 0$
  * Dist to $C_2 (60, 20) = \sqrt{(20-60)^2 + (80-20)^2} = \sqrt{1600 + 3600} = 72.1$
  * *Verdict*: Closest to $C_1$. **Assigned to Cluster 1 (Pink)**.

* **Point B (22, 75)**:
  * Dist to $C_1 (20, 80) = \sqrt{(22-20)^2 + (75-80)^2} = \sqrt{4 + 25} = \sqrt{29} \approx 5.38$
  * Dist to $C_2 (60, 20) = \sqrt{(22-60)^2 + (75-20)^2} = \sqrt{1444 + 3025} = \sqrt{4469} \approx 66.85$
  * *Verdict*: Closest to $C_1$. **Assigned to Cluster 1 (Pink)**.

* **Point C (60, 20)**:
  * Dist to $C_1 = 72.1$
  * Dist to $C_2 = 0$
  * *Verdict*: Closest to $C_2$. **Assigned to Cluster 2 (Blue)**.

* **Point D (62, 22)**:
  * Dist to $C_1 (20, 80) = \sqrt{(62-20)^2 + (22-80)^2} = \sqrt{1764 + 3364} = 71.6$
  * Dist to $C_2 (60, 20) = \sqrt{(62-60)^2 + (22-20)^2} = \sqrt{4 + 4} = \sqrt{8} \approx 2.83$
  * *Verdict*: Closest to $C_2$. **Assigned to Cluster 2 (Blue)**.

---

### 3️⃣ Step 3: Recalculate Centroid Positions (Round 1 Update)
Now, the centroids "fly" to the exact average center of their assigned members:

* **New Centroid 1 ($C_1'$)** (Average of A and B):
  * $X = \frac{20 + 22}{2} = 21$
  * $Y = \frac{80 + 75}{2} = 77.5$
  * *New Coordinates*: **(21, 77.5)**

* **New Centroid 2 ($C_2'$)** (Average of C and D):
  * $X = \frac{60 + 62}{2} = 61$
  * $Y = \frac{20 + 22}{2} = 21$
  * *New Coordinates*: **(61, 21)**

---

### 4️⃣ Step 4: Distance & Assignment (Round 2)
We recalculate distances to our new shifted centroids:

* **Point A (20, 80)**:
  * Dist to $C_1' (21, 77.5) = \sqrt{(20-21)^2 + (80-77.5)^2} = \sqrt{1 + 6.25} = 2.69$
  * Dist to $C_2' (61, 21) = \sqrt{(20-61)^2 + (80-21)^2} = 71.8$
  * *Verdict*: Remains in **Cluster 1**.

* **Point B (22, 75)**:
  * Dist to $C_1' = 2.69$
  * Dist to $C_2' = 67.9$
  * *Verdict*: Remains in **Cluster 1**.

* **Point C (60, 20)**:
  * Dist to $C_1' = 69.9$
  * Dist to $C_2' = 1.41$
  * *Verdict*: Remains in **Cluster 2**.

* **Point D (62, 22)**:
  * Dist to $C_1' = 69.1$
  * Dist to $C_2' = 1.41$
  * *Verdict*: Remains in **Cluster 2**.

---

## 📈 Convergence & Summary

Since **no points changed their cluster assignments** between Round 1 and Round 2, the algorithm has officially **converged**! The final groups are set:

| Customer | Coordinates (Age, Spend) | Final Cluster Assignment | Demographic Segment |
| :--- | :---: | :---: | :--- |
| **Point A** | (20, 80) | **Cluster 1** (Pink) | Young High Spenders |
| **Point B** | (22, 75) | **Cluster 1** (Pink) | Young High Spenders |
| **Point C** | (60, 20) | **Cluster 2** (Blue) | Senior Budget Shoppers |
| **Point D** | (62, 22) | **Cluster 2** (Blue) | Senior Budget Shoppers |

This trace shows how basic coordinate averages automatically separate completely different customer behaviors into neat, distinct target audiences.
