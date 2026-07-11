# **Practice Assignment** 

#### **Note:** 

1. In the following assignment, denotes the data matrix of shape where d and n are the number of features and samples, respectively. 

2. denotes the sample and denotes the corresponding label. 

3. denotes the weights (parameter) in the linear regression model. 

# **<u>Question 1</u>** 

## **Statement** 

Consider the following two models for two different datasets: 

> **[Extracted Question]**
> T1

> **[Extracted Question]**
> 11

Models are represented by the line and both the graphs are on the same scale. Which model will give the more training error? 

## **Options** 

### **(a)** 

Model 1 

### **(b)** 

Model 2 

## **Answer** 

(a) 

## **Solution** 

Since the error for a point is the perpendicular distance of that point from the model (line in this case), model 1 has a larger perpendicular distance than that model 2. That is why model 1 will give more training error. 

# **Common data for Questions 2 and 3** 

## **Statement** 

Consider the following linear regression model: 

where the noise  follows the following distribution: 

with .  is a parameter. 

# **<u>Question 2</u>** 

## **Statement** 

Find the log-likelihood function for the parameters if the samples are taken from the above model. 

**Note:** If , then 

## **Options** 

### **(a)** 

**(b)** 

### **(c)** 

### **(d)** 

## **Answer** 

(d) 

## **Solution** 

Given that 

Where the error  follows the below distribution 

Therefore, 

For the sample , the likelihood function is defined as (Constant terms are avoided) 

> **[Extracted Question]**
> fyle; (yi)
> ~Iyi
> Dil
> exp
> wT

Taking we got 

> **[Extracted Question]**
> og
> IIexp ( =lyi
> WT
> "3l)
> Ti
> Yi|
> (~lue

# **<u>Question 3</u>** 

## **Statement** 

Choose the correct statement. 

## **Options** 

### **(a)** 

ML estimator assuming noise following the above distribution is the same as linear regression with squared error. 

### **(b)** 

ML estimator assuming noise following the above distribution is the same as linear regression with absolute error. 

## **Answer** 

(b) 

## **Solution** 

Let be the ML estimate for , then 

> **[Extracted Question]**
> argmax log( L(w; 81,82,
> 8n, 91, 92
> Ei
> Yi |
> argmax
> Ti
> Yi|
> argmin
> ~lwt_

It implies that ML estimator assuming noise following the above distribution is the same as linear regression with absolute error. 

# **Common data for Questions 4, 5, and 6** 

Consider the following dataset with one feature and corresponding label: 

||**Label ( )**|
|---|---|
|2|2.2|
|0|-0.1|
|-3|-2.5|
|1|1|

# **<u>Question 4</u>** 

## **Statement** 

Fit the linear regression model 

using squared error. 

## **Options** 

**(a)** 

### **(b)** 

### **(c)** 

### **(d)** 

### **Answer** 

(c) 

## **Solution** 

The weight vector is given as 

> **[Extracted Question]**
> W =
> (XXT)-IXy
> [2.2
> 0.1,
> 2.5,1]

Here, and 

Doing the matrix multiplication, we get 

Therefore, the fit model is given as 

# **<u>Question 5</u>** 

## **Statement** 

What will be the prediction for the point ? Write your answer correct to two decimal places. 

## **Answer** 

3.6 Range = [3.5, 3.8] 

## **Solution** 

The model is given by 

at , we have 

# **<u>Question 6</u>** 

## **Statement** 

Find the root mean squared error (RMSE) for the training dataset. Write your answer correct to two decimal places. 

> **[Extracted Question]**
> RMSE
> (yi
> ya)?

## **Answer** 

0.23 Range = [0.1, 0.2] 

## **Solution** 

|**x_1**|**Label (y)**||
|---|---|---|
|2|2.2|1.8|
|0|-0.1|0|
|-3|-2.5|-2.7|
|1|1|0.9|

Therefore, the RMSE is given by 

> **[Extracted Question]**
> 1/2
> Zi-w))
> 1/2
> (42.2
> 1.8)2 + (~0.1)2 + (-2.5 + 2.7)2 + (1 _
> 0.9)2) )

# **<u>Question 7</u>** 

## **Statement** 

What are the possible issues with the gradient descent? 

## **Options** 

### **(a)** 

Gradient descent can never converge to the global minima. 

### **(b)** 

If the number of training samples is large, then the gradient descent assuming constant learning will take a long time to converge because a weight update is only happening once per data cycle. 

### **(c)** 

The larger your dataset, the more nuanced the gradients become, and the more time is used, and eventually, there will not be much learning. 

## **Answer** 

(b), (c) 

## **Solution** 

Statement (a) is false as if we initialize the weight vector such that the loss function value corresponding to the same weight is near the global minima, the gradient descent will converge to the global minima. 

Statement (b) is true since it will take more time to update the weights in each iteration when the number of samples becomes large. Even the matrix multiplications such as become very computationally large. 

Statement (c) is true since the larger the dataset, the more time is used to update the weights and the gradient descent becomes nuanced. 

# **<u>Question 8</u>** 

## **Statement** 

Gaussian kernel regression with parameter was applied to the following dataset with two features: 

The weight vector can be written as . The vector  is given by which is obtained as , where is the kernel matrix. What will be the prediction for point ? 

**Answer** 

## **Solution** 

The prediction is given by 

The kernel function is given by 

> **[Extracted Question]**
> Ilxi
> ei2`
> exp
> 2(02)
> exp (~Ilzi
> Ejl?) (: o2 = 1/2

Now, 

> **[Extracted Question]**
> k(l1,0, [1,1],
> exp( _ (0 + 1)
> k([o, 1], [1,1],
> exp(_ (1 + 0)
> k([1,1], [1,
> exp( ~ (0 +
> k([o, 0], [1,1]5
> exp(
> +1)

Putting the values in eq (1), we get 

# **<u>Question 9</u>** 

## **Statement** 

Is the following statement true or false? 

The line (or hyperplane in higher dimension) that passes through the origin will incur the minimum error out of all linear functions. 

## **Options** 

### **(a)** 

True 

**(b)** 

False 

## **Answer** 

(b) 

Consider the dataset as given in the following image: 

> **[Extracted Question]**
> x(l)

We can see that the model that passes through the origin (blue line) incurs more loss than the model that doesn't pass through the origin (green line). Therefore, the given statement is false. 

# **<u>Question 10</u>** 

## **Statement** 

Since the best fit line need not pass through the origin for some datasets, the model may not give the best fit solution. What should be the better way to tackle this problem? 

## **Options** 

### **(a)** 

mean-center the dataset. 

### **(b)** 

Add a dummy feature in the dataset and learn the model . 

## **Answer** 

(b) 

## **Solution** 

If we allow our model to have an intercept on the -axis (on the label axis), our model need not always pass through origin, we can tackle the above problem.