aWeek-6Karthik Thiagarajan[1. Ridge Estimator](#n0.6022333589951678) [2. Overfitting and Underfitting](#n0.6155351718275204) [2.1. Toy dataset](#n0.5841599987623121) [2.2. Overfitting](#n0.13937118463532228) [2.3. Data Augmentation](#n0.5496203470284673) [2.4. Underfitting](#n0.6500189090169048) [3. Model Complexity](#n0.26400240836187705) [4. Regularization](#n0.5132813700250285) [4.1. Ridge Regression](#n0.3129936501874018) [4.2. LASSO Regression](#n0.2962509751623972) [5. Cross Validation](#n0.22206035511176325) [5.1. k-Fold cross validation](#n0.9440106929318692) [5.2. Leave one out cross validation](#n0.2398450921044104) [6. Bayesian Viewpoint](#n0.6814311566000013) 1. Ridge EstimatorGoing back to the probabilistic perspective of linear regression, recall that the label yi∼N(wTxi,𝜎2). If we now consider the label vector y∈Rn, it becomes a random vector that follows a multivariate Gaussian distribution with mean XTw and covariance matrix 𝜎2I. The reason the covariance matrix is diagonal is because of the independence assumption among the data-points. Formally: y ∼N(XTw,𝜎2I) The ML estimator that we get from solving the normal equations is also a random vector: wML=(XT)†y For this discussion, let us assume that rank(X)=d, so that: wML=(XXT)-1Xy Statistically, we can try to understand the goodness of an estimator through various means. One way to quantify the goodness of an estimator is to look at its bias. Recall that the bias of an estimator is the average difference between the estimator and the true value it is trying to estimate. In this case: bias=E[wML]-w For the ML estimator we have, we see that: a

|  |  |
| --- | --- |
| E[wML] | =E[(XXT)-1Xy] |
|  | =(XXT)-1X⋅E[y] |
|  | =(XXT)-1X(XTw) |
|  | =(XXT)-1(XXT)w |
|  | =w |

 Here, we have used the fact that E[y]=XTw along with the linearity of expectation. Since E[wML]-w=0, we see that the bias is zero. Therefore, the ML estimator is an unbiased estimator. This is good news. What this means is that when we run the experiment of estimating wML using multiple datasets and average all the estimates, that will be very close to w. Of course, in practice one works with only one dataset, so we have only one estimate. But we can at least be assured in a statistical sense that it isn't going to be too bad. However, this is only one side of the story. An estimator can be unbiased but end up having a lot of fluctuation (variance) around the mean. Therefore, a better metric we turn to is the mean squared error of an estimator. The MSE gives us the average squared deviation of the estimator from the true value. Formally: MSE(wML)=E[||wML-w||2] With some linear algebra, one can show that: E[||wML-w||2]=𝜎2⋅trace[(XXT)-1] If the eigenvalues of XXT are 𝜆1⩾ ⋯ ⩾𝜆d>0, then we see that the MSE can be written as:E[||wML-w||2]=𝜎2[1𝜆1+⋯+1𝜆d] We can pause at this stage and ask if there are other estimators that will give us a smaller MSE. It turns out that there is one such estimator, called the ridge estimator, that achieves this feat under suitable conditions. The ridge estimator is defined as: wridge=(XXT+𝜆I)-1Xy

Existence theorem: There exists a value of 𝜆>0 such that: MSE(wridge)<MSE(wML)

 This is good news. In the next section, we will try to understand an approach to the ridge estimator from a more practical viewpoint. 2. Overfitting and Underfitting2.1. Toy datasetConsider a regression problem with one feature in which the true relationship between the label and the feature is given by: g(x)=sin2𝜋x, 0⩽x⩽1 The label is a noisy, corrupted version of this function. The noise is an error term 𝜖 that is sampled from a zero mean Gaussian with variance of 0.1: 𝜖∼N(0,0.1)The label is therefore: yi∼N(g(xi),0.1) This is the data-generation part. In reality, we don't know the functional form of g(x). This is a toy dataset meant to aid in visualizing things. Let us look at a dataset of size n=10: D={(x1,y1),⋯,(x10,y10)}

 Though the relationship is non-linear, we can turn this into a linear regression problem by forming non-linear polynomial features. Let us assume that we settle for a third degree polynomial. The feature vector is: x=a

|  |
| --- |
| 1 |
| x |
| x2 |
| x3 |

 X is going to be a d×n matrix with d=4 and n=10. d=4 since we are also adding an intercept. The label vector is y. Concretely, X=a

|  |  |  |
| --- | --- | --- |
| 1 | ⋯ | 1 |
| x1 | ⋯ | x10 |
| x21 | ⋯ | x210 |
| x31 | ⋯ | x310 |

, y=a

|  |
| --- |
| y1 |
| ⋮ |
| y10 |

 The weight vector is going to be: w=a

|  |
| --- |
| w0 |
| w1 |
| w2 |
| w3 |

 Therefore, our model is: a

|  |  |
| --- | --- |
| f(x) | =w0+w1x+w2x2+w3x3 |
|  | =wTx |

Remark: As far as the original problem is concerned, f is a non-linear function of the feature. After adding more (polynomial) features, f is linear in the weights. This is still called a linear regression problem as far the weights are concerned. As far as the original feature space is concerned, one could call it polynomial regression.

 We can now learn the optimal weights by minimizing the SSE. We get: w=(XXT)-1Xy The weights we end up with are: w=a

|  |
| --- |
| -0.04 |
| 9.54 |
| -28.12 |
| 18.61 |

 If we plot the function learnt, this is how it looks:

 It seems like a reasonable fit. 2.2. OverfittingWhat if we change the degree of the polynomial features to be p=9? The resulting data-matrix will be of shape d×n with d=10,n=10. a

|  |  |
| --- | --- |
| f(x) | =w0+w1x+⋯+w9x9 |
|  | =wTx |

 If we run linear regression with this model, this is the result we get:

The model fits the noise in addition to the signal. This can be seen by the wild twists and turns that force the model to go through every training data-point. This problem is termed overfitting. The corresponding weight vector is: w=a

|  |
| --- |
| 0.02 |
| 62.12 |
| -1383.34 |
| 13019.05 |
| -63619.93 |
| 178687.61 |
| -300179.44 |
| 297927.91 |
| -160994.34 |
| 36480.26 |

 Also note the really high magnitudes for the components of the weight vector. Such high values are required if the model has to twist and turn like the way it has done here. An overfit model is said to be a high variance model: small changes in the dataset can result in wildly different models. For example:  Note the boxed region. A small change in the position of one or two data-points caused a big change in the fitted curve. 2.3. Data AugmentationIncreasing the data or augmenting it (data-augmentation) is one way of mitigating the problem of overfitting. For n=100, the same degree 9 model results in the following fit. Note how it is now a much better fit. This is because, the increased size of the data makes it impossible for even a degree 9 model to fit the noise.

 Coming back to the regression problem, the weight vector for this model is: w=a

|  |
| --- |
| -0.06 |
| 10.91 |
| -85.89 |
| 609.29 |
| -2557.32 |
| 5953.79 |
| -8253.17 |
| 6949.81 |
| -3318.79 |
| 691.52 |

 Note the relatively smaller values for the weights when compared to the previous case. Models that are really complex tend to overfit. A high-degree polynomial is one such example. 2.4. UnderfittingUnderfitting is the opposite problem of being unable to capture the signal or patterns in the data. For example, consider fitting a line for this dataset:

A line is too simple for the given data and completely misses the patterns. When a model underfits, it is usually a good idea to look for more complex models. 3. Model ComplexityIf the train loss is low and the test loss is high, the model is overfitting. If the train loss is itself high, the model is underfitting. Here is a general plot of train and test loss with respect to model complexity. One can think of model complexity as the degree of the polynomial features used in the example we have been working with so far. LossModel complexitytraintestunderfitoverfitNote how the training loss keeps decreasing as the models get more and more complex. The test loss decreases for a while and starts increasing beyond a point. The region between the dotted lines is an ideal place to look for the best model. 4. RegularizationRegularization is a method to mitigate overfitting. We can't always resort to adding more training data. In such situations, we impose a constraint on the model's weights and do not allow it to become to big in magnitude. Recall that the high magnitudes of weights is one of the reasons for overfitting. We study two forms of regularization. 4.1. Ridge Regression The loss function is modified as follows. This is called the regularized loss function: (1)L(w)=12⋅n∑i=1(wTxi-yi)2⏠⏣⏣⏣⏣⏣⏡⏣⏣⏣⏣⏣⏢SSE+𝜆2||w||22⏠⏣⏣⏡⏣⏣⏢regularization termwhere: ||w||22=w21+⋯+w2d There are two aspects to the regularized loss:• data-dependent loss: SSE• model-dependent loss: regularization term ||w||2 is the L2 norm of w. This is the usual Euclidean norm. 𝜆 is called the regularization rate and is a hyperparameter. The regularization term controls the complexity of the model. As 𝜆 increases, we force the model weights to shrink further, thus mitigating the overfitting problem to some extent. If 𝜆 is too high, then the model may start underfitting. An optimum choice has to be arrived at using cross validation or using a validation data. Cross validation is discussed later in this document.

Hyperparameters versus Parameters • parameters are learnt from data• hyperparameters are chosen prior to the learning– however, the best hyperparameter for a given problem is still determined by making use of the (validation) data– if sufficient data is not available to partition the data into a separate validation set, we use cross-validation.

 In the example we have been working with, for 𝜆=0.001, this is the resulting model:

 The corresponding weight vector: w=a

|  |
| --- |
| 0.14 |
| 5.38 |
| -10.52 |
| -4.02 |
| 2.33 |
| 4.89 |
| 4.44 |
| 2.22 |
| -0.81 |
| -4.10 |

 Ridge regression has the effect of pushing the weights nearer to zero though not exactly to zero. Next, let us see how to solve for w analytically: L(w)=12⋅n∑i=1(wTxi-yi)2⏠⏣⏣⏣⏣⏡⏣⏣⏣⏣⏢SSE+𝜆2||w||22⏠⏣⏣⏡⏣⏣⏢regularization term On setting the gradient to zero we have XXTw-Xy+𝜆w=0 Simplifying: (XXT+𝜆I)w=Xy Therefore: w=(XXT+𝜆I)-1Xy And we are back to the ridge estimator! Therefore, the ridge estimator can be seen as a practical technique to reduce overfitting. Geometric view The optimization problem can be equivalently formulated as:

min

w12⋅n∑i=1(wTxi-yi)2⏠⏣⏣⏣⏣⏣⏡⏣⏣⏣⏣⏣⏢SSEsubject to ||w||2⩽𝜃 where 𝜃 is some scalar dependent on 𝜆. Plotting the contours of the SSE and the constraint region, we can see the solution has to be the point where the contours of the SSE just touches the circular constraint: -6-4-2246810121416180-22468w1w2wMLwridge  Contours of the SSE We can look at the contours of the SSE in little more detail. Since the SSE achieves its minimum at wML, the value of the SSE at any other point going to be some non-negative constant c more than the minimum value: a

|  |  |
| --- | --- |
| ||XTw-y||2 | =||XTwML-y||2+c |

 Expanding this and using the fact that XXTwML=Xy we get: (w-wML)T(XXT)(w-wML)=c This is a quadratic form in w-wML whose contours correspond to ellipses in R2 and ellipsoids in higher dimensions. In the figure above, c=0 would correspond to the yellow dot, wML. As c increases, we get concentric ellipses of increasing sizes. 4.2. LASSO RegressionIn ridge regression the regularization term uses the L2 norm of the weight vector. Hence, this is sometimes called L2 regularization. Instead, if we use the L1 norm, then we get what is called LASSO regression: L(w)=12⋅n∑i=1(wTxi-yi)2⏠⏣⏣⏣⏣⏣⏡⏣⏣⏣⏣⏣⏢SSE+𝜆||w||1⏠⏣⏣⏡⏣⏣⏢regularization term where the L1 norm is given by: ||w||1=|w1|+⋯+|w|d It is also the Manhattan distance of the point w from the origin in Rd. No closed form solution can be found for LASSO regression. As before, we can plot the contours of the SSE and the constraint region: -6-4-2246810121416180-22468w1w2wMLw With a high probability, the contours of the SSE will hit one of the corners of the square. This results in a sparse solution, that is, one where some of the weights are exactly zero. LASSO is actually an acronym and stands for Least Absolute Shrinkage Selection Operator:• Least: we are solving a minimization problem• Absolute: the L1 norm uses the sum of the absolute values• Shrinkage: the weights are going to become smaller• Selection: since some weights go to zero, it acts as a feature selector A key point to note is the difference in the ridge and LASSO solutions. In ridge, the weights are pushed to zero though none of them become exactly zero. In the case of LASSO, some of the weights become exactly zero. Another point of difference is that unlike the case of ridge where we could differentiate the objective, the LASSO objective is not differentiable. 5. Cross ValidationAs mentioned earlier, 𝜆 is called hyperparameter. The process of determining the best value of a hyperparameter for a given problem is called hyperparameter tuning. One of the methods of hyperparameter tuning is called cross-validation. 5.1. k-Fold cross validationHere, the dataset is divided into k folds. Each fold has nk data-points.Fold-1Fold-2⋯Fold-kWe now follow the algorithm given below to choose the best 𝜆:

Algorithm • For 𝜆 in [10-4,10-3,⋯,102]•  – For k rounds:\* Train on k-1 folds and test on the remaining fold.· The size of the training dataset is nk(k-1)· The size of the validation dataset is nk· Store the validation loss\* Average the validation losses from the k models•  • Return 𝜆 that gives least average validation loss

 5.2. Leave one out cross validationThis is an extreme case of k-fold cross-validation.

Algorithm • For 𝜆 in [10-4,10-3,⋯,102]•  – For n rounds:\* Train on n-1 data-points and test on the remaining data-point.· The size of the training dataset is n-1· The size of the validation dataset is 1· Store the validation loss\* Average the validation losses from the n models•  • Return 𝜆 that gives least average validation loss

 6. Bayesian ViewpointWe can understand ridge regression from a Bayesian viewpoint. As before, we assume that the label vector follows the following multivariate normal distribution: y∼N(XTw,𝜎2I) We now assume that the weights have a certain prior. We don't want the weights to be too large. Therefore, we settle for a Gaussian prior with mean zero and variance 𝛾2. Prior w∼N(0,𝛾2I) P(w)=1(𝛾2𝜋)dexp[-||w||22𝛾2] The likelihood is as before: Likelihood L(w;D)=1(𝜎2𝜋)dexp[-||y-XTw||22𝜎2] With this, we can compute the posterior: Posterior Posterior∝Prior×Likelihood P(w | D)∝exp[-||y-XTw||22𝜎2+-||w||22𝛾2] MAP To get a point estimate for w, we maximize the posterior. This is called the maximum a posteriori estimate. Taking log for convenience:

max

w -||y-XTw||22𝜎2+-||w||22𝛾2 Maximizing this is the same as minimizing the negative of the objective:

min

w ||y-XTw||22𝜎2+||w||22𝛾2 Multiplying throughout by 𝜎2 and setting 𝜆=𝜎2𝛾2, we have:

min

w 12||y-XTw||2+𝜆2||w||2 This is the same as the ridge regression problem. Thus the MAP estimate with a zero mean Gaussian prior is equivalent to the solution to the ridge regression. The inverse relationship between 𝜆 and 𝛾 can be understood as follows: • Smaller the value of 𝛾, tinier the region in which we would like w to lie.•  • Alternatively, higher the value of 𝜆, the smaller we want the norm of the weights to be.