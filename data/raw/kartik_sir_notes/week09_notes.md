aWeek-9Karthik Thiagarajan[1. Linear classifier](#n0.14332213768754642) [2. Linear Separability](#n0.397568462963253) [3. Linear Separability with 𝛾 margin](#n0.20673699908316445) [4. Perceptron Learning Algorithm](#n0.7178727262826614) [4.1. Algorithm](#n0.09880519750187378) [4.2. Proof of Convergence](#n0.8631470531057461) [4.2.1. Assumptions](#n0.6300513581581506) [4.2.2. Upper bound](#n0.025932444537480892) [4.2.3. Lower bound](#n0.41136480386206187) [4.2.4. Combining the bounds](#n0.9100700600595808) [4.2.5. Interpreting the bound](#n0.7365027084368698) [4.3. Example](#n0.07573861689584516) [4.4. Effect of Margin](#n0.5477376793407494) [5. Logistic Regression](#n0.6723278962686492) [5.1. Sigmoid Function](#n0.7549720080387343) [5.2. MLE: Computing the Log-Likelihood](#n0.17081577869755593) [5.3. MLE: Computing the Gradient](#n0.7898584132068531) [5.4. Gradient Ascent](#n0.8757369033972788) 1. Linear classifierRecall that a linear classifier is h:Rd→{1,-1} with h(x)=wTx, where w∈Rd. wwTx=01-1 We wish to minimize the 0-1 loss: 

min

w n∑i=1I[wTxi≠yi] This problem is NP-hard in general. We shall now impose some constraints on the data and see if it simplifies the problem. One such assumption is linear separability. 

Remark: For the rest of the document, we will assume that the labels lie in the set {1,-1}. Green data-points belong to class 1 and red data-points belong to class -1.

 2. Linear Separability 

StatementA dataset D={(x1,y1),⋯,(xn,yn)} is linearly separable if there exist a w∈Rd such that: (wTxi)yi⩾0, 1⩽i⩽n where yi∈{1,-1}.

In simple terms, a dataset is linearly separable if there exists a linear classifier that perfectly classifies (separates) all the data-points thereby producing zero training error. wwTx=0ExampleNon-Example We could also have a situation where a dataset is just about linearly separable. That is, there is only one linear classifier that perfectly separates the data (after normalizing the weights).wwTx=0For the algorithms that we plan to discuss, it would be convenient to get rid of this limitation. So we go for a stronger assumption. 3. Linear Separability with 𝛾 margin 

Statement A dataset D={(x1,y1),⋯,(xn,yn)} is linearly separable with 𝛾 margin if there exist a w∈Rd and a 𝛾>0 such that: (wTxi)yi⩾𝛾, 1⩽i⩽n where yi∈{1,-1}.

 As an example:wwTx=0wTx=2wTx=-2 For linearly separable datasets with a positive margin, we have algorithms that can return a valid classifier that achieves zero training error. 4. Perceptron Learning Algorithm4.1. AlgorithmThe prediction rule for the perceptron is given as: y=a

|  |  |  |
| --- | --- | --- |
| 1, |  | wTx⩾0 |
| -1, |  | wTx<0 |

 Note that in the situation where wTx=0, the predicted label is 1 as per our convention. 

a

|  |  |
| --- | --- |
| 1) | Initialize w(0)=0 |
| 2) | while sign(w(t)Txi)≠yi for some i: |
| 3) | 1111w(t+1)=w(t)+xiyi |

 In more detail:• w(0)=0• Cycle through the data-points in a fixed order, say:– (x1,y1)→⋯→(xn,yn)• If (xi,yi) is a mistake w.r.t w(t):– w(t+1)=w(t)+xiyi• If there are no mistakes for n consecutive iterations– terminate the algorithm– return the weight vector w(T)– here T is the number of updates to w  Some observations:• In this course, we always begin with w(0)=0• In the course of the algorithm, the number of mistakes made is equal to the number of updates to the weight vector.• The number of iterations is greater than or equal to the number of mistakes as there might be iterations in which there are no mistake.• For a linearly separable data with positive margin, the perceptron learning algorithm converges. 4.2. Proof of Convergence4.2.1. Assumptions Assumption-1: Linear Separability with 𝛾 margin There exists some 𝛾>0 and w\* such that for every point (xi,yi) in the dataset, we have: (w\*Txi)yi⩾𝛾 with ||w\*||=1. This assumption encodes the fact that the data is linearly separable with a margin of 𝛾. Since ||w\*||=1, the margin is the distance between the decision boundary and the closest point in the dataset. Assumption-2: Radius bound There exists some R>0 such that for every point (xi,yi) in the dataset, we have: ||xi||2⩽R2 This assumption encodes the fact that all data-points are within a ball of radius R centered at the origin. These two assumptions can be visualized using this image: w\*R𝛾We start with w(0)=0. Since each update to the weight vector happens after a mistake is observed, we will use the term mistakes and updates interchangeably. Formally, let the weight vector after t updates be denoted by w(t), where t⩾0. The case of t=0 corresponds to zero updates and the corresponding weight vector will be w(0). After t rounds, the perceptron has seen t mistakes and the weight vector has been updated t times. 4.2.2. Upper bound Assume that the perceptron has gone through t-1 updates. Let (x,y) be some point that is misclassified by the perceptron at this stage. This is the tth mistake that it is seeing. As the current weight vector of the perceptron is wt-1, we have: (w(t-1)Tx)y⩽0 This necessitates one more round of weight update. The update rule for this step is as follows: w(t):=w(t-1)+xy Let us now look at the norm of the weight vector and see how it changes across iterations: a

|  |  |
| --- | --- |
| ||w(t)||2 | =(w(t-1)+xy)T(w(t-1)+xy) |
|  |  |
|  | =||w(t-1)||2+y2⋅||x||2+2⋅y⋅(w(t-1)Tx) |
|  |  |
|  | ⩽||wt-1||2+R2 |

 We have used three facts to get the inequality: • y2=1• ||x||2⩽R2• (w(t-1)Tx)y⩽0 We can now apply this inequality recursively on the earlier rounds: a

|  |  |
| --- | --- |
| ||w(t)||2 | ⩽||w(t-1)||2+R2 |
|  | ⩽||w(t-2)||2+R2+R2 |
|  | ⩽||w(t-3)||2+R2+R2+R2 |
|  | ⩽ ⋮ |
|  | ⩽||w(t-t)||2+tR2 |
|  | =||w(0)||2+tR2 |
|  | =t⋅R2 |

 We have used the fact that w(0)=0. Therefore, the upper bound is: 

||w(t)||2⩽t⋅R2

 4.2.3. Lower bound Now, we look at the relationship between the optimal weight vector w\* and the weight vector w(t). The dot product is a measure of this relationship:a

|  |  |
| --- | --- |
| w\*Tw(t) | =w\*T(w(t-1)+xy) |
|  |  |
|  | =w\*Tw(t-1)+(w\*Tx)y |
|  |  |
|  | ⩾w\*Tw(t-1)+𝛾 |

 We have used the fact that (w\*Tx)y⩾𝛾 to get the above inequality. Recursively applying this for earlier rounds and using the fact that w(0)=0, we get:w\*Twt⩾t⋅𝛾 Now, we use the Cauchy-Schwartz inequality and the assumption that ||w\*||=1 to get:a

|  |  |
| --- | --- |
| ||w\*||⋅||w(t)|| | ⩾w\*Tw(t) |
| ||w(t)|| | ⩾w\*Tw(t) |
|  |  |

Clubbing this result with the previous one, we get: ||w(t)||⩾w\*Tw(t)⩾t⋅𝛾 Squaring the first and last terms: 

||w(t)||2⩾t2⋅𝛾2

 4.2.4. Combining the bounds We now have a lower bound and an upper bound for ||wt||2: 

t2⋅𝛾2⩽||wt||2⩽t⋅R2

 Using these two bounds, we have: 

t⩽R2𝛾2

 This is called the radius-margin bound. 4.2.5. Interpreting the bound w(t) is the weight vector after t updates. Another way of seeing this is w(t) is the weight vector after the perceptron has made t mistakes. Each update is mapped to one mistake. Therefore, the total number of updates to the weight vector is bounded above R2𝛾2. Or, we could also say, the perceptron has to correct at most R2𝛾2 mistakes. Since this is a finite quantity, the perceptron algorithm converges. Note that w(0) doesn't count as an update. 4.3. ExampleConsider the following dataset: X=a

|  |  |  |  |  |
| --- | --- | --- | --- | --- |
| 1 | 1 | -1 | -1 | -2 |
| 4 | -2 | -3 | 2 | 0 |

,y=a

|  |
| --- |
| 1 |
| 1 |
| -1 |
| -1 |
| -1 |

 Cycling through the data-points in the order 1→2→⋯→5:w(0)012-1-212x1x2-1-2x1 34-3-4345-3x2x3x4x5Since w(0)=0, all points are going to be predicted as 1. The first mistake is (x3,y3).a

|  |  |
| --- | --- |
| w(1) | =w(0)+x3y3 |
|  |  |
|  | =a  |  | | --- | | 0 | | 0 |  -a  |  | | --- | | -1 | | -3 | |
|  |  |
|  | =a  |  | | --- | | 1 | | 3 | |

Update-1w(1)012-1-212x1x2-1-2x134-3-4345-3x2x3x4x5We now have to resume the cycle from data-point (x4,y4).a

|  |  |
| --- | --- |
| w(2) | =w(1)+x4y4 |
|  |  |
|  | =a  |  | | --- | | 1 | | 3 |  -a  |  | | --- | | -1 | | 2 | |
|  |  |
|  | =a  |  | | --- | | 2 | | 1 | |

 Update-2w2012-1-212x1x2-1-2x134-3-4345-3x2x3x4x5We now have to resume the cycle from data-point (x5,y5). a

|  |  |
| --- | --- |
| w(3) | =w(2)+x4y4 |
|  |  |
|  | =a  |  | | --- | | 2 | | 1 |  -a  |  | | --- | | -1 | | 2 | |
|  |  |
|  | =a  |  | | --- | | 3 | | -1 | |

Update-3w(3)012-1-212x1x2-1-2x134-3-4345-3x2x3x4x5We now have to resume the cycle from data-point (x5,y5).a

|  |  |
| --- | --- |
| w(4) | =w(3)+x1y1 |
|  |  |
|  | =a  |  | | --- | | 3 | | -1 |  +a  |  | | --- | | 1 | | 4 | |
|  |  |
|  | =a  |  | | --- | | 4 | | 3 | |

 Update-4w4012-1-212x1x2-1-2x134-3-4345-3x2x3x4x5We now have to resume the cycle from data-point (x2,y2).a

|  |  |
| --- | --- |
| w(5) | =w(4)+x2y2 |
|  |  |
|  | =a  |  | | --- | | 4 | | 3 |  +a  |  | | --- | | 1 | | -2 | |
|  |  |
|  | =a  |  | | --- | | 5 | | 1 | |

Update-5w5012-1-212x1x2-1-2x134-3-4345-3x2x3x4x5We now have to resume the cycle from data-point (x3,y3). Now, we have five consecutive iterations without any mistake. Therefore, we stop and claim that perceptron has converged. 

Remark: There may be multiple valid weight vectors. Perceptron returns one of them. Depending on how you cycle through the data-points, it may return a different weight vector.

 4.4. Effect of MarginThis is an experiment that demonstrates the effect of the margin on the number of iterations needed to converge. Note that t refers to the number of updates to the weight vector. It is not the upper bound but the actual number of updates while training a perceptron.d=1t=1d=0.5t=2d=0.1t=7d=0.01t=44As the margin decreases, the number of updates increases. 5. Logistic RegressionThe assumption of linear separability is too strict. We now relax it and turn to a discriminative model that outputs non-trivial probabilities. Logistic regression is a popular classifier that models the conditional probability of the label given the data-point, P(y | x), in the following manner: P(y=1 | x)=𝜎(wTx) where, 𝜎(z)=11+e-z is called the sigmoid or the logistic function, and w is the parameter vector or weight vector (w∈Rd). The sigmoid function lies between 0 and 1. More about this function in the next section. To predict the label for a data-point using this model, the probability is converted to a binary outcome using a threshold. A typical threshold of 0.5 is used: • if P(y=1 | x)⩾0.5, the model outputs class-1• if P(y=1 | x)<0.5, the model outputs class-0 More formally, the classifier h:Rd→R is given as: h(x)=a

|  |  |  |
| --- | --- | --- |
| 1, |  | 𝜎(wTx)⩾0.5 |
| 0, |  | 𝜎(wTx)<0.5 |

=I[𝜎(wTx)⩾0.5] We need a way to learn the weights of this model. As we have begun with a probabilistic interpretation, we will turn to the method of parameter estimation using MLE. But before that, let us look at some properties of the sigmoid function. 5.1. Sigmoid FunctionThe graph of the sigmoid function looks as follows: 𝜎:R→(0,1)𝜎(z)=11+e-z -2-1120z𝜎(z)𝜎(z)=11+e-z0.51Useful properties:• As z→∞, 𝜎(z)→1 • As z→-∞, 𝜎(z)→0. • We have 𝜎(0)=0.5. • If z>0, then 𝜎(z)>0.5 and if z<0, 𝜎(z)<0.5. • Next, 𝜎(-z)=1-𝜎(z):a

|  |  |
| --- | --- |
| 𝜎(-z) | =1  1+ez |
|  | =e-z  1+e-z |
|  | =1-1  1+e-z |
|  | =1-𝜎(z) |

• Finally, 𝜎′(z)=𝜎(z)⋅[1-𝜎(z)]: a

|  |  |
| --- | --- |
| 𝜎′(z) | =-1  (1+e-z)2⋅e-z⋅(-1) |
|  | =1  1+e-z⋅e-z  1+e-z |
|  | =𝜎(z)⋅[1-𝜎(z)] |

 This is a very important property and will be used quite a lot in the upcoming sections. 5.2. MLE: Computing the Log-LikelihoodWe will assume that the labels are drawn independently. In such a case, the likelihood function is: a

|  |  |
| --- | --- |
| L(w;D) | =P(D | w) |
|  | =n∏i=1P(yi | xi;w) |

Recall that P(y=1 | x)=𝜎(wTx). For a data-point xi, let us call this probability 𝜎i: 𝜎i=P(y=1 | xi)=𝜎(wTxi) For example, if 𝜎i=0.75, the model believes that there is a 75% chance that xi belongs to class-1. The probability that this point belongs to class-0 is: P(y=0 | xi)=1-𝜎i The actual label for this data-point is yi, which is either 1 or 0, but we don't exactly know what it is. We therefore define it in a piece-wise manner:P(yi | xi)=a

|  |  |  |
| --- | --- | --- |
| 𝜎i, |  | yi=1 |
| 1-𝜎i, |  | yi=0 |

 However, we can't plug something like this into the likelihood function. We need a form that can be easily manipulated, something like this: P(yi | xi)=𝜎yii⋅(1-𝜎i)1-yi Notice how this is the same as the piece-wise function defined earlier, but much more suited for algebraic operations. Try out yi=1 and yi=0 to see the likeness. Armed with this expression, we go back to the likelihood: a

|  |  |
| --- | --- |
| L(w;D) | =P(D | w) |
|  | =n∏i=1P(yi | xi;w) |
|  | =n∏i=1𝜎yii⋅(1-𝜎i)1-yi |

 As it is easier to work with log, let us compute the log-likelihood: a

|  |  |
| --- | --- |
| l(w;D) | =n∑i=1yilog𝜎i+(1-yi)log(1-𝜎i) |
|  | =n∑i=1yilog[𝜎(wTxi)]+(1-yi)log[1-𝜎(wTxi)] |

 Cross Entropy Loss The negative log-likelihood function can be viewed as a loss function for the classifier. It is often called the cross entropy loss.CE(w,D)=n∑i=1-yilog[𝜎(wTxi)]-(1-yi)log[1-𝜎(wTxi)]The negative log-likelihood is a convex function. As a result of this convexity, the logistic regression model will have an optimal weight vector for any given dataset. This is independent of the data being linearly separable or not. 5.3. MLE: Computing the GradientLet us now turn to the gradient of the log-likelihood. We will make use of two facts:  • 𝜎′(z)=𝜎(z)⋅[1-𝜎(z)]• ∇(wTx)=x This derivation is all about a careful application of the chain-rule. We will split the sum into two parts and compute the gradient for each one of them. a

|  |  |
| --- | --- |
| ∇l(w) | =n∑i=1yi⋅1  𝜎(wTxi)⋅𝜎(wTxi)[1-𝜎(wTxi)]⋅xi |
|  | + n∑i=1(1-yi)⋅1  1-𝜎(wTxi)⋅{-𝜎(wTxi)[1-𝜎(wTxi)]}⋅xi |
|  |  |
|  | =n∑i=1yi⋅[1-𝜎(wTxi)]⋅xi-n∑i=1(1-yi)⋅𝜎(wTxi)⋅xi |
|  |  |
|  | =n∑i=1[yi-𝜎(wTxi)]xi |
|  |  |
|  | =n∑i=1(yi-𝜎i)xi |

 We can treat yi-𝜎i as some kind of an error in prediction. For example, if yi=1 and the model's probability is 𝜎i=0.7, then the error in prediction is 0.3. With this perspective, the gradient for a single data-point takes the following form: gradient=error×data-point Larger the error, more is the contribution of a data-point towards the gradient. If the model is already doing a good job of classifying a data-point, then the error is going to be small, and such a point won't disturb the gradient much. 5.4. Gradient AscentThough we have computed the gradient of the log-likelihood, we can't obtain a closed-form expression for w\*, the optimal weight vector, by setting the gradient to zero. As a result, we have to resort to numerical methods for optimization. One obvious choice is gradient ascent (not descent, as we are maximizing the log-likelihood): wt+1=wt+𝜂⋅∇l(w)|wt Plugging in the gradient, we get: wt+1=wt+𝜂⋅X(y-𝜎) Since the log-likelihood is concave, gradient ascent will converge to the optimal weight vector for suitable choices of 𝜂. In practice, gradient ascent is not used to learn the weights of a logistic regression model. Gradient ascent is a first order method, meaning, it uses the first derivatives or gradients. There are a class of second order methods that make use of the second derivatives or the Hessian.