# Support Vector Machine - Hard Margin and Ensemble Method

✉ 23f1001171@ds.study.iitm.ac.in (Piush Das)

## Soft Margin SVM

#### How to adapt the SVM when data has outliers?

→ Make every w feasible

→ Fix any w, w classifies some points correctly and misclassifies some points

→ The incorrectly classified points "pay bribe" to go to the correct side !

##### Modified Formulation

✉ 23f1001171@ds.study.iitm.ac.in (Piush Das)

##### Objective Function

##### Primal and Dual

Solving the unconstrained optimization problem within the dual, we get

and

If C ⟹ 0, ⟹ 𝛼* = 0 ∈ Rn ⟹ w* = 0 If C ⟹ ∞, ⟹ Hard Margin

##### Complimentary Slackness Conditions

✉ 23f1001171@ds.study.iitm.ac.in (Piush Das)

Primal View                                                                             Dual View

✉ 23f1001171@ds.study.iitm.ac.in (Piush Das)

### Ensemble Classifiers

In machine learning, ensemble methods use multiple learning algorithms to obtain better predictive performance than could be obtained from any of the constituent learning algorithms alone. The Purpose of Meta Classifiers is to convert weak learners into strong learners.

- A weak learner produces a classifier which is only slightly more accurate than random classification. The most commonly used type of weak learning model is the decision tree. This is because the weakness of the tree can be controlled by the depth of the tree during construction. The weakest decision tree consists of a single node that makes a decision on one input variable and outputs a binary prediction, for a binary classification task. This is generally referred to as a “decision stump.”

- A strong classifier is a model for binary classification that performs with arbitrary performance, much better than random guessing. We seek strong classifiers for predictive modeling problems. It is the goal of the modeling project to develop a strong classifier that makes mostly correct predictions with high confidence.

Weak learners are more prone to underfitting rather than overfitting. They are simple models that perform slightly better than random guessing but have high bias and low variance. On the other hand, strong learners are more complex models that can fit the training data well. If not controlled properly, they can overfit the data by capturing noise rather than true patterns, leading to high variance. In ensemble learning, multiple weak learners are combined to form a strong learner, reducing bias while trying to control variance.

✉ 23f1001171@ds.study.iitm.ac.in (Piush Das)

##### Bias and Variance

- Bias - This measures the accuracy of the predictions or how close the model is to the true labels. Smaller the error, lower the bias. As the complexity of the model increases, bias tends to decrease. High bias models tend to underfit.

- Variance -  This measures the variability in the model to fluctuations in the training dataset. As the complexity of the model increases, variance tends to increase. High variance models tend to overfit.

Bias and variance work in opposite directions. Models with a low bias tend to have high variance. Models with a high bias tend to have low variance.

✉ 23f1001171@ds.study.iitm.ac.in (Piush Das)

Error = Bias + Variance

✉ 23f1001171@ds.study.iitm.ac.in (Piush Das)

#### Bias-Variance Trade-off:

- High Bias (Underfitting) → The model is too simple and fails to capture patterns.

- High Variance (Overfitting) → The model is too complex and captures noise along with patterns

The goal is to find a balance where both bias and variance are minimized for optimal generalization.

#### Bagging

Bagging or bootstrap aggregation is a technique that tries to reduce the variance. The basic idea is this averaging a set of observations reduces the variance. Instead of averaging observations, we will be averaging over models trained on different datasets. There are two steps:

##### Bootstrapping

We start with the dataset D and create multiple versions or bags by sampling from D with replacement. Each bag has the same number of data-points as D. Let us call the number of bags  For example with B B = 3 :

Note that points can repeat in a given bag.

✉ 23f1001171@ds.study.iitm.ac.in (Piush Das)

##### Aggregation

We train a model on each bag. Typically, this is a high-variance model, such as a deep decision tree. We call this hi, the model for the i<sup>th</sup> bag. If there are  bags, we can aggregate the outputs of all these models. B

- For a regression problem, the method of aggregation could be the mean:

- For a classification problem, the method of aggregation could be the majority vote:

##### Distribution of Points of a Bag

1 Fix a bag and consider an arbitrary data-point, say (xi , yi<sup>)</sup> . The probability that this point gets picked as the first point in the bag is The n

- probability that this point doesn't get picked as the first point is 1<sup>1</sup> The probability that this point doesn't get picked at all in this bag is n

(gets picked at all)

✉ 23f1001171@ds.study.iitm.ac.in (Piush Das)

n
1
- -
 1  1
n

1 For a very large dataset, this is about 1 - ≈ 63%  Therefore, about 63% of the data-points in a bag is unique. e

##### Random Forest

Random forests bag deep decision trees with a slight twist. While growing each tree, at each split (question-answer pair), instead of considering

> all d features, it randomly samples a subset of m features to choose from. m is typically around d. In this way, the resulting trees are uncorrelated. Since the trees are grown independently on their own bags, the algorithm can be run in parallel.

##### Boosting

A weak learner is a model that does slightly better than a random model. For example, a model that produces an error rate of 0.48 would be a weak model. An error rate of 0.48 would mean that the model produces misclassifies 48% of the data-point. Decision stump is an example of weak model.

In boosting, we combine weak learners, typically high bias models such as decision stumps, and turn them into strong learners, with a low bias. This is achieved by a sequential algorithm that focuses on mistakes committed at each step.

✉ 23f1001171@ds.study.iitm.ac.in (Piush Das)

✉ 23f1001171@ds.study.iitm.ac.in (Piush Das)

##### Observations:

- Mistakes are boosted by e<sup>𝛼t</sup> and correct data-points are brought down by e<sup>-𝛼t</sup>

- If 𝜖t is high, then e<sup>𝛼t</sup> is low. That is, if the classifier in round  has a higher error, it is assigned a lower weight in the t final ensemble.

It can be shown that as the number of rounds increases, the training error keeps decreasing. The training error of the final classifier after  T rounds is at most:

✉ 23f1001171@ds.study.iitm.ac.in (Piush Das)

### **Reference**

**_Arun Raj Kumar, Lecture Slides for Machine Learning Techniques Karthik Thiagarajan, Machine Learning Techniques Github Notes. Indian Institute of Technology Madras , CS2007 Course Website Stanford University, CS229 Machine Learning Notes_**

# **Thank You !**

✉ 23f1001171@ds.study.iitm.ac.in (Piush Das)