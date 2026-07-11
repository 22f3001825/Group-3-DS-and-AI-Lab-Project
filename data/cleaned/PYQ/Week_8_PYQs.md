# <u>Week 8 Types of Model and Naive Bayes Algorithm</u>

Jan 2024 Term - Quiz 2

> **[Extracted Question]**
> Question 8
> 640653770622
> Total Mark
> 0.00
> Type
> COMPREHENSION
> Based on the above data, answer the given subquestions
> Consider
> naive Bayes model is trained 0n the following data matrix
> X of
> (d,n) and corresponding label vector y:
> T =
> y = [1
> 0 1
> 1jT"
> Assume that p and py;
> are
> estimates for
> =1) and P(f;
> Ily
> Yi) .
> respectively: Here; fa;
> i =4,.2.3is the ith feature:
> These parameters are estimated using MLE.
> shape
> P(y

> **[Extracted Question]**
> Question 9
> 640653770623
> 6
> Parent QN
> View Solutions (0)
> Total Mark
> 3.00 | Type
> SA
> Calculate the value of p;
> Answer (Numeric):
> Answer
> View

## Solution

> **[Extracted Question]**
> Zi-1l(fi
> =
> 1 , Yi = y)
> P i
> 2"-1l(;
> =
> y)
> 2i-1l(fz
> =
> 1 , Yi = 1)
> 0 + 0 + 0 + 1
> p2
> Zi=1l(yi = 1)
> 1 + 0 + 1 + 1

> **[Extracted Question]**
> Question 10
> 640653770624
> View Parent QN
> View Solutions (0)
> Total Mark
> 3.00 | Type
> SA
> Calculate the value of pi
> Answer (Numeric):
> Answer

## Solution

> **[Extracted Question]**
> Zi-1l(fi
> =
> = 1)
> 1 + 0 + 0 + 0
> Pi
> 2i-1l(yi
> =
> 1)
> 1 + 0 + 1 + 1
> 3
> 1 , Yi

> **[Extracted Question]**
> Suppose you have a five-class classification problem where class label y € (0,1,2,3.4) and
> each training example I; has binary features f1, f2, fs € (0.1).
> How many parameters
> do we need to know to classify
> am
> example using Naive Bayes classifier?
> Answer (Numeric):
> Answer

## Solution

Decide labels = 5 - 1 = 4 Estimate each features under each label = 2 - 1 = 1 Estimate all features under each label = 1 + 1 + 1 =3 Estimate all features under all labels is 3 + 3 + 3 + 3 + 3 =15 Total parameters we need to know is 15 + 4 = 19

> **[Extracted Question]**
> y
> f2
> f3
> f2
> f3
> ^^
> KN
> AA
> KN
> 1   01  0 1   0
> 01   0 1   0
> y =4

y = 0 y = 4
f1 f2 f3 f1 f2 f3
1 0 1 0 1 0 1 0 1 0 1 0

May 2024 Term - Quiz 2

> **[Extracted Question]**
> Question 24
> 640653852845
> Total Mark
> 0.00
> Type
> COMPREHENSION
> Assume that there is no smoothing: Answer the given subquestions:
> Consider the
> following dataset for a binary classification problem in which
> the features   are from {0,1}3 and the labels are
> {0, 1}.
> X =
> Y = [1
> 01
> A Naive Bayes classifier is trained on this dataset_
> The parameters to be
> estimated are represented as p4 , which are presented in the form of the
> table given below . Recall that   PY is the probability of feature i
> value
> in class y:
> from
> taking

## Solution

||=
=  =
pml
y
n
∑<sup>n</sup>
i= 1
i
4
8
1
2|
|---|---|
||=
p
y
j
1 f= 1 ,y=y
1 y=y
∑<sup>n</sup>
i= 1
i
j
i
∑<sup>n</sup>
i= 1 <sup>( i</sup>
)|
|i|y= 0
y= 1|
|1|1
4
3
4|
|2|3
4
2
4|
|3|2
4
3
4|

> **[Extracted Question]**
> Question 25
> 640653852846
> 6 View Parent QN
> View Solutions (0)
> Total Mark
> 2.00
> Type
> SA
> Find the value of c + d.
> Answer (Numeric):
> Answer

Solution 3 2 5 +  =  = 1.25 4 4 4

> **[Extracted Question]**
> Question 26
> 640653852847
> 6 View Parent QN
> View Solutions (0)
> Total Mark
> 2.00
> Type
> SA
> Find the value of a +C + e
> Answer (Numeric):
> Answer

## Solution

1 3 2 +  +  = 1.50 4 4 4

> **[Extracted Question]**
> Question 27
> 640653852848
> 6 View Parent QN
> View Solutions (0)
> Total Mark
> 2.00
> Type
> SA
> Find the predicted label for the
> test
> Answer (Numeric):
> Answer
> point

## Solution

> **[Extracted Question]**
> Pl
> 1
> Xtest _
> test
> 0
> Xtest_
> test
> 0
> otherwise
> P( ,
> Itest

> **[Extracted Question]**
> Pl
> 1
> P(
> ly
> 1 ) P(_
> 1)
> test
> test
> test
> Pl xtest
> [0
> 1
> 0 ]lyt
> test
> 1) P( test
> 1)
> (1-f;)
> I6) (-P)"
> X
> 2
> x4
> X
> 1
> 2
> 4
> 0.015625
> Xtest /
> Xtest!

> **[Extracted Question]**
> test
> 0 | Xtest _
> P( Xtestly test
> 0 ) P( test
> P( xtest
> [0
> 1
> 0 ]lyt
> test
> 0) PG_
> test
> 0)
> [II6"y (-p%"-ra-p
> 3
> X
> x4
> 4
> 4
> 2
> 0.046875
> Pl

> **[Extracted Question]**
> 0.046875
> 0.015625
> ==
> P(
> 0 | Xtest )
> P([
> 1
> Xtest )
> test
> y
> test
> test

> **[Extracted Question]**
> Question 28
> 640653852849
> Total Mark
> 0.00
> Type
> COMPREHENSION
> Consider
> a multi-class classification problem with 3 classes and
> 4 features, all of which are binary: A
> generative model is used to model the joint distribution of the features and labels Based on the above
> data, answer the given subquestions_

> **[Extracted Question]**
> Question 29
> 640653852850
> 0 View Parent QN
> View Solutions (0)
> Total Mark
> 2.00 | Type
> SA
> Find
> the
> total
> number
> of
> independent   (free)
> parameters
> the
> modelif
> the
> class
> conditional
> independence assumption is not enforced:
> Answer (Numeric):
> Answer

## Solution

> **[Extracted Question]**
> Number of parameters
> (k -
> 1) + (2d _ 1)
> +
> +
> (2d
> =k -1 +
> k(2d)
> ~k
> k(2d)
> - 1
> 3(24)
> 1
> 47

> **[Extracted Question]**
> Question 30
> 640653852851
> 6
> Parent QN
> View Solutions (0)
> Total Mark
> 2.00
> Type
> SA
> Find
> the
> total
> number
> of
> independent  (free)   parameters
> the
> model if   the
> class
> conditional
> independence assumption is enforced:
> Answer (Numeric):
> Answer
> View

## Solution

Decide labels = 3 - 1 = 2 Estimate each features under each label = 2 - 1 = 1 Estimate all features under each label = 1 + 1 + 1 + 1 =4 Estimate all features under all labels is 4 + 4 + 4 =12 Total parameters we need to know is 2 + 12 = 14

September 2024 Term - Quiz 2

> **[Extracted Question]**
> Question 5
> 6406531021045
> Total Mark
> 0.00
> Type
> COMPREHENSION
> Based on the above data, answer the given subquestions
> binary classification dataset has 2000 data points belonging to {0,1}?.
> Naive
> algorithm
> was run 0n the same
> dataset , resulting in the
> following estimates:
> P. estimate for Ply = 1) = 0.4
> Pi. estimate for P(fi = 1|y = 0) = 0.25
> p9,
> estimate for P(f2 = 1|y = 0) = 0.35
> Pi, estimate for P(fi = 1y =1) = 0.15
> PI , estimate for P(f2 = 1|y = 1) = 0.05
> Bayes

> **[Extracted Question]**
> Question 6 : 6406531021046
> 6 View Parent QN
> View Solutions (0)
> Total Mark
> 4.00
> Type
> SA
> What is the estimated value of P(f2 = 0 | y = 1)?
> Write Your answer correct to two decimal places.
> Answer (Numeric):
> Answer

## Solution

- P(f2 = 0|y = 1 = 1 ) 0.05 = 0.95

> **[Extracted Question]**
> Question 7 : 6406531021047
> 6 View Parent QN
> View Solutions (0)
> Total Mark
> 3.00
> Type
> SA
> What will be the predicted label for
> the data
> [1. 0]2
> Answer (Numeric):
> Answer
> point

## Solution

> **[Extracted Question]**
> Pl
> 1
> Xtest _
> test
> 0
> Xtest_
> test
> 0
> otherwise
> P ,
> Itest

> **[Extracted Question]**
> Pl
> 1
> P(
> ly
> 1 ) P(_
> 1)
> test
> test
> test
> P
> Xtest
> [1 0 ]lye
> test
> 1) P( ;
> test
> 1)
> (1-f;)
> II6;) (-P)
> =1
> (0.15 X 0.95)
> X 0.4
> 0.057
> Xtest /
> Xtest!

> **[Extracted Question]**
> P( test
> 0 | xtest _
> P( Xtestly test
> 0 ) P( test
> P( xtest
> [1 0 ]l y test
> 0) P( test
> 0)
> II6"Y (-p)"-rla-p
> (0.25 X 0.65) X0.6
> 0.0975

> **[Extracted Question]**
> 0.0975
> 0.057
> P(
> test
> 0 | xtest)
> P( test
> 1
> Xtest )
> y
> 0
> tcst

> **[Extracted Question]**
> Question 10
> 6406531021044
> View Solutions (0)
> Total Mark
> 4.00
> Type
> SA
> Suppose you want to use
> a Naive Bayes classifier to predict whether a student will pass or fail an
> exam based
> on two features: the number of hours they studied and whether they attended review
> sessions. Assume that the features are conditionally independent given the exam outcome and that the
> variances of the study hours distributions are equal for both pass and fail categories:
> How many parameters are required to classify a new student using this Naive Bayes classifier?
> Answer (Numeric):
> Answer

## Solution

Decide label = 2 - 1 =1

Parameter of feature f1 = 𝜇1 , 𝜇2 , Σ Parameter of feature f2for each label = 2-1 = 1 Parameter of feature f2for all label = 1 + 1 = 2 Total parameters we need to know is 1 + 3 + 2 = 6