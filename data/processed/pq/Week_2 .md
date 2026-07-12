# **Practice** **<u>assignment</u>** 

## **<u>Question: 1</u>** 

### **Statement** 

Assume that are  principal components corresponding to nonzero eigenvalues of the -dimensional centered data points . 

Statement 1: each can be written as a linear combination of . 

Statement 2: each can be written as a linear combination of . 

### **Options** 

#### **(a)** 

Statement 1 is correct but statement 2 is incorrect. 

#### **(b)** 

Statement 1 is incorrect but statement 2 is correct. 

#### **(c)** 

Both statements are correct. 

#### **(d)** 

Both statements are incorrect. 

#### **Answer:** 

(c) 

### **Solution** 

In the first week, we have seen that residues after  iterations become zero that is 

> **[Extracted Question]**
> xi
> W1 + xiwz +
> + xi wd) =
> Ti
> tTW +cTw? +
> xT
> (2;
> Wd

it implies that each can be written as a linear combination of . 

We know that the eigenvectors of the covariance matrix are the principal components of the dataset and by the definition of eigenvectors, we have 

> **[Extracted Question]**
> AkW k
> Tict
> Wk
> AkWk
> i=1
> 2T wk
> Wk:
> 8i
> nAk
> Cwk

That is ach can be written as a linear combination of . 

## **<u>Question: 2</u>** 

### **Statement** 

A transformation mapping  is defined as 

> **[Extracted Question]**
> $ : R + R4
> [x3_
> 3x2
> 3.1]T

Which of the following options are the same as for two points ? Hint: Rather than doing the calculation, try to figure out the appropriate kernel function. 

#### **(a)** 

#### **(b)** 

#### **(c)** 

#### **(d)** 

#### **Answer:** 

(a), (b), (d) 

### **Solution** 

It is easy to verify that 

It shows that the polynomial kernel of degree three refers to the given transformation . And since the dot product is commutative, we can check that options (a), (b), and (d) refer to the same expression. 

Therefore the correct answers are options (a), (b), and (d). 

## **<u>Question: 3</u>** 

### **Statement** 

Let be the covariance matrix of  data points in -dimensional space. Assume that the data points are mean-centered. If and  are the only non-zero eigenvalues of , what will be the non-zero eigenvalues of , where is the matrix of shape containing the data points? 

### **Options** 

#### **(a)** 

#### **(b)** 

#### **(c)** 

#### **(d)** 

Can not be determined 

#### **Answer: C** 

### **Solution** 

The covariance matrix is defined as and the nonzero eigenvalues of are given to be , and . 

nonzero eigenvalues of will be and . Since all the nonzero eigenvalues of and are the same, the nonzero eigenvalues of are , and . 

## **Common data for Questions 4 and 5** 

### **Statement** 

Consider an image dataset matrix of shape with . The principal component of the dataset can be written as , where, the vector is the data point. The largest eigenvalue and the corresponding eigenvector of are  and , respectively. 

## **<u>Question 4</u>** 

### **Statement** 

What will be the value of ? 

### **Options** 

#### **(a)** 

#### **(b)** 

#### **(c)** 

#### **(d)** 

#### **(e)** 

#### **Answer:** 

C 

### **Solution** 

We know that the principal component can be written as a linear combination of the data points that is 

And the vector can be obtained by eigen decomposition of as follows: 

If the largest eigenvalue and the corresponding unit eigenvector of are and , respectively then 

Therefore, by the given information, we can say that 

> **[Extracted Question]**
> @n]
> V5i
> V51
> V5l
> V5l
> 7Q1 =
> 2v51

## **<u>Question 5</u>** 

### **Statement** 

What will be the largest eigenvalue of the covariance matrix ? Note that as the length of the eigenvector of is 4. 

#### **Answer:** 

### **Solution** 

The largest eigenvalue of 

The nonzero eigenvalues of and are the same. The largest eigenvalue of The largest eigenvalue of 

### **Question: 6** 

### **Statement** 

A function  is defined as 

> **[Extracted Question]**
> k:R2 x R2 _ R
> k([z1, 82]T ,
> ly1, y2]T) 
> =
> 2ky2 + x3y3

Is  a valid kernel? 

Hint: Try to find out the appropriate . 

### **Options** 

#### **(a)** 

Yes 

#### **(b)** 

No 

#### **Answer:** 

A 

### **Solution** 

If we can find an appropriate transformation mapping  such that 

Then we can conclude that  is a valid kernel. 

The given kernel is 

> **[Extracted Question]**
> k:R2 x R2 _ R
> k(
> [y1, 92/T
> TeT,
> [0u

> **[Extracted Question]**
> Tiyi + czyz
> c} ,.31Tlyz, y2

If we define a function 

such that 

then we can say that 

It implies that  is a valid kernel. 

### **Question: 7** 

### **Statement** 

A dataset of 1000 second-hand cars has four features: kilometers driven ( ), mileage , the present price of the car , and the selling price . The selling price seems to have the following relationship (approximate) with the other three features. 

If we want to project the dataset into a lower dimensional space, which of the following task would be most appropriate? 

### **Options** 

#### **(a)** 

Standard PCA 

#### **(b)** 

Kernel PCA with a polynomial kernel of degree 2 

#### **(c)** 

Kernel PCA with a polynomial kernel of degree 3 

#### **(d)** 

Kernel PCA with a polynomial kernel of degree 4 

### **Answer** 

(c) 

### **Solution** 

Notice that the features are not linearly related. The feature is related to other features and the relationship is cubic in nature. 

That is why if we transform the dataset into a higher dimension using the degree three polynomial, then the dataset may live in a linear subspace. 

Therefore, kernel PCA with a polynomial kernel of degree 3 will be an appropriate task. 

## **<u>Question 8</u>** 

### **Statement** 

Abhishek runs a kernel PCA on a dataset containing  examples with  features. Which of the following strategy he should follow to center the data points? 

strategy 1: First center the dataset using the mean and then apply the kernel. 

Strategy 2: First apply the kernel and then center the matrix. 

### **Options** 

#### **(a)** 

Strategy 1 

#### **(b)** 

Strategy 2 

#### **(c)** 

Both strategies are the same 

### **Answer** 

(b) 

### **Solution** 

Applying transformation on the centered dataset is not mandatory to give the centered transformed dataset. For example, consider a centered dataset containing four points in two dimensions. 

Now apply the  transformation such that 

The transformed dataset will be 

Clearly, this dataset is not centered. Therefore, strategy 2 is best suited. 

## **<u>Question 9</u>** 

### **Statement** 

A dataset containing 1000 points in 3-dimensional space is run through the kernel PCA with the polynomial kernel of degree . If the transformed dataset lives in a ten-dimensional space, what will be the value of ? 

### **Answer** 

2 (No range required) 

### **Solution** 

Let and are three features. If we use the features will be 

that is the transformed space will be ten-dimensional. 

## **<u>Question 10</u>** 

### **Statement** 

A dataset containing 1000 examples in 10-dimensional space is projected into other dimension space using kernel PCA with the following kernel. 

> **[Extracted Question]**
> 11
> 12
> exp

What will be the dimension of the projected dataset? 

### **Options** 

#### **(a)** 

#### **(b)** 

#### **(c)** 

#### **(d)** 

Can not be determined 

### **Answer** 

(c) 

### **Solution** 

The given kernel is the gaussian kernel, which will lead to infinite dimension.