# **Practice** 

This document has  questions. 

## **<u>Question-1</u>** 

### **Statement** 

Consider a dataset that has only points, out of which points have the value , have value  and have value . We use a <u>categorical distribution</u> to model this data. The parameters of the distribution are: 

If the distribution seems unfamiliar to you, think about an imaginary dice with three faces. What is the likelihood function for this data under this distribution? 

### **Options** 

#### **(a)** 

#### **(b)** 

#### **(c)** 

### **Answer** 

(c) 

### **Solution** 

Let us use to refer to the number of ones, twos and threes respectively. By the i.i.d assumption, we have: 

## **<u>Question-2</u>** 

### **Statement** 

What is the value of 

? Enter your answer correct to two decimal places. 

### **Answer** 

Range: 

### **Solution** 

Since the sample space is 

, the probabilities should sum to . 

**<u>Question-3</u>** 

### **Statement** 

What is the maximum likelihood estimate of ? Enter your answer correct to two decimal places. 

### **Answer** 

Range: 

### **Solution** 

The log-likelihood is: 

If we want to maximize this likelihood, we can't just differentiate the function and set it to zero, as there is a constraint of involved. One way to get around this is to substitute to get an unconstrained problem in two variables : 

We can now compute the partial derivatives with respect to  and  and set them to zero. A fair amount of algebra will convince us that: 

An interesting insight that this equation gives us is the case when . This reduces to the MLE for a Bernoulli random variable. We can also see how this equation could be extended to the case of a categorical distribution that has a support whose cardinality is . This is left as an exercise to the learners. 

**<u>Question-4</u>** 

### **Statement** 

Consider a dataset of  data-points, . If we assume these points to have been generated from a Gaussian distribution, , what is the expression for the log-likelihood after removing constant terms? 

- (1) Constant terms are those that don't depend on either  or 

(2) always means unless otherwise specified. 

### **Options** 

#### **(a)** 

#### **(b)** 

#### **(c)** 

#### **(d)** 

### **Answer** 

(c) 

### **Solution** 

First, we compute the likelihood. Using the i.i.d assumption: 

> **[Extracted Question]**
> Ti
> p)
> exp
> '2To
> 202

Next, the log-likelihood: 

> **[Extracted Question]**
> log(-
> 2to

> **[Extracted Question]**
> xi
> p) 2
> 202

The first term inside the summation is independent of the s, hence it can be taken out after scaling it by a factor of : 

After removing the constants from the first term, we get: 

## **<u>Question-5</u>** 

### **Statement** 

Consider a dataset of heights of individuals. The first are drawn from the active pool of basketball players in the NBA. The next are drawn from the list of chess grand masters. The last are drawn randomly from the city of Chennai. All individuals are in the age-group of to . If we use a GMM to understand this data, what is a good choice of , the number of mixtures? 

### **Answer** 

### **Solution** 

Though there are three different classes of people, as far as heights are concerned, basketball players certainly are in a different zone. Height is not correlated with chess. Hence we can reason that the average height of a chess player will not be too different from the average height of someone from Chennai. So,  mixtures would be sufficient. 

## **Common Data for questions (6) to (8)** 

### **Statement** 

Consider the histogram of one million points sampled from a GMM with three mixtures as shown in the figure below. The mixtures are labeled from left to right as ,  and . The mean for each mixture is one of the ticks displayed on the x-axis. All the mixtures have unit variance: 

> **[Extracted Question]**
> -10
> -8
> ~6 _4 -2 0   2   4  6   8

## **<u>Question-6</u>** 

### **Statement** 

What is the mean of mixture-3? Note that the mean is an integer here. 

### **Answer** 

### **Solution** 

Visual inspection 

**<u>Question-7</u>** 

### **Statement** 

Which of the following could be the values of and ? 

### **Options** 

#### **(a)** 

#### **(b)** 

**(c)** 

**(d)** 

### **Answer** 

(c) 

### **Solution** 

The heights of the mixtures give us an idea of their importance. 

**<u>Question-8</u>** 

### **Statement** 

If the point is observed, what is the probability that it has come from mixture-2? Use the values of obtained from the previous question. Enter your answer correct to two decimal places. 

### **Answer** 

### **Solution** 

We need to compute . Using Bayes' rule: 

> **[Extracted Question]**
> P(z = 2) . f(r = -3
> 2 =
> 2
> f(a
> -3)

We have: 

. 

> **[Extracted Question]**
> pk
> exp
> 2ok
> 2tok

We now have to compute the each of these quantities. 

## **<u>Question-9</u>** 

### **Statement** 

Assume that you are given a set of one data-points in . You fit a GMM with for this dataset using the EM algorithm to estimate the parameters. The EM algorithm was initialized as follows: 

> **[Extracted Question]**
> p1 = -1,p2
> T1
> T2
> 0.5
> 02
> =1

(1) 

(2) 

(3) 

The estimated means are and for the the two mixtures. A little while later, a domain expert comes and tells you that the dataset given to you was actually sampled from a Gaussian with mean  and variance . Which of the following options is true? Code the EM algorithm and observe what happens. 

### **Options** 

#### **(a)** 

is very close to but both are not close to 

#### **(b)** 

is not close to and neither of them is close to 

#### **(c)** 

is very close to and both are close to 

### **Answer** 

(b) 

### **Solution** 

The points that are in the interval around the mean, somewhere around , form some sort of a barrier. The mixture on the left is unable to advance beyond a certain point to the right. Likewise, the mixture on the right is unable to advance beyond a certain point to the left. This is observed for initializations of the means that are significantly far away from the true mean. This problem will be discussed during the programming session.