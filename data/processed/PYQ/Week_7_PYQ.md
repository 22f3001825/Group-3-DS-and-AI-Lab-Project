# <u>Week 7 K-Nearest Neighbours and Decision Tree</u> 

## January 2024 Term Quiz 2 

> **[Extracted Question]**
> Question 2 : 640653770919
> Total Mark : 0.00
> Type
> COMPREHENSION
> Based on the above data
> answer the given subquestions:
> Consider
> binary classification problem with
> training dataset of
> 80 points, evenlv distributed between two classes
> (40
> in each class).
> You decide t0 train
> k-NN
> algorithm with k = 3
> Each point is considered its own neighbor
> classification.
> Discussions (0)
> Question 3 : 640653770920
> View Parent QN
> View Solutions (1)
> Total Mark
> 3.00
> Type
> What iS the minimm number of
> misclassifications that can OCcur
> in the
> training dataset when
> this k-NN algorithm?
> Answer (Numeric):
> Answer
> points
> during
> using

## Solution 

The k-NN algorithm (k = 3) classifies a point based on the majority vote of its three nearest neighbors, including itself. Since the dataset is evenly distributed and well-separated, each point will have at least two nearest neighbors from the same class, ensuring correct classification. Therefore, the minimum number of misclassifications is 0 

> **[Extracted Question]**
> Question 4 : 640653770921
> View Parent QN
> View Solutions (1)
> Total Mark
> 2.00
> Iype
> Assuming there are outliers, the decision
> boundary becomes smoother with increasing
> Value of k in
> k-NN algorithm (Fill in
> for yes and 0 for HlO)
> Answer (Numeric):
> Answer

## Solution 

We know, In the k-Nearest Neighbors (k-NN) algorithm, the decision boundary is influenced by the value of , Since increasing  leads to a smoother decision boundary, the answer should be k k 1 

> **[Extracted Question]**
> Question 18
> 640653770912
> View Solutions (0)
> Total Mark
> 4.00
> Type
> MCQ
> The
> training dataset for
> binary classification problem is &s follows:
> (u.1) .
> (-2u,0) .
> (3u.1) .
> (-4u.0) }
> where u € Rd is & constant, and the labels belong to 0,1.
> be the weight vector of
> linear classifier. What condition should the weight vector satisfy for the zero-one loss
> to be zero on this dataset?
> OPTIONS ;
> wTu < 0
> wTu > 0
> Wlu = 0
> We can never find a W for which the zero-one loss becomes zero on this dataset_
> Let `

## Solution 

for coefficient (u , 3u), the solution will be 1 - - for coefficient ( 2u , 4u), the solution will be 0 T T T w (u) > 0 , w (3u) > 0 ⟹ if k > 0 , w ku > 0 wT(-2u) < 0 , wT(-4u) < 0 ⟹ if k < 0 , wTku < 0 ⟹ k > 0 , wTku > 0 

> **[Extracted Question]**
> Question 19 : 640653770913
> View Solutions (0)
> Total Mark
> 400
> Type
> MSQ
> Consider the following data-points in
> binary classification problem; w is the weight vector corresponding to
> linear classifier The labels are +1 and -1. Which of the
> following statements are true?
> OPTIONS :
> 00 < wTxi < wx2 < wX}
> OwTx = 0
> <wTxe < WX1
> W" X?
> Owlis < 0
> T3 < 0
> Owl ,

Solution 

## (a) , (b) , (d) 

> **[Extracted Question]**
> Question 20 : 640653770914
> View Solutions (0)
> Total Mark
> 4.00
> Type
> MSQ
> Select all true statements
> OPTIONS :
> In Decision tree, ifa question Q1 is "better"
> question Q.
> information
> gains for Q1 is greater than information
> Qe always.
> The training dataset is required while predlicting the label of a test-
> the k-NN algorithm.
> question of the form f < 0 always partitions the dataset into two non-empty
> sels.
> The depth of the tree iS
> hyperparameter and has to be chosen
> CTOSS
> Falidation;
> 0Decision trees are prone t0 overfit if the maximum depth is set too
> thau 
> then
> gains
> point
> using
> low.

## Solution 

1. In Decision tree, if a question  is “better” than question , then information gains for  is greater than information gains  always. This aligns with the definition of “better” in the context of decision trees, where splits are chosen based on maximizing information gain. 

2. The training dataset is required while predicting the label of a test-point in the k-NN algorithm.The k-Nearest Neighbors (k-NN) algorithm requires the entire training dataset during prediction to calculate distances and find the nearest neighbors. 

3. A question of the form fk ⩽ 𝜃 always partitions the dataset into two non-empty sets. It is only possible for such a question to result in one empty set if all data points fall on one side of the threshold. 

**4.** The depth of the tree is a hyperparameter and has to be chosen using crossvalidation. The maximum depth of a decision tree is indeed a hyperparameter that controls overfitting and underfitting, and it is typically tuned using cross-validation. 

5. Decision trees are prone to overfit if the maximum depth is set too low.Decision trees are prone to underfitting, not overfitting, when the maximum depth is set too low because they cannot capture sufficient complexity in the data. 

May 2024 Term Quiz 2 

> **[Extracted Question]**
> Question 2
> 640653852823
> View Solutions (1)
> Total Mark
> 3.00
> Type
> MSQ
> Which of the following classifiers are certainly
> of achieving zero training
> error for any binary classification problem with features in R2? Note: while computing
> the
> cFTOT
> for KNN, each data-point is its Own neighbor.
> OPTIONS
> ODecision tree
> OKNN with k = 1
> OKNN with k = 5
> ONaive Bayes
> capable ,
> training

## Solution 

1. Decision Tree - A decision tree can achieve zero training error because it can perfectly split the data by creating partitions on the feature space to classify every training point correctly. Hence, this option is correct. 

2. KNN with k = 1 - When , the K-Nearest Neighbors (KNN) algorithm assigns the label of the nearest neighbor to each data point. Since each data point is its own neighbor, KNN with  will always classify training points correctly, resulting in zero training error. Hence, this option is correct. 

3. KNN with k = 5 - When , the classification depends on the majority label among the 5 nearest neighbors. For some datasets, this may not result in zero training error because a point’s label might differ from the majority label of its neighbors. Hence, this option is incorrect. 

4. Naive Bayes - Naive Bayes assumes feature independence and uses probabilistic modeling. It cannot guarantee zero training error for all binary classification problems because its assumptions might not hold true for all datasets. Hence, this option is incorrect. 

> **[Extracted Question]**
> Question 5
> 640653852826
> View Solutions (0)
> Total Mark : 3.00
> Type
> SA
> Consider the following decision boundary obtained for a decision tree trained
> On a
> dataset in R? for & binary classification problem. All green points (label 1) lie inside
> the box and the red
> points (label 0) are outside it.
> What it is the minimum depth of
> this tree?
> Recall that the depth is the number of edges
> On
> the longest
> from the
> root t0
> leaf:
> Legend
> Answer (Numeric):
> Answer
> path

## Solution 

2 x 3 = 6 

In d-dimensional space, a hyperectangle is defined by 2 splits per dimension. Each dimension requires 2 splits, the total number of splits required is Minimum Depth = 2d 

> **[Extracted Question]**
> Question 18
> 640653852839
> Total Mark
> 0.00
> Type
> COMPREHENSION
> If a and b are integers, answer the given subquestions that follow: Hint: Plotting the dataset helps:
> Consider the following training dataset for & binary classification problem with the data-
> points in R?, the labels in the set {0, 1} and a decision tree grown from it that achieves
> zero
> error:
> 12
> ~0.9
> 0.9
> 52
> ~0.9
> 0.9
> x=[
> 1
> 0.9
> 0.9
> -[
> ~0.9
> ~0.9
> T
> 1
> 81 < a
> y=[1 1 0 0 0 0 1 1]7
> Yes
> No
> T2 < b
> 12
> T2
> Yes
> No
> Yes
> No
> training

Solution 

> **[Extracted Question]**
> Question 19
> 640653852840
> 0 View Parent QN
> View Solutions (0)
> Total Mark : 1.00 | Type
> SA
> What is the value of a?
> Answer (Numeric):
> Answer

## Solution 

> **[Extracted Question]**
> Question 20
> 640653852841
> View Parent QN
> View Solutions (0)
> Total Mark
> 1.00 | Type
> SA
> What is the value of b?
> Answer (Numeric):
> Answer

## Solution 

> **[Extracted Question]**
> Question 21
> 640653852842
> 6 View Parent QN
> View Solutions (0)
> Total Mark : 1.00
> Type
> SA
> Find the entropy of the root node: Use log2_
> Answer (Numeric):
> Answer

Solution 

Entrophy(p) = - (p logp + 1( - p) log 1( - p)) 

4 here, p =  = 0.5 8 

we know when p = 0.5 , impurity = 1 

> **[Extracted Question]**
> Question 22 : 640653852843
> Parent QN
> View Solutions (0)
> Total Mark
> 2.00 | Type
> SA
> If ER is the entropy of the root and EL
> is the weighted entropy of all the leaves,
> what is ER
> EL? Use
> Answer (Numeric):
> Answer
> View '
> log2"

## Solution 

> **[Extracted Question]**
> Question 23
> 640653852844
> 6 View Parent QN
> View Solutions (0)
> Total Mark : 1.00
> Type : SA
> What is the predicted label of
> the test data-point
> Answer (Numeric):
> Answer

## Solution 

September 2024 Quiz 2 

> **[Extracted Question]**
> Question 9
> 6406531021036
> View Solutions (0)
> Total Mark
> 4.00
> Type
> SA
> Consider the following feature vectors in R?:
> Ti
> T2
> T3
> Ti =
> B: ~-[4
> 3
> The labels of these points are:
> 91 = 0,
> 92 = 1,
> Y3 = 1,
> Y4 = 0,
> Ys = [
> If
> we
> use
> k-NN algorithm with k
> = 3
> what  would be the predicted label  for the
> following test
> Ctest
> Answer (Numeric):
> Answer
> point:

## Solution 

> **[Extracted Question]**
> d(x1
> Xtest_
> =d
> 2
> V2
> 1.41
> 3
> Xtest_
> 4.12
> d(x3
> Xtest_
> d
> Hl
> 2.45
> d(x4 _
> Xtest)
> =d
> 2.24
> d(x5 _
> Xtest)
> =d
> -1
> 5.48
> -3
> AIVL
> Id(x2 _

for k = 3, 

three closest distance from xtest 

x1 with label 0 , x3 with label 1 , x4 with label 0 

∴ predicted label for xtest is 0 

> **[Extracted Question]**
> Question 11 : 6406531021037
> View Solutions (0)
> Total Mark
> 4.00
> Type
> MSQ
> Select all true statements
> OPTIONS
> In Decision
> if &
> question Q1 is
> better" than question Q2; then information
> for Q1 is greater than information
> Q2 always:
> The
> dataset is not required while predicting the label of a test-point in the
> k-NN algorithm:
> A question of the form fk <
> always partitions the dataset into two non-empty
> sets
> The depth of the tree is a hyperparameter and has to be chosen
> cross validation.
> Decision trees are prone to underfit if the maximum depth is set too low.
> treC .
> gains
> gains
> training
> using

## Solution 

1. In Decision tree, if a question  is “better” than question , then information gains for  is greater than information gains  always. This aligns with the definition of “better” in the context of decision trees, where splits are chosen based on maximizing information gain. 

2. The training dataset is required while predicting the label of a test-point in the k-NN algorithm.The k-Nearest Neighbors (k-NN) algorithm requires the entire training dataset during prediction to calculate distances and find the nearest neighbors. 

3.  A question of the form  always partitions the dataset into two non-empty sets.It is possible for such a question to result in one empty set if all data points fall on one side of the threshold . 

**4.** The depth of the tree is a hyperparameter and has to be chosen using crossvalidation. The maximum depth of a decision tree is indeed a hyperparameter that controls overfitting and underfitting, and it is typically tuned using cross-validation. 

5. Decision trees are prone to overfit if the maximum depth is set too low.Decision trees are prone to underfitting, not overfitting, when the maximum depth is set too low because they cannot capture sufficient complexity in the data. 

> **[Extracted Question]**
> Question 12 : 6406531021038
> Total Mark
> 0.00
> Type
> COMPREHENSION
> Consider
> binary classification problem with
> training dataset of 100 points, evenly distributed between
> two classes (50 points in each class) You decide to train
> a k-NN algorithm with
> 3. Each point is
> considered its own neighbor during classification:
> Based on the above data, answer the given subquestions_
> Discussions (0)
> Question 13 : 6406531021039
> View Parent QN
> View Solutions (0)
> Total Mark
> 3.00
> Type
> SA
> What is the minimum number of misclassifications that can occur in the training dataset when using this
> k-NN algorithm?
> Answer (Numeric):
> Answer

## Solution 

The k-NN algorithm (k = 3) classifies a point based on the majority vote of its three nearest neighbors, including itself. Since the dataset is evenly distributed and well-separated, each point will have at least two nearest neighbors from the same class, ensuring correct classification. Therefore, the minimum number of misclassifications is 0 

> **[Extracted Question]**
> Question 14 : 6406531021040
> 6 View Parent QN
> View Solutions (0)
> Total Mark
> 2.00
> Type
> MCQ
> Assuming there are outliers, the decision boundary becomes smoother with decreasing value of k
> in a k-NN algorithm:
> OPTIONS
> TRUE
> FALSE

## Solution 

We know, In the k-Nearest Neighbors (k-NN) algorithm, the decision boundary is influenced by the value of , Since increasing  leads to a smoother decision boundary, the answer should be k k False. 

> **[Extracted Question]**
> Question 18
> 6406531021041
> Total Mark
> 0.00
> Type
> COMPREHENSION
> Consider
> binary classification problem in which
> a decision tree is classifying data points into two
> classes, A and B.
> In
> particular node of the tree, 60% of the data points belong to class A, while the
> remaining 40% belong to class B.
> Based on the above data, answer the given subquestions_
> Discussions (0)
> Question 19
> 6406531021042
> 6 View Parent QN
> View Solutions (0)
> Total Mark
> 2.00 | Type
> MCQ
> Do you have enough information to find the entropy of this node?
> OPTIONS
> Yes
> No

Solution 

A = 0.6 B = 0.4 

> **[Extracted Question]**
> Question 20
> 6406531021043
> 0 View Parent QN
> View Solutions (0)
> Total Mark
> 4.00 | Type
> SA
> If the answer to the previous question is "Yes;" calculate the entropy of this node to three decimal places
> If the answer to the previous question is "No;" enter -1as your answer:
> Answer (Numeric):
> Answer

## Solution 

Entrophy(p) = - (p log2p + 1( - p) log2 1<sup>(</sup> - p)) = - 0.6 × ( log2<sup>(</sup> 0.6 + 0.4 × ) log2<sup>(</sup> 0.4)) 

= 0.971