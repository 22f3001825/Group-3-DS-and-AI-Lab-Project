# Week 2 FAQs
Source: https://mlt.pulki.in/week2/week2.html

## Question/Topic: 📚 Topics Covered in Week 2
Issues with PCA When \(d \gg n\) , calculating the eigenpairs of \(\frac{1}{n}XX^T\) becomes computationally expensive. PCA assumes that data points have a linear relationship. Kernel Functions Enable PCA to operate in higher-dimensional feature spaces without explicitly computing the coordinates. Common kernel functions: Polynomial, Gaussian, and Sigmoid. Kernel PCA A nonlinear extension of PCA using kernel functions. Useful for datasets that are not linearly separable.

## Question/Topic: 🔍 Relationship of Eigenpairs Between\(XX^T\)and\(X^TX\)
Let \((\lambda, v)\) be an eigenpair of \(X^TX\) : \[ \mathbf{X}^T\mathbf{X}\mathbf{v} = \lambda \mathbf{v} \] By pre-multiplying both sides by \(\mathbf{X}\) , we obtain: \[ \mathbf{XX}^{T}\mathbf{Xv} = \mathbf{X} \lambda \mathbf{v} \] \[ \left(\mathbf{XX}^{T}\right)\mathbf{Xv} = \lambda \mathbf{Xv} \] ✅ Conclusion If \((\lambda, v)\) is an eigenpair of \(X^TX\) , then \((\lambda, Xv)\) will be an eigenpair of \(XX^T\) . Note: Only the non-zero eigenvalues of \(XX^T\) and \(X^TX\) are equal. The normalized form of the eigenvector \(Xv\) of \(XX^T\) is: \[ \frac{1}{\sqrt{\lambda}} Xv \]

## Question/Topic: ✅ Conclusion
If \((\lambda, v)\) is an eigenpair of \(X^TX\) , then \((\lambda, Xv)\) will be an eigenpair of \(XX^T\) . Note: Only the non-zero eigenvalues of \(XX^T\) and \(X^TX\) are equal. The normalized form of the eigenvector \(Xv\) of \(XX^T\) is: \[ \frac{1}{\sqrt{\lambda}} Xv \]

## Question/Topic: 🔍 How to Check Whether a Given Function Is a Kernel Function
A kernel function allows us to compute relationships between data points in a higher-dimensional space without explicitly performing the transformation. To verify whether a function is a valid kernel, there are two approaches: Explicit Transformation: Identify the transformation \(\phi\) such that: \[k(x, y) = \phi(x)^T \phi(y)\] Mercer’s Theorem: A function is a valid kernel if and only if: It is symmetric. The kernel matrix \(K\) is positive semi-definite. ➡️ Learn More: Watch this video for a detailed explanation.

## Question/Topic: 🔍 Dimension of the Transformed Space Using a Polynomial Kernel
For data points in \(d\) dimensions and a polynomial kernel of degree \(p\) , defined as: \[ k(x, y) = (1 + x^T y)^p \] The dimension of the transformed space is given by: \[ \binom{p + d}{d} \]

## Question/Topic: 🔍 Scalar Projection Using Kernel PCA
In Kernel PCA, we first compute the eigenpairs of the kernel matrix \(K\) : \[ (\lambda_1, v_1), (\lambda_2, v_2), \dots, (\lambda_r, v_r) \] Where: \(\lambda_1 \geq \lambda_2 \geq \dots \geq \lambda_r\) \(\|v_i\| = 1\) The scalar projection of a data point \(\mathbf{x}_i\) onto the \(j^\text{th}\) principal component is given by: \[ \phi(\mathbf{x})^T w \] Where \(w\) is the eigenvector of the covariance matrix \(C\) . Using the relationship between eigenpairs of \(XX^T\) and \(X^TX\) , this can be expressed as: \[ \phi(\mathbf{x_i})^T \phi(\mathbf{X}) \frac{v_j}{\sqrt{n \lambda_j}} \] Expanding further: \[ = \sum_{p=1}^{n} \phi(\mathbf{x_i})^T \phi(\mathbf{x_p}) \frac{v_{jp}}{\sqrt{n \lambda_j}} \] \[ = \sum_{p=1}^{n} k(x_i, x_p) \frac{v_{jp}}{\sqrt{n \lambda_j}} \] ➡️ Learn More: Read detailed notes here (pages 10-12).

## Question/Topic: 💡 Need Help?
For any technical issues or errors, please contact: 📧 22f3001839@ds.study.iitm.ac.in ⬅️ Week 1 Week 3 ➡️