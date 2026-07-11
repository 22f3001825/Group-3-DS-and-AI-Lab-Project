aWeek-3Karthik Thiagarajan[1. Clustering](#n0.3355767526845632) [2. Cluster Membership and Cluster Centers](#n0.04997654126566753) [3. Optimization problem](#n0.28983850939904054) [4. LLoyd's Algorithm (K-means)](#n0.30765984678796743) [5. Convergence](#n0.4984997939580812) [6. (\*) Proof of Convergence](#n0.7617188065699214) [7. Nature of Clusters](#n0.193803854193501) [8. Other considerations](#n0.7965703994848783) [9. Towards Better Initialization: K-means++](#n0.013841334437350028) Starred (\*) section may be mathematically heavy. Handle with care.1. Clustering Continuing with our study of unsupervised learning, we turn to another approach to understand the data: clustering. The basic idea in clustering is to find groups of data-points that are tightly knit together and well separated from other such groupings. We call each group a cluster. A common use case of clustering is market segmentation; for example, it can be used to identify different "clusters" of customers based on their behavior on an e-commerce platform. Once we have these clusters, companies can then perform targeted interventions for different groups. An example of a dataset from the wild that shows clusterable patterns is the [Old Faithful](https://en.wikipedia.org/wiki/Old_Faithful) dataset (Bishop, Pg 681). From the scatter plot, it is clear that there are two distinct groups/clusters.Among the several clustering algorithms in the literature, we will take up K-means clustering, a simple yet effective technique to identify clusters. As in the case of linear PCA, K-means is not a panacea for all our clustering problems. Its effectiveness is closely tied to the existence of specific patterns in the dataset. 2. Cluster Membership and Cluster Centers The basic assumption in K-means is the presence of K points or centers that act as representatives for the K clusters in the dataset. For example, in the dataset given below, K=3 and the three red points denote the cluster centers. (1)(2)(3)xiEach point is assigned to one of the three clusters. The assignment is indicated with the help of a cluster-membership variable, zi. The data-point xi is assigned to cluster zi, where zi∈{1,⋯,K}. In the above image, zi=2 for the data-point xi. In general, we can form a cluster-membership vector of size n: z=a

|  |
| --- |
| z1 |
| ⋮ |
| zn |

wherez∈{1,⋯,K}n The total number of distinct cluster assignments possible is Kn. To see why, note that each point can be assigned to one of the K clusters and by the multiplication rule, the result follows: K×⋯×K⏠⏣⏣⏣⏡⏣⏣⏣⏢n points=Kn It is often convenient to use the indicator function in our computations. Recall that the indicator function I[⋅] is given by: I(condition)=a

|  |  |  |
| --- | --- | --- |
| 1, |  | condition is true |
| 0, |  | condition is false |

 The mean of cluster-k can be computed as the average of all the points that are assigned to it. Denoted as 𝜇k∈Rd, we have: 𝜇k=n∑i=1I(zi=k)⋅xin∑i=1I(zi=k) 3. Optimization problem So far we have assumed that data-points are magically grouped into their respective clusters. But how do we know if a particular grouping is good? For instance, consider these two groupings of the same dataset. Which one is better? Visually, the one on the left clearly feels better. How do we quantify this? We would like points within a group to be tightly knit. That is, the distance of points in a group to their mean must be as small as possible. We will pursue this idea now. Distance of xi to the mean of the cluster zi to which it is assigned is given by: ||xi-𝜇zi|| The diagram below illustrates this. 𝜇zixi||xi-𝜇zi|| Extending this to all the n points and replacing the distance with the squared distance for mathematical convenience, we have: f(z)=n∑i=1||xi-𝜇zi||2 We can equivalently express this function as: f(z)=K∑k=1n∑i=1I[zi=k]⋅||xi-𝜇k||2 The function f captures intra-cluster distances. That is, the closeness of data-points to their cluster centers. It says nothing about the separation between two clusters or the distance of a point from a neighboring cluster. One can also view f(z) as the sum of the (scaled) variances (spread) of points from their cluster centers. However, the variance plays a different role here when compared to PCA. In PCA, we interpreted variance as the information content and tried to maximize it along a direction. Here, we treat variance as a measure of dispersal and try to find a configuration that minimizes it. The task before us is to choose a cluster configuration that minimizes f: 

min

z∈{1,⋯,K}n f(z) The variable for optimization is the n dimensional vector z. However, each zi is some integer from 1 to K. The search space is combinatorial and hence this problem can be very hard to optimize exactly. If we were to use a brute force algorithm to evaluate each possible cluster configuration, we would have to search through Kn configurations. The number of configurations blows up combinatorially as n increases. 4. LLoyd's Algorithm (K-means) Lloyd's algorithm or the K-means algorithm is an iterative approach that gives a reasonably good approximate solution to the problem. The algorithm starts with random cluster initializations for the n points. We denote the random initialization by z(0)∈{1,⋯,K}n. The superscript denotes the iteration counter which starts at 0. z(0)=a

|  |
| --- |
| z(0)1 |
| | |
| z(0)n |

 Then, we alternate between two steps repeatedly. The first step computes the mean of the clusters: 𝜇(t)k=n∑i=1I[z(t)i=k]⋅xin∑i=1I[z(t)i=k] Here, 𝜇(t)k is the mean computed in the tth iteration. Once we have the means, we update the cluster assignments: z(t+1)i=

argmin

k∈{1,⋯,K} ||xi-𝜇(t)k||2 Fortunately, we don't have to repeat this process indefinitely. This process converges after a finite number of iterations. When the cluster assignments do not change from one iteration to the next, we claim that the algorithm has converged. Formally, the algorithm converges in T iterations if and only if: z(T)=z(T-1)⟹convergence The entire algorithm is given below: a

|  |  |
| --- | --- |
|  | K-Means(X,K) |
| 1 | z(0)←initialize(X,K) |
| 2 | do |
| 3 | 𝜇(t)1,⋯,𝜇(t)K←updateMeans(X,z(t)) |
| 4 | z(t+1)←reassignClusters(X,z(t),𝜇(t)) |
| 5 | while z(t+1)≠z(t) |
| 6 | return 𝜇(t)1,⋯,𝜇(t)K |

 The reader may be unfamiliar with the [do-while](https://en.wikipedia.org/wiki/Loop_(statement)#Post-test_loop) loop construct. A do-while loop is slightly different from a while loop in that the condition is checked at the end of each iteration after executing the body rather than at the beginning. In this way, the body of the loop runs at least once.  Moving on, here is a quick summary of the two main objects that get updated in the loop in every iteration: • 𝜇(t)– mean of clusters corresponding to assignment z(t)– gets updated at the beginning of iteration t • z(t+1)– cluster assignment corresponding to centers 𝜇(t)– gets updated at the end of iteration t 

Remark: While computing z(t+1)i, in the case of a tie between multiple clusters for xi, where z(t)i is one of the candidates in the tie, set z(t+1)i:=z(t)i. That is, do not shift allegiance. If it ain't broke, don't try to fix it. More on this in the section titled "Other Considerations".

 Here is the same algorithm highlighting the main steps: 

Initialize z(0)=a

|  |
| --- |
| z(0)1 |
| | |
| z(0)n |

 random Until convergence, run Update Means 𝜇(t)k=n∑i=1I[z(t)i=k]xin∑i=1I[z(t)i=k] Reassign Clusters z(t+1)i=

argmin

k∈{1,⋯,K} ||xi-𝜇(t)k||2

 If the algorithm converges in T iterations, then here is a quick look at how the superscripts change from one iteration to the next z(0)→𝜇(0)k→z(1)⏠⏣⏣⏣⏡⏣⏣⏣⏢(1)→𝜇(1)k→z(2)⏠⏣⏣⏣⏡⏣⏣⏣⏢(2)→⋯ →𝜇(T-2)k→z(T-1)⏠⏣⏣⏣⏣⏡⏣⏣⏣⏣⏢(T-1)→

𝜇(T-1)k

→z(T)⏠⏣⏣⏣⏣⏡⏣⏣⏣⏣⏢(T) We make the following observations: • T⩾1, that is, the algorithm has to run for at least one iteration, no matter what the input. • The means/centers are updated T times. It goes from 𝜇(0) to 𝜇(T-1). The mean returned is 𝜇(T-1). • The points are reassigned T times. It goes from z(1) to z(T). The final assignment is z(T). Note that z(T) is equal to z(T-1), which is the reason the algorithm terminated at this step. Also note that z(0) doesn't count as a reassignment. It is the initial assignment. 5. Convergence Lloyd's algorithm converges. There are two reasons that work in tandem to make this possible: • The value of the objective function strictly decreases from one iteration to the next as long as z(t)≠z(t+1). That is, if z(t)≠z(t+1), then f(z(t))>f(z(t+1)). • The number of cluster configurations is finite, namely, Kn. If we put the two facts together, we conclude that no two cluster configurations can repeat. Since there are only a finite number of configurations, we can't see new configurations indefinitely. So at some point two consecutive configurations have to be identical. Once we have z(t)=z(t+1), there is no point in continuing the algorithm and we declare convergence. The next section provides a rigorous argument for why this is true. 6. (\*) Proof of Convergence We return to the objective function. Earlier, we had represented it as f(z). We will now change it slightly to include the means: f(z,𝜇)=n∑i=1||xi-𝜇zi||2 We need to track the value of f after each iteration. More precisely, we track the following update: f(z(t),𝜇(t))→f(z(t+1),𝜇(t+1)) We can break this further by looking at the following sequence: f(z(t),𝜇(t))→f(z(t+1),𝜇(t))→f(z(t+1),𝜇(t+1)) We now have the key result below: 

Theorem: If z(t+1)≠z(t), then the following inequality holds: f(z(t),𝜇(t))>f(z(t+1),𝜇(t))⩾f(z(t+1),𝜇(t+1)) In particular, if z(t+1)≠z(t), then f(z(t),𝜇(t))>f(z(t+1),𝜇(t+1)). In simple terms, the objective function's value strictly decreases from one iteration to the next.

 To prove this, first consider the pair f(z(t),𝜇(t))→f(z(t+1),𝜇(t)). This transition corresponds to the reassignment step. Since z(t+1)≠z(t), we have at least one point xi for which z(t+1)i≠z(t)i. That is, this point got reassigned since it is closer to cluster z(t+1)i than to cluster z(t)i, which in turn means: ||xi-𝜇(t)z(t+1)i||2<||xi-𝜇(t)z(t)i||2 From this, it follows that f(z(t),𝜇(t))>f(z(t+1),𝜇(t)). Now for the second transition, f(z(t+1),𝜇(t))→f(z(t+1),𝜇(t+1)). This corresponds to the update of the means. In this step, the assignment stays fixed, only the means change. That is, the points assigned to cluster k remain the same, only the position of the mean changes. Consider the following diagram: 𝜇(t)k𝜇(t+1)k 𝜇(t+1)k is the mean of the data-points assigned to it. The claim is that the points are closer to 𝜇(t+1)k, their mean, than to 𝜇(t)k, which may or may not be their mean now that a reassignment has happened. The following lemma shows this. 

Lemma: If {x1,⋯,xn} is a set of points, then the point that is closest to the dataset in a "sum of squared distances" sense is the mean of the data-points. In other words: p\*=

argmin

p n∑i=1||xi-p||2⟹p\*=1nn∑i=1xiProof: Let the objective be g(p): a

|  |  |
| --- | --- |
| g(p) | =n∑i=1||xi-p||2 |
|  | =n∑i=1||xi||2+||p||2-2(xTip) |

 We can differentiate the objective: a

|  |  |
| --- | --- |
| ∇g(p) | =n∑i=1[2p-2xi] |
|  |  |
|  | =2[np-n∑i=1xi] |

 Setting it to zero, we get: p\*=1nn∑i=1xi

 So we see that f(z(t+1),𝜇(t))⩾f(z(t+1),𝜇(t+1)). The original result now follows: f(z(t),𝜇(t))>f(z(t+1),𝜇(t))⩾f(z(t+1),𝜇(t+1)) 7. Nature of Clusters Let us start with two clusters and identify the regions into which the plane is divided by the two cluster centers. The line perpendicular to the dotted line joining the two means and passing through its mid-point is the perpendicular bisector and is the boundary between the two regions.𝜇2𝜇112wTx+b=0S1={x:wTx+b⩾0}S2={x:wTx+b<0} During inference, any point falling in region 1 would belong to cluster-1 and the points falling in region 2 would belong to cluster-2. These two regions are called half-spaces.  The equation of the boundary separating the two cluster regions is given by the hyperplane, wTx+b=0. Why is this true? Any point on the boundary is equidistant from both cluster centers: a

|  |  |  |
| --- | --- | --- |
|  | ||x-𝜇1||2 | =||x-𝜇2||2 |
|  |  |  |
| ⟹ | ||x||2+||𝜇1||2-2(xT𝜇1) | =||x||2+||𝜇2||2-2(xT𝜇2) |
|  |  |  |
| ⟹ | (𝜇2-𝜇1)Tx+1  2[||𝜇1||2-||𝜇2||2] | =0 |

 Setting w=𝜇2-𝜇1 and b=12[||𝜇1||2-||𝜇2||2], we get the desired form. Note that this separating plane passes through the mid-point of the line segment joining the means, 𝜇1+𝜇22, and is perpendicular to 𝜇2-𝜇1 [this is the perpendicular bisector]. Extending this to three clusters, we get the following diagram: 𝜇2𝜇112𝜇333To get the region corresponding to each cluster, we intersect two half-spaces. The resulting regions after removing the dotted lines looks like this: 𝜇2𝜇112𝜇33 These are called Voronoi regions. Each "cell" that is formed is a convex set. In general, if there are K clusters: • Each cell is formed by the intersection of K-1 half-spaces, obtained by comparing one cluster with the remaining K-1 clusters.•  • The cell that is formed in this manner is convex since:– half-spaces are convex sets– the intersection of convex sets is convex 8. Other considerations • Lloyd's algorithm is deterministic. Given an initial cluster assignment, it will always return the same final clusters.•  • The number of clusters, K, is a hyperparameter and must be chosen appropriately. A hyperparameter is different from a parameter in that it is not "learnt from data" but is chosen before the learning begins. One heuristic to choose a value of K is the [elbow method](https://en.wikipedia.org/wiki/Elbow_method_(clustering)).•  • Initialization plays a key role in obtaining good clusters. Pathological initialization could lead to very poor clusters. In practice, for a given K, multiple runs of K-means with different initializations are performed. The run which yields the smallest objective function value is chosen. We discuss two possible initializations:•  – Initialize z(0)i randomly for each point. That is, for each point, pick a value from 1 to K at random.–  – Randomly choose k data-points from the dataset as the k initial means. Here, we bypass the z(0)i step and directly assign 𝜇(0)j.–  – Both are valid initializations. In our course, we will follow the first method for vanilla K-means and a variant of the second method when we discuss K-means++ in the next section.–  • There are a couple of edge cases:– The first one has to do with the update step. A cluster could become empty at some stage in the algorithm. For example, consider eight points with k=5 with the following initial configuration: (1)(1)(1)(1)(2)(3)(4)(5)•  – After the first iteration, one of the clusters has the origin as its mean. In the next iteration, none of the points will be assigned to this cluster. Therefore, this cluster will remain empty for that iteration. Once a cluster becomes empty, we can drop it from the rest of the algorithm with impunity.–  – Another edge case is when there is a tie during the assignment step. For example, consider a data-point xi for which there are two clusters closest to it at time step t, say 1,3. So should z(t)i=1 or z(t)i=3? If z(t-1)i=1, then retain z(t)i=1. That is, if the old assignment is one of the members of the set of closest clusters, do not disturb that. However, if z(t-1)i∉{1,3}, then we are at liberty to choose either 1 or 3 for z(t)i. In this case, choose the smaller of the two, so z(t)i=1. This is done for the sake of consistency and to retain the deterministic character of Lloyd's algorithm for a given initialization. 9. Towards Better Initialization: K-means++ Let us now turn to the question of the effect of initialization on the clusters formed. Here, we choose data-points as the initial means randomly. Consider the following dataset in R:aabNow, consider the ideal initialization given below along with the resulting clusters: An alternative initialization The resulting clustering is:

Remark: This is true when a/b is sufficiently large. One can show that a/b>3 produces this clustering.

 This is clearly a sub-optimal clustering. The main reason is the poor choice of initial clusters centers. Choosing all three of them so close to each other was the problem. K-means++ is a probabilistic algorithm that provides a sounder initialization so that the probability of such a bad clustering is small. We will describe the algorithm for the case of K=3. Step-1: Choose any of the n data-points as the first mean 𝜇1 by sampling from the data-points uniformly at random. For convenience, we will relabel the sampled mean as x1. That is, if x5 is sampled, swap the labels for x1 and x5. The probability of this choice is: P(𝜇1=x1)=1n Step-2: Choose the second mean as one of the remaining data-points using this process:• Find the distance, d(xi,𝜇1), of each point from 𝜇1, • Compute the score for each data-point as the squared distance: s(xi)=d(xi,𝜇1)2 • Form a probability distribution over the n-1 points using the scores. Recall that the summation starts from 2 since x1 has been chosen. The PMF of this distribution is given below: p(i)=s(xi)n∑j=2s(xj) • Sample a data-point using this distribution and assign it to 𝜇2. For convenience, relabel the sampled point x2. That is, if x5 is sampled, swap the labels and the scores for x2 and x5. P(𝜇2=x2 | 𝜇1=x1)=s(x2)n∑j=2s(xj) Step-3: Choose the third mean as one of the remaining data-points using this process • The score for each data-point is the squared distance of the distance of xi to the closest mean: s(xi)=

min

 (d(xi,𝜇1),d(xi,𝜇2))2 • Form a probability distribution over the n-2 points. Recall that the summation starts from 3 since x1 and x2 have been chosen. The PMF is given by: p(i)=s(xi)n∑j=3s(xj) • Sample a data-point using this distribution and assign it to 𝜇3. For convenience, relabel the sampled point x3. That is, if x5 is sampled, swap the labels and the scores for x3 and x5. P(𝜇3=x3 | 𝜇1=x1,𝜇2=x2)=s(x3)n∑j=3s(xj) The overall probability of choosing these three means in this order is the product of the three probabilities we have computed so far. That is,  a

|  |  |
| --- | --- |
|  | P(𝜇1=x1,𝜇2=x2,𝜇3=x3) |
| = | P(𝜇1=x1) |
| × | P(𝜇2=x2 | 𝜇1=x1) |
| × | P(𝜇3=x3 | 𝜇1=x1,𝜇2=x2) |

 Once the means are chosen, we can then run K-means as before with this initialization. On an average, the resulting clustering will be quite "good" when compared to the optimal clustering. Formally: E[n∑i=1||xi-𝜇zi||2]⩽O(logk)⋅

min

z||xi-𝜇zi||2 To understand the LHS, think about repeating K-means++ hundred times, calculating the objective function's value each time and then averaging the results. The claim is that this average value will not be too far from the optimum value. For K>3, the algorithm can be extended in a similar fashion.  A few points to note: • K-means++ is probabilistic. We won't get the same K initial cluster centers on each run of the algorithm. • For the same reason, we could end up with a bad initialization. However, the probability of this happening is very small. • K-means++ spends quite some time in computing the initial means since a lot of distance computations are involved. But once the initial means are there, the actual run of K-means is going to be faster than vanilla K-means because of the good initialization.