# **Principal Component Analysis** 

✉ 23f1001171@ds.study.iitm.ac.in (Piush Das) 

## **Unsupervised Learning - Representational Learning** 

Given a set of datapoints understand something useful about them ! 

### **Input** 



### **Output** 

Some Compressed representation of dataset 

### **Example** 



### **Compress the dataset** 









You can either use (1) with x coordinate or (2) with y coordinate to find the coefficient c 





### **Can we reconstruct the orginal dataset ?** 

representative × coefficients 



0 2 But using ∈ R as representative we cannot reconstruct the original dataset 0 

✉ 23f1001171@ds.study.iitm.ac.in (Piush Das) 

### **Visualise the dataset** 



**Figure 1:** all the data points lying on a same line 

If all the points lie on straigth line, then using representative and coeficients we can reconstruct the original dataset, i.e, length of recunstruction error is zero 

### **What have we gained compressing the dataset ?** 

Reduction in storage ! 

Real numbers nedded to store original dataset = d × n 

Real numbers nedded to store compressed dataset = d + n 

✉ 23f1001171@ds.study.iitm.ac.in (Piush Das) 

### **What if all the data points doesn't lie on same line?** 



**Figure 2:** all the data points doesnot lie on same line 

### **We have two options to consider** 

1. Give up exact reconstruction 

2. Increase number of representative (but thats computationally inefficient) 

So, we need to give up exact representation and find the proxy of the data point on to the line. Proxy should be choosen such that we loose least information - best case is projection of datapoint x onto representetive w. 

✉ 23f1001171@ds.study.iitm.ac.in (Piush Das) 



**Figure 3:** Labeled Diagram 

- Datapoint = x 

- Representative vector = w 

- Error Vector = x - xTw w (assumption is that w is unit vector, ‖w‖2 = 1 ) • Scalar(c) = xTw (assumption is that w is unit vector, ‖w‖2 = 1 ) 



### **Objective Function** 



### **To minimize** : 





### **Step 1: Expand f(c** ) 



### **Step 2: Differentiate f(c) with respect to (c)** 



df **Step 3: Set** = 0 dc 



### **Final Answer:** 



✉ 23f1001171@ds.study.iitm.ac.in (Piush Das) 

w1 w1 We can always pick such that length = 1 w2 w2 



✉ 23f1001171@ds.study.iitm.ac.in (Piush Das) 

### **There can be infinitely many representative lines but which line is the best representative ?** 

Given the dataset, find the line that has the least reconstruction error **Dataset** 



### **Error(line , dataset)** 



✉ 23f1001171@ds.study.iitm.ac.in (Piush Das) 





T Equivalently, max w C w ; where  is a covariance matrix of shape C d × d 2 w : ||w|| = 1 w is the eigen vector corresponding to the maximum value of C 



### **What does the best line represent?** 

The line that best represent the data in terms of the error minimisation of reconstruction is same as the line which maximizes the T w C w as C is the covariance matrix and this line is given by the eigen vector corresponding to the maximum eigen value of the covariance matrix. 

### **Should we throw away the residue ?** 



This x - xTw w might not be error but contain some information 

### **Dataset in Round 1** 



✉ 23f1001171@ds.study.iitm.ac.in (Piush Das) 



### **Dataset in Round 2** 



- All residue are orthogonal to w1 

- The relationship between principal components are that they are perpendicular to each other 





### **What have we gained doing this?** 

If data points lie in lower dimension linear subspace then residue becomes zero much earlier than d-rounds 

### **Example** 

Lets say our dataset is such that after 3 rounds residual becomes 0 

### **Dataset** 



### **Representative** 

{w1 , w2 , w3<sup>}</sup> 

### **Coefficients** 



Real numbers nedded to store original dataset = d × n Real numbers nedded to store compressed dataset = d × k +  k + n here k is the number of round after which residue becomes zero ! 

✉ 23f1001171@ds.study.iitm.ac.in (Piush Das) 

### **What does eigen value of C mean ?** 

we know, 











### **How many direction is good enough?** 



✉ 23f1001171@ds.study.iitm.ac.in (Piush Das) 



### **Dataset Centering** 



**Figure 4:** Dataset Centering 

Data centering is essential in PCA because it ensures that each feature has zero mean, allowing the covariance matrix to accurately capture the true directions of variance. Without centering, the principal components may be biased by the mean, leading to incorrect or misleading results. Centering aligns PCA with the geometric structure of the data by focusing on variation around the data's center rather than the origin. 

✉ 23f1001171@ds.study.iitm.ac.in (Piush Das) 

### **What does this proxies mean ?** 



**Figure 5:** datapoint showing proxies on representative line 



### **Average of Proxies** 



**Variance of Proxies** 



To Conclude, error minimisation on centered dataset ≡ Variance maximisation 

✉ 23f1001171@ds.study.iitm.ac.in (Piush Das) 

### **Why do we study PCA ?** 

In genreal, we want to find directions, that  has the highest variance and the direction is known as principal component {w1 , w2 , . . . . , wd<sup>}</sup> 

### **Steps Involved in PCA** 

**Step 1:** Center the dataset 



**Step 2:** Calculate the covariance matrix of the centered data 



− **Step 3:** Compute the eigenvectors and eigenvalues _<u>watch here</u>_ 

**Step 4:** Sort the eigenvalues in descending order and choose the top k eigenvectors corresponding to the highest eigenvalues 

**Step 5:** Transform the original data by multiplying it with the selected eigenvectors(PC's) to obtain a lower-dimensional representation. 

✉ 23f1001171@ds.study.iitm.ac.in (Piush Das) 

## **Reference** 

**_Arun Raj Kumar, Lecture Slides for Machine Learning Techniques Karthik Thiagarajan, Machine Learning Techniques Github Notes. Indian Institute of Technology Madras , CS2007 Course Website Stanford University, CS229 Machine Learning Notes_** 

# **Thank You !** 

✉ 23f1001171@ds.study.iitm.ac.in (Piush Das)