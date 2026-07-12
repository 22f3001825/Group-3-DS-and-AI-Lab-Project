# **Practice** 

## **<u>Question-1</u>** 

### **Statement** 

Consider the following image: 

The images shows two types of lines: Green and Orange. Which of these lines are used for calculating the residuals in linear regression? 

### **Options** 

#### **(a)** 

Green 

#### **(b)** 

Orange 

#### **(c)** 

Does not matter; Any of these may be used. 

#### **(d)** 

None of these 

### **Answer** 

(b) 

### **Solution** 

In linear regression, the task is to predict the y-axis value given the x-axis value (for a one variable scenario). The regression line tends to fit the given data points as best as possible, such that the residual error may be minimized. Here the residual error is the distance between the actual y- value and the y-value that is predicted by the regression line. Hence, this distance line will be a vertical line. Hence the orange lines will represent these residuals. 

The green lines on the other hand, represent the errors in PCA, as in PCA, the principal components tend to fit the data points such that the variance in the data is captured. The errors in PCA, thus are perpendicular lines. 

**<u>Question-2</u>** 

### **Statement** 

Assume that the eigenvalues of a matrix are 2, 3, 1.  What will be the eigenvalues of the matrix where  is a identity matrix. 

### **Options** 

#### **(a)** 

2, 3, 1 

#### **(b)** 

7, 8, 6 

#### **(c)** 

10, 15, 5 

#### **(d)** 

6, 6, 6 

### **Answer** 

(b) 

### **Solution** 

If a, b, c are eigenvalues of a matrix A, then then the eigenvalues of the matrix will be and . 

## **<u>Question-3</u>** 

### **Statement** 

What will be the trace of ? 

Note: are the eigenvalues of 

### **Options** 

#### **(a)** 

#### **(b)** 

#### **(c)** 

#### **(d)** 

### **Answer** 

(d) 

### **Solution** 

The trace of a matrix is the sum of its eigenvalues. 

If ‘s are the eigenvalues of , then will be the eigenvalues of . 

If a, b are eigenvalues of a matrix M, then 1/a and 1/b will be the eigenvalues of the matrix . 

So, the eigenvalues of will be . Hence the trace will be 

**<u>Question-4</u>** 

### **Statement** 

Assume that as part of 3-fold cross-validation, the data was divided into parts . Subsequently, cross-validation was performed. In this context, which of the following is True? 

### **Options** 

#### **(a)** 

In each iteration of cross-validation, one of will be used for training, and the remaining two parts will be used for testing. 

#### **(b)** 

In each iteration of cross-validation, two of will be used for training, and the remaining one part will be used for validation. 

#### **(c)** 

In each iteration of cross-validation, two of will be used for training, and the remaining one part will be used for testing. 

#### **(d)** 

In each iteration of cross-validation, one of will be used for training, and the remaining two parts will be used for validation. 

### **Answer** 

(b) 

### **Solution** 

In k-fold cross-validation, the training data is split into k parts. 

K-fold cross validation involves k iterations. 

In each iteration, one of the k parts is used for validation and the remaining k-1 parts are used for training. 

Hence, in k-fold cross validation, one part will be used for validation and remaining two will be used for training. 

**<u>Question-5</u>** 

### **Statement** 

Assume that we obtain the weight vector when = 3 is used in Ridge Regression. 

If  is increased to 6, which of the following is most likely to be the updated weight vector? 

### **Options** 

#### **(a)** 

#### **(b)** 

#### **(c)** 

### **Answer** 

(b) 

### **Solution** 

In regularization, as the value of  (which represents penalty for higher weights) is increased, the weights are further reduced. 

Therefore, in the given question, as the value of  is increased from 3 to 6, the penalty for having higher weights will increase, thus shrinking the weights. 

## **<u>Question-6</u>** 

### **Statement** 

The mean squared error of could come out to be large if 

### **Options** 

#### **(a)** 

Trace of is large. 

#### **(b)** 

Trace of is large. 

#### **(c)** 

is large. 

#### **(d)** 

‘s are large. 

### **Answer** 

(b), (c) 

### **Solution** 

MSE = 

Hence, MSE will come out to be large if is large or trace of is large. 

**<u>Question-7</u>** 

### **Statement** 

Cross validation may be useful as it may help in 

### **Options** 

#### **(a)** 

Reducing the trace of the inverse of covariance matrix. 

#### **(B)** 

Increasing the trace of the inverse of covariance matrix. 

### **Answer** 

(a) 

### **Solution** 

The expression for is given by Cross validation results into a weight vector 

> **[Extracted Question]**
> Xy
> +
> AI) -1Xy
> XXT

This in turn reduces the trace of the inverse of covariance matrix, thus reducing the MSE. 

**<u>Question-8</u>** 

### **Statement** 

Assume that Lasso is applied to a data set containing only one feature. If  is increased to a high value, which of the following is correct? 

### **Options** 

#### **(a)** 

The regression line may become horizontal. 

#### **(b)** 

The regression line may become horizontal. 

#### **(c)** 

The regression line will remain the same. 

#### **Answer** 

(a) 

### **Solution** 

In lasso, as the value of  is increased, due to a very high penalty, the coefficient of the only feature becomes zero. 

The coefficient represents the slope. And when slope = 0, it results into a horizontal line. 

**<u>Question-9</u>** 

### **Statement** 

In Ridge Regression, if  tends to zero, the solution approaches to 

### **Options** 

#### **(a)** 

Zero 

#### **(b)** 

One 

#### **(c)** 

Linear Regression 

#### **(d)** 

Lasso Regression 

#### **(e)** 

Infinity 

### **Answer** 

(c) 

### **Solution** 

The weight vector expression for linear regression is The weight vector expression for ridge regression is 

> **[Extracted Question]**
> XXT)-IXy
> XXT + AI)-1Xy

When  tends to zero, the solution of ridge is same as that of linear regression.