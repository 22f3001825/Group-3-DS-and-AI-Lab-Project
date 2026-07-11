# Week 3 FAQs
Source: https://mlt.pulki.in/week3/week3.html

## Question/Topic: 📚 Topics Covered in Week 3
K-means Clustering (Lloyd’s Algorithm) K-means++ Initialization

## Question/Topic: 🔍 K-means Reassignments and Centroid Update
Centroid Update \[ \mathbf{\mu} _{k} = \frac{\sum _{i=1}^{n}\mathbf{1}( z_{i} = k) \cdotp \mathbf{x}_{i}}{\sum _{i=1}^{n}\mathbf{1}( z_{i} = k)} \] Where \(z_i\) is the cluster indicator. Reassignment \[ z_{i}^{( t+1)} = \underset{k \in \{1, 2, \cdots, K\}}{\arg \min} \| \mathbf{x}_{i} - \mathbf{\mu }_{k}^{( t)} \| ^{2} \] Tie-Breaking Rule: In case of a tie between multiple clusters for \(\mathbf{x_i}\) , retain the cluster assignment from the previous time step \(t\) by setting \(z_i^{t+1} := z_i^{t}\) . Demonstration of K-Means Algorithm - Source : Standford.edu

## Question/Topic: Centroid Update
\[ \mathbf{\mu} _{k} = \frac{\sum _{i=1}^{n}\mathbf{1}( z_{i} = k) \cdotp \mathbf{x}_{i}}{\sum _{i=1}^{n}\mathbf{1}( z_{i} = k)} \] Where \(z_i\) is the cluster indicator.

## Question/Topic: Reassignment
\[ z_{i}^{( t+1)} = \underset{k \in \{1, 2, \cdots, K\}}{\arg \min} \| \mathbf{x}_{i} - \mathbf{\mu }_{k}^{( t)} \| ^{2} \] Tie-Breaking Rule: In case of a tie between multiple clusters for \(\mathbf{x_i}\) , retain the cluster assignment from the previous time step \(t\) by setting \(z_i^{t+1} := z_i^{t}\) . Demonstration of K-Means Algorithm - Source : Standford.edu

## Question/Topic: 🔍 Convergence of K-means
K-means always converges because it follows an iterative optimization process that monotonically decreases the within-cluster variance (or inertia) at each step. Specifically: Finite Assignments: There are only a finite number of ways to assign data points to clusters. Non-Increasing Objective Function: Each iteration reduces (or keeps constant) the sum of squared distances between points and their cluster centroids. Centroid Updates: The new centroids are always the mean of assigned points, ensuring a non-increasing loss. Lower Bound on Cost: Since the inertia is non-negative and decreasing, it must eventually reach a stable value. Thus, K-means always converges to a local minimum, though not necessarily the global optimum.

## Question/Topic: 🔍 Voronoi Regions
The boundary line between two clusters (say, clusters \(r\) and \(s\) ) is given by the perpendicular bisector of the line joining the centroids of these two clusters. Each Voronoi cell is formed by the intersection of \(K - 1\) half-planes, obtained by comparing a cluster with the remaining \(K - 1\) clusters. ➡️ More Info: Watch this video for a detailed explanation.

## Question/Topic: 🔍 Probability of Choosing Clusters in K-means++
Step 1: Choose the First Cluster \[ P(\mu_1 = \mathbf{x_1}) = \frac{1}{n} \] Where \(n\) is the number of data points. Step 2: Choose the Second Cluster Given that the first cluster is \(\mu_1 = \mathbf{x_1}\) , the probability of choosing the second cluster \(\mu_2 = \mathbf{x_2}\) is: \[ P( \mu_2 = \mathbf{x_2} \mid \mu_1 = \mathbf{x_1}) = \frac{s(\mathbf{x}_2)}{\sum_{j=2}^{n}s(\mathbf{x}_j)} \] Where \(s(\mathbf{x}_j)\) is the score for each data point, calculated as the squared distance from the already chosen mean \(\mathbf{x}_1\) : \[ s(\mathbf{x}_i) = d(\mathbf{x}_i, \mu_1)^2 \] Step 3: Choose the Third Cluster The probability formula is the same as for choosing the second cluster. However, the score is calculated differently: \[ s(\mathbf{x}_i) = \min \bigl(d(\mathbf{x}_i, \mu_1), d(\mathbf{x}_i, \mu_2)\bigr)^2 \] Step 4: Generalization for \(K > 3\) For more than three clusters, extend the approach by selecting each new cluster with a probability proportional to the squared distance from the nearest already chosen cluster.

## Question/Topic: Step 1: Choose the First Cluster
\[ P(\mu_1 = \mathbf{x_1}) = \frac{1}{n} \] Where \(n\) is the number of data points.

## Question/Topic: Step 2: Choose the Second Cluster
Given that the first cluster is \(\mu_1 = \mathbf{x_1}\) , the probability of choosing the second cluster \(\mu_2 = \mathbf{x_2}\) is: \[ P( \mu_2 = \mathbf{x_2} \mid \mu_1 = \mathbf{x_1}) = \frac{s(\mathbf{x}_2)}{\sum_{j=2}^{n}s(\mathbf{x}_j)} \] Where \(s(\mathbf{x}_j)\) is the score for each data point, calculated as the squared distance from the already chosen mean \(\mathbf{x}_1\) : \[ s(\mathbf{x}_i) = d(\mathbf{x}_i, \mu_1)^2 \]

## Question/Topic: Step 3: Choose the Third Cluster
The probability formula is the same as for choosing the second cluster. However, the score is calculated differently: \[ s(\mathbf{x}_i) = \min \bigl(d(\mathbf{x}_i, \mu_1), d(\mathbf{x}_i, \mu_2)\bigr)^2 \]

## Question/Topic: Step 4: Generalization for\(K > 3\)
For more than three clusters, extend the approach by selecting each new cluster with a probability proportional to the squared distance from the nearest already chosen cluster.

## Question/Topic: 💡 Need Help?
For any technical issues or errors, please contact: 📧 22f3001839@ds.study.iitm.ac.in ⬅️ Week 2 Week 4 ➡️