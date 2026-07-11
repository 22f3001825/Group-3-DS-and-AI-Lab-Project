# **Perceptron and Logistic Regression** 

✉ 23f1001171@ds.study.iitm.ac.in (Piush Das) 

## Perceptron Learning Algorithm 

The Perceptron Learning Algorithm (PLA) is a supervised learning algorithm widely employed for binary classification tasks. Its primary objective is to determine a decision boundary that effectively separates the two classes in the dataset. This algorithm belongs to the class of discriminative classification methods as it focuses on modeling the boundary between classes instead of characterizing the underlying probability distribution of each class. 



### The algorithm is based on two assumption: 



2. Linear Separability Assumption: The Linear Separability Assumption is a fundamental assumption made in various machine learning algorithms, It assumes that the classes to be classified can be accurately separated by a linear decision boundary 







### The objective function is defined as follows 



Even if H accounts only for the Linear Hypotheses, this problem is generally considered NP-Hard. Under the Linear Separability Assumption, T assuming the existence of w ∈ R<sup>d</sup> such that sign w xi = yi holds for all i ∈ 1, . . . , { n}, the Perceptron Learning Algorithm solves the convergence problem using an iterative algorithm. 

✉ 23f1001171@ds.study.iitm.ac.in (Piush Das) 

## Perceptron Algorithm 



- else 



end 

### Mistakes by Algorithm 

### Case I 





✉ 23f1001171@ds.study.iitm.ac.in (Piush Das) 

Case II 



Actual = 1 



This update rule effectively adjusts the decision boundary in the direction of correct classification for the misclassified example. The algorithm is guaranteed to converge to a linearly separable solution if the data is indeed linearly separable. However, if the data is not linearly separable, the perceptron algorithm may not converge to a solution. 

✉ 23f1001171@ds.study.iitm.ac.in (Piush Das) 

## Assumptions 

### Linear Seperability with  Margin𝛾 



### Radius Assumption 

∀i ∈ D ‖x ‖i 2 ⩽ R for some R > 0 




x : wTx = 𝛾<br>x : wTx = 0<br>x : wTx = - 𝛾<br>

✉ 23f1001171@ds.study.iitm.ac.in (Piush Das) 

### Normal Length for w<sup>*</sup> 

Without Loss of Generality, we assume ‖w*‖ = 1 




T<br>w* 𝛾<br>x =<br>‖w*‖ ‖w*‖<br>*' T '<br>w x = 𝛾<br>

✉ 23f1001171@ds.study.iitm.ac.in (Piush Das) 

## Analysis of Mistake of Perceptron 

### Upper bound 

Observe that an update happens only when an mistake occurs Assume that the perceptron has gone through  updates. Let l (x, y) be some point that is misclassified by the perceptron at this stage. This is the l<sup>th</sup> mistake that it is seeing. As the current weight vector of the perceptron is w<sup>l</sup> , we have 



This necessitates one more round of weight update. The update rule for this step is as follows: 



Let us now look at the norm of the weight vector and see how it changes across iterations: 





We have used three facts to get the inequality 



We can now apply this inequality recursively on the earlier rounds 







(0) We have used the fact that w = 0 Therefore, the upper bound is: 



✉ 23f1001171@ds.study.iitm.ac.in (Piush Das) 

### Lower bound 

Now, we look at the relationship between the optimal weight vector w<sup>*</sup> and the weight vector w(<sup>t+1</sup> ) The dot product is a measure of this relationship 



We can now apply this inequality recursively on the earlier rounds 





(0) We have used the fact that w = 0 Therefore, the Lower bound is: 



✉ 23f1001171@ds.study.iitm.ac.in (Piush Das) 

Now, we use the Cauchy-Schwartz inequality and the assumption that ||w*|| = 1 to get: 



### Combining the bounds 

l + 1 2 We now have a lower bound and an upper bound for ‖w ‖ 







## Logistic Regression 

Assumption that perceptron makes of linear separability with probabilistic view 



But, here we are assuming that the probabilty of some datpoints belongs to positive class is 1 and the probabilty of some datpoints belongs to negative class is 0,  Can we model probabilities differently with some relaxation ? 

Start with a simple Linear Model 



T Larger the value of score z = w x more the probabilty of being +1 









✉ 23f1001171@ds.study.iitm.ac.in (Piush Das) 

## Model: Logistic Regression 



Dataset = {(x1 , y1<sup>)</sup> . . . (xn , yn<sup>)}</sup> yi ∈ 0, 1{ } 

### How to Find w Using MLE( ) 



Goal: Maximize Log(L(w)) 



✉ 23f1001171@ds.study.iitm.ac.in (Piush Das) 

### Gradient Update Rule 





### Kernel Version 



Regularised Version 



✉ 23f1001171@ds.study.iitm.ac.in (Piush Das) 

## **Reference** 

**_Arun Raj Kumar, Lecture Slides for Machine Learning Techniques Karthik Thiagarajan, Machine Learning Techniques Github Notes. Indian Institute of Technology Madras , CS2007 Course Website Stanford University, CS229 Machine Learning Notes_** 

# **Thank You !** 

✉ 23f1001171@ds.study.iitm.ac.in (Piush Das)
