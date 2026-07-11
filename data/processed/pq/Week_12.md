# **Practice** 

## **Common Instructions for uestions 1-3** **<u>q</u>** 

Consider the following data set containing one feature: 

|**x**|**y**|
|---|---|
|1|+1|
|-1|+1|
|-3|-1|
|-2|-1|

Consider and . 

## **<u>Question-1</u>** 

### **Statement** 

If , what will be the value of 0-1 loss for this data? 

### **Answer** 

0 (No range required) 

### **Solution** 

Zero-one loss: if , then loss = 0, else 1 

Here, 

||||**y**|
|---|---|---|---|
|1|1+1 = 2|+1|+1|
|-1|-1+1 = 0|+1|+1|
|-3|-3+1 = -2|-1|-1|
|-2|-2+1 = -1|-1|-1|

Since for all data points, zero-one loss = 0 

## **<u>Question-2</u>** 

### **Statement** 

What will be the value of squared loss, i.e., where ? 

Note: For this loss, use wherever . 

### **Answer** 

7 (No range required) 

### **Solution** 

|||**y**||
|---|---|---|---|
|1|1+1 = 2|1|1|
|-1|-1+1 = 0|1|1|
|-3|-3+1 = -2|0|4|
|-2|-2+1 = -1|0|1|

Hence squared loss = 1+1+4+1 = 7 

## **<u>Question-3</u>** 

### **Statement** 

What will be the value of hinge loss, i.e., ? 

### **Answer** 

1 (No range required) 

### **Solution** 

||||||**Hinge loss**|
|---|---|---|---|---|---|
|1|1+1 = 2|+1|2|-1|0|
|-1|-1+1 = 0|+1|0|1|1|
|-3|-3+1 = -2|-1|2|-1|0|
|-2|-2+1 = -1|-1|1|0|0|

Total error = 0+1+0+0 = 1 

## **<u>Question-4</u>** 

### **Statement** 

Given a cat image, you want to classify which of the 10 cat breeds it belongs to, using a neural network. 

Which loss function will be appropriate? 

### **Options** 

#### **(a)** 

0-1 Loss 

#### **(b)** 

Cross entropy Loss 

#### **(c)** 

Squared Loss 

#### **(d)** 

Hinge Loss 

### **Answer** 

(b) 

### **Solution** 

It's a multi-class classification problem.  Hence, cross entropy loss will be correct. 

(0-1 loss is non-continuous and non-differentiable 

Squared loss is not an appropriate loss for classification. 

Hinge loss is used for binary classification.) 

**<u>Question-5</u>** 

### **Statement** 

Assume that and for a data point . What will be the value of the cross-entropy loss? 

### **Answer** 

0.5146 (Range: 0.50 to 0.55) 

### **Solution** 

Cross- entropy loss = 

## **<u>Question-6</u>** 

### **Statement** 

Following is the output produced by an activation function at some hidden layer of a neural network: 

[0, 4.9, 0, 5.2, 7.4, 0] 

Which of the following could possibly be the activation function? 

### **Options** 

#### **(a)** 

Sigmoid 

#### **(b)** 

ReLU 

#### **(c)** 

Tanh 

### **Answer** 

(b) 

### **Solution** 

Sigmoid transforms values in the range -1 to 0. So, it may not be correct. 

Tanh transforms values between -1 and 1, so, it may not be correct. 

ReLU transforms negative values to zero, and keeps the positive values as it is, so it may be the activation function used. 

**<u>Question-7</u>** 

### **Statement** 

Consider a neural network with 3 inputs and one output. If there are 3 hidden layers each with 3 neurons, how many parameters need to be learnt by the back-propagation algorithm? 

Note: Assume that each hidden and output layer neuron also contains a bias. 

### **Answer** 

40 (No range required) 

### **Solution** 

> **[Extracted Question]**
> X2
> X3
> input
> Hidden
> Hidden
> Hidden
> Output
> layer
> layer 1
> layer 2
> layer 3
> layer

#weights from input to hidden layer 1= 3*3 = 9 

#weights from hidden layer 1 to hidden layer 2= 3*3 = 9 

#weights from hidden layer 2 to hidden layer 3= 3*3 = 9 #weights from hidden layer 3 to output layer= 3*1 = 3 

Total number of neurons = 10 Hence, number of bias terms = 10 

Therefore, total number of parameters to be computed = 9+9+9+3+10 = 40 

## **<u>Question-8</u>** 

### **Statement** 

Which of the following is/are true? 

### **Options** 

#### **(a)** 

Both Sigmoid and Softmax are activation functions. 

#### **(b)** 

Sigmoid is used for binary classification tasks, while SoftMax applies to multiclass problems. 

#### **(c)** 

SoftMax function is an extension of the Sigmoid function. 

#### **(d)** 

Sigmoid function is also called Logistic function. 

#### **(e)** 

Both functions transform a real value to a number between 0 and 1. 

### **Answer** 

(a), (b), (c), (d), (e) 

### **Solution** 

Softmax function is a generalization of sigmoid function, to be used in multi-class classification, such that of there are k classes, the sum of probability values returned for each of these classes is equal to 1.