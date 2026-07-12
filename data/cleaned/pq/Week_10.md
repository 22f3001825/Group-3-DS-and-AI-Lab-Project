# **Practice**

This document has questions.

## **Common Data for Questions (1) to (6)**

### **Statement**

Consider a hard-margin SVM trained on a dataset in for a binary classification task. Red and green points belong to the training dataset. Red points belong to class and green points belong to class . The black-point is a test data-point. The dotted lines are the supporting hyperplanes for the SVM.

**Note** : We don't have access to the test data-point during training; it is given to us _after_ the model has been learned on the training dataset.

> **[Extracted Question]**
> T2
> (~9,
> wTx = 1
> wTx =
> -1
> (1, 0)
> (3, 1)

## **<u>Question-1</u>**

### **Statement**

What is the maximum number of support vectors that the model could have?

### **Answer**

### **Solution**

The number of support vectors is upper bounded by the total number of points that lie on the supporting hyperplanes. Recall that support vectors are those points for which . By complementary slackness, if then . So, we can rightfully claim that if , then that point lies on one of the two supporting hyperplanes.

Now, can we claim that the number of support vectors is exactly equal to ? This is a bit tricky. The claim we are trying to make here is stronger:

If a point lies on either of the two supporting hyperplane, then it is a support vector.

Mathematically, this means the following. If , then . This is something that is not guaranteed by complementary slackness. All that complementary slackness tell us is that for every point in the dataset, . It could be the case that both and . In such a case, the point wouldn't qualify as a support vector. To summarize, every support vector lies on one of the two supporting hyperplanes, but every point on the supporting hyperplanes need not be a support vector.

**<u>Question-2</u>**

### **Statement**

What is the value of the weight vector ? Select all options that are correct.

### **Options**

#### **(a)**

#### **(b)**

#### **(c)**

#### **(d)**

### **Answer**

(a)

### **Solution**

Let the weight vector be . Then, we have:

Solving this system of equations, we get:

**<u>Question-3</u>**

### **Statement**

What is the equation of the decision boundary? Select all options that are correct.

### **Options**

#### **(a)**

#### **(b)**

#### **(c)**

#### **(d)**

### **Answer**

(a), (b)

### **Solution**

The equation of the solid line (decision boundary) is given by:

We can now multiply both sides by  to get:

Note that this kind of scaling cannot be done with the weight vector! Scaling the weight vector alone would result in a different set of supporting hyperplanes. Moreover, the scaled weight vector would not be a solution to the primal problem.

## **<u>Question-4</u>**

### **Statement**

What is the width of the separation between the two supporting hyperplanes? Enter your answer correct to three decimal places.

**Note** : the exact value of the width is different from the solution to the optimization problem that is discussed in the lecture.

### **Answer**

Range: [5.36, 5.39]

### **Solution**

The width is given by:

> **[Extracted Question]**
> 5.378
> 5/21)2 + (2/7)2

## **<u>Question-5</u>**

### **Statement**

What is the predicted label of the black test-point?

### **Answer**

### **Solution**

We can infer this either from the graph or we can use:

**<u>Question-6</u>**

### **Statement**

Is the following statement true or false?

For any test-point that falls within the region bounded by the supporting hyperplanes, no label can be assigned, as it doesn't satisfy the constraints in the optimization problem.

### **Options**

#### **(a)**

True

#### **(b)**

False

### **Answer**

(b)

### **Solution**

The decision boundary is given by . Though the points on the supporting hyperplanes help in determining the value of , they don't meddle with the prediction of points that fall within them. This depends purely on the sign of .

## **<u>Question-7</u>**

### **Statement**

SVM is a ———

### **Options**

#### **(a)**

generative model

#### **(b)**

discriminative model

### **Answer**

(b)

### **Solution**

SVM is a discriminative model. There are no explicit probabilities involved, but we can present it this way:

We aren't really concerned about how the point  was generated. Given a point, we use the line to determine its label. Note that this kind of presentation is similar to what we saw for perceptrons.

## **<u>Question-8</u>**

### **Statement**

Study the similarities and differences between the following models:

(1) perceptron

- (2) logistic regression

(3) SVM

### **Solution**

Similarities:

- All three are linear models

- As a result, the decision boundary is given by for all three models

- All three are discriminative models.

Differences:

- Logistic regression associates an explicit probability for each data-point. Farther apart a point is from the decision boundary, greater is the confidence with which LR predicts its label. This is not the case with perceptron and SVM.

- SVM uses a more principled approach compared to perceptrons. Max-margin classifiers will generalize better than perceptrons.

- The soft-margin formulation is robust to outliers, this is not the case with perceptrons which is guaranteed to converge only in the linearly separable case. Logistic regression is also more forgiving with outliers compared to perceptrons.

**Common Data for Questions (9) and (13)**

### **Statement**

Consider a soft-margin SVM that has been trained on a dataset in . A subset of the data-points and the decision boundary (solid line) is shown below:

> **[Extracted Question]**
> wTx < -1
> wTx > 1
> Green:
> +1
> E6
> 83
> 87
> E2
> E5
> 84
> wTx =
> ~1
> wTx = 1

For each point, consider to be the minimum bribe that has to be paid to take it to the correct supporting hyperplane.

### **Solution**

For all the problems here, the basic idea is to start with the inequalities for the slack-variables:

> **[Extracted Question]**
> Si > 0
> Ei 21_ (wTxi)y

These correspond to the two inequalities in the soft-margin formulation for each point. Combining these two inequalities, we get:

Since we have been asked for the minimum bribe, it is going to be:

For points which are either on the right supporting hyperplane or beyond it, we have . As a result, we see that . That is, these points do not have to pay any bribe as they are already on the right side. Other points have to pay a non-zero, positive bribe. The value of the bribe can be computed by studying the geometry of the three parallel lines: , and .

## **<u>Question-9</u>**

### **Statement**

What is the value of ?

### **Answer**

## **<u>Question-10</u>**

### **Statement**

What is the value of ?

### **Answer**

## **<u>Question-11</u>**

### **Statement**

What is the value of ?

### **Answer**

## **<u>Question-12</u>**

### **Statement**

What is the value of ?

### **Answer**

## **<u>Question-13</u>**

### **Statement**

Select all true statements.

### **Options**

**(a)**

**(b)**

**(c)**

- **(d)**

**(e)**

**(f)**

### **Answer**

(b), (d), (e)