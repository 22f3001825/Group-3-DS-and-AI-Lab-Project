# **Week 11** 

## **<u>Question 1</u>** 

### **Statement** 

In a random forest model, let be the number of randomly selected features that are used to identify the best split at any node of a tree. Which of the following is true? ( is the total number of features) 

### **Options** 

#### **(a)** 

Increasing  reduces the correlation between any two trees in the forest. 

#### **(b)** 

Decreasing  reduces the correlation between any two trees in the forest. 

#### **(c)** 

Increasing  increases the performance of individual trees in the forest. 

#### **(d)** 

Decreasing  increases the performance of individual trees in the forest. 

### **Answer** 

(b), (c) 

### **Solution** 

If we increase the number of randomly selected features in a random forest model, classifiers tend to have a similar structure and the correlation between them will be higher. But decreasing the number of features may lead to a wide variety of trees and the correlation between them will decrease. 

Increasing the number of features increases the performance of individual trees as it considers the most number of features to split the node. 

## **<u>Question 2</u>** 

### **Statement** 

A dataset was generated as per the following process: 

where and  are the constants and the error  follows Gaussian distribution with mean 

and a fixed variance. The following two models were fit on the same dataset: 

model 1: model 2: 

Select the correct options. 

### **Options** 

#### **(a)** 

Model 1 has a higher bias than model 2. 

#### **(b)** 

Model 1 has a higher variance than model 2. 

#### **(c)** 

Model 1 is more likely to overfit. 

#### **(d)** 

Model 2 is more likely to overfit. 

#### **(e)** 

Model 1 is more likely to underfit. 

#### **(f)** 

Model 2 is more likely to underfit. 

### **Answer** 

(a), (d), (e) 

### **Solution** 

Model 1 has a less complex structure to capture the real structure of the dataset and therefore, it has a higher bias than model 2 as model 2 will try to fit each and every point in the dataset. 

If we make a slight change in the dataset, model 2 may deviate a lot as it always tries to capture noise in the dataset, and therefore model 2 has a higher variance than model 1. 

Model 1 has high bias and low variance and it tends to underfit. 

Model 2 has low bias and high variance and therefore it tends to overfit. 

## **<u>Question 3</u>** 

### **Statement** 

How does bagging help in improving the classification performance? 

### **Options** 

#### **(a)** 

It helps in reducing bias 

#### **(b)** 

It helps in reducing variance 

#### **(c)** 

Bagging is inefficient if the classifiers are fully uncorrelated (independent). 

#### **(d)** 

Bagging is inefficient if the classifiers are fully correlated. 

### **Answer** 

(b), (d) 

### **Solution** 

In bagging, classifiers having high variance are trained, and their aggregate outputs are considered as the final model. The aggregation results in reducing the variances of each classifier. 

If the classifiers are fully correlated, it means on average their output is the same and, therefore aggregating them does not make much difference. 

## **<u>Question 4</u>** 

### **Statement** 

Is the following statement true or false? 

If in the soft-margin SVM problem, then the data point is correctly classified by the optimal . 

### **Options** 

#### **(a)** 

True 

#### **(b)** 

False 

### **Answer** 

(a) 

### **Solution** 

Given that . 

Since 

Using 2nd CS condition, we have 

Now the first constraint, we have 

> **[Extracted Question]**
> *T
> 1 _ W
> Tiyi - Si <
> 71 _
> <0
> w*
> TiYi >
> w*T
> Tiyi

It implies that data point is correctly classified by . 

## **<u>Question 5</u>** 

### **Statement** 

Assume that the first decision stump of the AdaBoost algorithm misclassifies data points out of data points. What will be the weights assigned to the incorrectly classified points for sampling the data points to train the second decision stump? Assume that error is defined as the proportion of incorrectly classified examples by the decision stump. 

### **Options** 

**(a)** 

#### **(b)** 

#### **(c)** 

> **[Extracted Question]**
> V7/3
> 30
> 7/3+ 70-
> 37

#### **(d)** 

> **[Extracted Question]**
> 3/7
> 30
> 3/7
> 701/7/3

### **Answer** 

(c) 

### **Solution** 

Weights assigned for creating the 1st bag are given by 

the error by the first decision stump is 

Therefore 

> **[Extracted Question]**
> 1 _ 0.3
> In
> 0.3

> **[Extracted Question]**
> 3

The weight for the incorrectly classified points will be increased by 

> **[Extracted Question]**
> the
> which hi(x) # y
> 7/3
> LUU
> for
> Wwo

The weight for the correctly classified points will be decreased by 

> **[Extracted Question]**
> Wo (i )e
> the
> for which hi(x
> V3/7
> 100

There are 30 incorrectly classified points and 70 correctly classified points. We will normalize these weights to sum over all points equal to 1. For that, we will divide each weight with the sum of all weights. 

That is 

For incorrectly classified points weights will be 

> **[Extracted Question]**
> 100
> 30V7/3
> 70v3/7
> +
> 100
> 100
> '7/3
> 30
> /7/3+ 70
> 3

## **Common data for uestions 6 and 7** **<u>q</u>** 

### **Statement** 

You have been given a dataset in -d space, which consists of 4 positive data points and 3 negative data points . We want to learn a soft-margin SVM (though the dataset is linearly separable) for this dataset. Think those points on the real line. 

## **<u>Question 6</u>** 

### **Statement** 

If how many support vectors do we have? 

### **Answer** 

### **Solution** 

When , the soft margin problem turns out to be the hard margin and it is clear that the dataset is linearly separable. Therefore, the decision boundary will be the origin and the support vectors will be and . So, there will be two support vectors. 

## **<u>Question 7</u>** 

### **Statement** 

If how many support vectors do we have? 

### **Answer** 

### **Solution** 

If , then the problem collapses as and the concept of support vectors becomes moot. So, there will be no support vectors as for support vectors, but here, . 

## **<u>Question 8</u>** 

### **Statement** 

Is the following statement true or false? 

For a fixed size of the training and test set, increasing the complexity of the model always leads to a reduction of the test error. 

### **Options** 

#### **(a)** 

True 

#### **(b)** 

False 

### **Answer** 

(b) 

### **Solution** 

If we increase the complexity of the model, the model tends to overfit as it tries to fit each and every data point including noise in the training dataset but may fail to classify the test data point. Therefore, the model will tend to overfit, and test errors may go up. 

## **<u>Question 9</u>** 

### **Statement** 

If we remove all the non-support vectors from the dataset, what will be the effect on the model? 

### **Options** 

#### **(a)** 

Model will overfit 

#### **(b)** 

Model will underfit 

#### **(c)** 

The model will not be changed 

#### **(d)** 

Can not say 

### **Answer** 

(c) 

### **Solution** 

Remember that the weight vector in the SVM problem comes out to be 

That is only the points for which (the support vectors) decide on the weight vector. 

Therefore, if we remove the non-support vectors from the dataset, the model will not change.