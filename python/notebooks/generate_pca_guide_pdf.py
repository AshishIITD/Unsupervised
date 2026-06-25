import os
import subprocess

def create_guide_files():
    pdf_path = "/home/gaian/Unsupervised/PCA_Eigen_Intuition_Guide.pdf"
    md_path = "/home/gaian/Unsupervised/python/dimensionality/pca_eigen_intuition_guide.md"
    temp_html_path = "/tmp/pca_guide_temp.html"
    
    # 1. Markdown Content
    md_content = """# Eigenvalues, Eigenvectors, and PCA: A Deep-Dive Intuition Guide

This guide explains the linear algebra foundations and physical intuition behind **Principal Component Analysis (PCA)**, **Eigenvectors**, and **Eigenvalues**.

---

## 1. What are Eigenvectors and Eigenvalues?

An **eigenvector** is a special vector that does not change its direction when a linear transformation (like stretching, rotating, or shearing) is applied to it. Instead, it only scales up, scales down, or flips backwards.

An **eigenvalue** is the scaling factor—the number that tells you how much that eigenvector stretched, shrunk, or flipped during the transformation.

### The Matrix Equation
Mathematically, this relationship is written as a simple equation:

$$Av = \lambda v$$

Where:
* **$A$** is a square matrix (the linear transformation).
* **$v$** is the eigenvector (the direction that stays the same).
* **$\lambda$ (lambda)** is the eigenvalue (the scaling multiplier).

---

### A Visual Analogue: The Mona Lisa Stretch
Imagine a giant rubber sheet with a picture of the **Mona Lisa** printed on it. Now, you grab the left and right sides of the sheet and pull them hard, stretching the image horizontally.

1. **The Horizontal Axis (Eigenvector)**: Any arrow drawn pointing strictly left or right will still point strictly left or right after the stretch. It did not rotate or tilt. This horizontal axis is an **eigenvector**. If the sheet became twice as long, its corresponding **eigenvalue is 2**.
2. **The Diagonal Lines (Non-Eigenvectors)**: An arrow pointing diagonally will tilt and change its direction as the sheet stretches. Because its direction changed, it is **not** an eigenvector.

---

### Step-by-Step Numerical Example
Let's see how they work with a simple $2 \times 2$ transformation matrix $A$:

$$A = \begin{pmatrix} 3 & 1 \\ 0 & 2 \end{pmatrix}$$

If we multiply this matrix by a random vector like $\begin{pmatrix} 1 \\ 1 \end{pmatrix}$, the direction changes completely:

$$\begin{pmatrix} 3 & 1 \\ 0 & 2 \end{pmatrix} \begin{pmatrix} 1 \\ 1 \end{pmatrix} = \begin{pmatrix} 4 \\ 2 \end{pmatrix}$$

This is not an eigenvector. But, watch what happens if we multiply it by the special vector $v = \begin{pmatrix} 1 \\ 0 \end{pmatrix}$:

$$Av = \begin{pmatrix} 3 & 1 \\ 0 & 2 \end{pmatrix} \begin{pmatrix} 1 \\ 0 \end{pmatrix} = \begin{pmatrix} (3 \times 1) + (1 \times 0) \\ (0 \times 1) + (2 \times 0) \end{pmatrix} = \begin{pmatrix} 3 \\ 0 \end{pmatrix}$$

Notice that $\begin{pmatrix} 3 \\ 0 \end{pmatrix}$ is exactly **3 times** our original vector $v = \begin{pmatrix} 1 \\ 0 \end{pmatrix}$.

* **Eigenvector ($v$)**: $\begin{pmatrix} 1 \\ 0 \end{pmatrix}$ (The direction did not change).
* **Eigenvalue ($\lambda$)**: **3** (The vector became exactly 3 times longer).

---

## 2. PCA and the Concept of Maximum Variance

Yes, exactly! In **Principal Component Analysis (PCA)**, the eigenvector with the largest eigenvalue points directly in the direction of the **maximum variance** (the maximum spread of the data).

### The Intuition: What is Variance?
Variance is a measure of information spread:
* **High Variance**: The data points are stretched out far apart along an axis (lots of unique, distinct information).
* **Low Variance**: The data points are tightly packed together (very little unique information; mostly redundant).

If you want to compress your data from 2D down to 1D without losing important details, you must project your data onto the line that keeps the points as spread out as possible.

### How Eigenvectors Find the Maximum Variance
Imagine a 2D scatter plot of data shaped like an elongated **football**, tilted diagonally:
1. **The First Eigenvector ($v_1$)**: The algorithm draws a line straight through the longest part of the football. This is the axis where the data has the absolute **maximum variance**. This line is the first eigenvector (**Principal Component 1**).
2. **The First Eigenvalue ($\lambda_1$)**: The length or strength of this axis is its eigenvalue. Because the data is highly stretched here, $\lambda_1$ will be the largest number.
3. **The Second Eigenvector ($v_2$)**: The algorithm then finds a line perpendicular (at 90 degrees) to the first one, capturing the width of the football. This is the direction of the **minimum variance** (**Principal Component 2**). It will have a much smaller eigenvalue ($\lambda_2$).

### Real-World Example: Predicting House Prices
Suppose you have a dataset with two features: **House Size (sq. ft)** and **Number of Rooms**. Generally, as size increases, the number of rooms also increases. If you plot this, you get a highly correlated diagonal line of data points.

* **Direction of Maximum Variance ($v_1$)**: This axis captures the combined concept of **"Overall House Scale"**. It tells you the most about how houses differ from each other.
* **Direction of Low Variance ($v_2$)**: This axis only captures minor noise (e.g., whether a house happens to have unusually small rooms).

By choosing the eigenvector with the maximum variance ($v_1$), you can drop the low-variance axis ($v_2$) entirely. You successfully compress your data from two columns down to one single column ("House Scale") while keeping nearly all of the original information!

---

## 3. How PCA Works Behind the Scenes

Principal Component Analysis (PCA) is an unsupervised learning technique used to reduce the dimensionality of large datasets. It compresses data by transforming a large set of variables into a smaller one while retaining as much information (variance) as possible.

Here is the exact step-by-step process of how PCA works behind the scenes:

### Step 1: Standardise the Data
Before doing anything else, you must standardise your features so they all have a mean of 0 and a standard deviation of 1.
* **Why?** PCA is incredibly sensitive to the scale of your data. If one column is "Salary" (ranging in thousands) and another is "Age" (ranging from 1 to 100), PCA will completely ignore Age because the numbers in the Salary column vary much more widely. Standardisation puts all variables on an equal playing field.

### Step 2: Calculate the Covariance Matrix
Next, PCA looks at how all the features vary together. It creates a square matrix called a **Covariance Matrix**.
* If you have 3 features, you get a $3 \times 3$ matrix.
* The diagonal values show the variance of each individual feature.
* The off-diagonal values show the covariance between features (e.g., how much Feature A increases or decreases when Feature B changes). This highlights redundant, highly correlated information.

### Step 3: Compute Eigenvectors and Eigenvalues
This is where the linear algebra kicks in. PCA calculates the eigenvectors and eigenvalues of that Covariance Matrix.
* **Eigenvectors**: These represent the directions of the new axes. These new axes are called **Principal Components (PCs)**. They are mathematically forced to be orthogonal (at a 90-degree angle) to each other, meaning they capture completely independent information.
* **Eigenvalues**: These are coefficients that represent the magnitude or amount of variance carried by each Principal Component.

### Step 4: Sort and Select Principal Components
The algorithm sorts the eigenvectors in descending order based on their eigenvalues.
* The eigenvector with the largest eigenvalue becomes **Principal Component 1 (PC1)**. It aligns perfectly with the direction of maximum variance in the data.
* The eigenvector with the second largest eigenvalue becomes **PC2**, and so on.
* To compress your data, you choose how many components to keep. For example, if you have 100 features, you might find that PC1 and PC2 combined capture 95% of the total variance. You decide to drop the remaining 98 components.

### Step 5: Recast the Data Along the New Axes
In the final step, the original data points are re-oriented from their original, complex axes onto your newly selected Principal Components.
* Mathematically, you multiply your original standardised data matrix by the matrix of your selected eigenvectors. The result is a brand-new dataset with significantly fewer columns, completely un-correlated features, and almost all of your original information intact.

```
[Original Data] 
       ↓
[Standardise (Mean=0, SD=1)] 
       ↓
[Build Covariance Matrix] 
       ↓
[Extract Eigenvectors & Eigenvalues] 
       ↓
[Sort by Eigenvalue (Highest to Lowest)]
       ↓
[Keep Top 'K' Components & Re-project Data]
```

---

## 4. The Physical Intuition of PCA

The physical intuition of PCA is **finding the best angle to photograph a complex, 3D object so that you can still see its true shape in a flat, 2D picture**.

If you take the photo from a bad angle, the object squishes together, shapes overlap, and you lose critical information. PCA spins the object around until it finds the widest, most descriptive view.

Here are three physical analogies to help visualize exactly what PCA is doing:

### 1. The Shadow Puppet Analogy (Dimensionality Reduction)
Imagine you are holding a 3D football in a dark room and shining a flashlight on it to project a 2D shadow onto a wall.
* **The Bad Angle (Low Variance)**: If you point the flashlight directly down the tip of the football, its shadow on the wall looks like a small, perfect circle. Looking only at the shadow, you would think the object is a flat disc. You lost the information about its length because you flattened out its longest axis.
* **The PCA Angle (Maximum Variance)**: PCA tells you to rotate the football so the flashlight shines directly on its side. Now, the shadow on the wall is a wide, long oval. This shadow captures the maximum amount of the football's true shape and size.

*PCA finds the exact angle to project high-dimensional data onto a lower-dimensional screen while keeping the shadow as wide and detailed as possible.*

### 2. The Galaxy of Stars Analogy (The New Coordinate System)
Imagine a swarm of bees or a galaxy of stars floating in a 3D room. They form a long, stretched-out, cigar-shaped cloud that tilts diagonally across the room.
* Right now, to describe the position of one star, you have to give its coordinates using the room's walls: $X$ (Left/Right), $Y$ (Front/Back), and $Z$ (Up/Down).
* PCA walks into the room and says, *"The room's walls are poorly aligned with this galaxy."* PCA physically builds a brand-new coordinate system inside the cloud:
  * **Axis 1 (PC1)**: It lays down a long rod straight through the longest center line of the cigar cloud. This is the eigenvector of maximum variance. If you only know a star's position along this one rod, you already know roughly where it is in the galaxy.
  * **Axis 2 (PC2)**: It places a second rod at a perfect 90-degree angle to the first, measuring the width of the cloud.
  * **Axis 3 (PC3)**: It places a third rod measuring the thickness of the cloud.

If the cloud is very thin, the thickness (PC3) matters very little. You can throw Axis 3 away completely. You have simplified your world from 3D space to a 2D flat plane without the stars losing their relative positions to one another.

### 3. The Physical Concept of Rigidity (Total Variance)
Think of the dataset as a stiff, physical rod or piece of wood.
* **Eigenvectors** act like the natural physical axes of symmetry of that object.
* **Eigenvalues** represent the physical stiffness or resistance to bending along those axes.

By finding the dominant eigenvalues, you are finding the rigid skeleton of your data—the primary structure that holds all the information together, allowing you to ignore the minor, bendable noise.
"""

    # 2. HTML template for PDF compiling
    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Eigenvalues, Eigenvectors, and PCA: Intuition Guide</title>
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
            page-break-before: auto;
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
        .analogy-panel {{
            background-color: #f7fafc;
            border-left: 5px solid #3182ce;
            padding: 20px;
            margin: 25px 0;
            border-radius: 4px;
        }}
        .analogy-title {{
            font-family: 'Arial', sans-serif;
            font-weight: bold;
            color: #2c5282;
            margin-bottom: 10px;
            font-size: 1.1rem;
        }}
        .math-block {{
            background-color: #f8fafc;
            border: 1px solid #e2e8f0;
            padding: 15px;
            margin: 20px auto;
            text-align: center;
            font-family: 'Courier New', Courier, monospace;
            font-size: 1.1rem;
            font-weight: bold;
            border-radius: 4px;
            max-width: 80%;
        }}
        .workflow-block {{
            background-color: #2d3748;
            color: #edf2f7;
            padding: 20px;
            font-family: 'Courier New', Courier, monospace;
            font-size: 0.95rem;
            border-radius: 6px;
            margin: 25px 0;
            text-align: left;
            line-height: 1.5;
        }}
        .page-break {{
            page-break-before: always;
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

    <h1>Eigenvalues, Eigenvectors, and PCA:<br>A Deep-Dive Intuition Guide</h1>
    
    <p style="font-size: 1.15rem; text-align: center; font-style: italic; color: #4a5568; margin-bottom: 50px;">
        A visual and conceptual guide to the rigid skeleton of high-dimensional data.
    </p>

    <!-- SECTION 1 -->
    <h2>1. What are Eigenvectors and Eigenvalues?</h2>
    <p>
        An <strong>eigenvector</strong> is a special vector that does not change its direction when a linear transformation 
        (like stretching, rotating, or shearing) is applied to it. Instead, it only scales up, scales down, or flips backwards.
    </p>
    <p>
        An <strong>eigenvalue</strong> is the scaling factor—the number that tells you how much that eigenvector stretched, 
        shrunk, or flipped during the transformation.
    </p>
    
    <h3>The Matrix Equation</h3>
    <p>Mathematically, this relationship is written as a simple equation:</p>
    <div class="math-block">
        Av = &lambda;v
    </div>
    <p>Where:</p>
    <ul>
        <li><strong>A</strong> is a square matrix representing the linear transformation.</li>
        <li><strong>v</strong> is the eigenvector (the direction that remains constant).</li>
        <li><strong>&lambda; (lambda)</strong> is the eigenvalue (the scaling factor).</li>
    </ul>

    <div class="analogy-panel">
        <div class="analogy-title">🖼️ A Visual Analogue: The Mona Lisa Stretch</div>
        <p>
            Imagine a giant rubber sheet with a picture of the <strong>Mona Lisa</strong> printed on it. Now, you grab the left 
            and right sides of the sheet and pull them hard, stretching the image horizontally.
        </p>
        <ul>
            <li><strong>The Horizontal Axis (Eigenvector)</strong>: Any arrow drawn pointing strictly left or right will still point 
                strictly left or right after the stretch. It did not tilt or rotate. This axis is an eigenvector. If the sheet 
                became twice as long, its eigenvalue is <strong>2</strong>.</li>
            <li><strong>The Diagonal Lines</strong>: An arrow pointing diagonally will tilt and change direction as the sheet stretches. 
                Because its direction changed, it is <strong>not</strong> an eigenvector.</li>
        </ul>
    </div>

    <h3>Step-by-Step Numerical Example</h3>
    <p>Let's see how they work with a simple $2 \times 2$ transformation matrix A:</p>
    <div class="math-block">
        A = | 3   1 |<br>
            | 0   2 |
    </div>
    <p>
        If we multiply this matrix by a random vector like (1, 1), the direction changes completely. It is not an eigenvector. 
        But, watch what happens if we multiply it by the vector <strong>v = (1, 0)</strong>:
    </p>
    <div class="math-block">
        A * v = | 3   1 | * | 1 | = | (3*1) + (1*0) | = | 3 |<br>
                | 0   2 |   | 0 |   | (0*1) + (2*0) |   | 0 |
    </div>
    <p>Notice that <strong>(3, 0)</strong> is exactly <strong>3 times</strong> our original vector <strong>(1, 0)</strong>.</p>
    <ul>
        <li><strong>Eigenvector (v)</strong>: (1, 0) - The direction did not change.</li>
        <li><strong>Eigenvalue (&lambda;)</strong>: 3 - The vector became exactly 3 times longer.</li>
    </ul>

    <div class="page-break"></div>

    <!-- SECTION 2 -->
    <h2>2. PCA and the Concept of Maximum Variance</h2>
    <p>
        In <strong>Principal Component Analysis (PCA)</strong>, the eigenvector with the largest eigenvalue points directly 
        in the direction of the <strong>maximum variance</strong> (the maximum spread of the data).
    </p>
    
    <h3>The Intuition: What is Variance?</h3>
    <p>Variance is simply a measure of information spread:</p>
    <ul>
        <li><strong>High Variance</strong>: The data points are stretched out far apart along an axis (lots of unique information).</li>
        <li><strong>Low Variance</strong>: The data points are tightly packed together (very little unique information).</li>
    </ul>
    <p>
        If you want to compress your data from 2D down to 1D without losing important details, you must project your data 
        onto the line that keeps the points as spread out as possible (maximizing variance).
    </p>

    <h3>How Eigenvectors Find the Maximum Variance</h3>
    <p>Imagine a 2D scatter plot of data shaped like an elongated, diagonal <strong>football</strong>:</p>
    <ol>
        <li><strong>The First Eigenvector (v1)</strong>: The algorithm draws a line straight through the longest part of the football. 
            This is the axis of <strong>maximum variance</strong> (Principal Component 1).</li>
        <li><strong>The First Eigenvalue (&lambda;1)</strong>: The length of this axis is its eigenvalue. Because the data is highly 
            stretched here, &lambda;1 will be the largest number.</li>
        <li><strong>The Second Eigenvector (v2)</strong>: The algorithm finds a line perpendicular (at 90 degrees) to the first, 
            representing the width of the football (Principal Component 2). It has a much smaller eigenvalue (&lambda;2).</li>
    </ol>

    <div class="analogy-panel">
        <div class="analogy-title">🏡 Real-World Example: Predicting House Prices</div>
        <p>
            Suppose you have a dataset with two features: <strong>House Size (sq. ft)</strong> and <strong>Number of Rooms</strong>. 
            Generally, as size increases, the number of rooms also increases. If you plot this, you get a highly correlated diagonal line.
        </p>
        <ul>
            <li><strong>Direction of Maximum Variance (v1)</strong>: This axis captures the combined concept of <strong>"Overall House Scale"</strong>. 
                It tells you the most about how houses differ from each other.</li>
            <li><strong>Direction of Low Variance (v2)</strong>: This axis only captures minor noise (e.g., whether a house happens to have unusually small rooms).</li>
        </ul>
        <p>
            By choosing the eigenvector with the maximum variance (v1), you can drop the low-variance axis (v2) entirely, compressing 
            two columns down to one ("House Scale") while retaining nearly all the original information!
        </p>
    </div>

    <div class="page-break"></div>

    <!-- SECTION 3 -->
    <h2>3. How PCA Works Behind the Scenes</h2>
    <p>
        PCA is an unsupervised learning technique used to reduce the dimensionality of large datasets. 
        It compresses data by transforming a large set of variables into a smaller one while retaining as much information (variance) as possible.
    </p>

    <h3>Step 1: Standardise the Data</h3>
    <p>
        Before doing anything else, you must standardise your features so they all have a mean of 0 and a standard deviation of 1. 
        PCA is incredibly sensitive to the scale of your data. If one column is "Salary" (in thousands) and another is "Age" (1 to 100), 
        PCA will completely ignore Age because Salary varies much more. Standardisation puts all variables on an equal playing field.
    </p>

    <h3>Step 2: Calculate the Covariance Matrix</h3>
    <p>
        Next, PCA looks at how all the features vary together. It creates a square <strong>Covariance Matrix</strong>.
        The diagonal values show the variance of each individual feature, while the off-diagonal values show the covariance 
        between features, highlighting redundant, highly correlated information.
    </p>

    <h3>Step 3: Compute Eigenvectors and Eigenvalues</h3>
    <p>
        PCA calculates the eigenvectors and eigenvalues of that Covariance Matrix.
    </p>
    <ul>
        <li><strong>Eigenvectors</strong>: Represent the directions of the new axes, called <strong>Principal Components (PCs)</strong>. 
            They are mathematically forced to be orthogonal (at a 90-degree angle) to each other, capturing completely independent information.</li>
        <li><strong>Eigenvalues</strong>: Coefficients representing the magnitude of variance carried by each Principal Component.</li>
    </ul>

    <h3>Step 4: Sort and Select Principal Components</h3>
    <p>
        The algorithm sorts the eigenvectors in descending order based on their eigenvalues. The eigenvector with the largest eigenvalue 
        becomes <strong>PC1</strong>. The eigenvector with the second largest becomes <strong>PC2</strong>, and so on. To compress your data, 
        you choose to keep only the top 'K' components that capture the vast majority of the variance (e.g., keeping 2 components out of 100).
    </p>

    <h3>Step 5: Recast the Data Along the New Axes</h3>
    <p>
        Finally, original data points are projected from their original, complex axes onto your newly selected Principal Components. 
        The result is a brand-new dataset with significantly fewer columns, completely un-correlated features, and almost all information intact.
    </p>

    <div class="workflow-block">
[Original Data] 
       &darr;
[Standardise (Mean=0, SD=1)] 
       &darr;
[Build Covariance Matrix] 
       &darr;
[Extract Eigenvectors & Eigenvalues] 
       &darr;
[Sort by Eigenvalue (Highest to Lowest)]
       &darr;
[Keep Top 'K' Components & Re-project Data]
    </div>

    <div class="page-break"></div>

    <!-- SECTION 4 -->
    <h2>4. The Physical Intuition of PCA</h2>
    <p>
        The physical intuition of PCA is <strong>finding the best angle to photograph a complex, 3D object so that you can still see its 
        true shape in a flat, 2D picture</strong>. 
    </p>
    <p>
        If you take the photo from a bad angle, the object squishes together, shapes overlap, and you lose critical information. 
        PCA spins the object around until it finds the widest, most descriptive view.
    </p>

    <div class="analogy-panel">
        <div class="analogy-title">👤 1. The Shadow Puppet Analogy (Dimensionality Reduction)</div>
        <p>
            Imagine you are holding a 3D football in a dark room and shining a flashlight on it to project a 2D shadow onto a wall.
        </p>
        <ul>
            <li><strong>The Bad Angle (Low Variance)</strong>: If you point the flashlight directly down the tip of the football, 
                its shadow on the wall looks like a small, perfect circle. You lost the information about its length because you 
                flattened out its longest axis.</li>
            <li><strong>The PCA Angle (Maximum Variance)</strong>: PCA tells you to rotate the football so the flashlight shines directly 
                on its side. Now, the shadow is a wide, long oval. This shadow captures the maximum amount of the football's true shape and size.</li>
        </ul>
    </div>

    <div class="analogy-panel">
        <div class="analogy-title">🌌 2. The Galaxy of Stars Analogy (The New Coordinate System)</div>
        <p>
            Imagine a swarm of bees or a galaxy of stars floating in a 3D room. They form a long, stretched-out, cigar-shaped cloud 
            that tilts diagonally across the room.
        </p>
        <ul>
            <li>To describe a star's position, you originally have to give its coordinates using the room's walls: X, Y, and Z.</li>
            <li>PCA walks into the room and physically builds a brand-new coordinate system inside the cloud:
                <ul>
                    <li><strong>Axis 1 (PC1)</strong>: Lays a long rod straight through the longest center line of the cigar cloud (eigenvector of maximum variance).</li>
                    <li><strong>Axis 2 (PC2)</strong>: Places a second rod at a perfect 90-degree angle to the first, measuring the cloud's width.</li>
                    <li><strong>Axis 3 (PC3)</strong>: Places a third rod measuring the cloud's thickness.</li>
                </ul>
            </li>
        </ul>
        <p>
            If the cloud is very thin, the thickness (PC3) matters very little. You can throw Axis 3 away entirely. You have simplified 
            your world from 3D space to a 2D flat plane without the stars losing their relative positions to one another.
        </p>
    </div>

    <div class="analogy-panel">
        <div class="analogy-title">🦴 3. The Physical Concept of Rigidity (Total Variance)</div>
        <p>
            Think of the dataset as a stiff, physical rod or piece of wood.
        </p>
        <ul>
            <li><strong>Eigenvectors</strong> act like the natural physical axes of symmetry of that object.</li>
            <li><strong>Eigenvalues</strong> represent the physical stiffness or resistance to bending along those axes.</li>
        </ul>
        <p>
            By finding the dominant eigenvalues, you are finding the rigid skeleton of your data—the primary structure that holds 
            all the information together, allowing you to ignore the minor, bendable noise.
        </p>
    </div>

    <div class="footer">
        <p>Unsupervised Learning Masterclass Workbook &bull; &copy; 2026 Visual Explorer Project</p>
    </div>

</body>
</html>
"""

    # Write Markdown file
    with open(md_path, "w") as f:
        f.write(md_content.strip() + "\n")
    print(f"[+] Saved Markdown guide: {md_path}")
    
    # Write Temp HTML file
    with open(temp_html_path, "w") as f:
        f.write(html_content)
        
    # Render PDF using headless google-chrome
    cmd = [
        "google-chrome",
        "--headless",
        "--disable-gpu",
        f"--print-to-pdf={pdf_path}",
        temp_html_path
    ]
    
    try:
        subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
        print(f"[+] Rendered beautiful PDF guide at: {pdf_path}")
    except Exception as e:
        print(f"[!] Failed rendering PDF guide: {e}")
        
    # Cleanup temp HTML
    if os.path.exists(temp_html_path):
        os.remove(temp_html_path)

if __name__ == "__main__":
    create_guide_files()
