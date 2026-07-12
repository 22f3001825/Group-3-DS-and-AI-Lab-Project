# **Linear Regression**

✉ 23f1001171@ds.study.iitm.ac.in (Piush Das)

### **Supervised Learning**

Supervised learning is a type of machine learning where a model is trained on a set of labeled data, meaning each input is paired with the correct output. The model learns to predict the output for new input data by comparing its predictions with the actual answers provided in the training data, adjusting itself to minimize errors and improve accuracy.

##### **Input**

##### **Regression**

that captures the underlying relationship (pattern) between data-points and labels and generalizes it to unseen data-points. The defining characteristic of a regression problem is that the labels are continuous valued real numbers(Example - Rainfall Prediction)

##### **Classification**

that captures the underlying relationship (pattern) between data-points and labels and generalizes it to unseen data-points. The defining characteristic of a classification problem is that the labels are from a finite, discrete set. If  k = 2 , the problem is called **binary classification** (Example - Spam vs Non-Spam mails). If k>2 , the problem is called **multi-class classification** (Example - Digit Classification)

✉ 23f1001171@ds.study.iitm.ac.in (Piush Das)

##### **Regression**

##### **Input**

Goal of linear regression is to find a mapping between the input and output variables, represented as follows:

- R<sup>d</sup> is feature space

- R is label space

d But the issue is, there are infinitely many function from R → R , How do we measure the goodness of the function for respective dataset ?

- h(xi) → predicted label for xi

- yi → true label for xi

✉ 23f1001171@ds.study.iitm.ac.in (Piush Das)

Ideally, this error,

However, achieving this may only result in memorizing the data and its outputs as this way we will get zero error on training data, which is not a desired outcome, as we care about the test performance.

To mitigate the memorization problem, introducing a structure to the mapping becomes necessary. The simplest and commonly used structure is linear, which we will adopt as the underlying structure for our data.

Simplest fix -  Impose linear structure to reduce our search space

Thus, our modified goal is to minimize:

##### **Optimising The Error Function**

Defining a function f(w) that captures this minimization problem, we have:

Setting the gradient equation to zero 𝛻 f(w) = 0 , we obtain:

† Here, XXT represents the pseudo-inverse of XXT

✉ 23f1001171@ds.study.iitm.ac.in (Piush Das)

##### **Geometric Interpretation**

for example, for any data matrix X of shape d = 2 , n = 3

f1 f2
x1 | | y1
x2 | | y2
x3 | | y3

y ∈ R 3
* * T *
𝛼 f1 + 𝛼 f2  = x 𝛼
| | 𝛼1
f1 f2
| | 𝛼2
f1 ∈ R3
3
f2 ∈ R
Space spanned by feature vector

✉ 23f1001171@ds.study.iitm.ac.in (Piush Das)

We Know,

* * Substituting w = 𝛼 in eq. (1) we get,

Conclusion, XTw* corresponds to the projection of the labels onto the subspace spanned by the features.

✉ 23f1001171@ds.study.iitm.ac.in (Piush Das)

##### **Gradient Descent**

† † * T T The normal equation for linear regression w = XX (Xy) involves calculating XX which can be computationally expensive with a complexity of O d3

But, We know w<sup>*</sup> represents the solution of an unconstrained optimization problem, so taking the computational consideration into account it can be solved using gradient descent.

- Choose the initial point w<sup>0</sup>

- Define the learning rate 𝜂

- Calculate the gradient at the current point 𝛻 f wt

minima.

✉ 23f1001171@ds.study.iitm.ac.in (Piush Das)

The iterative formula for gradient descent for linear regression :

Here, 𝜂 is a scalar that controls the step-size  of the descent, and  represents the current iteration. t

Observe, there is no need to compute inverse but the issue arrives when n ≫ d.

✉ 23f1001171@ds.study.iitm.ac.in (Piush Das)

##### **Stochastic Gradient Descent**

##### **for t = 1 , . . . , t**

- At each step sample a bunch of datapoints (k) uniformly at random from set of all datapoints.

- Pretend that sample is the entire dataset and take gradient w.r.t. it

##### **End**

After T rounds we get,

The progress of SGD is less smooth given that we are only using an approximate version the gradient, but it is guaranteed to converge to optima with high probability.

✉ 23f1001171@ds.study.iitm.ac.in (Piush Das)

##### **Kernel Regression**

†
* T
w  =  XX (Xy)
w *
˜
w

w<sup>*</sup> must lie on the span of the data-points

✉ 23f1001171@ds.study.iitm.ac.in (Piush Das)

What if the data points reside in a non-linear subspace? Similar to dealing with non-linear data clustering, kernel functions are employed in this scenario as well

✉ 23f1001171@ds.study.iitm.ac.in (Piush Das)

To make prediction for some Xtest ∈ Rd

Here, 𝛼i* denotes the importance of the -th data point in relation to i w<sup>*</sup> and k(xi , xtest<sup>)</sup> signifies the similarity between xtest and xi

#### 𝜙 **transformation can be:**

✉ 23f1001171@ds.study.iitm.ac.in (Piush Das)

##### **Probabilistic View of Linear Regression**

> Consider a dataset {(x1 , y1<sup>) (</sup> x2 , y2<sup>)</sup> . . . (xn , yn<sup>)}</sup> with x ∈ Rd ; y ∈ R The probabilistic view of linear regression assumes that the target variable yi can be modeled as a linear combination of the input features xi , with an additional noise term  following a zero-mean Gaussian distribution with variance 𝜖 𝜎<sup>2</sup> . Mathematically, this can be expressed as:

2 Assumin 𝜖 ~ N 0 , 𝜎

To estimate the weight vector w that best fits the data, we can apply the principle of Maximum Likelihood (ML). The ML estimation seeks to find the parameter values that maximize the likelihood of observing the given data. Assuming that the noise term  follows a zero-mean Gaussian distribution 𝜖 with variance 𝜎<sup>2</sup> , we can express the likelihood function as:

This expression is equivalent to the mean squared error (MSE) objective function used in linear regression. Therefore, finding the maximum likelihood estimate wml assuming zero mean Gaussian noise is equivalent to solving the linear regression problem using the squared error loss.

✉ 23f1001171@ds.study.iitm.ac.in (Piush Das)

## **Reference**

**_Arun Raj Kumar, Lecture Slides for Machine Learning Techniques Karthik Thiagarajan, Machine Learning Techniques Github Notes. Indian Institute of Technology Madras , CS2007 Course Website Stanford University, CS229 Machine Learning Notes_**

# **Thank You !**

✉ 23f1001171@ds.study.iitm.ac.in (Piush Das)