import os
import subprocess

def get_html_template(title, content):
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>{title}</title>
    <style>
        body {{
            font-family: 'Georgia', 'Times New Roman', serif;
            line-height: 1.6;
            color: #333333;
            max-width: 800px;
            margin: 40px auto;
            padding: 20px;
            background-color: #ffffff;
        }}
        h1 {{
            font-family: 'Arial', sans-serif;
            color: #1a365d;
            text-align: center;
            border-bottom: 3px double #1a365d;
            padding-bottom: 15px;
            font-size: 2.2rem;
            margin-bottom: 40px;
        }}
        h2 {{
            font-family: 'Arial', sans-serif;
            color: #2b6cb0;
            border-bottom: 1px solid #e2e8f0;
            padding-bottom: 8px;
            margin-top: 40px;
            font-size: 1.6rem;
        }}
        h3 {{
            font-family: 'Arial', sans-serif;
            color: #4a5568;
            margin-top: 25px;
            font-size: 1.2rem;
        }}
        p, li {{
            font-size: 1.05rem;
            text-align: justify;
        }}
        ul, ol {{
            margin-bottom: 20px;
            padding-left: 25px;
        }}
        li {{
            margin-bottom: 8px;
        }}
        .highlight {{
            font-weight: bold;
            color: #2b6cb0;
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
            margin: 25px 0;
            font-family: 'Arial', sans-serif;
            font-size: 0.95rem;
        }}
        th, td {{
            border: 1px solid #cbd5e0;
            padding: 12px 15px;
            text-align: left;
        }}
        th {{
            background-color: #ebf8ff;
            color: #2c5282;
            font-weight: bold;
        }}
        tr:nth-child(even) {{
            background-color: #f7fafc;
        }}
        .footer {{
            margin-top: 60px;
            text-align: center;
            font-size: 0.85rem;
            color: #718096;
            border-top: 1px solid #e2e8f0;
            padding-top: 20px;
        }}
    </style>
</head>
<body>
    <h1>{title}</h1>
    {content}
    <div class="footer">
        <p>Unsupervised Learning Masterclass &bull; &copy; 2026 Visual Explorer Project</p>
    </div>
</body>
</html>
"""

def generate_pdfs():
    # Setup directories
    pdf_dir = "/home/gaian/Unsupervised/walkthroughs_pdf"
    os.makedirs(pdf_dir, exist_ok=True)
    
    # 1. Individual Walkthrough Contents (in HTML format for printing)
    kmeans_html = """
    <p>
        K-Means is an iterative, partition-based clustering algorithm. It groups data points into 
        <span class="highlight">K</span> distinct clusters by minimizing the distance between points and their respective 
        cluster centers (centroids). It runs in a loop of <strong>Assignment</strong> (assigning points to the nearest centroid) 
        and <strong>Update</strong> (moving centroids to the average center of their assigned points) until convergence.
    </p>
    
    <h3>The Sample Dataset</h3>
    <p>Imagine we have 4 retail customers with two features: Age and Spending Score (1-100):</p>
    <ul>
        <li><strong>Point A</strong>: Age = 20, Spending = 80 (Young High Spender)</li>
        <li><strong>Point B</strong>: Age = 22, Spending = 75 (Young High Spender)</li>
        <li><strong>Point C</strong>: Age = 60, Spending = 20 (Senior Budget Shopper)</li>
        <li><strong>Point D</strong>: Age = 62, Spending = 22 (Senior Budget Shopper)</li>
    </ul>
    <p>We want to group them into <strong>K = 2 clusters</strong>.</p>

    <h3>Iteration 1: Starting the Loop</h3>
    <p><strong>Step 1: Initial Centroid Placement</strong><br>
       We randomly choose two points to act as our starting cluster centers:
    </p>
    <ul>
        <li>Centroid 1 ($C_1$): Placed at Point A <strong>(20, 80)</strong></li>
        <li>Centroid 2 ($C_2$): Placed at Point C <strong>(60, 20)</strong></li>
    </ul>

    <p><strong>Step 2: Distance & Cluster Assignment</strong><br>
       We calculate the straight-line (Euclidean) distance from every point to both centroids:
       $$\text{Distance} = \sqrt{(X_{\text{point}} - X_{\text{centroid}})^2 + (Y_{\text{point}} - Y_{\text{centroid}})^2}$$
    </p>
    <ul>
        <li><strong>Point A (20, 80)</strong>: Dist to $C_1$ is 0. Dist to $C_2$ is 72.1. <span class="highlight">Verdict: Cluster 1</span>.</li>
        <li><strong>Point B (22, 75)</strong>: Dist to $C_1$ is $\sqrt{(22-20)^2 + (75-80)^2} = \sqrt{29} \approx 5.39$. Dist to $C_2$ is 66.85. <span class="highlight">Verdict: Cluster 1</span>.</li>
        <li><strong>Point C (60, 20)</strong>: Dist to $C_1$ is 72.1. Dist to $C_2$ is 0. <span class="highlight">Verdict: Cluster 2</span>.</li>
        <li><strong>Point D (62, 22)</strong>: Dist to $C_1$ is 71.61. Dist to $C_2$ is $\sqrt{(62-60)^2 + (22-20)^2} = \sqrt{8} \approx 2.83$. <span class="highlight">Verdict: Cluster 2</span>.</li>
    </ul>

    <p><strong>Step 3: Recalculate Centroid Positions (Centroid Update)</strong><br>
       Centroids shift to the exact average center of their assigned members:
    </p>
    <ul>
        <li><strong>New Centroid 1 ($C_1'$)</strong> (Average of A and B): Age = $\frac{20+22}{2} = 21$, Spending = $\frac{80+75}{2} = 77.5$. Coordinates: <strong>(21, 77.5)</strong>.</li>
        <li><strong>New Centroid 2 ($C_2'$)</strong> (Average of C and D): Age = $\frac{60+62}{2} = 61$, Spending = $\frac{20+22}{2} = 21$. Coordinates: <strong>(61, 21)</strong>.</li>
    </ul>

    <h3>Iteration 2: Verifying Convergence</h3>
    <p><strong>Step 4: Recalculate Distances & Assignments</strong><br>
       We check if any points change their cluster labels when measured against the shifted centroids $C_1'$ (21, 77.5) and $C_2'$ (61, 21):
    </p>
    <ul>
        <li><strong>Point A (20, 80)</strong>: Dist to $C_1'$ is $\sqrt{(20-21)^2 + (80-77.5)^2} = 2.69$. Dist to $C_2'$ is 71.85. Remains in <strong>Cluster 1</strong>.</li>
        <li><strong>Point B (22, 75)</strong>: Dist to $C_1'$ is 2.69. Dist to $C_2'$ is 67.90. Remains in <strong>Cluster 1</strong>.</li>
        <li><strong>Point C (60, 20)</strong>: Dist to $C_1'$ is 69.90. Dist to $C_2'$ is $\sqrt{(60-61)^2 + (20-21)^2} = 1.41$. Remains in <strong>Cluster 2</strong>.</li>
        <li><strong>Point D (62, 22)</strong>: Dist to $C_1'$ is 69.11. Dist to $C_2'$ is 1.41. Remains in <strong>Cluster 2</strong>.</li>
    </ul>

    <p>Since no points changed their cluster assignments, the algorithm has officially <strong>converged</strong>!</p>

    <table>
        <thead>
            <tr>
                <th>Customer</th>
                <th>Age, Spend</th>
                <th>Final Cluster</th>
                <th>Demographic Segment</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td><strong>Point A</strong></td>
                <td>(20, 80)</td>
                <td>Cluster 1</td>
                <td>Young High Spenders</td>
            </tr>
            <tr>
                <td><strong>Point B</strong></td>
                <td>(22, 75)</td>
                <td>Cluster 1</td>
                <td>Young High Spenders</td>
            </tr>
            <tr>
                <td><strong>Point C</strong></td>
                <td>(60, 20)</td>
                <td>Cluster 2</td>
                <td>Senior Budget Shoppers</td>
            </tr>
            <tr>
                <td><strong>Point D</strong></td>
                <td>(62, 22)</td>
                <td>Cluster 2</td>
                <td>Senior Budget Shoppers</td>
            </tr>
        </tbody>
    </table>
    """

    dbscan_html = """
    <p>
        DBSCAN groups points based on local density. It does not require you to pre-specify the number of clusters, 
        and it is capable of discovering clusters of arbitrary shapes (like concentric rings) while cleanly filtering out outliers.
        It relies on a search radius <strong>&epsilon; (Epsilon)</strong> and a neighborhood threshold <strong>MinPts</strong>.
    </p>
    
    <h3>The Sample Dataset</h3>
    <p>Imagine we have 5 points plotted on a 2D coordinate grid:</p>
    <ul>
        <li><strong>Point A</strong>: (1, 1)</li>
        <li><strong>Point B</strong>: (1, 2)</li>
        <li><strong>Point C</strong>: (2, 1)</li>
        <li><strong>Point D</strong>: (1, 10)</li>
        <li><strong>Point E</strong>: (10, 10)</li>
    </ul>
    <p>We set <strong>&epsilon; = 3</strong> and <strong>MinPts = 2</strong>.</p>

    <h3>Step-by-Step Execution</h3>
    <p><strong>Round 1: Scanning Point A (1, 1)</strong><br>
       1. Select Point A as our start point.<br>
       2. Scan neighbors within distance &epsilon; = 3: B (1, 2) and C (2, 1) are inside. D and E are outside.<br>
       3. Count neighborhood size: Neighbors of A are {A, B, C} (3 points).<br>
       4. Evaluate density: Since the count (3) is &ge; MinPts (2), <span class="highlight">Point A is labeled a Core Point</span>.<br>
       5. Form cluster: A starts <strong>Cluster 1</strong>. Its unvisited neighbors {B, C} are added to the expansion queue.
    </p>
    
    <p><strong>Round 2: Expanding via Point B (1, 2)</strong><br>
       1. Pop Point B from the queue.<br>
       2. Scan neighbors: Neighbors are {A, B, C} (3 points).<br>
       3. Evaluate density: Since count &ge; MinPts, <span class="highlight">Point B is also a Core Point</span>.<br>
       4. Expand: B joins Cluster 1.
    </p>

    <p><strong>Round 3: Expanding via Point C (2, 1)</strong><br>
       1. Pop Point C from the queue.<br>
       2. Scan neighbors: Neighbors are {A, B, C} (3 points).<br>
       3. Evaluate density: Since count &ge; MinPts, <span class="highlight">Point C is a Core Point</span>.<br>
       4. Expand: C joins Cluster 1. The queue is now empty. Cluster 1 is complete!
    </p>

    <p><strong>Round 4: Scanning Point D (1, 10)</strong><br>
       1. Select Point D (next unvisited point).<br>
       2. Scan neighbors: The only neighbor of D is {D} (1 point). Distance to E (10, 10) is 9.0 (Outside).<br>
       3. Evaluate density: Since the count (1) is < MinPts (2), Point D is not a Core Point.<br>
       4. Label status: Since D has no connections to Core points, it is labeled as <span class="highlight">Noise (Outlier)</span>.
    </p>

    <p><strong>Round 5: Scanning Point E (10, 10)</strong><br>
       1. Select Point E (last unvisited point).<br>
       2. Scan neighbors: Only {E} (1 point).<br>
       3. Evaluate density: Since count < MinPts, Point E is not a Core Point.<br>
       4. Label status: Point E is labeled as <span class="highlight">Noise (Outlier)</span>.
    </p>

    <table>
        <thead>
            <tr>
                <th>Point</th>
                <th>Coordinates</th>
                <th>Neighbors Found</th>
                <th>Class Type</th>
                <th>Final Assignment</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td><strong>Point A</strong></td>
                <td>(1, 1)</td>
                <td>3</td>
                <td>Core Point</td>
                <td>Cluster 1</td>
            </tr>
            <tr>
                <td><strong>Point B</strong></td>
                <td>(1, 2)</td>
                <td>3</td>
                <td>Core Point</td>
                <td>Cluster 1</td>
            </tr>
            <tr>
                <td><strong>Point C</strong></td>
                <td>(2, 1)</td>
                <td>3</td>
                <td>Core Point</td>
                <td>Cluster 1</td>
            </tr>
            <tr>
                <td><strong>Point D</strong></td>
                <td>(1, 10)</td>
                <td>1</td>
                <td>Outlier</td>
                <td>Noise (Isolated Outlier)</td>
            </tr>
            <tr>
                <td><strong>Point E</strong></td>
                <td>(10, 10)</td>
                <td>1</td>
                <td>Outlier</td>
                <td>Noise (Isolated Outlier)</td>
            </tr>
        </tbody>
    </table>
    """

    pca_html = """
    <p>
        Principal Component Analysis (PCA) simplifies high-dimensional data by projecting it onto a 
        lower-dimensional subspace (e.g., compressing 2D down to 1D) while keeping the maximum amount of 
        original spread (variance) of the shape.
    </p>
    
    <h3>The Sample Dataset</h3>
    <p>Imagine we have 3 points plotted on a 2D coordinate grid:</p>
    <ul>
        <li><strong>Point A</strong>: (1, 2)</li>
        <li><strong>Point B</strong>: (3, 4)</li>
        <li><strong>Point C</strong>: (5, 6)</li>
    </ul>
    <p>These points form a diagonal line. We want to compress them into a single <strong>1D coordinate</strong>.</p>

    <h3>Step-by-Step Mathematical Compression</h3>
    <p><strong>Step 1: Mean Centering</strong><br>
       We shift the data so its average center rests exactly at (0, 0).
    </p>
    <ol>
        <li>Calculate averages: Mean X = 3, Mean Y = 4.</li>
        <li>Subtract the means:
            <ul>
                <li><strong>Point A'</strong> = (-2, -2)</li>
                <li><strong>Point B'</strong> = (0, 0)</li>
                <li><strong>Point C'</strong> = (2, 2)</li>
            </ul>
        </li>
    </ol>

    <p><strong>Step 2: Compute the Covariance Matrix</strong><br>
       Using the sample covariance formula (dividing by $N-1 = 2$):
    </p>
    <ol>
        <li>$\text{Cov}(X, X) = \frac{(-2)^2 + 0^2 + 2^2}{2} = \mathbf{4}$</li>
        <li>$\text{Cov}(Y, Y) = \frac{(-2)^2 + 0^2 + 2^2}{2} = \mathbf{4}$</li>
        <li>$\text{Cov}(X, Y) = \frac{(-2 \times -2) + (0 \times 0) + (2 \times 2)}{2} = \mathbf{4}$</li>
    </ol>
    <p>Our Covariance Matrix ($S$) is:
       $$S = \begin{pmatrix} 4 & 4 \\ 4 & 4 \end{pmatrix}$$
    </p>

    <p><strong>Step 3: Find Eigenvalues & Eigenvectors</strong><br>
       1. Solve $\det(S - \lambda I) = 0$:
          This yields: <strong>$\lambda_1 = 8$</strong> (PC1, captures 100% of variance) and <strong>$\lambda_2 = 0$</strong> (PC2).<br>
       2. Solve for the eigenvector $\mathbf{v}$ for $\lambda_1 = 8$:
          Normalizing this vector gives:
          $$\mathbf{v} = \begin{pmatrix} 0.7071 \\ 0.7071 \end{pmatrix}$$
    </p>

    <p><strong>Step 4: Projection to 1D</strong><br>
       We calculate the dot product of centered coordinates with $\mathbf{v}$:
       $$\text{Projected Coordinate} = (X_{\text{centered}} \times 0.7071) + (Y_{\text{centered}} \times 0.7071)$$
    </p>
    <ul>
        <li><strong>Point A' (-2, -2)</strong>: $(-2 \times 0.7071) + (-2 \times 0.7071) = \mathbf{-2.83}$</li>
        <li><strong>Point B' (0, 0)</strong>: $(0 \times 0.7071) + (0 \times 0.7071) = \mathbf{0.00}$</li>
        <li><strong>Point C' (2, 2)</strong>: $(2 \times 0.7071) + (2 \times 0.7071) = \mathbf{2.83}$</li>
    </ul>

    <table>
        <thead>
            <tr>
                <th>Original 2D Point</th>
                <th>Centered 2D Point</th>
                <th>Compressed 1D Coordinate</th>
                <th>Information Retained</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td><strong>Point A</strong> (1, 2)</td>
                <td>(-2, -2)</td>
                <td>-2.83</td>
                <td>100% (No loss)</td>
            </tr>
            <tr>
                <td><strong>Point B</strong> (3, 4)</td>
                <td>(0, 0)</td>
                <td>0.00</td>
                <td>100% (No loss)</td>
            </tr>
            <tr>
                <td><strong>Point C</strong> (5, 6)</td>
                <td>(2, 2)</td>
                <td>2.83</td>
                <td>100% (No loss)</td>
            </tr>
        </tbody>
    </table>
    """

    isolation_html = """
    <p>
        Isolation Forest isolates anomalies directly by recursively slicing the data space with random lines. 
        Because anomalies are sparse and far away from the crowd, they get isolated in very few slices (shallow tree depth), 
        whereas normal points require many slices to separate.
    </p>
    
    <h3>The Sample Dataset</h3>
    <p>Imagine we are auditing Credit Card Transactions with two features: Spend Amount ($) and Distance from Home (km). 
       We have 4 transactions (3 normal, 1 outlier):
    </p>
    <ul>
        <li><strong>Point A</strong>: Spend = $20, Distance = 2 km (Normal)</li>
        <li><strong>Point B</strong>: Spend = $25, Distance = 5 km (Normal)</li>
        <li><strong>Point C</strong>: Spend = $30, Distance = 3 km (Normal)</li>
        <li><strong>Point X</strong>: Spend = $500, Distance = 80 km (Anomaly Outlier)</li>
    </ul>

    <h3>Step-by-Step Space Slicing</h3>
    <p><strong>Round 1: The First Split</strong><br>
       1. Pick random feature: The algorithm randomly chooses **Spend Amount**.<br>
       2. Find range: The minimum spend is $20 (Point A) and maximum is $500 (Point X).<br>
       3. Pick random split value: It picks a random number between $20$ and $500$. Let's say it picks **$150**.<br>
       4. Divide the dataset:
          <ul>
              <li>Left Branch (Spend < $150): Contains Point A, Point B, Point C.</li>
              <li>Right Branch (Spend &ge; $150): Contains Point X.</li>
          </ul>
       <span class="highlight">✨ Point X is now completely alone. It is isolated in just 1 split! (Path Length = 1)</span>
    </p>
    
    <p><strong>Round 2: Splitting the Left Branch</strong><br>
       We look only at the remaining group {A, B, C} on the left branch:<br>
       1. Pick random feature: It randomly chooses **Distance from Home**.<br>
       2. Find range: Min = 2 km, Max = 5 km.<br>
       3. Pick random split value: It picks a random number between 2 and 5. Let's say it picks **4 km**.<br>
       4. Divide the remaining dataset:
          <ul>
              <li>Left Sub-Branch (Distance < 4 km): Contains Point A (2 km) and Point C (3 km).</li>
              <li>Right Sub-Branch (Distance &ge; 4 km): Contains Point B (5 km).</li>
          </ul>
       <span class="highlight">✨ Point B is now completely alone. It is isolated after 2 splits! (Path Length = 2)</span>
    </p>

    <p><strong>Round 3: Splitting the Last Group</strong><br>
       Only Point A and Point C are left together:<br>
       1. Pick random feature: It chooses **Spend Amount**.<br>
       2. Find range: Min = $20, Max = $30.<br>
       3. Pick random split value: It randomly picks **$26**.<br>
       4. Divide the dataset:
          <ul>
              <li>Left Sub-Branch (Spend < $26): Contains Point A ($20).</li>
              <li>Right Sub-Branch (Spend &ge; $26): Contains Point C ($30).</li>
          </ul>
       <span class="highlight">✨ Point A and Point C are now both isolated. (Path Length = 3 for both)</span>
    </p>

    <table>
        <thead>
            <tr>
                <th>Data Point</th>
                <th>Transaction Details</th>
                <th>Splits to Isolate (Path Length)</th>
                <th>Verdict</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td><strong>Point X</strong></td>
                <td>Anomaly ($500, 80km)</td>
                <td><strong>1 split</strong> (Very Shallow)</td>
                <td>🚨 <strong>HIGH RISK FRAUD FLAG</strong></td>
            </tr>
            <tr>
                <td><strong>Point B</strong></td>
                <td>Normal ($25, 5km)</td>
                <td>2 splits</td>
                <td>✅ Approved (Normal)</td>
            </tr>
            <tr>
                <td><strong>Point A</strong></td>
                <td>Normal ($20, 2km)</td>
                <td>3 splits (Deep)</td>
                <td>✅ Approved (Normal)</td>
            </tr>
            <tr>
                <td><strong>Point C</strong></td>
                <td>Normal ($30, 3km)</td>
                <td>3 splits (Deep)</td>
                <td>✅ Approved (Normal)</td>
            </tr>
        </tbody>
    </table>
    """

    apriori_html = """
    <p>
        The Apriori algorithm is used for Market Basket Analysis to discover purchase relationships between products. 
        It operates on the principle that: <em>If an itemset is frequent, then all of its subsets must also be frequent</em>. 
        This allows the algorithm to prune (discard) unpopular item combinations early, saving massive amounts of computation.
        It evaluates rules using <strong>Support</strong>, <strong>Confidence</strong>, and <strong>Lift</strong>.
    </p>
    
    <h3>The Sample Dataset</h3>
    <p>Imagine our supermarket database has exactly 3 customer receipts (transactions):</p>
    <ul>
        <li><strong>Receipt 1 (T1)</strong>: {Bread, Butter}</li>
        <li><strong>Receipt 2 (T2)</strong>: {Bread, Butter, Milk}</li>
        <li><strong>Receipt 3 (T3)</strong>: {Milk}</li>
    </ul>
    <p>We configure Apriori with a <strong>Minimum Support of 50%</strong> (must appear in &ge; 2 receipts) and a <strong>Minimum Confidence of 60%</strong>.</p>

    <h3>Step-by-Step Association Mining</h3>
    <p><strong>Step 1: Candidate Single Items ($C_1$)</strong><br>
       We list individual items and count their support:
    </p>
    <ul>
        <li><strong>{Bread}</strong>: 2 receipts (T1, T2) &rarr; Support = 66.7% (Passes!)</li>
        <li><strong>{Butter}</strong>: 2 receipts (T1, T2) &rarr; Support = 66.7% (Passes!)</li>
        <li><strong>{Milk}</strong>: 2 receipts (T2, T3) &rarr; Support = 66.7% (Passes!)</li>
    </ul>
    <p>All items become <strong>Frequent 1-Itemsets ($L_1$)</strong>.</p>

    <p><strong>Step 2: Candidate Item Pairs ($C_2$)</strong><br>
       We combine items from $L_1$ into pairs and count support:
    </p>
    <ul>
        <li><strong>{Bread, Butter}</strong>: 2 receipts (T1, T2) &rarr; Support = 66.7% (Passes!)</li>
        <li><strong>{Bread, Milk}</strong>: 1 receipt (T2) &rarr; Support = 33.3% (<span class="highlight">❌ Pruned! Below 50%</span>)</li>
        <li><strong>{Butter, Milk}</strong>: 1 receipt (T2) &rarr; Support = 33.3% (<span class="highlight">❌ Pruned! Below 50%</span>)</li>
    </ul>
    <p>Only <strong>{Bread, Butter}</strong> becomes a <strong>Frequent 2-Itemset ($L_2$)</strong>.</p>

    <p><strong>Step 3: Rule Generation & Metric Audits</strong><br>
       We extract rules from our frequent pair {Bread, Butter}:
    </p>
    <ul>
        <li><strong>Rule A: $[Bread] \rightarrow [Butter]$</strong><br>
            - Support (Popularity): Support of {Bread, Butter} = $\mathbf{66.7\%}$<br>
            - Confidence (Reliability): 100% (Passes &ge; 60%!)<br>
            - Lift (Strength): 1.5x (Positive correlation!)
        </li>
        <li style="margin-top: 15px;"><strong>Rule B: $[Butter] \rightarrow [Bread]$</strong><br>
            - Support: 66.7%<br>
            - Confidence: 100% (Passes!)<br>
            - Lift: 1.5x
        </li>
    </ul>

    <table>
        <thead>
            <tr>
                <th>Discovered Rule</th>
                <th>Rule Popularity (Support)</th>
                <th>Rule Reliability (Confidence)</th>
                <th>Strength Multiplier (Lift)</th>
                <th>Retail Recommendation</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td><strong>[Bread] &rarr; [Butter]</strong></td>
                <td>66.7%</td>
                <td>100%</td>
                <td>1.5x</td>
                <td>Place Bread and Butter on the same aisle to drive convenience buys.</td>
            </tr>
            <tr>
                <td><strong>[Butter] &rarr; [Bread]</strong></td>
                <td>66.7%</td>
                <td>100%</td>
                <td>1.5x</td>
                <td>Bundle them together in a "Breakfast Special" package promotion.</td>
            </tr>
        </tbody>
    </table>
    """

    # Build individual PDFs
    walkthroughs = [
        ("1_kmeans_walkthrough", "K-Means Clustering: Numerical Walkthrough", kmeans_html),
        ("2_dbscan_walkthrough", "DBSCAN Density Clustering: Numerical Walkthrough", dbscan_html),
        ("3_pca_walkthrough", "PCA Dimensionality Reduction: Numerical Walkthrough", pca_html),
        ("4_isolation_forest_walkthrough", "Isolation Forest Outliers: Numerical Walkthrough", isolation_html),
        ("5_apriori_walkthrough", "Apriori Association Rules: Numerical Walkthrough", apriori_html)
    ]

    for basename, title, content in walkthroughs:
        # Create temp html
        temp_html_path = f"/tmp/{basename}.html"
        pdf_output_path = f"{pdf_dir}/{basename}.pdf"
        
        with open(temp_html_path, "w") as f:
            f.write(get_html_template(title, content))
            
        # Run headless chrome to print to PDF
        cmd = [
            "google-chrome",
            "--headless",
            "--disable-gpu",
            f"--print-to-pdf={pdf_output_path}",
            temp_html_path
        ]
        
        try:
            subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
            print(f"[+] Rendered PDF: {pdf_output_path}")
        except Exception as e:
            print(f"[!] Failed rendering {basename}.pdf: {e}")
            
        # Cleanup
        if os.path.exists(temp_html_path):
            os.remove(temp_html_path)

    # 2. Also compile the consolidated master PDF in the root directory!
    master_html_path = "/home/gaian/Unsupervised/Unsupervised_Learning_Walkthroughs.html"
    master_pdf_path = "/home/gaian/Unsupervised/Unsupervised_Learning_Walkthroughs.pdf"
    
    if os.path.exists(master_html_path):
        cmd = [
            "google-chrome",
            "--headless",
            "--disable-gpu",
            f"--print-to-pdf={master_pdf_path}",
            master_html_path
        ]
        try:
            subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
            print(f"\\n[+] Rendered Consolidated Master PDF at: {master_pdf_path}")
        except Exception as e:
            print(f"[!] Failed rendering consolidated PDF: {e}")

if __name__ == "__main__":
    generate_pdfs()
