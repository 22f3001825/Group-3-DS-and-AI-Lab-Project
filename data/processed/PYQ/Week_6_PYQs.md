# <u>Week 6 Cross Validation and Ridge and Lasso Regression</u> 

# - <u>January 2024 Term Quiz 2</u> 

> **[Extracted Question]**
> Based on the above data, answer the given subquestions:
> Consider
> datasel wich the
> following data
> and the target variable:
> Sample No
> 13
> The linear regression model is given by y = Wo +
> Assume that the
> LeaveOne-Out Cross-Validation technique is
> Discussions (0)
> Question 12 : 640653770615
> View Parent QN
> View Solutions (0)
> Total Mark
> 4.00
> Type
> Enter the vale of W1 obtained
> when the 3rd sample is used as
> the validation data point.
> Answer (Numeric):
> Answer
> Check Answer
> points
> WT.
> applied,

## Solution 

> **[Extracted Question]**
> w*
> (xXT)" (Xy)
> 1
> x =[3
> 0
> 6]andy
> 3
> 13
> 3
> XT
> 1
> 0
> 6
> 3
> 9
> XXT
> 9
> 45
> (xxT)'
> 45
> 6
> 54
> -9
> 3
> 1
> 35
> 18
> 8
> 24
> Xv = [5 & &]
> 3
> 102
> 13

> **[Extracted Question]**
> 120
> 102
> (xxT)"
> 6
> 6
> 24
> 3
> (Xy)
> 1
> 1
> 102
> -72
> + 102
> 1.67
> 6
> 18
> 18

> **[Extracted Question]**
> Question 13 : 640653770616
> 0 View Parent QN
> View Solutions (1)
> Total Mark
> 4.,00
> Type
> MCQ
> What will be the predicted value for the left-out data point?
> OPTIONS
> 12.3
> 11.3
> None of these

## Solution 

> **[Extracted Question]**
> y
> 3 +
> 1.67x
> y
> 3
> 1.67(5)
> 11.33

> **[Extracted Question]**
> Question 17 : 640653771205
> View Solutions (0)
> Total Mark
> 4.00
> Type
> MCQ
> Given
> design matrix   €
> and
> target vector Y € Rnxl_
> where d represents the
> number of features.
> represents the number of data points; and the data is defined as:
> T=
> 3
> Y =
> [5]
> Calculate the coefficients B for Ridge regression with A = 1
> OPTIONS :
> 8 = [0.5,0.5]
> 8 = [1,0.5]
> 8 = [0.54,0.88]
> p =
> [0.67. 0.33]
> None of these
> Rdk"

Solution 

Given, 

> **[Extracted Question]**
> 1 2
> 3
> X =
> y
> 3 4
> 5

We Know, 

> **[Extracted Question]**
> W R
> (xx" + AI)
> Xy
> 1
> 3
> AJz :]+[s %]) [: 2H[3
> 4
> 5  11 |
> +[8 %]) 
> 13
> 11 25_
> 29
> 11
> 13
> 11
> 26
> 29
> 26
> -11
> 13
> 35
> -11
> 29
> 19
> 35
> 31
> 0.54
> 0.88

> **[Extracted Question]**
> 8
> [0.54
> 0.88

# - <u>May 2024 Term Quiz 2</u> 

> **[Extracted Question]**
> Question 9 : 640653853168
> Total Mark
> 0.00
> Type : COMPREHENSION
> Based on the above data, answer the given subquestions
> dataset for ridge regression has 1000 data-points  k-fold cross validation is performed
> to estimate the value of A in ridge regression with k = 4
> For & given value of A:
> Discussions (0)
> Question 10 : 640653853169
> Parent QN
> View Solutions (0)
> Total Mark : 1.50 | Type : SA
> How many models have to be trained?
> Answer (Numeric):
> Answer
> View

## Solution 

K = 4 

Therefore 4 Models Will be Trained 

> **[Extracted Question]**
> Question 11
> 640653853170
> View Parent QN
> View Solutions (0)
> Total Mark : 1.50 | Type
> SA
> While training each of these models; how many data-points does the training
> have?
> Answer (Numeric):
> Answer
> set

## Solution 

n = 1000 k = 4 1000 Number of datapoints in each fold = = 250 4 

∴ While Training Models, 3 × 250 = 750 datapoints will be present in training set 

> **[Extracted Question]**
> Question 12 : 640653853171
> Total
> Mark
> 0,00
> Type : COMPREHENSION
> Based on the above data, answer the given subquestions:
> Consider the
> following image of the parameter space in
> regression problem
> with regularization.
> is the sum of squared
> errors
> (SSE) and A is the
> regularization parameter.
> The weight vector is W
> [w1
> We]
> The contours of
> and the
> regularization
> term In
> the loss are
> displayed
> f(w) = C1
> f(w) = C
> 01
> Discussions (0)
> Question 13
> 640653853172
> Vlew Parent QN
> Vlew Solutions (1)
> Total Mark : 1.00
> Type : MCQ
> What kind of
> regression problem is this?
> OPTIONS
> Ridge regression
> LASSO regression
> below :

## Solution 

- The blue shape in the plot represents the constraint region, which appears to be a diamond  This corresponds to an L1 norm, which is used in LASSO regression. 

- The ellipses represent the contours of the loss function, and the optimal solution is where the contours first touch the constraint region. 

- LASSO regression applies an L1 penalty, which encourages sparsity, meaning some coefficients can become exactly zero. 

Lasso Regression 

> **[Extracted Question]**
> Question 14 : 640653853173
> Vlew Parent QN
> Vlew Solutlons (0)
> Total Mark
> 0.,50
> Type
> What is the optimal value of w1?
> Answer
> (Numeric):
> Answer

> **[Extracted Question]**
> Question 15 : 640653853174
> 0 View Parent QN
> Solutions (0)
> Total Mark
> 0.50
> Type
> What is the optimal value of w2?
> Answer (Numeric):
> Answer
> View

## Solution 

The L1 constraint region (diamond shape) has its corners at points where one weight is zero (e.g) (t, 0 , 0,) ( t) , (-t, 0 , 0,) ( -t) The contour first touches the constraint at (1, 0) meaning w1 = 1 and w2 = 0 

> **[Extracted Question]**
> Question 16 : 640653853175
> View Parent QN
> View Solutlons (0
> Total Mark
> 1.00
> Type
> MCQ
> Which of the following statements is true?
> OPTIONS :
> Feature-1
> can be discarded
> Feature
> can be discarded:
> Any one of the two features can be discarded:
> Both features are
> equally important and neither of them can be discarded

## Solution 

Since optimal value of w2 is 0, thus Feature 2 can be discarded 

> **[Extracted Question]**
> Question 17 : 640653853176
> View Parent QN
> View Solutions (0)
> Total Mark
> 2.00
> Type
> MSQ
> Which of the following statements are true? Exactly two options are correct:
> OPTIONS :
> Oc
> Oc1
> Total loss at optimal point
> +A
> Total loss at optimal point is C2 + A
> is C1

## Solution 

The outer contour represents to f(w) = c1 The inner contour represents to f(w) = c2 Since contours represent levels of SSE, and the goal of regression is to minimize SSE, we know that c1 > c2 

At the optimal point, The regression loss is given by the contour where the constraint is first touched. The optimal solution lies on f(w) = c1 because it is the smallest attainable SSE value within the constraint.Thus, the total loss at the optimal point is : c1 + 𝜆 

# - <u>September 2024 Term Quiz 2</u> 

> **[Extracted Question]**
> Question 8 : 6406531021348
> View Solutions (0)
> Total Mark
> 4.00
> Type
> Consider the
> following dataset:
> D =
> {(1,2). (2,2) . (0,1)}.
> Assume that
> one
> cross validation is applied on this dataset and the model
> used IS y
> Wo +
> W =
> LWo_
> W1]" be the weight obtained when (2.2) is used
> in the validation set.
> Then calculate
> Uwlll:
> Answer (Numeric):
> Answer
> Leave
> out
> Suppose
> W.

## Solution 

> **[Extracted Question]**
> x = [18] x -[1 8
> v = [1
> xxi = [2 1]
> (xxT)'
> [~1
> 3
> Xy = [i&ll:] - [

> **[Extracted Question]**
> 1
> -1 Il3 |
> (xXT) ' Xy
> -1
> 2 Il2
> =i
> Iw*

> **[Extracted Question]**
> Ilw*|VZ
> ="i/uz
> (Vi2
> +
> 12)2
> = 2

> **[Extracted Question]**
> Question 15 : 6406531021345
> Total Mark
> 0.00
> Type
> COMPREHENSION
> Based on the above data, answer the given subquestions_
> Consider the following
> regression model
> Ti =Wfi+ti;
> where the noise
> Normal(o,1).
> Discussions (O)
> Question 16 : 6406531021346
> View Parent QN
> View Solutions (0)
> Total Mark
> 2.00
> Type
> MCQ
> For some A > 0, where A € R;
> MSE of WML is greater than MSE of
> OPTIONS :
> TRUE
> FALSE
> lincar
> WRidge"

## Solution 

In the absence of regularization, the MLE of w is simply obtained by minimizing the sum of squared errors (SSE), which results in 

> **[Extracted Question]**
> w*
> (xxT)'
> (Xy)

Ridge regression introduces an l2 - norm penalty to the loss function 

> **[Extracted Question]**
> w
> (xxT + AI)"
> Xy

The regularization parameter λ>0 reduces the variance by shrinking the weight values, potentially leading to a lower Mean Squared Error (MSE) 

> **[Extracted Question]**
> for any 1
> 0 The MSE of w
> The MSE 0f

> **[Extracted Question]**
> Question 17 : 6406531021347
> View Parent QN
> View Solutions (0)
> Total Mark
> 4.00
> Type
> McQ
> Consider the Bayesian formulation of the
> linear regression problem.  where
> the
> for W iS assumed to be
> Laplace(0.2/A).
> Then , which among the following
> is true?
> Hint: If 4 ~ Laplace(u.b) . then
> fx(1)
> e-/r-01/b.
> 26
> OPTIONS
> WMAP
> arg min
> '(w I;
> 9a)? + Allwl; where Hwl? =
> ATg mnax
> Allwll?; where |wll? =
> WMAP
> aTg min
> Yi)? + Allwll; where |wllh =
> WMAP =
> max
> Zk =
> yi)? + Allwlli, where Uwlhi = Z
> prior
> ("l _
> "a)?_
> WMAD
> (wt _
> arg !

## Solution 

> **[Extracted Question]**
> 2
> t
> Laplace

We need to determine the correct form of the Maximum A Posteriori (MAP) Estimation for 𝑤, given this prior. The Laplace distribution has a PDF 

> **[Extracted Question]**
> fx(x)

> **[Extracted Question]**
> Given, w
> Laplace 
> 2
> we set Ul
> 0 and b
> 2
> so the PDF simplifies to

> **[Extracted Question]**
> 2
> fx(x)
> 2
> X
> 2
> =^ Iwl
> fx(x)
> 4
> P(x)
> IIfx()
> i =1
> ~1
> Iwl
> P(x)
> =
> ~e
> 4
> 1 =

Taking Logarithm, 

> **[Extracted Question]**
> log P(x)
> log
> f;e
> Iw|
> log
> 1
> Iw|
> 4
> 4
> 2

Ignoring the Constant terms, 

> **[Extracted Question]**
> log P(x)
> Iwl

This is equivalent as L1 norm 

> **[Extracted Question]**
> Ilwlli
> Iwl
> 1 =

In linear regression, the likelihood function assumes Gaussian noise is 

> **[Extracted Question]**
> (w" x;
> L(w _
> X1 ,
> Xn
> V1 ,
> Yn)
> IIe
> 2o2
> 277
> 1 =
> Xi
> Yi)
> log( L(w ,
> X1 ,
> Xn , Y1 ,
> Yn))
> 202
> 2
> maxw
> (wTx;
> yd)
> min
> (wTxi
> yi)
> 1 =
> ~(wT,

By Bayes’ theorem, the posterior probability is 

P(w | X, y) ∝ P(y | X, w) . P(y) 

Taking the log-posterior and maximizing: 

> **[Extracted Question]**
> arg min
> (wTxi
> yd) 
> Allwll1
> where Ilwll1
> Iwl