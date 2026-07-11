aWeek-2Karthik Thiagarajan[1. Issues with PCA](#n0.2935762241029449) [2. Addressing complexity (XXT and XTX)](#n0.25220607688124863) [3. Addressing non-linearity (Feature Transformation)](#n0.4085903317719388) [4. Kernels](#n0.7078252888908614) [5. Kernel PCA](#n0.10076463828279647) [6. Kernel Centering](#n0.9766823206731394) Note: In Kernel PCA, the notation and approach used are a bit different from the ones discussed in the lecture. Readers are requested to make a note of this.1. Issues with PCAThere are two issues with PCA. The first has to do with the time complexity of the algorithm. How does PCA scale as the number of features increases? Not so well. A key step in PCA is eigen decomposition, which takes about O(d3) steps. This can become an issue when d is very high. The other issue is more serious. If the dataset has a non-linear structure, then PCA will not be effective. Recall that PCA assumes that the dataset lives close to a linear subspace of Rd. For example:  An example of a non-linear structure would be the following  We can still run PCA on this dataset, however, the resulting PCs would not really help us in dimensionality reduction. We would need both PCs to explain the dataset in this case. It turns out that there is one technique, kernels, that will help us address both these issues to some extent. Before we get there, we will first start with the first issue. 2. Addressing complexity (XXT and XTX) We are going to assume that d≫n and see what can be done in this case. A key fact that we will use is the relationship between the matrices XXT and XTX. We already know that XXT leads us to the covariance matrix, a d×d matrix that encodes the relationship between the features: C=1nXXT We shall denote the matrix XTX as K and call it the gram matrix. This is an n×n matrix and encodes the pair-wise relationship between data-points: K=XTX To see why, consider K in more detail: a

|  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| K | =a  |  |  |  | | --- | --- | --- | | - | xT1 | - | |  | ⋮ |  | | - | xTn | - |  a  |  |  |  | | --- | --- | --- | | | |  | | | | x1 | ⋯ | xn | | | |  | | | |

 Each entry of the matrix is the dot-product between two data-points. The dot-product gives a measure of similarity between two data-points. For more on this interpretation, refer to [cosine similarity](https://en.wikipedia.org/wiki/Cosine_similarity). Kij=xTixj We will now briefly state some key facts that link the matrices XXT and XTX which will be used later in the document. The properties are stated without proof. Those interested in detailed proofs can refer to this [appendix](https://notes.karthikthiagu.com/mlf/appendix/a-transpose-a). Properties • XXT and XTX have non-negative eigenvalues (in other words, the two matrices are positive semi-definite) • XXT and XTX have the same non-zero eigenvalues, including multiplicity•  • rank(XTX)=rank(XXT)=rank(X)=r Let 𝜇1⩾ ⋯ ⩾𝜇r>0 be the r non-zero eigenvalues of XTX and let the corresponding unit-norm eigenvectors be v1,⋯,vr. In other words, (𝜇i,vi) is an eigenpair of XTX with 𝜇i≠0 and ||vi||=1. How does this help us? If we know the eigenpairs of XTX we can easily compute the eigenpairs of XXT!

From XTX to XXT If (𝜇i,vi) is an eigenpair of XTX with 𝜇i≠0, then: a

|  |  |  |
| --- | --- | --- |
|  | XTXvi | =𝜇ivi |
| ⟹ | XXTXvi | =𝜇iXvi |
| ⟹ | (XXT)(Xvi) | =𝜇i(Xvi) |

 We see that (𝜇i,Xvi) is an eigenpair of XXT! We can now normalize Xvi as: a

|  |  |
| --- | --- |
| Xvi  (Xvi)T(Xvi) | =Xvi  vTi(XTX)vi |
|  | =Xvi  𝜇i |

 Therefore, the corresponding eigenpair for XXT is (𝜇i,Xvi𝜇i).

 Since C is a scaled version of XXT, the eigenvalues get scaled while the eigenvectors remain the same. The ith principal component and the variance along it is therefore:

wi=Xvi𝜇i, 𝜆i=𝜇in

 How has all this helped address issue-1? Rather than performing the eigen decomposition of XXT, which takes O(d3) steps, we can perform eigen decomposition of XTX, which takes O(n3) steps. Since d≫n, this is a significant improvement.

Summary • Compute the matrix K=XTX•  • Compute the eigen decomposition of K:•  – (𝜇i,vi) is an eigenpair– ||vi||=1, 𝜇i≠0•  • Set wi=Xvi𝜇i,𝜆i=𝜇in•  – wi is the ith PC– 𝜆i is the variance of the dataset along wi

Remark: An interesting observation concerning the PCs. Each wi with 1⩽i⩽r can be expressed as a linear combination of the data-points because: a

|  |  |
| --- | --- |
| wi | =1  𝜇iXvi |
|  | =1  𝜇i(vi1x1+⋯+vinxn) |

 We can arrive at the above results by starting with this observation also. This is what has been achieved in the lectures.

 3. Addressing non-linearity (Feature Transformation) As stated earlier, non-linearity is a more serious issue. To fix this, we take the help of a concept called feature transformation. Consider the dataset given below:x1x2All data-points lie on a circle (say of radius 1) and hence satisfy the equation: x21+x22=1 Let us now transform the dataset by introducing a new set of features, X1=x21,X2=x22. If we plot this transformed dataset, we see that all the data-points lie on the line: X1+X2=1  x1x2X1X2X1=x21X2=x22Original datasetTransformed dataset→ This is called a feature transformation. This feature transformation has helped us convert a non-linear dataset into a linear dataset. In general, a feature transformation can be defined by a function 𝜙:Rd→RD that takes a data-point as input and returns a transformed data-point as output: 𝜙:Rd→RD x→𝜙(x) In the above example, we had: 𝜙:R2→R2 𝜙(x1,x2)=(x21,x22) In this particular transformation, we have lost some information. The sign of x1 and x2, for instance, is lost in the transformation. In general, it is more common to transform points to higher dimensional spaces with minimal loss of information. In such cases D>d. Rd is called the original feature space, while RD is called the transformed feature space. Another example is a polynomial transformation: 𝜙:R2→R6defined as 𝜙(a

|  |
| --- |
| x1 |
| x2 |

)=a

|  |
| --- |
| 1 |
| x1 |
| x2 |
| x21 |
| x22 |
| x1x2 |

 We add more complex features and transform the data to a higher dimensional space in the hope that resulting dataset is linear in the transformed space. So the goal of feature transformation is linearization of the dataset. In this transformation, note that we don't lose any information since x1,x2 are retained as two of the features in the transformed space as well. Why does this help solve issue-2? Once we have an approximately linear dataset, we can go ahead and perform PCA on it. However, it is not as simple as it sounds. In the previous example, we ended up with D=6 after starting with d=2. In general, D might be quite a big value for even moderate values of d. Thus, feature transformation might result in a situation where D≫n. This brings us back to issue-1. Fortunately, we already know how to solve it. Let us now proceed with PCA on the transformed dataset using the trick employed in dealing with the first issue. We first form the transformed data-matrix: 𝜙(X)∈RD×n where 𝜙(X)=a

|  |  |  |
| --- | --- | --- |
| | |  | | |
| 𝜙(x1) | ⋯ | 𝜙(xn) |
| | |  | | |

 We have the following procedure: • Compute the matrix K=𝜙(X)T𝜙(X)•  • Compute the eigen decomposition of K:•  – (𝜇i,vi) is an eigenpair– ||vi||=1, 𝜇i≠0•  • Set wi=𝜙(X)vi𝜇i,𝜆i=𝜇in•  – wi is the ith PC– 𝜆i is the variance of the dataset along wi What we have done is replace X with 𝜙(X) wherever needed. Have we solved issue-2 as well? Not quite. Computing 𝜙(xi) for each xi is likely to be a costly operation. So computing 𝜙(X) is itself quite costly. On top of this, we need to compute 𝜙(X)T𝜙(X), where each element is of the form 𝜙(xi)T𝜙(xj). Besides, what is a good 𝜙? How do we know what transformations to choose? What follows in the next section is the description of a tool called a kernel that allows us to completely sidestep this problem of dealing with 𝜙. 4. Kernels

Definition: A valid kernel is a function k:Rd×Rd→R such that there exists a function 𝜙:Rd→RD that satisfies k(x,y)=𝜙(x)T𝜙(y) for all x,y∈Rd.

 A kernel is a tool that computes the dot product of two data-points in the transformed space. Why would such a tool be useful? Recall that computing K=𝜙(X)T𝜙(X) requires the pair-wise dot product 𝜙(xi)T𝜙(xj). A kernel computes this very quantity, but without having to explicitly compute 𝜙! This may seem counter-intuitive at first. So let us consider an example of a kernel: Let k:R2×R2→R be defined as: k(x,y)=(1+xTy)2 Expanding this with x=a

|  |
| --- |
| x1 |
| x2 |

,y=a

|  |
| --- |
| y1 |
| y2 |

: a

|  |  |
| --- | --- |
| k(x,y) | =(1+x1y1+x2y2)2 |
|  | =1+x21y21+x22y22 |
|  | +2x1y1+2x2y2+2x1x2y2y2 |
|  | =1⋅1+x21y21+x22y22 |
|  | +(2x1)(2y1)+(2x2)(2y2) |
|  | +(2x1x2)(2y2y2) |

 Introducing 𝜙:R2→R6: 𝜙(z)=𝜙(z1,z2)=a

|  |
| --- |
| 1 |
| z21 |
| z22 |
| 2z1 |
| 2z2 |
| 2z1z2 |

 we see that k(x,y)=𝜙(x)T𝜙(y) The beauty of the kernel is that it allows us to compute the dot product in the transformed space without explicitly computing 𝜙. In general, we have what are called polynomial kernels of order p defined as k:Rd×Rd→R k(x,y)=(1+xTy)p The transformation corresponding to this maps data-points to a space RD where: D=a

|  |
| --- |
| p+d |
| d |

(\*) Why is D=a

|  |
| --- |
| p+d |
| d |

? This follows from the [stars and bars formula](https://en.wikipedia.org/wiki/Stars_and_bars_(combinatorics)).Consider (1+xTy)p. (1+x1y1+⋯+xdyd)p We can treat this as the product of p expressions. To get one term in the final expansion, we choose some xiyi from each of the p expressions. The resulting term can be characterized as: 1p0⋅(x1y1)p1⋯(xdyd)pd with p0+p1+⋯+pd=p and 0⩽pi⩽p. Each term in the final expansion gives way to one feature in the transformed space. Therefore, D is the number of terms in the expansion. This is the same as the number of solutions to: p0+p1+⋯+pd=p with 0⩽pi⩽d. This is the same as distributing p balls into d+1 buckets, allowing for empty buckets. We can use d sticks and and interpret the number of balls in a bucket as the number of balls between consecutive sticks. For example, with p=6 and d=3, we have three sticks. In the configuration shown below, bucket-1 has one ball, bucket-2 has two balls, bucket-3 has no balls and bucket-4 has the rest, corresponding to p0=1,p1=2,p2=0 and p3=3.The number of solutions is therefore the number of arrangements of the p balls and d sticks. This turns out to be a

|  |
| --- |
| p+d |
| d |

.

 Another popular kernel is the Gaussian kernel, k:Rd×Rd→R defined as: k(x,y)=exp(-||x-y||22𝜎2) where 𝜎 is a parameter chosen by the user. To see what this kernel does, consider a 1D case. The kernel's value as a function of ||x-y|| is plotted below. This should remind you of the bell-curve from statistics.-3-2-112301||x-y||𝜎=1𝜎=2

Remark: It turns out that the 𝜙 corresponding to the Gaussian kernel transforms points to an infinite dimensional space. This requires some advanced math to prove. So we will just state this fact here. Also, this calls into question the definition of a kernel, in which we had mentioned the existence of a 𝜙:Rd→RD. This has to be corrected to allow for infinite dimensional spaces. Also, when infinite dimensional spaces come in, the simple dot-product would have to be replaced by a valid inner product. This is beyond the score of this course. Interested readers can refer to [functional analysis](https://en.wikipedia.org/wiki/Functional_analysis).

 Recall that our aim is to compute 𝜙(X)T𝜙(X) without explicitly having to compute 𝜙(xi). We now define the kernel matrix, K∈Rn×n, with each element being: Kij=k(xi,xj) Note that this is effectively nothing but 𝜙(X)T𝜙(X). A quick example for a dataset of two points. Let D={(1,1),(2,1)} and k be the polynomial kernel of degree 2, then one can see that K has to be: K=a

|  |  |
| --- | --- |
| 9 | 16 |
| 16 | 36 |

 What does K capture? It captures the relationship between data-points in the transformed space.

Remark: In general, C is a d×d matrix that captures the relationship between features. K is an n×n matrix that captures the relationship between data-points.

 The next question that arises is this: if we have a function k:Rd×Rd→R, how do we know that it is a valid kernel? One way is to work with the definition of a valid kernel and show that there is a 𝜙 that satisfies k(x,y)=𝜙(x)T𝜙(y). Is there an alternative method? Mercer's theorem tries to answer this:

Mercer's Theorem: A kernel k:Rd×Rd→R is valid if and only if: • k is symmetric and•  • For any set of data-points {x1,⋯,xn}, the kernel matrix K of shape n×n is symmetric and positive semi-definite.

 One utility of this definition is that it allows us to build new kernels. For example: • Let k be a valid kernel, then 𝛼k is also a valid kernel whenever 𝛼>0. Why? According to Mercer, we see that any kernel matrix K is p.s.d. With the new kernel, the corresponding kernel matrix becomes 𝛼K and 𝛼K with 𝛼>0 is p.s.d whenever K is p.s.d.• Let k1 and k2 be valid kernels, then k1+k2 is also a valid kernel. Why? Invoking Mercer again, we see that kernel matrices K1 and K2 are p.s.d. The kernel matrix corresponding to k1+k2 is K1+K2 which is p.s.d whenever K1,K2 are p.s.d.

Remark: Recall that a matrix A∈Rn×n is p.s.d (positive semi-definite) if zTAz⩾0 for all z∈Rn

 5. Kernel PCA Let us quickly take stock of where we were before we embarked on our kernel adventure. This was the algorithm we had come up with:

PCA with explicit feature transformation • Compute the matrix K=𝜙(X)T𝜙(X)•  • Compute the eigen decomposition of K:•  – (𝜇i,vi) is an eigenpair– ||vi||=1, 𝜇i≠0•  • Set wi=𝜙(X)vi𝜇i,𝜆i=𝜇in•  – wi is the ith PC– 𝜆i is the variance of the dataset along wi

 We are now ready to replace 𝜙(X)T𝜙(X) with the kernel matrix K. The eigen decomposition step remains unchanged. But we still have a 𝜙 intruding in the last step when we go from vi→wi. This is, however, not as big a problem as it might seem. In PCA, what we need in most cases is the final scalar projections on the P.Cs and not the P.Cs themselves. That is, if wi is a PC, we are interested in xTjw. In the transformed space, this becomes 𝜙(xj)Twi. Using the last step from above: a

|  |  |
| --- | --- |
| 𝜙(xj)Twi | =1  𝜇i𝜙(xj)T𝜙(X)vi |

 If we peep into 𝜙(xj)T𝜙(X), it looks like this: a

|  |  |  |
| --- | --- | --- |
| - | 𝜙(xj)T | - |

a

|  |  |  |
| --- | --- | --- |
| | |  | | |
| 𝜙(x1) | ⋯ | 𝜙(xn) |
| | |  | | |

 =a

|  |  |  |
| --- | --- | --- |
| 𝜙(xj)T𝜙(x1) | ⋯ | 𝜙(xj)T𝜙(xn) |

 The result is nothing but the jth row of K! Therefore, we can express the scalar projection as:a

|  |  |
| --- | --- |
| 𝜙(xj)Twi | =1  𝜇i(Kvi)j |

 where (Kvi)j is the jth component of the vector. Including all n data-points, in matrix form, the projections of each of them on the ith PC is: 𝜙(X)Twi=1𝜇iKvi Recall that we have r PCs for K. The final matrix of the dimensionality reduced dataset, X′, is going to have a shape r×n. We need to stack each of the above vectors that contains the scalar projections in rows: X′=a

|  |  |  |
| --- | --- | --- |
| - | 1  𝜇1vT1K | - |
|  | ⋮ |  |
| - | 1  𝜇rvTrK | - |

 This can be further simplified by introducing two new matrices, D∈Rr×r, a diagonal matrix and V∈Rn×r: D=a

|  |  |  |
| --- | --- | --- |
| 1  𝜇1 |  |  |
|  | ⋱ |  |
|  |  | 1  𝜇r |

, V=a

|  |  |  |
| --- | --- | --- |
| | |  | | |
| v1 | ⋯ | vr |
| | |  | | |

 With all this, X′ becomes: X′=DVTK We have all the ingredients to specify the algorithm that we call kernel PCA. a

|  |  |
| --- | --- |
|  | kernel-PCA(X,k) |
| 1 | K←compute-kernel-matrix(X,k) |
| 2 | D,V←eigen-decomposition(K) |
| 3 | return DVTK |

 The schematic diagram is given below:

X,k

→

kernel-PCA

→

X′

 A d×n matrix and kernel function go in as input, an r×n matrix is returned as the output, where r is the rank of the kernel matrix. In kernel-PCA, it may so happen that r>d. This may seem counter-productive. Instead of a reduction in the number of dimensions, we end up with a larger number of dimensions. This is a trade-off we have to live with if we want to get PCA to work on a non-linear dataset. The increased dimensionality is the price we pay for linearizing the dataset. 6. Kernel Centering In all the above discussions, we have been silent about one key aspect, the mean of the dataset. Ideally, we should have centered the transformed dataset 𝜙(X) before running PCA. This is what we will fix now. The mean of the transformed dataset is: 1nn∑i=1𝜙(xi) We need to subtract this from every column of 𝜙(X). A nice way to do that is to let: 𝜙c(X)=𝜙(X)-𝜙(X)1n×n where 1n×n=1na

|  |  |  |
| --- | --- | --- |
|  | ⋮ |  |
| ⋯ | 1 | ⋯ |
|  | ⋮ |  |

 1n×n is a matrix where each element is 1n. The reader is encouraged to verify this fact. 𝜙c(X) is the centered matrix. With this, the kernel matrix for the transformed, centered dataset becomes: a

|  |  |
| --- | --- |
| Kc | =𝜙c(X)T𝜙c(X) |

 Expanding this, we have: a

|  |  |
| --- | --- |
| Kc | =(𝜙(X)-𝜙(X)1n×n)T(𝜙(X)-𝜙(X)1n×n) |
|  |  |
|  | =𝜙(X)T𝜙(X)-𝜙(X)T𝜙(X)1n×n |
|  | -1n×n𝜙(X)T𝜙(X)+1n×n𝜙(X)T𝜙(X)1n×n |
|  |  |
|  | =K-K1n×n-1n×nK+1n×nK1n×n |

 We now replace K with Kc in the kernel-PCA algorithm by introducing one intermediate step. a

|  |  |
| --- | --- |
|  | kernel-PCA-centered(X,k) |
| 1 | K←compute-kernel-matrix(X,k) |
| 2 | Kc←center-kernel(K) |
| 3 | D,V←eigen-decomposition(Kc) |
| 4 | return DVTKC |