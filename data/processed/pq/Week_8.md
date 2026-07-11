# **Practice** **<u>assignment</u>** 

## **<u>Question 1</u>** 

### **Statement** 

Consider a 3-class classification dataset with labels and . The data points belong to . If we apply the generative model-based algorithm on the same dataset, how many features need to be estimated? Assume that the features given the label are not independent. 

### **Answer** 

### **Solution** 

We need to estimate the parameters for . Since , we need to estimate two parameters for the distribution of . 

For the distribution of , we need to estimate the parameters for . 

Since , we can have possible data points and we need to estimate the probability for 26 such points as the sum will be one. 

Similarly, for and , we need 26 parameters each. 

Therefore, total parameters to estimate = 

## **<u>Question 2</u>** 

In question , if the features are conditionally independent given the labels, how many parameters need to be estimated? 

### **Answer** 

### **Solution** 

We need to estimate the parameters for . Since , we need to estimate two parameters for the distribution of . 

For a given label (say ), we need to estimate 

) 

Similarly, for labels and . 

Therefore, total parameters to estimate = 

## **Common data for questions 3, 4, and 5** 

### **Statement** 

Consider a naive Bayes model is trained on the following data matrix of shape and corresponding label vector : 

Assume that   and are estimates for and , respectively. Here, is the feature. These parameters are estimated using MLE. 

## **<u>Question 3</u>** 

### **Statement** 

If a test point has label , what will be the probability that the point is ? 

### **Options** 

#### **(a)** 

**(b)** 

#### **(c)** 

#### **(d)** 

### **Answer** 

(d) 

### **Solution** 

We know that is the estimate for . It implies that is the estimate for 

Therefore, 

## **<u>Question 4</u>** 

### **Statement** 

What is the value of ? 

### **Answer** 

### **Solution** 

is the estimate for 

> **[Extracted Question]**
> 2"(fi = 1,y = 1)
> Eiky = 1)

<!-- Start of picture text -->
𝟙<br>𝟙<br><!-- End of picture text -->

Here, the first two examples belong to label  and the first feature value for both examples is , therefore 

## **<u>Question 5</u>** 

### **Statement** 

What will be the probability that a test data point is labeled as ? Assume no smoothing of data is done. 

### **Answer** 

**Solution** 

> **[Extracted Question]**
> Plx
> [0, 1/ly = 0). P(y
> P(z = [0,1])
> P{)pgp
> P(x

Here 

Therefore, 

## **<u>Question 6</u>** 

### **Statement** 

Consider a spam classification problem that was modeled using naive Bayes. The features take a value of  or  depending on whether a word is present in the email or not. Assume that the probability of a mail being spam is 0.2. The following table gives the estimation for conditional probabilities for some of the words: 

|**word**|**label**||
|---|---|---|
|Hurray!|spam|0.7|
|win|spam|0.2|
|exciting|spam|0.01|
|prizes|spam|0.3|
|Hurray!|Non-spam|0.01|
|win|Non-spam|0.02|
|exciting|Non-spam|0.01|
|prizes|Non-spam|0.1|

Consider a mail with the following sentence: "Hurray! win exciting prizes" 

With what probability the mail will be predicted spam? Assume that these are the only possible words (that is there are four features) in a mail.  Write your answer correct to two decimal places. A 

### **Answer** 

Range: 

### **Solution** 

Here, 

Denote spam as  and non-spam as . 

Therefore, 

> **[Extracted Question]**
> P(mail/0) (0.2,
> P(mail/0) (0.2) + P(maill1) (0.8
> P(Hurrayl/0) P(win/o) P(exciting/0) P(prizes/0) (0.2)
> P(Hurray! 0) P(win/0) P(exciting/0)P(prizes 0)(0.2) + P(Hurrayl|1)P(win/1) P(exciting/1) P(prizes/1) (0.
> 0.7(0.2) (0.01)(0.3)(0.2)
> 7(0.2) (0.01) (0.3) (0.2) + 0.01(0.02) (0.01) (0.1) (0.8)
> 0.99

**<u>Question 7</u>** 

### **Statement** 

A binary classification dataset contains only one feature and the data points given the label follow the gaussian distributions whose means and variances are already estimated as: 

What will be the decision boundary learned using the naive Bayes algorithm? Assume that , an estimate for , is . 

Hint: Solve 

### **Options** 

#### **(a)** 

**(b)** 

**(c)** 

**(d)** 

### **Answer** 

(a) 

### **Solution** 

The decision boundary is given by 

> **[Extracted Question]**
> {c : Ply = Ilx) = Ply = Olz)}
> Ply = Ilz) = P(y = Ox)
> Plzly =4) Ply=4)
> P(cly = 0). P(y = 0)
> P(z)
> P(z)
> ~P(zly = 1) = P(zly = 0)
> ( Ply = 0) = Ply = 1) = 0.
> exp(~ (1
> 2)2/4) =
> exp( = (2)? /2)
> "2Tv2
> V2t
> exp(- (x
> 2)2/4) = Vzexp(-(x)?/2)
> In(exp(
> 2)2/4))
> ln(V2exp(- (2)?/2))
> 2)2
> In 2 +
> 2) 2
> ~ln 2

## **Common data for questions 8, 9 and 10** 

### **Statement** 

Consider the gaussian naive Bayes algorithm was run on the following dataset: 

|**feature 1**|**feature 2**<br>**Label**|
|---|---|

> **[Extracted Question]**
> 1.5
> 1.6
> 2.1
> 2.4

**feature 1 feature 2 Label** 

## **<u>Question 8</u>** 

### **Statement** 

What will be the value of ? 

### **Answer** 

Range; [0.74, 0.76] 

### **Solution** 

## **<u>Question 9</u>** 

### **Statement** 

What will be the value of ? 

### **Options** 

#### **(a)** 

#### **(b)** 

#### **(c)** 

#### **(d)** 

### **Answer** 

(c) 

### **Solution** 

## **<u>Question 10</u>** 

### **Statement** 

What will be the value of ? 

### **Options** 

- **(a)** 

- **(b)** 

- **(c)** 

**(d)** 

### **Answer** 

(d) 

**Solution** 

> **[Extracted Question]**
> Ei(yi = 1)xi
> 1(yi
> 1)

<!-- Start of picture text -->
𝟙<br>𝟙<br><!-- End of picture text -->