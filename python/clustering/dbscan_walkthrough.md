# DBSCAN Clustering: Step-by-Step Educational Walkthrough

DBSCAN (Density-Based Spatial Clustering of Applications with Noise) groups points based on local density. Unlike K-Means, it does not require you to pre-specify the number of clusters, and it is capable of discovering clusters of arbitrary shapes (like concentric rings) while cleanly filtering out outliers.

It relies on two parameters:
1. **$\epsilon$ (Epsilon)**: The maximum distance radius to search for neighbors.
2. **MinPts**: The minimum number of points (including itself) required inside a point's $\epsilon$-neighborhood to classify it as a **Core Point**.

---

## 📊 The Sample Dataset
Imagine we have 5 points plotted on a 2D coordinate grid:

* **Point A**: (1, 1)
* **Point B**: (1, 2)
* **Point C**: (2, 1)
* **Point D**: (1, 10)
* **Point E**: (10, 10)

We configure DBSCAN with a search radius **$\epsilon = 3$** and **$MinPts = 2$**.

---

## 🔍 Step-by-Step Algorithm Execution

### 1️⃣ Round 1: Scanning Point A
1. **Select Point A (1, 1)** as our starting point.
2. **Scan neighbors** within distance $\epsilon = 3$:
   * Distance to B (1, 2) = $1.0$ (Inside)
   * Distance to C (2, 1) = $1.0$ (Inside)
   * Distance to D (1, 10) = $9.0$ (Outside)
   * Distance to E (10, 10) = $12.7$ (Outside)
3. **Count neighborhood size**: The neighbors of A are **{A, B, C}** ($3$ points).
4. **Evaluate density**: Since the count ($3$) is $\ge MinPts$ ($2$), **Point A is labeled a Core Point**.
5. **Form cluster**: A starts **Cluster 1**. Its unvisited neighbors **{B, C}** are added to our expansion queue.

---

### 2️⃣ Round 2: Expanding via Point B
1. **Pop Point B (1, 2)** from the queue.
2. **Scan neighbors** of B within radius $\epsilon = 3$:
   * Neighbors of B are **{A, B, C}** ($3$ points).
3. **Evaluate density**: Since count ($3$) is $\ge MinPts$, **Point B is also a Core Point**.
4. **Expand cluster**: Since B is a Core point, any of its unvisited neighbors would be added to the queue (A and C are already visited or in queue, so no new additions). B is colored to join **Cluster 1**.

---

### 3️⃣ Round 3: Expanding via Point C
1. **Pop Point C (2, 1)** from the queue.
2. **Scan neighbors** of C within radius $\epsilon = 3$:
   * Neighbors of C are **{A, B, C}** ($3$ points).
3. **Evaluate density**: Since count ($3$) is $\ge MinPts$, **Point C is also a Core Point**.
4. **Expand cluster**: C is colored to join **Cluster 1**. 
5. The queue is now empty. **Cluster 1 expansion is complete**!

---

### 4️⃣ Round 4: Scanning Point D
1. **Select Point D (1, 10)** (next unvisited point).
2. **Scan neighbors** within radius $\epsilon = 3$:
   * Distance to E (10, 10) = $9.0$ (Outside)
   * All other points are far away.
3. **Count neighborhood size**: The only neighbor of D is **{D}** ($1$ point).
4. **Evaluate density**: Since the count ($1$) is $< MinPts$ ($2$), **Point D is not a Core Point**.
5. **Label status**: Since D has no path to any existing Core points and fails the density test, it is labeled as **Noise (Outlier)**.

---

### 5️⃣ Round 5: Scanning Point E
1. **Select Point E (10, 10)** (last unvisited point).
2. **Scan neighbors** within radius $\epsilon = 3$:
   * The only neighbor is **{E}** ($1$ point).
3. **Evaluate density**: Since count ($1$) is $< MinPts$, **Point E is not a Core Point**.
4. **Label status**: Point E is labeled as **Noise (Outlier)**.

---

## 📈 Summary of Results

| Point | Coordinates | Neighbors Found | Classification | Final Assignment |
| :--- | :---: | :---: | :--- | :--- |
| **Point A** | (1, 1) | 3 | **Core Point** | **Cluster 1** (Community) |
| **Point B** | (1, 2) | 3 | **Core Point** | **Cluster 1** (Community) |
| **Point C** | (2, 1) | 3 | **Core Point** | **Cluster 1** (Community) |
| **Point D** | (1, 10) | 1 | **Outlier** | 🔲 **Noise** |
| **Point E** | (10, 10) | 1 | **Outlier** | 🔲 **Noise** |

### Key Takeaway
DBSCAN successfully grouped the tightly packed neighborhood **{A, B, C}** together into a single community, while correctly identifying **D** and **E** as isolated outliers. If a point had landed at `(1, 4)`, it would have had only 1 neighbor (Point B) within radius 3; it wouldn't be a Core point, but because it connected to Core point B, DBSCAN would have welcomed it as a **Border Point** in Cluster 1.
