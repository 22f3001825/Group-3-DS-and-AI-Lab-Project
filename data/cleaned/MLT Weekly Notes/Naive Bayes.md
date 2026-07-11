Naive Bayes

✉ 23f1001171@ds.study.iitm.ac.in (Piush Das)

## Types of Modelling

In ML, we have some training data and we have built some model based on the training data, but we are going to test the model on test data; which are different from training data

The connection between testset and training set is via Distribution D

#### Generative Model

A Generative model based algorithm is an approach that seeks to model the probability distribution of the input data and generate new samples based on this distribution. The key idea involves learning the joint probability distribution of the features and labels in the training data and utilizing this learned model to make predictions for previously unseen data. Learn the joint distribution between features and labels.

#### Discriminative Model

A discriminative model-based algorithm is an approach that directly learns to distinguish between different classes or categories in a dataset. The key idea is to model the decision boundary or the conditional probability of the labels given the input features, without explicitly modeling the underlying distribution of the data itself.

✉ 23f1001171@ds.study.iitm.ac.in (Piush Das)

### Generative Model Based Algorithm

#### Data

Example: Spam Classification Mail: "how are you"

#### want to model P(x, y)

### The general steps of generative model algorithm are as follows:

1. Decide the labels by tossing a coin with p(yi = 1 = ) p 2. Decide the features using the label in step 1 by p(xi | yi<sup>)</sup>

✉ 23f1001171@ds.study.iitm.ac.in (Piush Das)

|spam (y|= 1|p<br>)<br>n|on -|spam (y = 0)|
|---|---|---|---|---|
|0|0|0<br>0|0|0|
|0|0|1<br>0|0|1|
|0|1|0<br>0|1|0|
|0|1|1<br>0|1|1|
|1|0|0<br>1|0|0|
|1|0|1<br>1|0|1|
|1|1|0<br>1|1|0|
|1|1|1<br>1|1|1|

Number of parameters in the model if class conditional independence is not assumed

#### Issue

Too Many parameters !

### Alternative Generative Model

p<br>spam (y = 1) non - spam (y = 0)<br>w1 w2 w3 w1 w2 w3<br>p1 1 p2 1 p3 1 p1 0 p2 0 p3 0<br>

#### Number of parameters in the model if class conditional independence is assumed

#### Class Conditional Independence

The class-conditional independence assumption is a fundamental concept in probability theory and machine learning, particularly relevant in the context of classification tasks. It states that given a particular class label, the features (or attributes) of an instance are conditionally independent of each other. This means that the occurrence of one feature does not provide any information about the occurrence of another feature when the class label is known.

### Naive Bayes Algorithm

The Naive Bayes algorithm is a classification algorithm based on Bayes’ theorem, which assumes that the features are independent of each other given the class label. The model calculates the probability of a sample belonging to a class by estimating the conditional probability of each feature given the class and then combining these probabilities using Bayes’ theorem. Despite its simple assumption, Naive Bayes has been found to perform well in various applications, particularly when the number of features is large but the training data is limited

#### Parameter Estimation

Using This Estimated parameters, We will develop a Model for Prediction Given, xtest ∈ 0 , 1{ }<sup>d</sup>

#### Using Bayes rule, we can express

However, since we are only interested in the comparison of these probabilities, we can avoid calculating P(xtest) Therfore by solving

we get,

Similarly, by solving

we get,

Therefore, the model predict ytest = 1 if

Otherwise, ytest = 0

The Naive Bayes algorithm employs two main techniques:

- The Class Conditional Independence Assumption.

- ’

- • Utilizing Bayes Rule.

As a result, this algorithm is commonly referred to as Naive Bayes.

✉ 23f1001171@ds.study.iitm.ac.in (Piush Das)

### Pitfalls of Naive Bayes Algorithm

The Issue with the algorithm is that if a word doesn't appear in the training set, but appears in a test datapoint, the prediction probabilities for both the class become zero.

1 0 If any feature fi was absent in the training set, it results in pi = pi = 0, leading to

A popular remedy for this issue is to introduce two “pseudo” data points with labels 1 and 0, respectively, into the dataset, where all their features are set to 1. This technique is also known as Laplace smoothing.

In brief, Laplace smoothing is a technique employed to address the zero-frequency problem in probabilistic models, particularly in text classification. It involves adding a small constant value to the count of each feature and the number of unique classes to avoid zero probability estimates, which can cause problems during model training and prediction. By incorporating this smoothing term, the model becomes more robust and better suited for handling unseen data.

### Decision Function of Naive Bayes

✉<br>

✉ 23f1001171@ds.study.iitm.ac.in (Piush Das)

predict 1<br>w<br>T<br>predict 0 w x + b = 0<br>T<br>w x = 0<br>

✉ 23f1001171@ds.study.iitm.ac.in (Piush Das)

### Gaussian Naive Bayes

Gaussian Naive Bayes, also known as Gaussian Discriminant Analysis (GDA) represents a variant of the Naive Bayes algorithm designed for classification tasks. This approach assumes that the features in the dataset follow a Gaussian (normal) distribution and computes the likelihood of a class for a given set of feature values by estimating the mean and variance of the feature values within each class.

#### Generative Story

p<br>spam (y = 1) non - spam (y = 0)<br>

✉ 23f1001171@ds.study.iitm.ac.in (Piush Das)

#### Parameter Estimation

✉ 23f1001171@ds.study.iitm.ac.in (Piush Das)

#### Prediction

Predict ytest = 1, if

This inequality can be expressed as a linear decision function

T This is of the form w xtest + b ⩾ 0, Thus, the decision function of Gaussian Naive Bayes is linear.

#### Decision Boundaries for Different Covariances

- When the covariance matrices are equal for both classes: the decision boundary is linear

✉ 23f1001171@ds.study.iitm.ac.in (Piush Das)

- When the covariance matrices are not equal for both classes:the decision boundary is a quadratic function when the covariance matrices are not equal for both classes

✉ 23f1001171@ds.study.iitm.ac.in (Piush Das)

## Reference

Arun Raj Kumar, Lecture Slides for Machine Learning Techniques Karthik Thiagarajan, Machine Learning Techniques Github Notes. Indian Institute of Technology Madras , CS2007 Course Website Stanford University, CS229 Machine Learning Notes

# **Thank You !**

✉ 23f1001171@ds.study.iitm.ac.in (Piush Das)