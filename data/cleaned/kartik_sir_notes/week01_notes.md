aWeek-1Karthik Thiagarajan[1. Dataset](#n0.30806374225262256) [2. Goal and Assumption](#n0.9832286963263548) [3. Centering the dataset](#n0.5799816340205481) [4. Covariance matrix](#n0.6472071774092065) [5. Reconstruction Error](#n0.09032007845233636) [6. Reconstruction Error Minimization](#n0.529880656249196) [7. Variance Maximization](#n0.5206458251394297) [8. Principal component](#n0.05077126667841503) [9. PCA in Higher Dimensions](#n0.19291045833171117) [10. Dimensionality Reduction](#n0.9517436598570135) [11. Example](#n0.8023521746359399) [12. Reconstruction](#n0.030625178191411973) [13. (\*) Principal Components and Change of Basis](#n0.00963957917223801) [14. Choice of k](#n0.4306100749824908) Starred (\*) section may be mathematically heavy. Handle with care.1. DatasetWe will work with a sample dataset in R2 as shown below throughout this document. But note that all the results that we derive are applicable for a dataset in Rd with d features.  2. Goal and Assumption • Assumption: The fundamental assumption in PCA is that the dataset "lies very close" to a linear subspace. That is, the dataset has an approximately "linear structure". Linearity loosely translates to "line" or "plane". Since we are looking for a subspace and since subspaces pass through the origin, it becomes important to center the dataset at the origin. • Goal: The goal of PCA is to extract this underlying lower-dimensional, linear structure in the dataset and return a dataset with reduced dimension while preserving maximum information. For an example of what we mean by this, in the example that we will work with, the lower-dimensional subspace is a line passing through the origin in R2 as demonstrated in the figure. Though the original dataset needs two dimensions, one dimension (a line) would be sufficient to express the underlying structure. For most of this document, we will work on devising a technique to find the "best" line or the "closest" line to the dataset. This line is called the first principal component. One can also call it the "best-fit" line. PCA is an algorithm that extracts this line from the dataset; expressed as a flowchart:

Dataset

→

PCA

→

First P.C.

 This is of course not the complete picture. We will return to this flowchart and update it at the end.

Remark: We can perform PCA even if the linearity assumption is not valid, however, that will not help us achieve the goal of dimensionality reduction.

 3. Centering the datasetThe dataset has to be centered before performing PCA. The mean of the data-points is represented as ⏨x∈Rd: ⏨x=1nn∑i=1xi If the dataset is already centered, ⏨x=0. If ⏨x≠0, do the following for each data-point: x′i=xi-⏨x Inserting the ith data-point into the ith column of matrix Xc, we have: Xc=a

|  |  |  |
| --- | --- | --- |
| | |  | | |
| x′1 | ⋯ | x′n |
| | |  | | |

 Xc is the centered data-matrix of shape d×n.

Remark: From now we will work only with the centered data-matrix and will be calling it X (the subscript c will be dropped).

 4. Covariance matrixThe covariance matrix is a d×d matrix that condenses the information in the dataset by capturing the pairwise relationship among features and will play an important role in finding the "best" line.  For example:C=a

|  |  |
| --- | --- |
| 1 | -0.9 |
| -0.9 | 1 |

In this example, C11 and C22 capture the variance along features 1 and 2 respectively. C12=C21 capture the covariance between these two features. The two features are negatively correlated as can be seen both from the graph and from the matrix. Shape C∈Rd×d Outer-product form The covariance matrix can be written as the sum (average) of n matrices, each of which is a matrix of shape d×d, and rank 1 and is of the form xixTi. Note that the individual components in the RHS are vectors which are combined via an outer-product to produce a matrix. C=1nn∑i=1xixTi Matrix-form In this form, the data-matrix X replaces the sum of outer products. C=1nXXT

Remark: To be accurate, the covariance matrix is defined as: C=1n(X-𝜇)(X-𝜇)T where 𝜇 is the mean of the columns of X. It reduces to 1nXXT since 𝜇=0 for a centered matrix.

 Scalar form Cpq captures the covariance between the pth feature and the qth feature.  Cpq=1nn∑i=1xipxiq As a special case: Cpp=1nn∑i=1x2ip Cpp captures the variance of the pth feature. Properties of the covariance matrix • The covariance matrix is symmetric, that is, CT=C.•  • All the eigenvalues of C are non-negative. If we denote the eigenvalues of C by 𝜆1,⋯,𝜆d, then 𝜆1⩾⋯⩾𝜆d⩾0.•  • There is an orthonormal basis for Rd made up of eigenvectors of C:•  – We can find a set of orthonormal eigenvectors 𝛾={w1,⋯,wd} corresponding to the eigenvalues 𝜆1,⋯,𝜆d.\* Cwi=𝜆iwi, 1⩽i⩽d\* wTiwj=0,i≠j\* wTiwj=1–  – 𝛾 is an orthonormal basis for Rd. The existence of such a basis is guaranteed by the spectral theorem.

Note: If C is a square matrix, then (𝜆,w) is said to be an eigenvalue-eigenvector pair if Cw=𝜆w. Note that w≠0 for it to be an eigenvector.

Remark: wi will always represent a unit-norm vector in the rest of the document.

5. Reconstruction ErrorThe goal is to find the direction w of the line that is "closest" to the dataset. The original data-points are in blue while its proxies on the line are in green. Since we are only interested in the direction, we will assume ||w||=1. w Among all possible proxies to a point, the "best" proxy is the projection of the point onto the line:wx(xTw)wx-(xTw)wunit circleprojectiondata-pointerrorNote: error is orthogonal to the lineThe projection of x onto the line is given by: (xTw)w By default, whenever we use the term projection, we mean the orthogonal vector projection. The scalar projection would be xTw. Now, the error in projection is given by: e=x-(xTw)w The magnitude of the error, ||e||, gives a sense of how close the data-point is to its proxy on the line. Since it is more convenient to deal with squared lengths, we stick to ||e||2. This is the reconstruction error: the error incurred if we replace the data-point with its proxy. ||e||2=||x-(xTw)w||2 The (average) reconstruction error for the entire dataset is therefore: 1nn∑i=1||xi-(xTiw)w||2 6. Reconstruction Error MinimizationThe "best" line or the "closest" line to the dataset is one which returns the smallest reconstruction error. So we have to solve the following optimization problem:

min

w||w||=1 1nn∑i=1||xi-(xTiw)w||2 The optimization variable is w. Let us take one term in the objective function we wish to minimize: ||xi-(xTiw)w||2. Back to the image of the projection, we see that the (data-point, projection, error) form a right triangle. Using the Pythagorean theorem on the lengths of these vectors: projection2+error2=data-point2  wxixi-(xTiw)w(xTiw)w Algebraically: a

|  |  |
| --- | --- |
| (xTiw)2+||xi-(xTiw)w||2 | =||xi||2 |

 Rearranging, the squared length of the error is: a

|  |
| --- |
| ||xi-(xTiw)w||2 |

=||xi||2-(xTiw)2 We can recast the optimization problem as:

min

w||w||=1 1nn∑i=1||xi||2-(xTiw)2 7. Variance MaximizationSince the term ||xi||2 is independent of w, it has no effect on the solution to the problem. We can therefore drop it with impunity to get the following equivalent problem:

min

w||w||=1 -1nn∑i=1(xTiw)2 Negating the objective function changes min to max:

max

w||w||=1 1nn∑i=1(xTiw)2 If we study the quantity 1nn∑i=1(xTiw)2, we see that this is the variance of the centered dataset along the direction w. To see why, note the projections of the points along w. The quantity (xTiw) is the (signed) distance of the projection of xi from the origin along the line w: w(xT2w)(xT1w)(xT3w)(xT4w)x1x2x3x4 Variance along w is therefore the average spread about the mean (zero): 1nn∑i=1(xTiw)2 Therefore, what we want to maximize is the variance of the dataset along a direction w. In other words, we want to find that direction that holds the maximum information (variance) contained in the dataset. We can simplify the objective function further: a

|  |  |
| --- | --- |
| 1  nn∑i=1(xTiw)2 | =1  nn∑i=1(xTiw)(xTiw) |
|  |  |
|  | =1  nn∑i=1(wTxi)(xTiw) |
|  |  |
|  | =1  nn∑i=1wT(xixTi)w |
|  |  |
|  | =wT[1  nn∑i=1xixTi]w |
|  |  |
|  | =wTCw |

 where C is the covariance matrix of the centered dataset. The final optimization problem is:

max

w||w||=1 wTCw Therefore, we see that reconstruction error minimization is equivalent to variance maximization. They are two different perspectives to view the same problem. 8. Principal componentThe solution to the optimization problem is what concerns us next:

max

w||w||=1 wTCw The quantity wTCw is called the Rayleigh quotient. For now, we will state the following fact without proof: the quantity that maximizes wTCw is the eigenvector w1 corresponding to the largest eigenvalue 𝜆1 of C. At w1 the objective function's value becomes 𝜆1: a

|  |  |
| --- | --- |
| wT1Cw1 | =wT1(𝜆1w1) |
|  |  |
|  | =𝜆1(wT1w1) |
|  |  |
|  | =𝜆1 |

 We call w1 the first principal component. Recall that the quantity wTCw is the variance of the dataset along the direction w. That is:1nn∑i=1(xTiw)2=wTCw Therefore, wT1Cw1=𝜆1 is the variance of the dataset along the first principal component. The eigenpair (𝜆1,w1) has this important interpretation: the direction that captures the maximum variance in the dataset is w1 and this variance is given by 𝜆1. Visually, it should be clear why this is the case:w1 ais a unit vectoralong this line

Remark: Note that the first principal component in this case is unique up to the sign. w1 and -w1 are both valid candidates.

 Closing the optimization problem, we have: a

|  |  |
| --- | --- |
| max w||w||=1 wTCw | =𝜆1 |
|  |  |
| argmax w||w||=1 wTCw | =w1 |

 9. PCA in Higher DimensionsSo far we have focused on finding the best line given a dataset. Real datasets are going to have tens of hundreds of dimensions (features). While they may have a linear structure, it is very rarely going to be just a line passing through the origin. Therefore, we need to see how to extract the entire lower-dimensional structure. If this lower dimensional structure is a k-dimensional subspace, then we need to look for the best k directions. Consequently, we are hunting for the vectors w1,⋯,wk that go on to span this subspace. As an example, consider data-points in R3 which actually lie on a plane:w1w2 We need to hunt for a two-dimensional subspace in this situation which can be defined by the span of two principal components: w1,w2. We can now go back to the flow chart and refine it:

Dataset

→

PCA

→

Top k P.C.

 We understand the procedure to extract the best direction. What about the other k-1 directions? It turns out that the same recipe works with small changes. To find the second best line, we continue to look for the second best direction that captures as much information as possible:

max

w||w||=1wTw1=0 wTCw To emphasize that we are looking for the second-best direction, we have added an additional constraint wTw1=0. The solution to this optimization problem is the eigenvector corresponding to the second largest eigenvalue, w2, and the variance along that direction is 𝜆2. a

|  |  |
| --- | --- |
| max w||w||=1wTw1=0 wTCw | =𝜆2 |
|  |  |
| argmax w||w||=1wTw1=0 wTCw | =w2 |

 Continuing in this fashion, the ith direction yields the ith principal component wi: a

|  |  |
| --- | --- |
| max w||w||=1wTw1=0,⋯,wTwi-1=0 wTCw | =𝜆i |
|  |  |
| argmax w||w||=1wTw1=0,⋯,wTwi-1=0 wTCw | =wi |

 Note that we have specified wi to be orthogonal to the first i-1 principal components. Though the algorithm is presented in this sequential manner, the upshot is the following:

PCA: The k-dimensional subspace that is closest to the centered dataset, X, is the subspace spanned by the k eigenvectors, w1,⋯,wk, corresponding to the k largest eigenvalues, 𝜆1⩾⋯⩾𝜆k, of the covariance matrix, C, of the dataset. The k principal components form an orthonormal set.

 10. Dimensionality ReductionNow that we have k directions that capture the underlying structure of the dataset, we can see how to get the lower-dimensional representation of the dataset. When we had just one direction w1, the representations of the ith data-point has been given by (xTiw1)w1, the projection of xi on w1. When we have a k-dimensional subspace, the representation of the ith data-point is the projection of xi onto this subspace. Since {w1,⋯,wk} forms an orthonormal set, the projection is: (xTiw1)w1+⋯+(xTiwk)wk We can now do two things depending on the application: • retain only the scalar projections•  • retain the d-dimensional projections, the full reconstruction We will look at scalar projections first and the full reconstruction in the next section. To represent the scalar projections in matrix form, we form the following k×n matrix: X′=a

|  |  |  |
| --- | --- | --- |
| xT1w1 |  | xTnw1 |
| | | ⋯ | | |
| xT1wk |  | xTnwk |

 The ith column is the k-dimensional representation of the ith data-point. Note how we have retained the scalar projections alone. We can decompose this into the product of two matrices: a

|  |  |  |  |  |  |  |  |  |  |  |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| X′ | =a  |  |  |  | | --- | --- | --- | | xT1w1 |  | xTnw1 | | | | ⋯ | | | | xT1wk |  | xTnwk | |
|  |  |
|  | =a  |  |  |  | | --- | --- | --- | | wT1x1 |  | wT1xn | | | | ⋯ | | | | wTkx1 |  | wTkxn | |
|  |  |
|  | =a  |  |  |  | | --- | --- | --- | | - | wT1 | - | |  | ⋮ |  | | - | wTk | - |  a  |  |  |  | | --- | --- | --- | | | |  | | | | x1 | ⋯ | xn | | | |  | | | |
|  |  |
|  | =WTX |

 where, W is the d×k matrix defined as: W=a

|  |  |  |
| --- | --- | --- |
| | |  | | |
| w1 | ⋯ | wk |
| | |  | | |

 We are now ready to present the algorithm. If we want a k dimensional representation of the dataset, then we have: a

|  |  |
| --- | --- |
|  | PCA(X,k) |
| 1 | X←center(X) |
| 2 | C←1  nXXT |
| 3 | W←eigen-decompose(C,k) |
| 4 | return WTX |

 Here, the function eigen-decompose(C,k) returns the top-k eigenvectors of the covariance matrix. To look at the compression achieved,  • for the new dataset, we need to store k values for each of the n data-points•  • for the original dataset, we need to store d values for each of the n data-points The compression ratio, defined as new/old is: nknd=kd 11. ExampleAssume that we want to distinguish images of handwritten digits into two classes, 0 and 1. The feature dimension here is 784, which is obtained by arranging the pixels in this 28×28 image in a row or column.

 There are 2000 images, 1000 in each class. The data matrix X is of shape d×n, where d=784 and n=2000. Running PCA on this dataset and retaining the scalar projections on the top two principal components results in this scatter plot for the data:

 Green corresponds to one of the two classes and red to the other. Notice how the first two PCs have managed to separate the classes quite well. We can now run a standard classification algorithm on this transformed dataset. This is a typical use-case of PCA: reduce the dimensionality of the dataset before passing it to a downstream task such as classification. 12. ReconstructionWe can now turn to the full reconstruction. Reusing the W computed in the previous section, we have the projection matrix WWT. This matrix projects vectors in Rd onto the span of the columns of W. This is precisely what our representatives are in a complete reconstruction. Allowing it to operate on the data-matrix, we get: X′=WWTX We get X′ to be a d×n matrix here. Recall that the reconstruction error is given by: 1nn∑i=1||xi-x′i||2 where xi′ is the reconstruction (projection) of xi. More formally, this error can be expanded as: 1nn∑i=1aaxi-k∑j=1(xTiwj)wjaa2 Note that the inner summation is over the top k principal components. Earlier, it was just over the first component. We can now look at the compression achieved. In this representation, we need to store: • k principal components, each of which requires d values • k scalar projections for each of the n data-points The total size is kd+nk=k(n+d). The original dataset requires a storage of nd. The compression ratio, defined as new/old is: k(n+d)nd=kd+kn 13. (\*) Principal Components and Change of Basis Instead of stopping with the top k principal components, if we go the full distance, we end up with d principal components: {w1,⋯,wd}. This set forms an orthonormal basis for Rd, where each basis vector is an eigenvector of C. It is important to note that any two directions here are orthogonal.  What does this mean? One way to interpret it is that PCA reorients the original basis in such a way that the new basis captures the maximum information in the first few directions. For instance, in the 2D example we have been working with so far, {e1,e2}→{w1,w2}. w1w2e1e2w2w1→ Notice that the new basis has been reoriented in such a way that the w1 points in the direction with maximum information. Therefore, PCA can be seen as a change-of-basis operation, where the choice of the basis is driven by the data, whose signature is given by the covariance matrix. The moment we bring in change-of-basis, a natural question arises. How does a data-point's representation in the original basis gets transformed in the new basis? If x=(x1,⋯,xd) is the data-point, its representation in the old basis is just: x=x1e1+⋯+xded That is, the coordinates of the point are (x1,⋯,xd) with respect to the old basis. Using the new basis. x=(xTw1)w1+⋯+(xTwd)wd The coordinates of the point with respect to the new basis are: (xTw1,⋯,xTwd) Another way to understand this is, if W is the d×d matrix whose columns form the basis (it is d×d now as we are letting k=d), the we can equivalently express the coordinates as: a

|  |
| --- |
| xTw1 |
| | |
| xTwd |

=WTa

|  |
| --- |
| x1 |
| | |
| xd |

 WT is the change of basis matrix. It takes a representation in the standard basis and transforms it into a representation in the new basis. Finally, what does a principal component mean practically? It can be viewed as a new feature direction that is obtained by linearly combining the old feature directions. What are the coefficients of the combination and where do they come from? They come from the data and it is the job of PCA to find them. Going back to the example, we see that w1=12a

|  |
| --- |
| -1 |
| 1 |

 and w2=12a

|  |
| --- |
| 1 |
| 1 |

. So: a

|  |  |
| --- | --- |
| w1 | =(-1  2)e1+(1  2)e2 |
|  |  |
| w2 | =(1  2)e1+(1  2)e2 |

 14. Choice of kWe now come to the question of the choice of k in PCA. To understand this, we need to look at the total variance present in the dataset and the proportion of it retained in the lower-dimensional representation. First, what could total variance mean? One way to define it is the spread of the data around its mean. Since the mean is zero here, we can compute this as: 1nn∑i=1||xi||2 On an average, this captures how far (squared distance) away the data-points are from the mean, which is our conventional definition of variance. Now, recall that the principal components, {w1,⋯,wd}, form an orthonormal basis. So we can rewrite ||xi||2 as: ||xi||2=(xTiw1)2+⋯+(xTiwd)2 Therefore, the total variance becomes: 1nn∑i=1[(xTiw1)2+⋯+(xTiwd)2] Decomposing this into n sums: 1nn∑i=1(xTiw1)2+⋯+1nn∑i=1(xTiwd)2 Recall that the variance along the principal component wi is given by: 1nn∑i=1(xTiw1)2=wTiCwi=𝜆i Therefore, the total variance becomes: 𝜆1+⋯+𝜆d The sum of the eigenvalues of the covariance matrix gives us the complete information content in the dataset. The top-k principal components capture the following fraction of that information: 𝜆1+⋯+𝜆k𝜆1+⋯+𝜆d We can now use the following heuristic to choose k: find the smallest value of k that captures at least 95% of the variance in the dataset.