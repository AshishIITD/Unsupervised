import os

def generate_text_files():
    output_dir = "/home/gaian/Unsupervised/walkthroughs_text"
    os.makedirs(output_dir, exist_ok=True)

    # 1. K-Means Walkthrough Text
    kmeans_txt = """================================================================================
K-MEANS CLUSTERING: STEP-BY-STEP NUMERICAL WALKTHROUGH
================================================================================

K-Means is a partition-based clustering algorithm. It groups data points into
K distinct clusters by minimizing the distance between points and their respective
cluster centers (centroids). It runs in an iterative loop of:
1. ASSIGNMENT: Assign points to the nearest centroid.
2. UPDATE: Move centroids to the average center of their assigned points.

This process repeats until centroids stop shifting (converge).

--------------------------------------------------------------------------------
1. THE SAMPLE DATASET
--------------------------------------------------------------------------------
Imagine we have 4 retail customers with two features: Age and Spending Score (1-100).

  * Point A: Age = 20, Spending = 80  (Young High Spender)
  * Point B: Age = 22, Spending = 75  (Young High Spender)
  * Point C: Age = 60, Spending = 20  (Senior Budget Shopper)
  * Point D: Age = 62, Spending = 22  (Senior Budget Shopper)

We want to group them into K = 2 clusters.

--------------------------------------------------------------------------------
2. ITERATION 1: STARTING THE LOOP
--------------------------------------------------------------------------------

[STEP 1] INITIAL CENTROID PLACEMENT:
We randomly choose two points to act as our starting cluster centers:
  * Centroid 1 (C1): Placed at Point A (20, 80)
  * Centroid 2 (C2): Placed at Point C (60, 20)

[STEP 2] DISTANCE & CLUSTER ASSIGNMENT (ROUND 1):
We calculate the straight-line (Euclidean) distance from every point to both
centroids using the formula:
  Distance = sqrt((X_point - X_centroid)^2 + (Y_point - Y_centroid)^2)

  * Point A (20, 80):
    - Dist to C1 (20, 80) = 0.00
    - Dist to C2 (60, 20) = sqrt((20-60)^2 + (80-20)^2) = sqrt(1600+3600) = 72.11
    - Verdict: Closest to C1. Assigned to CLUSTER 1.

  * Point B (22, 75):
    - Dist to C1 (20, 80) = sqrt((22-20)^2 + (75-80)^2) = sqrt(4+25) = 5.39
    - Dist to C2 (60, 20) = sqrt((22-60)^2 + (75-20)^2) = sqrt(1444+3025) = 66.85
    - Verdict: Closest to C1. Assigned to CLUSTER 1.

  * Point C (60, 20):
    - Dist to C1 (20, 80) = 72.11
    - Dist to C2 (60, 20) = 0.00
    - Verdict: Closest to C2. Assigned to CLUSTER 2.

  * Point D (62, 22):
    - Dist to C1 (20, 80) = sqrt((62-20)^2 + (22-80)^2) = sqrt(1764+3364) = 71.61
    - Dist to C2 (60, 20) = sqrt((62-60)^2 + (22-20)^2) = sqrt(4+4) = 2.83
    - Verdict: Closest to C2. Assigned to CLUSTER 2.

[STEP 3] RECALCULATE CENTROID POSITIONS (ROUND 1 UPDATE):
Centroids shift to the exact average center of their assigned members.

  * New Centroid 1 (C1') [Average of A (20,80) and B (22,75)]:
    - X = (20 + 22) / 2 = 21
    - Y = (80 + 75) / 2 = 77.5
    - New Coordinates: (21, 77.5)

  * New Centroid 2 (C2') [Average of C (60,20) and D (62,22)]:
    - X = (60 + 62) / 2 = 61
    - Y = (20 + 22) / 2 = 21
    - New Coordinates: (61, 21)

--------------------------------------------------------------------------------
3. ITERATION 2: VERIFYING CONVERGENCE
--------------------------------------------------------------------------------

[STEP 4] RECALCULATE DISTANCES & ASSIGNMENTS (ROUND 2):
We check if any points change their cluster labels when measured against the
newly shifted centroids C1' (21, 77.5) and C2' (61, 21).

  * Point A (20, 80):
    - Dist to C1' (21, 77.5) = sqrt((20-21)^2 + (80-77.5)^2) = sqrt(1+6.25) = 2.69
    - Dist to C2' (61, 21) = 71.85
    - Verdict: Remains in CLUSTER 1.

  * Point B (22, 75):
    - Dist to C1' = 2.69
    - Dist to C2' = 67.90
    - Verdict: Remains in CLUSTER 1.

  * Point C (60, 20):
    - Dist to C1' = 69.90
    - Dist to C2' = sqrt((60-61)^2 + (20-21)^2) = sqrt(1+1) = 1.41
    - Verdict: Remains in CLUSTER 2.

  * Point D (62, 22):
    - Dist to C1' = 69.11
    - Dist to C2' = 1.41
    - Verdict: Remains in CLUSTER 2.

--------------------------------------------------------------------------------
4. CONVERGENCE & SUMMARY
--------------------------------------------------------------------------------
Since no points changed their cluster assignments between Iteration 1 and
Iteration 2, the algorithm has officially CONVERGED!

FINAL CUSTOMER GROUPS:
+------------+-----------------+-------------------+--------------------------+
| Customer   | Age, Spend      | Final Cluster     | Demographic Segment      |
+------------+-----------------+-------------------+--------------------------+
| Point A    | (20, 80)        | Cluster 1         | Young High Spenders      |
| Point B    | (22, 75)        | Cluster 1         | Young High Spenders      |
| Point C    | (60, 20)        | Cluster 2         | Senior Budget Shoppers   |
| Point D    | (62, 22)        | Cluster 2         | Senior Budget Shoppers   |
+------------+-----------------+-------------------+--------------------------+

By using simple coordinate averages, the algorithm automatically separated the
entire customer base into two highly distinct target audiences!
================================================================================"""

    # 2. DBSCAN Walkthrough Text
    dbscan_txt = """================================================================================
DBSCAN CLUSTERING: STEP-BY-STEP NUMERICAL WALKTHROUGH
================================================================================

DBSCAN (Density-Based Spatial Clustering) groups points based on local density.
It does not require you to pre-specify the number of clusters, and it easily
discovers winding, circular, or nested shapes while discarding outliers.

It relies on two parameters:
1. Epsilon (Eps): The maximum search radius to look for neighbors.
2. MinPts: The minimum number of points (including itself) required inside the
   search radius to classify a point as a "Core Point".

--------------------------------------------------------------------------------
1. THE SAMPLE DATASET
--------------------------------------------------------------------------------
Imagine we have 5 points plotted on a 2D grid:

  * Point A: (1, 1)
  * Point B: (1, 2)
  * Point C: (2, 1)
  * Point D: (1, 10)
  * Point E: (10, 10)

We set Epsilon (Eps) = 3 and MinPts = 2.

--------------------------------------------------------------------------------
2. STEP-BY-STEP DENSITY SCANNING
--------------------------------------------------------------------------------

[ROUND 1] SCANNING POINT A (1, 1):
1. Select Point A as our start point.
2. Scan neighbors within search radius Eps = 3:
   - Distance to B (1, 2) = 1.00 (Inside)
   - Distance to C (2, 1) = 1.00 (Inside)
   - Distance to D (1, 10) = 9.00 (Outside)
   - Distance to E (10, 10) = 12.72 (Outside)
3. Count neighborhood size: Neighbors of A are {A, B, C} (3 points).
4. Evaluate density: Since count (3) is >= MinPts (2), Point A is labeled a CORE POINT.
5. Form cluster: A starts CLUSTER 1. Its unvisited neighbors {B, C} are added
   to our expansion queue.

[ROUND 2] EXPANDING VIA POINT B (1, 2):
1. Pop Point B from the expansion queue.
2. Scan neighbors of B within radius Eps = 3:
   - Neighbors of B are {A, B, C} (3 points).
3. Evaluate density: Since count (3) is >= MinPts, Point B is labeled a CORE POINT.
4. Expand: B joins CLUSTER 1. No new unvisited neighbors need to be queued.

[ROUND 3] EXPANDING VIA POINT C (2, 1):
1. Pop Point C from the queue.
2. Scan neighbors of C within radius Eps = 3:
   - Neighbors of C are {A, B, C} (3 points).
3. Evaluate density: Since count (3) is >= MinPts, Point C is labeled a CORE POINT.
4. Expand: C joins CLUSTER 1.
5. The queue is now empty. CLUSTER 1 expansion is complete!

[ROUND 4] SCANNING POINT D (1, 10):
1. Select Point D (next unvisited point).
2. Scan neighbors within radius Eps = 3:
   - Neighbors of D is only {D} (1 point). Distance to E (10, 10) is 9.00 (Outside).
3. Evaluate density: Since count (1) is < MinPts (2), Point D is NOT a Core Point.
4. Label status: Since D has no connections to Core points, it is labeled as NOISE (Outlier).

[ROUND 5] SCANNING POINT E (10, 10):
1. Select Point E (last unvisited point).
2. Scan neighbors within radius Eps = 3:
   - Neighbors of E is only {E} (1 point).
3. Evaluate density: Since count (1) is < MinPts (2), Point E is NOT a Core Point.
4. Label status: Point E is labeled as NOISE (Outlier).

--------------------------------------------------------------------------------
3. FINAL RESULTS SUMMARY
--------------------------------------------------------------------------------
DBSCAN has completed scanning the entire dataset.

FINAL DENSITY CHART:
+---------+-------------+-----------------+---------------+--------------------+
| Point   | Coordinates | Neighbors Found | Class Type    | Final Assignment   |
+---------+-------------+-----------------+---------------+--------------------+
| Point A | (1, 1)      | 3               | Core Point    | Cluster 1          |
| Point B | (1, 2)      | 3               | Core Point    | Cluster 1          |
| Point C | (2, 1)      | 3               | Core Point    | Cluster 1          |
| Point D | (1, 10)     | 1               | Outlier       | NOISE (Grey Cross) |
| Point E | (10, 10)    | 1               | Outlier       | NOISE (Grey Cross) |
+---------+-------------+-----------------+---------------+--------------------+

Key Takeaway:
DBSCAN successfully grouped the tightly packed neighborhood {A, B, C} into a
single community while filtering out D and E as isolated noise. If another point
had landed at (1, 4), it would have only 1 neighbor (B), making it a BORDER POINT
(joining Cluster 1 but not acting as a core expander).
================================================================================"""

    # 3. PCA Walkthrough Text
    pca_txt = """================================================================================
PCA DIMENSIONALITY REDUCTION: STEP-BY-STEP NUMERICAL WALKTHROUGH
================================================================================

Principal Component Analysis (PCA) simplifies high-dimensional data by projecting
it onto a lower-dimensional subspace (e.g., compressing 2D down to 1D) while
retaining the maximum possible spread (variance) of the original shape.

Here is a step-by-step trace of how 2D data is compressed into 1D numbers.

--------------------------------------------------------------------------------
1. THE SAMPLE DATASET
--------------------------------------------------------------------------------
Imagine we have 3 points plotted on a 2D coordinate grid:

  * Point A: (1, 2)
  * Point B: (3, 4)
  * Point C: (5, 6)

These points lie along a perfect diagonal line. We want to compress these 2D
points into a single 1D coordinate while keeping their spacing intact.

--------------------------------------------------------------------------------
2. STEP-BY-STEP COMPRESSION MATH
--------------------------------------------------------------------------------

[STEP 1] MEAN CENTERING:
We shift the data so its average center rests exactly at (0, 0).
1. Calculate averages:
   - Mean X = (1 + 3 + 5) / 3 = 3
   - Mean Y = (2 + 4 + 6) / 3 = 4
2. Subtract means from each point:
   - Point A' = (1-3, 2-4) = (-2, -2)
   - Point B' = (3-3, 4-4) = (0, 0)
   - Point C' = (5-3, 6-4) = (2, 2)

[STEP 2] COMPUTE COVARIANCE MATRIX:
We measure how X and Y vary together. Using the sample covariance formula (dividing by N-1 = 2):
  Cov(X, Y) = sum((X - MeanX) * (Y - MeanY)) / (N - 1)

1. Cov(X, X) = ((-2)^2 + 0^2 + 2^2) / 2 = (4 + 0 + 4) / 2 = 4
2. Cov(Y, Y) = ((-2)^2 + 0^2 + 2^2) / 2 = (4 + 0 + 4) / 2 = 4
3. Cov(X, Y) = ((-2 * -2) + (0 * 0) + (2 * 2)) / 2 = (4 + 0 + 4) / 2 = 4

Our Covariance Matrix (S) is:
  S = | 4   4 |
      | 4   4 |

[STEP 3] EIGENDECOMPOSITION:
We solve for the directions of maximum variance.
1. Find Eigenvalues (lambda) by solving det(S - lambda * I) = 0:
   det | 4-lambda     4     | = 0
       |    4      4-lambda |
   (4-lambda)^2 - 16 = 0
   lambda^2 - 8*lambda = 0
   This yields:
   - lambda_1 = 8  (Primary Axis - PC1. Retains 100% of information)
   - lambda_2 = 0  (Secondary Axis - PC2. Retains 0% of information)

2. Find the Eigenvector (v) for lambda_1 = 8:
   | 4-8   4  | * | x | = 0  -->  | -4   4 | * | x | = 0
   |  4   4-8 |   | y |           |  4  -4 |   | y |
   This simplifies to -4x + 4y = 0, or x = y.
   To make it a unit vector (length of 1.0), we normalize it:
   v = [ 1/sqrt(2), 1/sqrt(2) ] = [ 0.7071, 0.7071 ]
   (This vector points at a 45-degree angle, matching our data perfectly!)

[STEP 4] PROJECT TO 1D:
We project our centered 2D points onto our 1D unit eigenvector v by calculating
the dot product:
  Projected Coordinate = (X_centered * 0.7071) + (Y_centered * 0.7071)

  * Point A' (-2, -2):
    - (-2 * 0.7071) + (-2 * 0.7071) = -1.4142 - 1.4142 = -2.83
  * Point B' (0, 0):
    - (0 * 0.7071) + (0 * 0.7071) = 0.00
  * Point C' (2, 2):
    - (2 * 0.7071) + (2 * 0.7071) = 1.4142 + 1.4142 = 2.83

--------------------------------------------------------------------------------
3. FINAL SUMMARY
--------------------------------------------------------------------------------
+--------------------+---------------------+----------------------+------------+
| Original 2D Point  | Centered 2D Point   | Compressed 1D Coord  | Info Kept  |
+--------------------+---------------------+----------------------+------------+
| Point A (1, 2)     | (-2, -2)            | -2.83                | 100%       |
| Point B (3, 4)     | (0, 0)              | 0.00                 | 100%       |
| Point C (5, 6)     | (2, 2)              | 2.83                 | 100%       |
+--------------------+---------------------+----------------------+------------+

Key Takeaway:
We successfully compressed 2D coordinates into 1D numbers. Because the points
were perfectly aligned, PC1 captured 100% of the variance, allowing us to
compress the data with absolutely ZERO information loss!
================================================================================"""

    # 4. Isolation Forest Walkthrough Text
    isolation_txt = """================================================================================
ISOLATION FOREST OUTLIERS: STEP-BY-STEP EDUCATIONAL WALKTHROUGH
================================================================================

Isolation Forest isolates anomalies directly by recursively slicing the data
space with random lines. Because anomalies are sparse and far away from the crowd,
they get isolated in very few slices (shallow tree depth), whereas normal points
require many slices to separate.

Here is a step-by-step example using a tiny dataset to show exactly how it works.

--------------------------------------------------------------------------------
1. THE SAMPLE DATASET
--------------------------------------------------------------------------------
Imagine we are auditing Credit Card Transactions with two features: Spend Amount ($)
and Distance from Home (km). We have 4 transactions (3 normal, 1 outlier):

  * Point A: Spend = $20, Distance = 2 km  (Normal)
  * Point B: Spend = $25, Distance = 5 km  (Normal)
  * Point C: Spend = $30, Distance = 3 km  (Normal)
  * Point X: Spend = $500, Distance = 80 km (Anomaly Outlier)

--------------------------------------------------------------------------------
2. STEP-BY-STEP RANDOM SPACE SLICING
--------------------------------------------------------------------------------

[ROUND 1] THE FIRST SPLIT:
1. Pick random feature: The algorithm randomly chooses Spend Amount.
2. Find range: The minimum spend is $20 (Point A) and maximum is $500 (Point X).
3. Pick random split value: It picks a random number between $20 and $500.
   Let's say it picks $150.
4. Divide the dataset:
   - Left Branch (Spend < $150): Contains Point A, Point B, Point C.
   - Right Branch (Spend >= $150): Contains Point X.

✨ Point X is now completely alone in its branch. It is successfully isolated in
just 1 split! (Path Length = 1)

[ROUND 2] SPLITTING THE LEFT BRANCH:
Now, the algorithm looks only at the remaining group {A, B, C} on the left branch
and repeats the process:
1. Pick random feature: It randomly chooses Distance from Home.
2. Find range: For A, B, and C, the distances are 2 km, 5 km, and 3 km.
   Min = 2 km, Max = 5 km.
3. Pick random split value: It picks a random number between 2 and 5.
   Let's say it picks 4 km.
4. Divide the remaining dataset:
   - Left Sub-Branch (Distance < 4 km): Contains Point A (2 km) and Point C (3 km).
   - Right Sub-Branch (Distance >= 4 km): Contains Point B (5 km).

✨ Point B is now completely alone. It is isolated after 2 splits! (Path Length = 2)

[ROUND 3] SPLITTING THE LAST GROUP:
Only Point A and Point C are left together. The algorithm repeats the process
one last time:
1. Pick random feature: It chooses Spend Amount.
2. Find range: For A ($20) and C ($30), Min = $20, Max = $30.
3. Pick random split value: It randomly picks $26.
4. Divide the dataset:
   - Left Sub-Branch (Spend < $26): Contains Point A ($20).
   - Right Sub-Branch (Spend >= $26): Contains Point C ($30).

✨ Point A and Point C are now both isolated. (Path Length = 3 for both)

--------------------------------------------------------------------------------
3. FINAL RESULTS SUMMARY
--------------------------------------------------------------------------------
+------------+----------------------+----------------------+-------------------+
| Data Point | Transaction Details  | Splits to Isolate    | Verdict           |
+------------+----------------------+----------------------+-------------------+
| Point X    | Anomaly ($500, 80km) | 1 split (Shallow)    | 🚨 HIGH RISK FLAG |
| Point B    | Normal ($25, 5km)    | 2 splits             | ✅ Approved       |
| Point A    | Normal ($20, 2km)    | 3 splits (Deep)      | ✅ Approved       |
| Point C    | Normal ($30, 3km)    | 3 splits (Deep)      | ✅ Approved       |
+------------+----------------------+----------------------+-------------------+

Because Point X took significantly fewer steps to isolate, the algorithm flags
it as an anomaly. In a real scenario, it repeats this random cutting hundreds of
times across many trees to get a highly accurate, stable average score.
================================================================================"""

    # 5. Apriori Walkthrough Text
    apriori_txt = """================================================================================
APRIORI ASSOCIATION RULES: STEP-BY-STEP NUMERICAL WALKTHROUGH
================================================================================

The Apriori algorithm is used for Market Basket Analysis to discover hidden purchase
relationships between products. It operates on a simple rule: "If an itemset is
frequent, then all of its subsets must also be frequent." This allows the algorithm
to prune (discard) unpopular item combinations early, saving massive amounts of
computation.

It evaluates rules using three main metrics:
1. Support: How popular is the itemset? (Fraction of all receipts containing the items)
2. Confidence: How reliable is the rule? (If they buy A, how likely do they buy B?)
3. Lift: How strong is the rule? (Does buying A boost the probability of buying B
   compared to random chance?)

--------------------------------------------------------------------------------
1. THE SAMPLE DATASET
--------------------------------------------------------------------------------
Imagine our supermarket database has exactly 3 customer receipts (transactions):

  * Receipt 1 (T1): {Bread, Butter}
  * Receipt 2 (T2): {Bread, Butter, Milk}
  * Receipt 3 (T3): {Milk}

We configure Apriori with a Minimum Support of 50% (must appear in >= 2 receipts)
and a Minimum Confidence of 60%.

--------------------------------------------------------------------------------
2. STEP-BY-STEP ASSOCIATION MINING
--------------------------------------------------------------------------------

[STEP 1] CANDIATE SINGLE ITEMS (C1):
We list every individual item bought and count how many receipts contain it:
  * {Bread}: 2 receipts (T1, T2) -> Support = 2 / 3 = 66.7%
  * {Butter}: 2 receipts (T1, T2) -> Support = 2 / 3 = 66.7%
  * {Milk}: 2 receipts (T2, T3) -> Support = 2 / 3 = 66.7%

All three items meet our Minimum Support of 50%. They all become Frequent
1-Itemsets (L1).

[STEP 2] CANDIDATE ITEM PAIRS (C2):
We combine the frequent items from L1 to create pairs, and count their support:
  * {Bread, Butter}: 2 receipts (T1, T2) -> Support = 2 / 3 = 66.7% (Passes!)
  * {Bread, Milk}: 1 receipt (T2) -> Support = 1 / 3 = 33.3% (Pruned! Below 50%)
  * {Butter, Milk}: 1 receipt (T2) -> Support = 1 / 3 = 33.3% (Pruned! Below 50%)

Only {Bread, Butter} survives the support threshold. It is our only Frequent
2-Itemset (L2).

[STEP 3] RULE GENERATION & METRIC AUDITS:
We extract potential "If-Then" rules from our frequent pair {Bread, Butter} and
calculate their metrics:

* RULE A: [Bread] -> [Butter]
  - Support (Popularity): Support of {Bread, Butter} = 66.7%
  - Confidence (Reliability): What fraction of Bread buyers also bought Butter?
    Confidence = Support(Bread, Butter) / Support(Bread) = 2 / 2 = 100%
    (Passes our 60% threshold!)
  - Lift (Strength): Does buying Bread boost Butter purchases?
    Lift = Confidence(Bread -> Butter) / Support(Butter) = 1.00 / 0.667 = 1.5x
    (Buying bread makes a customer 1.5 times more likely to purchase butter.)

* RULE B: [Butter] -> [Bread]
  - Support: 66.7%
  - Confidence: Support(Bread, Butter) / Support(Butter) = 2 / 2 = 100% (Passes!)
  - Lift: 1.00 / 0.667 = 1.5x

--------------------------------------------------------------------------------
3. FINAL DISCOVERED RULES
--------------------------------------------------------------------------------
+-------------------------+-----------+------------+------+--------------------+
| Discovered Rule         | Support   | Confidence | Lift | Retail Action      |
+-------------------------+-----------+------------+------+--------------------+
| [Bread] -> [Butter]     | 66.7%     | 100%       | 1.5x | Co-locate products |
| [Butter] -> [Bread]     | 66.7%     | 100%       | 1.5x | Bundle deal promo  |
+-------------------------+-----------+------------+------+--------------------+

Key Takeaway:
Apriori successfully pruned away low-support pairs early (like Bread + Milk) and
focused exclusively on the strong, reliable rules, allowing retailers to optimize
store layouts and cross-selling campaigns with simple counts.
================================================================================"""

    # Write all files
    files = {
        "1_kmeans_walkthrough.txt": kmeans_txt,
        "2_dbscan_walkthrough.txt": dbscan_txt,
        "3_pca_walkthrough.txt": pca_txt,
        "4_isolation_forest_walkthrough.txt": isolation_txt,
        "5_apriori_walkthrough.txt": apriori_txt
    }

    for filename, content in files.items():
        filepath = os.path.join(output_dir, filename)
        with open(filepath, "w") as f:
            f.write(content.strip() + "\n")
        print(f"[+] Saved: {filepath}")

    print(f"\\n[+] All plain text walkthroughs successfully created in: {output_dir}")

if __name__ == "__main__":
    generate_text_files()
