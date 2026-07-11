# **Cross Validation and Regularisation**

✉ 23f1001171@ds.study.iitm.ac.in (Piush Das)

## **Goodness of MLE for Linear Regression**

Consider a dataset

The probabilistic view of linear regression assumes that the target variable yi can be modeled as a linear combination of the input features xi , with an additional noise

> term  following a zero-mean Gaussian distribution with variance 𝜖 𝜎<sup>2</sup> . Mathematically, this can be expressed as:

2 Assuming 𝜖 ~ N 0 , 𝜎

To estimate the weight vector w that best fits the data, we can apply the principle of Maximum Likelihood (ML). The ML estimation seeks to find the parameter values that maximize the likelihood of observing the given data. Assuming that the noise term  follows a zero-mean Gaussian distribution 𝜖 with variance 𝜎<sup>2</sup> , we can express the likelihood function as:

✉ 23f1001171@ds.study.iitm.ac.in (Piush Das)

This expression is equivalent to the sum squared error (SSE) objective function used in linear regression. Therefore, finding the maximum likelihood estimate wml assuming zero mean Gaussian noise is equivalent to solving the linear regression problem using the squared error loss.

To evaluate the quality of the estimated parameters, we measure the mean squared error (MSE) between the estimated parameters and the true parameters w

The MSE is given by:

Interestingly, the MSE can be expressed as:

†<br>E ‖wml - w‖22  = 𝜎2 × trace XXT implies how features are related<br>noise from<br>covariance among features<br>variance y of the data contained in X<br>

✉ 23f1001171@ds.study.iitm.ac.in (Piush Das)

## **Cross Validation for Minimizing MSE**

†<br>trace XXT<br>

For any Matrix Ad × d ,

d d<br>trace  (A)  =  ∑ ai =  ∑ 𝜆i Eigenvalues of A<br>i = 1 i = 1<br>diagonal entries<br>of A<br>

Let, Eigen Values of XXT be {𝜆1 , 𝜆2 , . . . . , 𝜆d<sup>}</sup>

**Mean Squared Error  can now be expressed as**

✉ 23f1001171@ds.study.iitm.ac.in (Piush Das)

To Improve the estimator we added a new term 𝜆I and modified the estimator to wnew

> Here 𝜆 ∈ R and I ∈ R<sup>d × d</sup> represnt a identity matrix

For some matrix A, let eigenvalues be {𝜆1 , 𝜆2 , . . . . , 𝜆d<sup>}</sup>

### **Why do we add** 𝜆I **?**

The MSE error depends upon variance and trace, we aim to reduce the value of trace to reduce MSE Overall, thus if we increase the value in the denominator, its reciprocal will become small value.

#### **Existence Theorem**

According to the Existence Theorem, there exists a value of  such that 𝜆 wnew exhibits a lower mean squared error than wml In practice, the value for 𝜆 is determined using cross-validation techniques.

**Training-Validation Split:** The training set is randomly divided into a training set and a validation set, typically in an 80:20 ratio.Train on the

training set and check for error in validation set. Among various  values, the one that yields the lowest error is selected. 𝜆

Training Set Validation Set<br>

But what is the right way to split into 80:20? we might split it random but we might get unlucky and the 20% in validation set might not be the good represntetative of what we are learning from the 80% training set, so the error might not be true error. To avoid this, we use K-Fold cross validation

**K-Fold Cross Validation:** The training set is partitioned into K equally-sized parts. The model is trained K times, each time using K-1 parts as the training set and the remaining part as the validation set. The  value that leads to the lowest average error is chosen. 𝜆

- Validate on Fi

- Pick  that gives the least average error 𝜆

✉ 23f1001171@ds.study.iitm.ac.in (Piush Das)

#### **How to choose K ?**

The Larger the value of K, the Better. In extreme cases, you can use LOOCV.

**Leave-One-Out Cross Validation:** The model is trained using all but one sample in the training set, and the left-out sample is used for validation. This process is repeated for each sample in the dataset. The optimal  is determined based on the least average error across all iterations. 𝜆

By employing cross-validation techniques, we can enhance the performance of the linear regression model by selecting an appropriate value of 𝜆

✉ 23f1001171@ds.study.iitm.ac.in (Piush Das)

## **Bayesian Modeling for Linear Regression**

Alternative way to look at wml is Bayesian Modeling. In Bayesian Modeling, we have a prior over the parameter we want to estimate and then we have likelihood, based on this we get a posterior.

Here our parameter of estimate is w , we need a prior on w , i. e , p(w) and likelihood is given as T y | x ~ N w x , 1 Therefore a choice of prior will be Normal as well 2 w ~ N 0 , 𝛾 I

where 𝛾2I is a matrix of shape d x d

As Ususal,

P(w / {(x1 , y1 )  . . . . (xn , yn )}) ∝ P({(x1 , y1 )  . . . . (xn , yn )} / w) . P(w)<br>Posterior Likelihood Prior<br>

✉ 23f1001171@ds.study.iitm.ac.in (Piush Das)

#### **How the Maximum Aposteriori Estimation will look like ?**

### Take derivative w.r.t w and equate it to 0

Conclusion, MAP Estimator for linear regression with a Gaussian prior N 0 , 𝛾2I for w is quivalent to new estimator wnew we discussed earlier -1 T wnew = XX + 𝜆I Xy

✉ 23f1001171@ds.study.iitm.ac.in (Piush Das)

## **Ridge Regression**

- Ridge regression is a linear regression technique that addresses multicollinearity and overfitting by adding a penalty term to the ordinary least squares method.

- Regularizer is used for penalizing the length of w, and pushing it as close to zero.

- Whereas, Loss function is trying to find the w for which the loss is as small as possible.

- In case of redundant features in a dataset, Ridge Regression will choose those features that have least weight

#### **Relation Between Linear Regression and Ridge Regression**

Here, the value of  depends on  For every choice of 𝜃 𝜆 𝜆 > 0 , ∃ 𝜃 s.t. optimal solution of (1 ) and 2( ) Coincide

wml<br>2<br>w : ‖ w ‖ ⩽ 𝜃<br>w12 + w22 ⩽ 𝜃<br>

✉ 23f1001171@ds.study.iitm.ac.in (Piush Das)

What is the loss/error of linear regression wml

Consider the set of all w s.t.

Every w ∈ Sc satisfies

On Simplification

T The Value of  depends on c, c<sup>,</sup> XX , wml and not on w If XXT = I

wR wml<br>(w - wml) T XXT (w - wml)<br>w : ‖ w ‖2 ⩽ 𝜃<br>w12 + w22 ⩽ 𝜃<br>

Conclusion : Ridge Regression pushes weight towards 0, but doesn't necessarily make it 0

✉ 23f1001171@ds.study.iitm.ac.in (Piush Das)

#### **Relation Between Linear Regression and LASSO Regression**

An alternate way to regularise would be using ‖ . ‖1 norm instead of ‖ . ‖2 norm

Lasso (Least Absolute Shrinkage and Selection Operator) regression is a linear regression technique that employs a regularization approach to shrink the coefficients of less important features to zero. This method effectively performs feature selection and mitigates overfitting.

✉ 23f1001171@ds.study.iitm.ac.in (Piush Das)

wml<br>wL<br>(w - wml) T XXT (w - wml)<br>w : ‖ w ‖12 ⩽ 𝜃<br>

- LASSO doesn't have closed form solution

- Sub Gradient Methods are usually used to solve LASSO

- ✉ 23f1001171@ds.study.iitm.ac.in (Piush Das)

**Sub Gradient**

✉ 23f1001171@ds.study.iitm.ac.in (Piush Das)

## **Reference**

**_Arun Raj Kumar, Lecture Slides for Machine Learning Techniques Karthik Thiagarajan, Machine Learning Techniques Github Notes. Indian Institute of Technology Madras , CS2007 Course Website Stanford University, CS229 Machine Learning Notes_**

# **Thank You !**

✉ 23f1001171@ds.study.iitm.ac.in (Piush Das)