```

# **Clustering**

✉ 23f1001171@ds.study.iitm.ac.in (Piush Das)

### **Story So Far**

Given data points.

Find eigen directions with maximum variance.

Project proxies of the data points along the eigen direction.

But, by applying PCA on the given dataset Have we really understood the underlying structure in the data ? It is one thing to say that there is a linear subspace that has most of the information that is present in the data. But within the linear subpace there there may be more structure to be uncovered.

The shape of the dataset is d × n , where  is 2 and  is 8 d n

✉ 23f1001171@ds.study.iitm.ac.in (Piush Das)

##### **Input**

##### **Goal**

Partition the  datapoints into  different parts n k

##### **Example**

Partition the 5 (n) datapoints into 3 (k) different clusters

##### **Possible Clusters**

In general k<sup>n</sup> cluster possibilities are there

✉ 23f1001171@ds.study.iitm.ac.in (Piush Das)

##### **Notations**

Datapoints

Cluster Indicator

Each datapoint belongs to  cluster k

- L1 Norm  Manhattan Norm

- L2 Norm  Euclidean Norm

✉ 23f1001171@ds.study.iitm.ac.in (Piush Das)

##### **Question**

Given a cluster assignment how good is it ?

##### **Indicator Function**

##### **How to Calculate Cluster Mean**

for cluster  : k

✉ 23f1001171@ds.study.iitm.ac.in (Piush Das)

##### **Goal**

But too many possibilities ! kn Thus it is a NP Hard Problem

##### **Llyod's Algorithm (k - means)**

For this K means problem, Llyods algorithm is a solution

- Initialisation Randomly assign cluster indicator

Until convergence

#### 1. Compute Means ∀k

✉ 23f1001171@ds.study.iitm.ac.in (Piush Das)

#### 2. Reassignment Step ∀i

If the mean of the current assignment  is smallest, then donot re-assign

Fact: Llyods Algorithm Converges but the converged solution may not be the the optimal solution yet produces reasonable cluster in practice.

✉ 23f1001171@ds.study.iitm.ac.in (Piush Das)

##### **Convergence of K means Algorithm**

Lets say we are at iteration  of Llyods algorithm. t

Given, current cluster assignments :

mean of cluster  in assignment k t

Say we update our assignment

After the assignment has been made

✉ 23f1001171@ds.study.iitm.ac.in (Piush Das)

#### from (1) and (2) we got

This implies that the objective function strictly reduces after re-assignment

∵ There are only finite number of partitions at most kn and once a partition has been visited, it cannot be revisited. so eventually the algorithm has to converge surely (may be to local minima)

✉ 23f1001171@ds.study.iitm.ac.in (Piush Das)

##### **Nature of Clusters Produced**

Lets say K = 2

Llyods algorithm converges and produces two cluster with means 𝜇1 and 𝜇2

##### **What can we say about points assigned to the cluster ?**

By algorithm construction(for cluster 1)

‖x‖2 + ‖𝜇1‖2 - 2xT𝜇1 ⩽ ‖x‖2 + ‖𝜇2‖2 - 2xT𝜇2

✉ 23f1001171@ds.study.iitm.ac.in (Piush Das)

##### **For K = 3**

Cluster regions are intersection of half spaces known as voronoi region

✉ 23f1001171@ds.study.iitm.ac.in (Piush Das)

##### **Initialisation of centroids**

- Pick k-means uniformly at random from the dataset

- K means ++

K-means++ is an algorithm that provides a sounder initialization which results in some convergence guarantees. The algorithm is probabilistic in nature. We will describe the algorithm for k = 3

**Step-1:** Choose any of the  data-points as the first mean n 𝜇1 by sampling uniformly at random from {x1 , . . . , xn<sup>}</sup>

**Step-2:** Choose the second mean as one of the remaining data-points using this process

The score for each data-point is the squared distance:

✉ 23f1001171@ds.study.iitm.ac.in (Piush Das)

A probability distribution over the n-1 points. Recall that the summation starts from 2 since x1 has been chosen.

Sample a data-point using this distribution and assign it to 𝜇2 . For convenience, relabel the sampled point x2 . That is, if x5 is sampled, swap the labels and the scores for x2 and x5

**Step-3:** Choose the third mean as one of the remaining data-points using this process

d(xi , 𝜇j<sup>)</sup> = distance of datapoint xi from mean 𝜇j

The score for each data-point is the squared distance of the distance of xi to the closest mean :

✉ 23f1001171@ds.study.iitm.ac.in (Piush Das)

A probability distribution over the n-2 points. Recall that the summation starts from 3 since x1 and x2 has been chosen.

Sample a data-point using this distribution and assign it to 𝜇3 . For convenience, relabel the sampled point x3 . That is, if x7 is sampled, swap the labels and the scores for x3 and x7

The overall probability of choosing these three means in this order is the probability of the three probabilities we have computed so far. For K>3, the algorithm can be extended in a similar fashion.

k-means ++ is a computationally heavier but it is practically a solid way to initialize lloyds algorithm.

✉ 23f1001171@ds.study.iitm.ac.in (Piush Das)

##### **Choice of K**

k is a hyperparameter and must be chosen appropriately. A hyperparameter is different from a parameter in that it is not "learnt from data" but is chosen before the learning begins. One heuristic to choose a value of k is the elbow method.

The elbow method selects the optimal number of clusters  by plotting the within-cluster sum of squares (WCSS) against  and identifying the point k k where the rate of decrease sharply slows, forming an "elbow."

##### **when is the objective function optimal?**

We want k to be as small as possible , thus we penelize large values of k

✉ 23f1001171@ds.study.iitm.ac.in (Piush Das)

##### **Some Common Criterion As Well**

Akaike Information Criterion (AIC) and Bayesian Information Criterion (BIC) are used in K-means clustering to select the optimal number of clusters k by balancing model fit and complexity. Both are based on the log-likelihood of the data under a Gaussian mixture assumption and include a penalty term to discourage overfitting as  increases. AIC penalizes complexity with a constant factor, while BIC applies a stronger penalty based on the k number of data points. In K-means, for each , we compute the within-cluster sum of squares (WCSS), estimate the likelihood, and calculate AIC and k BIC scores. The optimal  is the one that minimizes these criteria, providing a statistically grounded alternative to heuristic methods like the elbow k method.

##### **Application of K-means**

The k-means algorithm has a wide range of applications across various domains.

- One of its primary uses is in customer segmentation, where companies divide their customers into groups based on common characteristics to target specific clusters for advertising campaigns.

- Another application is in document classification, where the algorithm is used to allocate various classes or categories to documents.

- Additionally, k-means clustering is used in recommendation engines, where it helps in recommending products or services to users based on their past purchases or preferences.

- In the field of image processing, k-means is applied for image segmentation, which involves dividing an image into different segments to identify specific objects, boundaries, or patterns.

- The algorithm is also utilized in the analysis of data sets, such as in the case of the Breast Cancer Wisconsin Diagnosis dataset, where it is used for classifying breast tumors as malignant or benign.

✉ 23f1001171@ds.study.iitm.ac.in (Piush Das)

## **Reference**

**_Arun Raj Kumar, Lecture Slides for Machine Learning Techniques Karthik Thiagarajan, Machine Learning Techniques Github Notes. Indian Institute of Technology Madras , CS2007 Course Website Stanford University, CS229 Machine Learning Notes_**

# **Thank You !**

✉ 23f1001171@ds.study.iitm.ac.in (Piush Das)