# PCA: Step-by-Step Educational Walkthrough

Principal Component Analysis (PCA) is a linear dimensionality reduction technique. It simplifies high-dimensional data by projecting it onto a lower-dimensional subspace (e.g., compressing 3D down to 2D, or 2D down to 1D) while keeping the maximum amount of original information (variance).

Here is a step-by-step trace of how 2D data is compressed into 1D numbers using manual linear algebra.

---

## 📊 The Sample Dataset
Imagine we have 3 points plotted on a 2D coordinate grid:
* **Point A**: (1, 2)
* **Point B**: (3, 4)
* **Point C**: (5, 6)

If we plot these, they form a perfect diagonal line running upwards at a 45-degree angle. We want to compress these 2D points into a single **1D coordinate** without losing their relative spacing.

---

## 📐 Step-by-Step Mathematical Compression

### 1️⃣ Step 1: Mean Centering
First, we must shift the dataset so its average center rests exactly at $(0, 0)$.
1. **Calculate the averages (means)**:
   * $\text{Mean } X = \frac{1 + 3 + 5}{3} = 3$
   * $\text{Mean } Y = \frac{2 + 4 + 6}{3} = 4$
2. **Subtract the means** from each coordinate:
   * **Point A'** = $(1 - 3, 2 - 4) = \mathbf{(-2, -2)}$
   * **Point B'** = $(3 - 3, 4 - 4) = \mathbf{(0, 0)}$
   * **Point C'** = $(5 - 3, 6 - 4) = \mathbf{(2, 2)}$

Our points are now centered at $(0, 0)$.

---

### 2️⃣ Step 2: Compute the Covariance Matrix
The covariance matrix measures how the features vary together. Using the sample covariance formula (dividing by $N - 1 = 2$):
$$\text{Cov}(X, Y) = \frac{\sum (X - \text{Mean } X)(Y - \text{Mean } Y)}{N - 1}$$

1. **Calculate Covariance of X with itself ($\text{Cov}(X, X)$)**:
   * $\frac{(-2)^2 + 0^2 + 2^2}{2} = \frac{4 + 0 + 4}{2} = \mathbf{4}$
2. **Calculate Covariance of Y with itself ($\text{Cov}(Y, Y)$)**:
   * $\frac{(-2)^2 + 0^2 + 2^2}{2} = \frac{4 + 0 + 4}{2} = \mathbf{4}$
3. **Calculate Cross-Covariance ($\text{Cov}(X, Y)$)**:
   * $\frac{(-2 \times -2) + (0 \times 0) + (2 \times 2)}{2} = \frac{4 + 0 + 4}{2} = \mathbf{4}$

Our **Covariance Matrix ($S$)** is:
$$S = \begin{pmatrix} 4 & 4 \\ 4 & 4 \end{pmatrix}$$

---

### 3️⃣ Step 3: Find Eigenvalues & Eigenvectors (Eigendecomposition)
Now, we solve for the directions along which the data stretches the most.
1. **Find Eigenvalues ($\lambda$)** by solving the characteristic equation $\det(S - \lambda I) = 0$:
   $$\det \begin{pmatrix} 4 - \lambda & 4 \\ 4 & 4 - \lambda \end{pmatrix} = 0$$
   $$(4 - \lambda)^2 - 16 = 0 \implies \lambda^2 - 8\lambda = 0$$
   This gives two eigenvalues:
   * **$\lambda_1 = 8$** (Primary component — captures 100% of the variance!)
   * **$\lambda_2 = 0$** (Secondary component — captures 0% of the variance!)

2. **Find the Eigenvector ($v$)** for the primary eigenvalue $\lambda_1 = 8$:
   $$\begin{pmatrix} 4 - 8 & 4 \\ 4 & 4 - 8 \end{pmatrix} \begin{pmatrix} x \\ y \end{pmatrix} = 0 \implies \begin{pmatrix} -4 & 4 \\ 4 & -4 \end{pmatrix} \begin{pmatrix} x \\ y \end{pmatrix} = 0$$
   This simplifies to $-4x + 4y = 0 \implies x = y$. 
   To make it a unit vector (length of 1), we normalize it:
   $$\mathbf{v} = \begin{pmatrix} \frac{1}{\sqrt{2}} \\ \frac{1}{\sqrt{2}} \end{pmatrix} \approx \begin{pmatrix} 0.7071 \\ 0.7071 \end{pmatrix}$$
   *This vector points exactly at a 45-degree angle—the direction of our diagonal data!*

---

### 4️⃣ Step 4: Projection to 1D
To compress our 2D centered points, we project (dot product) them onto our 1D unit eigenvector $\mathbf{v}$:
$$\text{Projected Value} = X_{\text{centered}} \times 0.7071 + Y_{\text{centered}} \times 0.7071$$

* **Point A' (-2, -2)**:
  * $(-2 \times 0.7071) + (-2 \times 0.7071) = -1.4142 - 1.4142 = \mathbf{-2.8284}$
* **Point B' (0, 0)**:
  * $(0 \times 0.7071) + (0 \times 0.7071) = \mathbf{0.0}$
* **Point C' (2, 2)**:
  * $(2 \times 0.7071) + (2 \times 0.7071) = 1.4142 + 1.4142 = \mathbf{2.8284}$

---

## 📈 Summary of Results

| Original 2D Coordinate | Centered 2D Coordinate | Compressed 1D Coordinate | Information Retained |
| :--- | :---: | :---: | :---: |
| **Point A** (1, 2) | (-2, -2) | **-2.83** | **100%** |
| **Point B** (3, 4) | (0, 0) | **0.00** | **100%** |
| **Point C** (5, 6) | (2, 2) | **2.83** | **100%** |

### Key Takeaway
We have successfully compressed our 2D dataset down into single 1D coordinates. Because the original points were perfectly aligned, **PC1 captures 100% of the variance ($\lambda_1 = 8$, $\lambda_2 = 0$)**, meaning we compressed the data with absolutely **zero information loss**! The relative distances between A, B, and C are perfectly preserved.
