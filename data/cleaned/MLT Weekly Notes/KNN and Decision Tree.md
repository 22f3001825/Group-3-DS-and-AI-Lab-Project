# KNN and Decison Tree

✉ 23f1001171@ds.study.iitm.ac.in (Piush Das)

## Introduction To Binary Classification

Binary classification is a fundamental task in machine learning, commonly employed in various domains such as computer vision, natural language processing,

and bioinformatics. Its objective is to assign objects into one of two categories based on their features.

Input

Label

Goal

Zero-One Loss

This is the average number of errors in prediction by the classifier

✉ 23f1001171@ds.study.iitm.ac.in (Piush Das)

Linear Classifier

n<br>min 1(h(xi) ≠ yi )<br>h ∈ Hlinear ∑<br>i = 1<br>T<br>Hlinear =  hw : h(x) = sign w x<br>1, if z > 0<br>sign(z) =<br>0 , otherwise<br>

The optimization problem given below is NP hard

✉ 23f1001171@ds.study.iitm.ac.in (Piush Das)

### Using Linear Regression To Solve Classification Problem ?

Using the SSE for classification is not a good idea. The SSE is sensitive to outliers,it becomes evident that linear regression-based classification not only separates the two categories based on their respective sides but also considers their positions. As a consequence, the classification boundary may shift with respect to the outliers in the dataset. Hence, this approach is not suitable for binary classification.

## K-Nearest Neighbours Algorithm

The K-Nearest Neighbors (K-NN) algorithm is a widely-used non-parametric method utilized for both classification and regression tasks in machine learning. It operates by identifying the K-nearest data points to the target object and classifying or regressing the target object based on the majority of its nearest neighbors. The algorithm follows these steps:

### Issue ?

Can get affected by outliers(lets a negative datapoint among positive datapoint cluster)

### Fix ?

Ask more neighbours before prediction

### How Many Neigbours ?

As  increases, the model becomes less k flexible,smaller the value of , complicated the decision boundary. k Thus,Choosing  is a hyper-parameter, thus cross validate for kk

✉ 23f1001171@ds.study.iitm.ac.in (Piush Das)

If K = 1, the classification is highly sensitive to outliers leading to overfitting If K = n, the classification becomes overly smooth leading to underfitting

### Issues With KNN?

- The choice of distance function can yield different results. The Euclidean distance, commonly used, might not always be the best fit for all scenarios.

- Computationally, the algorithm can be demanding. When making predictions for a single test data point, the distances between that data point and all training points must be calculated and sorted.

- The algorithm does not learn a model but instead relies on the training dataset for making predictions.

✉ 23f1001171@ds.study.iitm.ac.in (Piush Das)

## Introduction to Decision Tree

Decision trees are widely used in machine learning for classification and regression tasks. They operate by recursively partitioning the data based on the most informative features until a stopping criterion is met. Decision trees can be visualized as tree-like structures.

### Input

### Output

Parent / Root Node<br>Internal Node<br>Prediction/Leaf Node<br>

### Prediction

Given a datapoint xtest, traverse through the tree to reach a leaf node. ytest = value in the leaf node

✉ 23f1001171@ds.study.iitm.ac.in (Piush Das)

### Question

Question is a (feature,value) pair. To measure the "Goodness of a Question", we need a measure of “impurity” for a set of labels {y1 , y2 , . . . . , yn<sup>}</sup> , we will use Entrophy function to measure the impurity.

Entrophy(p) = - (p logp + 1( - p) log 1( - p)) n <u>p</u> here, p = n

Pictorial representation of the Entropy function

- Measure of impurity is highest when p =<sup>1</sup> 2

- Measure of impurity is 0 when p = 0 or 1

✉ 23f1001171@ds.study.iitm.ac.in (Piush Das)

Information Gain is then utilized to measure the quality of a split in the decision tree algorithm.

Information gain is a commonly used criterion in decision tree algorithms that quantifies the reduction in entropy or impurity of a dataset after splitting based on a given feature. High information gain signifies features that effectively differentiate between the different classes of data and lead to accurate predictions. Information gain is calculated as

D<br>Dyes Dno<br>

## Decision Tree Algorithm

### The decision tree algorithm follows these steps:

1. Discretize each feature within the range [min, max].

2. Select the question that provides the highest information gain.

3. Repeat the procedure for subsets Dyes and Dno.

### Points to Remember

- “ ”

- • Stop growing the tree when a node becomes sufficiently pure

- Depth of tree (The number of edges on the longest path from the root to a leaf) is a hyper parameter.

- Different measures, such as the Gini Index, can also be employed to evaluate the quality of a question.

✉ 23f1001171@ds.study.iitm.ac.in (Piush Das)

### Decision Boundary

In general, boundaries of the regions are parallel to the axes

## Advantages and Disadvantages

### Advantages

- Shallow trees are interpretable

- Easy to implement

### Disadvantages

- Simple model with low predictive power.

- Deep trees have high variance, i.e; small changes to the training data result in big changes in the resulting tree.

✉ 23f1001171@ds.study.iitm.ac.in (Piush Das)

## Reference

Arun Raj Kumar, Lecture Slides for Machine Learning Techniques Karthik Thiagarajan, Machine Learning Techniques Github Notes. Indian Institute of Technology Madras , CS2007 Course Website Stanford University, CS229 Machine Learning Notes

# **Thank You !**

✉ 23f1001171@ds.study.iitm.ac.in (Piush Das)