**<u>Practice Questions from Week 5</u>** 

> **[Extracted Question]**
> Question 5
> 640653770609
> Total Mark
> 0.00
> Type
> COMPREHENSION
> Consider a regression problem where you are tasked with predicting the sale prices of houses based on their square footage: You decide to
> experiment with two different models: The training dataset consists of information on 200 houses
> and you use the models to make
> predictions on
> test dataset of 50 houses The Mean Squared Error (MSE) is chosen as the evaluation metric. Based
> on the above data,
> answer the given subquestions
> Model P
> Wq
> WT
> Model Q
> Wo
> Wit + WpT
> Discussions (0)
> Question 6 : 640653770610
> View Parent QN
> View Solutions (1)
> Total Mark
> 3.00
> Type
> McQ
> Considering the specific context of predicting house prices based on square footage, which model is
> more likely to provide accurate
> predictions on the training dataset?
> OPTIONS ;
> Model
> Model Q
> Both models are equally likely to provide accurate predictions
> It depends on the distribution of house prices in the dataset

# **Solution** 

Model P is a simpler linear model with only two parameters (w0 , w1<sup>)</sup> and Model Q is more complex, with three parameters (w0 , w1 , w2<sup>)</sup> . A complex model (Model Q) generally has greater flexibility and can fit the training data more closely compared to a simpler model (Model P). This is because Model Q can capture both linear and quadratic patterns in the data, whereas Model P can only capture linear trends. Therefore, Model Q is more likely to provide accurate predictions on the training dataset because it has greater flexibility to fit the data. 

> **[Extracted Question]**
> Question 7
> 640653770611
> View Parent QN
> View Solutions (0)
> Total Mark
> 3,00
> Type
> MSQ
> Identify the factors that could influence the model's performance on the training dataset in this housing price prediction scenario. Select all
> correct statements:
> OPTIONS
> Model
> may struggle to capture non-linear relationships present in houseprice data_
> Model Q might be sensitive to outliers in the square footage variable:
> The choice between Model
> and Model Q depends on the budget constraintsof potential homebuyers:
> Model Q will always perform well on the test dataset:

# **Solution** 

**a) Model P is a linear regression model and cannot account for non-linear patterns in the data. If house prices have a non-linear relationship with square footage, Model P will struggle to fit the training data accurately.** 

2 **b) Model Q includes a quadratic term** x **, which can amplify the effect of outliers in the square footage variable. This makes it more sensitive to outliers compared to Model P.** 

c) The choice of model depends on the ability to capture relationships in the data, not on external factors like budget constraints of homebuyers. This statement is irrelevant to model performance. 

d) While Model Q may fit the training data better due to its flexibility, overfitting could cause poor generalization to unseen test data. It is not guaranteed that Model Q will always perform well on the test dataset. 

> **[Extracted Question]**
> Question 14
> 640653770613
> View Solutions (0)
> Total Mark
> 3.00
> Type
> Kernel regression with
> polynomial kernel of degree three is applied on
> data set
> {K.y}.
> Let the weight vector be given by
> o(1)p2.3,-1.0,0.4,~0.7]T
> Here 0(1) is the transformed data matrix whose ith column is 0(T;). What will be the
> prediction for the data
> [0, 0,0,0jT?
> Answer (Numeric):
> Answer
> point

# **Solution** 

The prediction of test data point in kernel regression is 

> **[Extracted Question]**
> Za" k(x;
> Xtest_
> 1 =

The given kernel function is 

> **[Extracted Question]**
> Xtest;
> xTxtest;
> 1)
> p(x)
> =
> [1
> 1
> 1
> 1]
> 23
> -1.0
> 2
> a" k(xi
> Xtest )
> [1
> 1 1 1]
> 23 -1 + 0.4 -0.7
> =
> 0.4
> i=1
> -0.7
> k(xi

> **[Extracted Question]**
> Question 16 : 640653770612
> View Solutions (0)
> Total Mark
> 3.00
> Type
> MCQ
> Let  be the data matrix of
> shape (d,n) and y be the corresponding label vector:
> regression
> of the form Yi
> WTTi is fit
> the squared error on the same
> dataset . If the solution W
> to the
> optimization problem is orthogonal to the subspace
> spanned of the data
> (columns of matrix .), what will be the squared error?
> OPTIONS :
> Ilyll?
> Insufficient information t0 answer
> lineat
> model
> using
> point

# **Solution** 

We are given a data matrix 𝑋 of shape (d,n) and a corresponding label vector 𝑦 . A linear regression model of the form 

> **[Extracted Question]**
> V
> wl,

is fit using the squared error on the same dataset. The solution w<sup>*</sup> to the optimization problem is orthogonal to the subspace spanned by the data points (columns of matrix 𝑋 ) We need to determine the squared error. In linear regression, the optimal weight vector w<sup>*</sup> is typically found by minimizing the squared error: 

> **[Extracted Question]**
> min Ily
> XTwll2

here, XTw represents the projection of w onto the columnspace of X , This implies that the projection of 𝑦 onto the column space of 𝑋 is zero 

> **[Extracted Question]**
> Ily
> Oll=

> **[Extracted Question]**
> Ilyll?

> **[Extracted Question]**
> Question 3 : 640653852824
> View Solutions (0)
> Total Mark
> 3.00
> Type
> Consider the
> following training dataset for
> linear regression problem with
> one feature;
> 12
> 0.1
> 2T
> Find the value of w
> the
> weight.
> Answer (Numeric):
> Answer
> optimal

# **Solution** 

> **[Extracted Question]**
> w*
> (xxT)t (Xy)

> **[Extracted Question]**
> 1.2
> 0.1
> X = [1
> -1 2 -2]
> y =
> 2
> -1

> **[Extracted Question]**
> XT
> 2

> **[Extracted Question]**
> XXT
> 10
> (xxT )'
> 10
> Xy =
> 7.3
> 1
> w
> (xxT)" (Xy)
> X 7.3
> 0.73
> 10

> **[Extracted Question]**
> Question 4 : 640653852825
> View Solutions (0)
> Total Mark
> 3.00
> Type
> Consider the
> following dataset for
> kernel regression problem with
> polynomial
> kerne] of
> LWO
> With the coefficient vector 0:
> ~0.625
> x= [' ?
> e=
> If the prediction for the data-point
> is 0, find the value of 01.
> Answer (Numeric):
> Answer
> degree
> aloug

# **Solution** 

The prediction of test data point in kernel regression is 

> **[Extracted Question]**
> a" k(xi
> Xtest_
> i =

The given kernel function is 

> **[Extracted Question]**
> k(xi
> (xT xtest;
> +
> 1)2
> x(aI[:))
> (1 oH1]+1) = 4
> xUxHih
> (o 141/+1) = 4
> (aJi)
> (-1 o41/+1) = o
> (l9JI:])
> ([o -1][1]+1)
> = 0
> Xtest;

> **[Extracted Question]**
> Ea" k(x;
> Xtest )
> = 0
> i=1
> ==
> 01(4) + 02(4) + 03(0) + 04(0)
> ==
> 01(4)
> 0.625 X 4
> = 0
> ==
> 01(4)
> 0.625 X 4
> 0.625 X 4
> ==
> Q1
> =
> C1
> 0.625

> **[Extracted Question]**
> Question 6
> 640653852827
> Total Mark
> 0.00
> Type
> COMPREHENSION
> Based on the above data, answer the given subquestions:
> Consider
> linear regression problem that has two features with
> training dataset of
> 10.000
> The blue
> in the image below is the weight vector.
> aL somC
> iteration of gradient descent.
> W2, Wg are unit vectors. Specifically; W1 is & unit vector
> the direction of the gradient at this point:
> Wg
> V1o
> WI =
> val:]
> W2 =
> 1[=
> Viol-
> W(t)
> points.
> point
> Wa
> w(t)

> **[Extracted Question]**
> Question 7 : 640653852828
> View Parent QN
> View Solutions (0)
> Total Mark
> 2.00
> Type
> If the next iteration of
> gradient descent is
> expressed as w(t+l) = wl) + TWk with n > 0,
> what would be the value of k?
> Answer (Numeric):
> Answer
> Check Answer

# **Solution** 

2 (Visual Inspection) 

> **[Extracted Question]**
> Question 8 : 640653852829
> View Parent QN
> View Solutions (0)
> Total Mark
> 2.00
> Type
> If w()
> and 1
> find
> Ilw(+V)6,
> 0.1
> Vio
> where
> We use the usua]
> Lz
> nOFM.
> Answer (Numeric):
> Answer

# **Solution** 

> **[Extracted Question]**
> w(t+1)
> wt
> nwk
> |0.4
> X
> 0.1
> V1o
> 10)
> 0.4
> 0.3
> 0.1
> 0.1
> Ilz
> V(o.1)2
> (0)2
> 0.1

> **[Extracted Question]**
> Question 2 : 6406531021341
> Total Mark
> 0.00
> Type
> COMPREHENSION
> Based on the above data
> answer the given subquestions:
> Kernel regression with
> polynomial kernel is applied on the following
> dataset with two features:
> X =
> 9
> y = [2,1,2]"
> Weight
> vector can be written
> 45  W
> p( XJa; where 0 is the
> transformation mapping corresponding to the kernel
> Ti) = (1 +
> Hi;)?. The vector a
> is given by (K)-ly;
> where K is the kernel matrix:
> K(T .

> **[Extracted Question]**
> Question 3 : 6406531021342
> View Parent QN
> View Solutions (0)
> Total Mark
> 3.00
> Type
> MCQ
> Compute K.
> OPTIONS :
> (1h
> (19
> (1h
> (1h

# **Solution** 

> **[Extracted Question]**
> Given k(xi
> Xj)
> =
> (1 +
> xTx;)?
> x(leJla))
> 1 + [1
> olsl) = (+1 = 2
> = 4
> x(lsl:h)
> +[1
> ode]
> = 1
> x(lalleh)
> + [1
> oe]
> =
> 4 1
> k =
> 1 4
> 1
> 1 1 1

> **[Extracted Question]**
> Question 4 : 6406531021343
> Parent QN
> View Solutions (0)
> Total Mark
> 4,00
> Type
> What will be the prediction for the data
> point [1, ~1JT? Enter the answer correct
> to two decimal places
> Answer (Numeric):
> Answer
> View

# **Solution** 

> **[Extracted Question]**
> We Know ,
> a*
> = K-ly
> 4 1
> 0
> -3
> 3
> -3
> 3
> 0
> -3
> K =
> 1 4 1
> M =
> 0   3
> 3
> 0
> 3
> -3
> cT
> Adj
> 0
> 3
> -3
> -3
> 3
> 15
> -3
> -3
> 15
> -3
> -3
> 15
> 3
> 0
> Adj
> -3
> 1
> 3
> -3
> K-1
> 0
> 3
> det(K)
> 3
> -3
> -3
> 15
> 3 =
> 5
> K-1

> **[Extracted Question]**
> 1
> 0
> 0
> 3
> 0
> 3
> H
> 1
> 1
> 5
> 3
> 3
> K-Ty =

> **[Extracted Question]**
> Given k(xi
> Xj)
> =
> (1 + x7x;)
> x(al-:]
> /1 + [1
> o-| =a+1
> = 22
> =
> x(leH[:1)
> +[0
> 141
> = (1 - 1)2 = 0
> UcH[-1
> +[0
> o[-]
> = 12 = 1
> K = [4 0 1]

> **[Extracted Question]**
> We Know ,
> ax*
> Xtest_
> k(x;

> **[Extracted Question]**
> 0
> [4 0 1] =
> 2.33
> 3
> =1
> {

> **[Extracted Question]**
> Question 21: 6406531021344
> View Solutions (0)
> Total Mark
> 3.00
> Type
> MSQ
> Consider
> regression
> with loss
> L(w)
> Ya)?
> where
> are the d-diensional
> training data points and y'$ are their
> corresponding labels:
> For the
> weight
> Vector W
> which among the following is correct?
> OPTIONS
> OIf we double all the values of yi. w"
> will also get doubled:
> If we double all the values of yi, w"
> will get halved.
> If we double all the values of T;, w
> will get halved:
> 0If we double all the values of
> will also get doubled:
> E(wl ,
> lineat
> model
> optimal
> Ii;

# **Solution** 

(a) , (c) 

> **[Extracted Question]**
> We Know, L(w)
> (wTxi
> ya)
> i=l
> w*
> (xxT) ' Xy

If we double all the values of yi 

> **[Extracted Question]**
> w'
> (xxT) x(y)
> w'
> 2( (xxT)  Xy)

w' = 2w* 

if we double all the value of xi 

> **[Extracted Question]**
> w'
> ((2X)(2x2)) (2Xly
> w'
> (4xx")t (2X)y
> w'
> (xxt)  (2Xy
> 4
> 1
> '
> X
> 2((xxt)tXy)
> w'
> 1
> ((xxt)  Xy)
> w'
> w"
> 2