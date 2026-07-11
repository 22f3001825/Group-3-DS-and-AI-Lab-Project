# **Practice**

This document has questions.

## **<u>Question-1</u>**

### **Statement**

You are given a training dataset of data-points for a classification task. You wish to use a - NN classifier, with . is a function that returns the Euclidean distance between two points and . Calling  an a pair of points corresponds to a single distance computation. If you want to predict the label of a new test point, how many distances would you have to compute?

### **Answer**

### **Solution**

We would have to compute distances: for .

## **Common Data for questions (2) to (3)**

### **Statement**

Consider the following data-points in a binary classification problem. is the weight vector corresponding to a linear classifier. The labels are and .

> **[Extracted Question]**
> T2
> X3
> X2
> XI
> X5
> T1
> X4

## **<u>Question-2</u>**

### **Statement**

What is the predicted label for these five points?

### **Options**

#### **(a)**

All five points are predicted as .

#### **(b)**

All five points are predicted as .

#### **(c)**

and are predicted as and are predicted as .

#### **(d)**

and are predicted as and are predicted as .

### **Answer**

(c)

### **Solution**

For a linear classifier with weight vector , the prediction for a test-point  is given by:

The geometric interpretation of this is as follows: a linear classifier divides the space into two halfspaces. This decision is made just by looking at the sign of the dot-product.

<u>Half-space-1: The dot-product is positive.</u>

This corresponds to those cases in which the data-point makes an acute angle with the weight vector.

<u>Half-space-2: The dot-product is non-positive.</u>

This corresponds to those cases in which the data-point makes either a right angle or an obtuse angle with the weight vector. When a point lies on the line (right angle with weight), it could be classified either way. As per convention, we choose .

## **<u>Question-3</u>**

### **Statement**

Which of the following statements are true?

### **Options**

#### **(a)**

#### **(b)**

#### **(c)**

#### **(d)**

#### **(e)**

### **Answer**

(a), (c), (e)

### **Solution**

The farther away a data-point is from the decision boundary, the larger the magnitude of its projection onto the weight vector. Hence:

Since all these three points lie on the positive half-plane, these dot products will be positive and we can remove the modulus sign. As for point , its projection on will be zero as it is orthogonal to it. Finally, will be negative as lies in the negative half-plane.

## **Comprehension Type (4 - 5)**

### **Statement**

Consider the following decision tree for a binary classification problem that has two features:

.

> **[Extracted Question]**
> X<3
> Yes
> No
> y > 2
> Yes
> No
> Yes
> No
> y < 4

**<u>Question-4</u>**

### **Statement**

Which of the following statements are true?

### **Options**

#### **(a)**

is classified as

#### **(b)**

is classified as

#### **(c)**

is classified as

#### **(d)**

is classified as

### **Answer**

(b), (d)

### **Solution**

Start at the root of the decision tree and keep traversing the internal nodes until you end up with a prediction/leaf node.

**<u>Question-5</u>**

### **Statement**

This decision tree partitions the feature space into four regions as shown below:

> **[Extracted Question]**
> R4
> R1
> R3
> R2
> 3

Assume that for all points. What can you say about the predicted labels of points that fall in the four regions?

### **Options**

#### **(a)**

> **[Extracted Question]**
> R1 : +
> R2
> R3
> +
> R4

#### **(b)**

> **[Extracted Question]**
> R1
> _
> R2
> +
> R3
> T
> Ra

#### **(c)**

> **[Extracted Question]**
> R1
> R2
> +
> R3
> Ra
> +l

**(d)**

> **[Extracted Question]**
> Ri : +3
> Rz
> +
> R:
> R4

### **Answer**

(b)

### **Solution**

The tree partitions the space into four regions: . These four regions correspond to the four leaves from left to right.

**<u>Question-6</u>**

### **Statement**

Consider the following training dataset for a binary classification task:

|x|y|
|---|---|
|2|1|
|10|0|
|8|0|
|-4|1|
|0|1|
|9|0|

<!-- Start of picture text -->
y<br><!-- End of picture text -->

<!-- Start of picture text -->
0<br><!-- End of picture text -->

<!-- Start of picture text -->
1<br><!-- End of picture text -->

<!-- Start of picture text -->
0<br><!-- End of picture text -->

The following decision tree cleanly separates the two classes, such that the resulting leaves are pure.

> **[Extracted Question]**
> Q-1
> Yes
> No

Q-1 is of the form . How many possible integer values can  take?

### **Answer**

### **Solution**

can take any one of the values from this set: . It can also take the value  as will go to the right branch for the data-point .

**<u>Question-7</u>**

### **Statement**

is the proportion of points with label in some leaf in a decision tree. For what values of  will this node be assigned a label of ? Select the most appropriate option.

### **Options**

#### **(a)**

#### **(b)**

#### **(c)**

### **Answer**

(b)

### **Solution**

In a vote, we need more points to belong to class  than class . Therefore,

**<u>Question-8</u>**

### **Statement**

is some internal node (question node) of a decision tree that splits into two leaf nodes (prediction nodes) and . The proportion of data-points belonging to class  in each of the three nodes is the same and is equal to . What is the information gain for the question corresponding to node ?

### **Answer**

### **Solution**

Let  be the proportion of ones in each node. Then, all three nodes have the same entropy as entropy only depends on . Call this . If  is the ratio into which the original dataset is partitioned by this question, then:

We gain nothing because of this split. Intuitively this makes sense because in both leaf nodes the status quo prevails. To put it in another way, none of the child nodes have become purer than the parent node. They have the same level of impurity as their parent.

**<u>Question-9</u>**

### **Statement**

Consider the following decision tree for a classification problem in which all the data-points are constrained to lie in the unit square in the first quadrant. That is, .

> **[Extracted Question]**
> xl < 0.5
> Yes
> No
> x2 > 0.5
> Yes
> No

If a point is picked at random from the unit square, what is the probability that the decision tree predicts this point as belonging to class ?

### **Answer**

Range: [0.74, 0.76]

### **Solution**

The decision regions will look as follows:

> **[Extracted Question]**
> 82
> 0.5
> 1
> 1
> 0.5
> x 1

We see that of the region belongs to class , hence the required probability is

.

**<u>Question-10</u>**

### **Statement**

Consider the following dataset. By visually inspecting the data-points, construct a decision tree.

### **Solution**

The structure of the data seems clear. There are four blobs of red and green points. From left to right, we have blob-1, blob-2, blob-3 and blob-4. They take the colors red, green, red and green respectively. Assume that the lines parallel to the y-axis that separate consecutive blobs are , and . Think about why we need only three lines. One tree that we could construct has the following form:

> **[Extracted Question]**
> X < 2
> Yes
> No
> Red
> X < 4
> Yes
> No
> Green
> X < 6
> Yes
> Red
> Green
> No

<!-- Start of picture text -->
x < 2<br>Yes No<br>Red x < 4<br>Yes No<br>Green x < 6<br>Yes No<br>Red Green<br><!-- End of picture text -->

**<u>Question-11</u>**

### **Statement**

is the entropy of a node.  is the proportion of points that belong to class .  is the proportion of points that belong to class . Which of the following statements is true?

### **Options**

#### **(a)**

#### **(b)**

#### **(c)**

#### **(d)**

Insufficient information. We need the number of data-points that are in this node.

### **Answer**

(c)

### **Solution**

We notice the symmetry in the entropy function about the axis . Therefore, :

Since , we have . So, for determining the impurity of a node, we could either use the proportion of ones or the proportion of zeros.

## **<u>Question-12</u>**

### **Statement**

The -NN algorithm can be adapted to perform regression giving us what is called the -NN regressor. Rather than looking at the majority vote among the  nearest neighbors, a -NN regressor computes the mean of the labels of the  nearest neighbors and returns this as the prediction. Consider the following dataset:

> **[Extracted Question]**
> (11,4,28.9)
> (2,2,1.8)
> 5,2,3
> (11,2,13.5)
> (1,1,0.6)
> (5,1,6.3)
> 12

All blue points belong to the training dataset. The annotation for each point should be understood as . What is the predicted label for the black test-point? Use .

### **Answer**

2.9 Range: [2.8, 3]

### **Solution**

The three nearest neighbors are:

> **[Extracted Question]**
> 5,
> (2

The prediction for the test-point is the average of the labels corresponding to these three points: