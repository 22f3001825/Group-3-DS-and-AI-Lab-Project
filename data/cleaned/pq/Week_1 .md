# **Practice**

This document has questions.

**<u>Question-1</u>**

### **Statement**

An image is a collection of pixels. A pixel is stored as a float value and typically occupies 4 bytes of memory. Consider a dataset of images, where each image has dimensions . Approximately, how much memory does the entire dataset occupy?

### **Options**

#### **(a)**

4 KB

#### **(b)**

4 MB

#### **(c)**

40 MB

#### **(d)**

4 GB

### **Answer**

(c)

### **Solution**

We require float values to represent one image. Since each float value occupies  bytes of memory, a single image occupies bytes of memory. Roughly, this corresponds to KB. The entire dataset would occupy KB or MB of memory. Here, we have used the following facts:

KB bytes MB KB

**<u>Question-2</u>**

### **Statement**

Consider a dataset that has points that belong to . All of them are found to lie on a line that passes through the origin. We use a unit vector along the line as a representative and the coefficients with respect to it to represent the individual data-points. Compute the percentage decrease in the size of the dataset if we move to this new representation. Assume that it takes one unit of space to store one feature. Enter your answer correct to two decimal places; it should be in the range .

### **Answer**

Range:

### **Solution**

The size of the dataset in its original form is:

The size of the dataset after moving to the new representation:

The percentage decrease in the size of the dataset is therefore:

## **Common Data for questions (3) and (4)**

### **Statement**

Consider the following dataset that has four points, all of which lie on a line:

Answer the questions that follow:

**<u>Question-3</u>**

### **Statement**

Among the vectors given below, choose a representative that has unit length.

### **Options**

#### **(a)**

#### **(b)**

#### **(c)**

#### **(d)**

### **Answer**

(c)

### **Solution**

The length of a vector is given by:

We need to find that vector which has . From the options, we see that the required vector is:

**<u>Question-4</u>**

### **Statement**

With respect to the representative in the previous question, compute the coefficients for these four points. The element from the left in each option is the coefficient for the element from the left in the set .

### **Options**

**(a)**

**(b)**

**(c)**

**(d)**

### **Answer**

(a)

### **Solution**

The representative and the dataset are given below:

The coefficient of a point  with respect to is:

Note that this equation holds only if . What will change if ? Think about this. The coefficients are therefore:

**Common Data for questions (5) to (7)**

### **Statement**

Consider the following image. is a point in 2D space. is a proxy for this point on a line passing through the origin. The image is drawn to scale.

Answer the questions that follow:

**<u>Question-5</u>**

### **Statement**

Which of the following is the error vector?

### **Options**

#### **(a)**

#### **(b)**

#### **(c)**

### **Answer**

(c)

### **Solution**

Given these three vectors:

a point its proxy the error vector

The following relationship holds:

The error-vector is the difference between the original point and its proxy. Replacing the words with vector notation, we have:

We have used the concept of <u>vector addition</u> which was covered in maths-2.

**<u>Question-6</u>**

### **Statement**

Is the "best" representation of on the line?

#### **(a)**

Yes

#### **(b)**

No

### **Answer**

(b)

### **Solution**

No, is not the best representation of on the line. Geometrically, the best representation would be the one for which the error vector is perpendicular to the line. From the figure, we see that the line segment does not satisfy this property.

**<u>Question-7</u>**

### **Statement**

If is the "best" representation of on the line, then which of the following statements are true? Notation: is the length of the vector .

### **Options**

#### **(a)**

#### **(b)**

#### **(c)**

#### **(d)**

### **Answer**

(b), (d)

### **Solution**

Computationally, the best representation would have the lowest reconstruction error. The smallest reconstruction error is achieved by the point , the tip of the projection of onto the line. The reconstruction error is the square of the length of the error-vector. These are the terms

and . But we directly compare the lengths of the two error vectors. Think about why this is true.

We now have:

Since and are two different points on the line, we have .

**<u>Question-8</u>**

### **Statement**

Is the following statement true or false?

The projection of  onto was derived to be , where is a unit vector. Since this derivation was done for the special case of 2D vectors, this formula is not applicable in the general case of -dimensional vectors.

### **Options**

#### **(a)**

True

#### **(b)**

False

### **Answer**

(b)

### **Solution**

This formula still holds for any two -dimensional vectors. The geometry of 2D space is generalized to -dimensional space. In 2D space, we can visually see what it means for the errorvector/residue to be perpendicular to the line. Though this visualization is not possible for higher dimensional spaces, the basic ideas still stand. For instance, the dot-product between two vectors in is:

Likewise, the length of a vector is given by:

## **<u>Question-9</u>**

### **Statement**

Consider a mean-centered dataset of  points where each point belongs to . are the first  principal components obtained by running PCA on the dataset, where . The following relationship is observed:

> **[Extracted Question]**
> Zefw;)w;]
> = 0,
> 1 < i < n

Which of the following statement about the dataset is true?

### **Options**

#### **(a)**

The dataset lies in a -dimensional subsapce of

#### **(b)**

The dataset lies in a -dimensional subspace of

#### **(c)**

The dataset lies in a -dimensional subspace of

#### **(d)**

The dataset lies in a -dimensional subspace of

### **Answer**

(b)

### **Solution**

First, the dataset has  features and  examples. So, it doesn't make sense to talk about as is the number of examples. Secondly, we note that each principal component, , is a vector in . Thirdly, we know that the  principal components are orthogonal, and hence linearly independent. It follows that is a -dimensional subspace of . Finally, since each data-point in the dataset is a linear combination of these  principal components, we see that all of them should lie in .

**<u>Question-10</u>**

### **Statement**

In the context of PCA, given  data-points in that are mean-centered, after estimating in the first round, what is the mean of the residues?

### **Options**

#### **(a)**

#### **(b)**

### **Answer**

(b)

### **Solution**

The mean of the residuals is the zero vector in :

> **[Extracted Question]**
> 0
> Xi
> W1
> W1

Here, we have used the fact that

> **[Extracted Question]**
> = 0
> Lxi

as the data is mean-centered.

**<u>Question-11</u>**

### **Statement**

Consider two ways of representing  datapoints that belong to in the form of a matrix:

**Approach-1** : A matrix of dimension

**Approach-2** : A matrix of dimension

Assume that the dataset is mean-centered. Select all correct expressions for the covariance matrix.

### **Options**

**(a)**

**(b)**

**(c)**

**(d)**

### **Answer**

(a), (d)

### **Solution**

Let the data-point be . The expression for the covariance matrix is:

There are two ways to arrange the  data-points. We have a matrix, where each column corresponds to one data-point. This form is particularly important as we will be using this extensively in the second week of the course:

Then, we have:

On the other hand, we have a

matrix, where each row corresponds to one data-point:

Since , we have:

**<u>Question-12</u>**

### **Statement**

Consider a mean-centered dataset obtained from the banking domain that has data-points, each of which is described by  features. The dataset is represented as a matrix, . You run PCA on this dataset and observe that the residues vanish completely after  iterations.

A little later, a domain expert makes the following observations. If represents the column of , then:

The set of vectors are linearly independent.

The following relations are satisfied:

What is the value of ? Assume that the dataset is already mean-centered.

### **Answer**

### **Solution**

Since the last three columns are linear combinations of the first four, and since the first four columns are linearly independent, the rank of the matrix is . This means that the rows of the matrix (the data-points) belong to a four dimensional subspace of . Intuitively, we see that PCA should terminate after four iterations and the principal components will form a basis of this subspace. For now, we shall skip the proof of this statement.

**<u>Question-13</u>**

### **Statement**

Consider the following image:

> **[Extracted Question]**
> 82
> R1
> T1
> R2

Here, is a vector and is a line perpendicular to that passes through the origin. and are two regions on either side of the line . If  is an arbitrary vector in the plane, select all correct statements.

### **Options**

**(a)**

#### **(b)**

**(c)**

**(d)**

**(e)**

### **Answer**

(a), (d), (e)

### **Solution**

All points (vectors) in the region make an acute angle with . Hence, for these points. All points (vectors) in the region make an obtuse angle with . Hence, for these points. All points on the line make a right angle with . Hence, for these points.