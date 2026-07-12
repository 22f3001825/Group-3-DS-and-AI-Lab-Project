# **Practice** 

## **<u>Question-1</u>** 

### **Statement** 

Which of the following data sets is/are linearly separable? 

D1: , , , , , D2: , , , , , 

### **Options** 

#### **(a)** 

D1 

#### **(b)** 

D2 

#### **(c)** 

Both D1 and D2 

#### **(d)** 

Neither D1 nor D2 

### **Answer** 

(a) 

### **Solution** 

Below, red points belong to -ve class, green points belong to +ve class. 

D1: 

D2: 

In D2, there is an intermixing of data points belonging to green and red class and there is no linear separator that can separate the data points beloning to the two classes. 

**<u>Question-2</u>** 

### **Statement** 

Consider the following data set with three data points: 

, , 

If the Perceptron algorithm is applied to this data with the initial weight vector to be a zero vector,  what will be the outcome? 

### **Options** 

#### **(a)** 

The algorithm will converge with 

#### **(b)** 

The algorithm will converge with 

#### **(c)** 

The algorithm will converge with 

#### **(d)** 

The algorithm will never converge. 

### **Answer** 

(d) 

### **Solution** 

Iteration 1: 

> **[Extracted Question]**
> T1
> 82
> 0T
> U
> 13
> R0 ?
> kor

> **[Extracted Question]**
> Y3 pred
> I1pred
> (y2 pred

, hence , hence , hence 

Mistake is for Hence, Iteration 2: When we compute ‘s’ we find a mistake for , hence we update the weight vector to: 

Iteration 3: 

The mistake is found to be for 

. 

is same as 

. 

Hence, perceptron will keep oscillating ans repeating these weights, and will never converge. 

**<u>Question-3</u>** 

### **Statement** 

Assume that Perceptron algorithm is applied to a data set in which the maximum of the lengths of the data points is 4. Assume that the squared length of the weight vector in an iteration of the algorithm is 36. As per the given information, which of the following can be a valid squared length of the new weight vector obtained in the next iteration? 

### **Options** 

#### **(a)** 

#### **(b)** 

#### **(c)** 

#### **(d)** 

### **Answer** 

(a) 

### **Solution** 

R = 4 

> **[Extracted Question]**
> wl|l2
> 36
> 2l+1|l2
> IlwlI2 + R2
> 36 + 16
> 52

**<u>Question-4</u>** 

### **Statement** 

Assume that Perceptron algorithm is applied to a data set in which the maximum of the lengths of the data points is 4 and the value of margin ( ) is 1. What is the maximum number of mistakes that can be made by the algorithm on this data? 

### **Options** 

#### **(a)** 

#### **(b)** 

#### **(c)** 

#### **(d)** 

### **Answer** 

(c) 

### **Solution** 

> **[Extracted Question]**
> R = 4

#mistakes 

## **<u>Question-5</u>** 

### **Statement** 

Assume that each of the four corners of a unit square represents a data point. Each of these data points can either be assigned a positive class or a negative class. 

(a) How many different data sets (as per different assignments of positive and negative labels) will be possible using these data points? 

(b) Out of those data sets, how many will the Perceptron algorithm be able to correctly classify? 

### **Options** 

#### **(a)** 

(a): 8, (b): 4 

#### **(b)** 

(a):8, (b): 6 

#### **(c)** 

(a): 16, (b): 14 

#### **(d)** 

(a):16, (b):12 

### **Answer** 

(c) 

### **Solution** 

(a) Each corner can be assigned either a positive class or a negative class. Hence there are two possibilities for each corner, resulting into a total of 2^4 = 16 possibilities. 

(b) The following two data sets will not be linearly separable. 

## **<u>Question-6</u>** 

### **Statement** 

Assume that you trained a Perceptron and after training got finished, you found that the data that was used for training had been accidentally labeled opposite to what it should have been, i.e., every example that was labelled +1 should have been a -1, and vice versa. 

Assume that you no longer have the data and have no ability to change the code that uses the perceptron to flip its answers. All you have access to is the weight vector of the perceptron ( ). How would you change the weights to obtain in order to flip all the answers? You may assume that there are no data points that fall exactly on the boundary between the two classes. 

### **Options** 

#### **(a)** 

#### **(b)** 

#### **(c)** 

#### **(d)** 

### **Answer** 

(a) 

### **Solution** 

will predict a positive class and will predict a negative class. 

If we only have access to the weights, we can negate the weight vector, i.e., 

So that wherever and we get a positive class as a prediction, and hence will predict a negative class, and vice versa. 

## **<u>Question-7</u>** 

### **Statement** 

Assume that in the truth tables of logic gates OR, AND and XOR, every occurrence of 0 is replaced by -1 and every occurrence of 1 is replaced by +1. In this way, three different data sets are generated respectively. 

Perceptron algorithm will not be able to correctly classify the data set produced by which of the three gates? 

### **Options** 

#### **(a)** 

OR 

#### **(b)** 

AND 

#### **(c)** 

XOR 

#### **(d)** 

None of these 

#### **(e)** 

All of these 

### **Answer** 

(c) 

### **Solution** 

Following will be the datat sets generated: 

|||**OR**|**AND**|**XOR**|
|---|---|---|---|---|
|-1|-1|-1|-1|-1|
|-1|1|1|-1|1|
|1|-1|1|-1|1|
|1|1|1|1|-1|

XOR data set is similar to what we saw in Q5, and is not linearly separable. 

**<u>Question-8</u>** 

### **Statement** 

Consider the following three data sets, where a white circle represents a negative class and a black circle represents a positive class: 

> **[Extracted Question]**
> 0

<!-- Start of picture text -->
1.<br><!-- End of picture text -->

> **[Extracted Question]**
> 2

<!-- Start of picture text -->
2.<br><!-- End of picture text -->

<!-- Start of picture text -->
3.<br><!-- End of picture text -->

Which of these data sets will the Perceptron Algorithm be able to correctly classify? 

### **Options** 

#### **(a)** 

1 only 

#### **(b)** 

1 and 3 

#### **(c)** 

2 only 

#### **(d)** 

3 only 

#### **(e)** 

All of these 

#### **(f)** 

None of these 

### **Answer** 

(f) 

### **Solution** 

None of the data sets is linearly separable. 

## **<u>Question-9</u>** 

### **Statement** 

Consider two points and with value of 10 and -10 respectively. Let and be the probabilities returned by Logistic Regression for these two data points. Which of the following is correct? 

### **Options** 

#### **(a)** 

will be same as 

. 

#### **(b)** 

will be much higher than . 

#### **(c)** 

will be much higher than . 

### **Answer** 

(c) 

### **Solution** 

> **[Extracted Question]**
> 1
> 1 + elo
> ~10
> 1 + e

Hence, will be much higher than .