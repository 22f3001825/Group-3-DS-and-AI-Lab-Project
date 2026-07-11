aWeek-5Karthik Thiagarajan[1. Supervised Learning](#n0.3355767526845632) [1.1. Regression](#n0.42846121520847835) [1.2. Classification](#n0.14996237257454803) [2. Regression](#n0.10399265127570123) [3. Linear Regression](#n0.8063269695982422) [3.1. Model](#n0.49377155496697345) [3.2. Loss Function](#n0.7966681005775083) [3.3. Optimization](#n0.41013867971149387) [3.3.1. Gradient](#n0.6723615502473772) [3.3.2. Normal equations](#n0.4438364729004869) [3.4. Gradient descent](#n0.4703750280522039) [3.5. Stochastic Gradient Descent](#n0.985777885411955) [3.6. Evaluation](#n0.05793183745850161) [4. Geometric Perspective](#n0.6831403037660848) [4.1. Best-fit surface, Rd+1 view](#n0.526003120893924) [4.2. Projections, Rn view](#n0.8314695896519342) [5. Probabilistic Perspective](#n0.15841643185924048) [6. Kernel Regression](#n0.9419218562943297) [6.1. Learning](#n0.8993152105503981) [6.2. Prediction](#n0.8717642164196395) 1. Supervised Learning 1.1. Regression Given a dataset D={(x1,y1),⋯,(xn,yn)}, where yi∈R, our goal is to learn a function f:Rd→R that captures the underlying relationship (patterns) between data-points and labels. The defining characteristic of a regression problem is that the labels are continuous-valued real numbers. 1.2. Classification Given a dataset D={(x1,y1),⋯,(xn,yn)}, where yi∈{1,⋯,k}, our goal is to learn a function: f:Rd→{1,⋯,k} that captures the underlying relationship (patterns) between data-points and labels. The defining characteristic of a classification problem is that the labels are from a finite, discrete set. If k=2, the problem is called binary classification. If k>2, the problem is called multi-class classification.  Almost any ML algorithm can be understood in terms of four components: • Model• Loss function• Optimization• Evaluation A supervised learning problem involves training a model on a training dataset by optimizing (minimizing) the loss function with the eventual goal of achieving a high evaluation on a test dataset.

Remark: It is important to note the final goal in any supervised learning problem is good performance on the test dataset. Note that the test dataset is not available during training. For this reason, it is often called a set of unseen data-points. A "good" supervised ML model is said to generalize well to unseen data-points. Here, the term generalization denotes the ability of the model to capture the real patterns in the data, while ignoring the noise, which in turn gives it the power to perform well on points it has not seen before. In our course, we will spend most of the time with the training data. The training data is the raw material for learning the model. It is important to acquire a good working knowledge of the various techniques to train a model. That said, the learner is encouraged to keep the importance of the test dataset in the back of his mind at all points of time.

 2. Regression If f:Rd→R is a potential mapping (model) from data-points to labels, we use the following metric to measure the goodness of the model. L(f,D)=12n∑i=1(f(xi)-yi)2 • yi → true label for xi• f(xi)→ predicted label• f(xi)-yi→ error in prediction This is called the sum of squared errors or SSE. The 1/2 is added for mathematical convenience. This is particularly useful when we differentiate the loss function with respect to the parameters of the model.  Dividing the SSE by n gives the mean squared error or MSE: L(f,D)=12nn∑i=1(f(xi)-yi)2 The task is to find a function f that minimizes the loss function on the training dataset while generalizing well to unseen data-points. Since the class of all possible functions is so huge, we usually choose a more tractable set: the class of linear functions. Hence, the approach we will study now is called linear regression. 3. Linear Regression 3.1. Model When f is assumed to be a linear function, the resulting solution approach is called linear regression. Consider f:Rd→R such that: f(x)=wTx=w1x1+⋯+wdxd where w∈Rd is called the weight vector. We call f a linear model. For a given data-point-label pair (xi,yi), f(xi) is called the predicted label and yi is the true label. For all data-points, the predicted label vector can be expressed as: y=XTw To see why, expand the RHS: y=a

|  |
| --- |
| xT1w |
| ⋮ |
| xTnw |

 where, y∈Rn. 3.2. Loss Function The SSE loss function with a linear model can be expressed in three different but equivalent forms: Vector-scalar form  L(w)=12n∑i=1(wTxi-yi)2 Vector-vector form If y=XTw, we have: L(w)=12||y-y||2 Matrix-vector form  L(w)=12||XTw-y||2 A visualization of the squared loss and its contours for w∈R2 is given below. This is called the parameter space. In the parameter space, the loss function is a surface. As we move along the w1-w2 plane, we see that the loss function's value changes. Note that the loss function depends on the dataset as well as the model parameters. Here is an example loss surface.L(w1,w2)w1w2L(w)=(w1-1)2+(w2+1)2+1w=a

|  |
| --- |
| 1 |
| -1 |

The height of the surface above the w1-w2 plane is the value of the loss function.

Convexity of SSE: The SSE loss function is convex. To see why, consider the function again: L(w)=12n∑i=1(wTxi-yi)2 Each term is of the form (wTxi-yi)2. First, note that wTxi-yi is convex since affine functions are convex. Next, (wTxi-yi)2 is convex. This is because a composition of a convex function and an affine function is convex. Finally, the sum of all these convex functions is again convex.

 The convexity of SSE makes life very simple. If the function has a local minimum, then it has to be global. 3.3. Optimization The task is to find a w that minimizes the loss: w=

min

w 12n∑i=1(wTxi-yi)2 As stated before, the SSE loss function, L(w), is convex. Hence, all its local minima are global minima. In addition, since L(w) is differentiable, if it has a minimum, then ∇L(w)=0 has to hold at that point. So the next step is to compute the gradient. 3.3.1. Gradient The gradient is the vector of partial derivatives: ∇L(w)=a

|  |
| --- |
| ∂L(w)  ∂w1 |
| ⋮ |
| ∂L(w)  ∂wd |

 Let us now compute this for one term in the loss function: a

|  |  |
| --- | --- |
| ∇(wTxi-yi)2 | =2⋅(wTxi-yi)⋅xi |

 Summing this over the n data-points: a

|  |  |
| --- | --- |
| ∇L(w) | =1  2⋅n∑i=12⋅(wTxi-yi)⋅xi |
|  | =n∑i=1(wTxi-yi)xi |

 Let us now express this in two different but equivalent forms: Vector-scalar form ∇L(w)=n∑i=1(wTxi-yi)xi Matrix-vector form Playing around with the previous equation, we get: a

|  |  |
| --- | --- |
| ∇L(w) | =n∑i=1(wTxi-yi)xi |
|  |  |
|  | =n∑i=1xi(xTiw-yi) |
|  |  |
|  | =[n∑i=1xixTi]w-n∑i=1xiyi |
|  |  |
|  | =XXTw-Xy |

 This leads us to another equivalent equation for the gradient: ∇L(w)=XXTw-Xy 3.3.2. Normal equations Setting the gradient to zero, we get: XXTw=Xy This system linear equations equations are called the normal equations. It is consistent for any choice of X and y. One special solution is given by: w=(XT)†y where (XT)† is called the pseudo-inverse of XT.

What is the pseudo-inverse and why do we need it? The pseudo-inverse of a matrix A of shape m×n is a unique matrix A† of shape n×m that behaves like an inverse. The pseudo-inverse is defined for all matrices, unlike the inverse which is defined for only some square matrices. The pseudo-inverse is intimately tied to a system of linear equations. Consider the system: Ax=b If Ax=b is not consistent, one can still hunt for an approximate solution by looking for x that minimizes ||Ax-b||2. Since Ax is a vector in the column space of A, we are searching for a vector in the column space of A that is as close to b as possible: Ax≈b It turns out that one of the possible solutions for x is given using the pseudo-inverse of A: x=A†b In the linear regression setting, A=XT,x=w,b=y. We are looking for a parameter vector w so that the predicted label vector, XTw, is as close as possible to the true label vector, y, that is: XTw≈y The solution is given by: w=(XT)†y If rank(X)=d, then the pseudo-inverse of XT can be written as: (XT)†=(XXT)-1X For more details, refer to [Moore Penrose inverse](https://en.wikipedia.org/wiki/Moore%E2%80%93Penrose_inverse). If Ax=b is consistent, A†b gives the solution that has the least norm.

 (XT)† is the pseudo-inverse of XT and is a d×n matrix. It turns out that w lies in the span of the data-points. This is a key observation and will be used when we discuss kernel regression. If rank(X)<d, there are infinitely many solutions. Out of all of them, w is the solution that has the least norm. Any solution to the system can be written as w+w⟂, where w⟂ is perpendicular to the span of the data-points since: XXT(w+w⟂)=Xy Specifically, if rank(X)=d the solution is unique and is given by: w=(XXT)-1Xy w is often termed as the least squares solution, since it is obtained by minimizing the SSE. 3.4. Gradient descent XXT is a d×d matrix. If d is a large value, then computing the inverse of XXT is going to be a costly operation. Rather than finding a closed form solution that involves the inverse, we can settle for an iterative approach using gradient descent. If w(t) represents the weight vector at time t, the update is given by: w(t+1)=w(t)-𝜂∇L(w)|w(t) Substituting the gradient: w(t+1)=w(t)-𝜂(XXTw(t)-Xy) 𝜂>0 is the learning rate. Since the objective is convex, gradient descent is guaranteed to converge to the global minimum for suitable choices of the learning rate 𝜂. 𝜂 is called a hyperparameter (something that you choose). w(0)=0 is one of the choices for the initial weight vector. However, it is quite common to choose w(0) randomly, say by sampling a vector of length d from a standard normal Gaussian distribution or a uniform distribution. In our course, unless otherwise stated, we will stick to a zero initialization. Visually, we can see the progress of the algorithm on the parameter space. In the image below, we have the contours of the loss function for the case of d=2. The individual dots represent the iterates w(t) for various values of t:w1w2Dark green indicates early stage of the optimization process, yellow indicates the intermediate stage and red indicates the final stage of the process as the iterates get close to the minimum. In this example, we see the progress from w(0)=(0,0) to w(T)=(-2,5). An important observation here is the direction of the trajectory and the angle it makes with the contours along the way. Notice how the trajectory seems to be perpendicular to the contours at every point. This is not a coincidence. Recall that the gradient of a function at a point is orthogonal to the contours at that point.

Remark: The gradient for a single data-point has a nice interpretation. Consider the gradient expression again: (wTxi-yi)xi This can be rewritten as (yi-yi)xi If we treat yi-yi as the error in prediction, then the gradient of the loss with respect to the weight vector for a single data-point assumes the form: error×data-point What this means is that, a data-point's contribution to the weight update depends on two things:• The magnitude depends on how well the model is performing currently on that data-point. The poorer the performance, higher the error, bigger the contribution. • The direction of the contribution is parallel (anti-parallel) to the data-point.

 3.5. Stochastic Gradient Descent For large datasets, computing the entire gradient in one go might be costly. To see why the size of the dataset matters, recall that the gradient is given by: n∑i=1(wTxi-yi)xi As n increases, the time taken to compute the gradient on the entire dataset increases. In such cases, a random subset (random sample) of the dataset is extracted and the gradient on this subset is used to approximate the full gradient. If X′∈Rd×m represents a sample of m points, then the update equation for the approximate setting becomes: w(t+1)=w(t)-𝜂[(X′)(X′)Tw(t)-X′y] This algorithm is called stochastic gradient descent (SGD). The qualifier stochastic arises from the randomness in picking the subset of points for the update. The progress of SGD is less smooth compared to GD given that we are only using an approximate version the gradient. Eventually, SGD also reaches the local minimum under suitable choices of the learning rate. Gradient DescentStochastic Gradient Descent Notice how the trajectory in the case of SGD is no longer orthogonal to the contours. This is because, the gradient in the case of SGD is the approximate gradient and not the full gradient of the loss function. In practice, how does SGD work? First we divide the n data-points into a set of batches, each having a small number of data-points. For example, if we have 320 data-points, we might divide into 10 batches, each having 32 data-points. The batch-size is denoted as the number of data-points in a batch, which is 32 in this example.  Next, we compute the gradient for each batch and use that in the update rule for SGD. One complete pass over the training dataset is called an epoch. That is, in an epoch, every data-point is used exactly once in some update. In our example, in one epoch, we will update the parameters 10 times, once for each batch. Before every epoch begins, it is also important to shuffle the data-points. This makes the learning more robust. The need for shuffling the dataset will be taken up when we discuss SGD in the context of classification. In general, if we have a training dataset of n data-points and a batch-size B, then one epoch will witness nB updates to the parameters, where nB is the number of batches. Visually:n data-points⋯BBBB→batch-size  3.6. EvaluationThe model's performance is evaluated on a test dataset which is a collection of data-points not seen during training. As stated before, a good score on the test dataset is the goal of any supervised ML problem. A good performance metric in the case of regression is the root mean squared error (RMSE): 1nn∑i=1(wTxi-yi)2 This has the same units as the label which makes the error more interpretable. The factor of 1/2 can be omitted from here since the RMSE isn't used in an optimization context. 4. Geometric Perspective We can view the regression problem from the standpoint of two spaces: Rd+1 and Rn. 4.1. Best-fit surface, Rd+1 view The geometry of the relationship between predicted label and features in linear regression takes the following form in different dimensions:

|  |  |  |  |
| --- | --- | --- | --- |
| d | Space | Object | Interpretation |
| 1 | R2 | Line passing through the origin | Best-fit line |
| 2 | R3 | Plane passing through the origin | Best-fit plane |
| ⩾3 | Rd+1 | Hyperplane passing through the origin | Best-fit hyperplane |

 Here is a visualization of the first two cases: yxy=wxyx1x2y=w1x1+w2x2Each blue point here represents (xi,yi), where yi is the true label. Note that the point (xi,yi) need not lie on the hyperplane. However, the point (xi,yi) will lie on the hyperplane. In general, for d features, the feature-label space is Rd+1. The best-fit hyperplane is of the form wTx. This is a hyperplane of dimension d embedded in the space Rd+1. 4.2. Projections, Rn view Feature vectors If all the feature values for a given feature are added as components of a vector, we get a feature vector. For example, rj will have the values for the jth feature for all data-points: rj∈Rn We can now look at X in two ways: Columns made up of data-points X=a

|  |  |  |
| --- | --- | --- |
| | |  | | |
| x1 | ⋯ | xn |
| | |  | | |

,XT=a

|  |  |  |
| --- | --- | --- |
| - | xT1 | - |
|  |  |  |
| - | xn | - |

 Rows made up of feature vectors X=a

|  |  |  |
| --- | --- | --- |
| - | rT1 | - |
|  | ⋮ |  |
| - | rTd | - |

,XT=a

|  |  |  |
| --- | --- | --- |
| | |  | | |
| r1 | ⋯ | rd |
| | |  | | |

  The row space of X, which is the same as the column space of XT, is the span of the feature vectors. The SSE objective can be understood as follows. Find a point in the row space of X that is closest to y:

min

w ||XTw-y||2 yXTwRowspace of XRn The required point is the projection of y on the row space of X. Let XTw be this projection. It follows that y-XTw is orthogonal to the row space of X: X(y-XTw)=0 This leads us back to the normal equations, XXTw=Xy. The vector w is given by (XT)†y. 5. Probabilistic Perspective The final perspective is perhaps the most important. We assume that the true relationship between the features and labels is linear, corrupted by some noise. We model this noise to be a zero-mean Gaussian. The noise is independent of the features and we denote it by 𝜖i for the ith data-point: yi=wTxi+𝜖i Setting 𝜖i∼N(0,𝜎2), where 𝜎2 is the variance in the noise, we have: yi∼N(wTxi,𝜎2) We can now use MLE to estimate w. In this, note that xi is treated as a constant. yi is the random variable. Likelihood L(w)∝n∏i=1exp[-(yi-wTxi)22𝜎2] Log-likelihood After collecting terms that do not affect the optimization in c: l(w)=-12𝜎2n∑i=1(yi-wTxi)2+c Maximizing the log-likelihood is the same as minimizing the negative log-likelihood. Therefore we end up with the same optimization problem that we saw before:

min

w n∑i=1(yi-wTxi)2 Minimizing the SSE is equivalent to maximizing the likelihood under a zero mean, Gaussian noise assumption. This gives a probabilistic motivation to the original optimization problem involving the SSE. It gives some sort of justification for our choice of SSE as a suitable objective function for linear regression. While the SSE presents itself as an intuitive choice, the probabilistic approach justifies its use with a slightly more principled approach. Since we have turned linear regression into an estimation problem (using MLE), we will call w the maximum likelihood estimator or the ML estimator of w: wML=(XXT)-1Xy Once we have an estimator, we can ask how good it is in a statistical sense. This will be taken up in the beginning of the next document. 6. Kernel RegressionSo far we have assumed f to be linear. A linear model is the right choice if the underlying data is linear. However, this is rarely the case in the real world. Most of the datasets are non-linear. A sample non-linear dataset with one feature is shown below: xy We can deal with non-linearity by introducing feature transformations and try to fit a linear model in the transformed feature space. The hope is that the transformed dataset is linear in this higher dimensional space. All that we have learnt about linear regression can therefore be directly brought to bear upon the non-linear case. For more on non-linear transformations, refer to week-2. 6.1. LearningConsider the non-linear transformation of the features: 𝜙:Rd→RD The transformed dataset is: {(𝜙(x1),y1),⋯,(𝜙(xn),yn)} The transformed data-matrix is: 𝜙(X)∈RD×n We can now perform regression in the transformed feature space. The model is: f:RD→R f(x)=wT𝜙(x) The loss function becomes: L(w)=||𝜙(X)Tw-y||2 Recall that we can chose the optimal weight vector w such that it lies in the span of the data-points. Therefore, we posit the existence of some 𝛼∈Rn such that: a

|  |  |
| --- | --- |
| w | =𝜙(X)𝛼 |
|  |  |
|  | =a  |  |  |  | | --- | --- | --- | | | |  | | | | 𝜙(x1) | ⋯ | 𝜙(xn) | | | |  | | |  a  |  | | --- | | 𝛼1 | | ⋮ | | 𝛼n | |

 Plugging w into the objective, the loss now becomes a function of 𝛼: L(𝛼)=||𝜙(X)T𝜙(X)𝛼-y||2 The matrix 𝜙(X)T𝜙(X) should be familiar. It is the matrix of pair-wise dot-products between points in the transformed space, the Gram matrix. This immediately suggests that we can use the kernel trick. If the kernel associated with 𝜙 is: k:Rd×Rd→R the kernel matrix K∈Rn×n is: K=𝜙(X)T𝜙(X) which is computed element-wise as Kij=k(xi,xj) Plugging the kernel matrix into the loss, the final form is: L(𝛼)=||K𝛼-y||2 Minimizing the L would result in: 𝛼=K†y If K is invertible, we have 𝛼=K-1y If this is not clear, refer to the write-up on the pseudoinverse earlier in this document. Comparing this with Ax≈b, we have to substitute A=K, b=y, x=𝛼. With this, w=𝜙(X)𝛼. However, w cannot be computed since 𝜙 is not explicitly specified. We infer it from the kernel. Thankfully, what we need is only the prediction for a test data-point and to compute that we have enough information. 6.2. Prediction For a test data-point xtest, the predicted label is: y=𝜙(xtest)Tw Using w=𝜙(X)𝛼, we have:  y=𝜙(xtest)T𝜙(X)𝛼 The product before 𝛼 is a 1×n vector: 𝜙(xtest)Ta

|  |  |  |
| --- | --- | --- |
| | |  | | |
| 𝜙(x1) | ⋯ | 𝜙(xn) |
| | |  | | |

=a

|  |  |  |
| --- | --- | --- |
| 𝜙(xtest)T𝜙(x1) | ⋯ | 𝜙(xtest)T𝜙(xn) |

 Each component of this vector is nothing but a kernel function evaluation. Expanding the RHS of the predicted label: y=n∑i=1𝛼i⋅k(xtest,xi) This predicted label has a nice interpretation. It depends on two things: • 𝛼i: importance of ith data-point in predicting the label for xtest• k(xtest,xi): similarity between xtest and xi