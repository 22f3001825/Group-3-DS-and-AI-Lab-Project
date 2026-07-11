# **Kernel Principal Component Analysis** 

✉ 23f1001171@ds.study.iitm.ac.in (Piush Das) 

##### **Issues with PCA ?** 

### **1. Time Complexity Issue** 

Finding the eigen value and eigen vector is compuatationally heavy. we know C ∈ R<sup>d × d</sup> 3 ∴ The time complexity of the algorithm grows at a rate of O d when d ≫ n 

### **2. Non Linearity Issue** 



**Figure 1:** representation of datapoints in subspace 

Data may not be necessarily live in a low-dimensional linear subspace, PCA assumes data lies in linear subspace. PCA works well in linear subspace. If we run PCA on non-linear datatset, the error will be very high. 

But, Interestingly the solution for both the issue is same! 

✉ 23f1001171@ds.study.iitm.ac.in (Piush Das) 

##### **Addressing the Time Complexity Issue** 

##### **Datamatrix** 



##### **Calculating Covariance Matrix** 





∴ The time complexity of the algorithm in this case is O d3 

✉ 23f1001171@ds.study.iitm.ac.in (Piush Das) 

##### **Calculating Gram Matrix** 





3 ∴ The time complexity of the algorithm in this case is O n 

✉ 23f1001171@ds.study.iitm.ac.in (Piush Das) 

> Let, wk be the eigen vector corresponding to the k<sup>th</sup> largest eigenvalue (λk<sup>)</sup> of C 



wk is a linear combination of datapoints. 



Observe to get wk , we need 𝛼k , that indeed need wk ! 

✉ 23f1001171@ds.study.iitm.ac.in (Piush Das) 

#### **How to get** 𝛼k **without being dependent upon** wk 



if we can find 𝛼k that satisfies 



we know length of wk is 1. what is length of 𝛼k ? 



We wanted the Eigenvectors of XX<sup>T</sup> but now we have solved the Eigen equation of , where  is just K K XTX . Now, somehow this also involves λk . We need to know λk for which is the Eigen value of XX<sup>T</sup> . But we are only solving the Eigen equation for XX<sup>T</sup> . So is there any relation between eigen values of XX<sup>T</sup> and XTX . 



##### **What are the common properties between them ?** 

- XX<sup>T</sup> and XTX are positive semi-definite matrix T 

- • XX<sup>T</sup> and X X have same non-zero eigen values T T 

- • rank XX = rank X X = rank (X) = r 

- 𝜆1 ⩾ 𝜆2 ⩾ . . . ⩾ 𝜆r > 0 

##### **Linear Algebra Fact** 

The non-zero eigen values of XX<sup>T</sup> and XTX are exactly the same. 



eigenvectors = {w1 , . . . wk<sup>}</sup> , such that ‖wk‖<sup>2</sup> = 1 eigenvalues = {𝜆1 ⩾ . . . ⩾ 𝜆k<sup>}</sup> 







✉ 23f1001171@ds.study.iitm.ac.in (Piush Das) 



Is 𝛽k = 𝛼k ? 



we can see that there is some scaling of n λk so, we can set 



Now 



**Possible Algorithm when** d ≫ n 

Given dataset 







✉ 23f1001171@ds.study.iitm.ac.in (Piush Das) 

##### **Addressing the Non - Linearity Issue** 



**Figure 2:** non - linear relationship among data 

Consider some data points lying uniformly on a circle with the center at the origin. The relationship between features and datapoints are defined as 



example we will take some datapoint  and transform it to 6D space say x 𝜙(x) 



now, we will take some arbitrary datapoint in 6D say u ∈ R<sup>6</sup> 





we can obsereve that each datapoint sataisfies 



This implies the datapoints actaully lie in a linear supspace of R<sup>6</sup> _A circle in 2 dimension can be a line in 6 dimension !_ 

##### **Main Idea** 



Now, since we increase our dimension to much bigger space(D) from smaller feature space(d), we will use Kernel PCA as we know when d ≫ n we look at 𝜙(x)<sup>T</sup> 𝜙(x) instead of 𝜙(x) 𝜙(x)<sup>T</sup> 

##### **Are We All Set ?** 

𝜙(x) ∈ Rd may be too hard to compute, for example : Lets capture a cubic relation with data having 4 features 



In general, if we have d features and we map it using pth power transformation. the dimension of the transformed feature space is calculated using the formulae 

✉ 23f1001171@ds.study.iitm.ac.in (Piush Das) 



Now, Transformed dataset might be linear in the transformed feature space. PCA can be run on this transformed dataset in R . But explicit transformations can be hard. Kernels help here. 

✉ 23f1001171@ds.study.iitm.ac.in (Piush Das) 

##### **Solved Example** 

Finding dot product 𝜙(xi)<sup>T</sup> 𝜙(xj) without explicitly finding 𝜙(xi) and 𝜙(xj) 

x = a b 

y = c d 

consider the following polynomial function 





2 2 2 2 = a c + b d + 1 + 2acbd + 2ac + 2bd 





✉ 23f1001171@ds.study.iitm.ac.in (Piush Das) 

##### **Kernel Function** 

d d Any function K : R × R → R which is a "Valid" map is called a **Kernel function** 

##### **Types of Kernels Polynomial kernel of degree p** 



##### **Gaussian/Radial Basis Kernel** 



Interestingly,  in this case maps  to an infinite dimensional space. 𝜙 x 

d d **But How can we say that give a function** K : R × R → R **is a "Valid" kernel ?** Method 1 : Exhibit  map explicitly but that might be hard sometimes ! 𝜙 Method 2 : Mercers Theorem ! 





✉ 23f1001171@ds.study.iitm.ac.in (Piush Das) 

##### **Kernel PCA** 

##### **Input** 

Dataset 



Kernel 



**Step 1 :** Compute K ∈ R<sup>n × n</sup> where Kij = K(xi , xj<sup>)</sup> **Step 2 :** Centering the Kernel 



**Step 4 :** wk = 𝜙(x)𝛼k →  defeats the putpose because for that we need to calculate 𝜙(x) (So instead of this step to find eigenvector we will directly compute the projection of the datapoint in transformed space) 





But for a given dataset, the data may be centered, but after applying  map, the kernel might not be centred. we need to get centred kernel to measure 𝜙 the accurate direction. 

✉ 23f1001171@ds.study.iitm.ac.in (Piush Das) 

##### **Kernel Centering** 

Given K ∈ R<sup>n×n</sup> where Kij = k(x ,i xj<sup>)</sup> ∀ i, j 

Create a new kernel, K<sup>c</sup> 



where 





1j = Vector which has  in the 1 j<sup>th</sup> position and zero every where. It is a  dinensional vector. n 

✉ 23f1001171@ds.study.iitm.ac.in (Piush Das) 







1 where 𝜇 = ∑ 𝜙(xi) n i 





✉ 23f1001171@ds.study.iitm.ac.in (Piush Das) 

## **Reference** 

**_Arun Raj Kumar, Lecture Slides for Machine Learning Techniques Karthik Thiagarajan, Machine Learning Techniques Github Notes. Indian Institute of Technology Madras , CS2007 Course Website Stanford University, CS229 Machine Learning Notes_** 

# **Thank You !** 

✉ 23f1001171@ds.study.iitm.ac.in (Piush Das)