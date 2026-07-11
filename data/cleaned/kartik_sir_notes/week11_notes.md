aWeek-11Karthik Thiagarajan[1. Soft Margin SVM](#n0.14332213768754642) [1.1. Soft Margin](#n0.2723056712363945) [1.2. Optimization Problem](#n0.8547029968630644) [1.3. Hinge Loss Formulation](#n0.9462094155939169) [1.4. Solving the Optimization Problem](#n0.29765423086516996) [1.5. Primal and Dual](#n0.14054698903507146) [1.6. Complementary Slackness and Support vectors](#n0.21056625067439438) [1.6.1. Primal view](#n0.23862829063395652) [1.6.2. Dual view](#n0.3763623165757646) [1.7. SVM Scenarios](#n0.5942715504698526) [2. Overfitting and Underfitting](#n0.9106898472136027) [3. Ensemble Techniques](#n0.13944922017726924) [3.1. Bagging](#n0.10368092820345187) [3.1.1. Bootstrapping](#n0.8541100778363888) [3.1.2. Aggregation](#n0.9136947862931144) [3.1.3. Distribution of points in a bag](#n0.13853697690232591) [3.1.4. Random Forest](#n0.05510482491984292) [3.2. Boosting](#n0.3255761786345195) [3.2.1. AdaBoost](#n0.5433763680177357) 1. Soft Margin SVM1.1. Soft MarginWe will get rid of the linear separability assumption. In the context of SVM, this would mean that we allow points to violate the margin. That is, we are not going to stipulate a strict inequality of the form (wTxi)yi⩾1. Instead, we are going to be more lenient and allow some slack. Hence, the origin of the name "soft-margin". The two supporting hyperplanes continue to remain at wTx=±1. In order to penalize data-points that violate the margin, we assign a non-negative quantity 𝜉i for each data-point. Consider the specific case of a positive data-point violating the margin: wwTx=1wTx=0𝜉i||w||(wTxi)yi||w||+𝜉i||w||=1||w||wTx=(wTxi)yi(wTxi)yi||w||𝜉i=1-(wTxi)yi We can think of 𝜉i as the minimum (scaled) distance that the point has to move in the correct direction so that it no longer violates the margin. Here are some sample points along with their 𝜉i values: wwTx=1wTx=0wTx=-1𝜉=0wTx=3𝜉=0𝜉=1𝜉=2𝜉i=max(0,1-(wTxi)yi)(wTxi)yi+𝜉i⩾1 Points that violate the margin and are farther away from the correct supporting hyperplane suffer greater penalty. Points that are beyond the margin and on the right side of it do not suffer any penalty. This is expressed in a neat formula: 𝜉i=max(0,1-(wTxi)yi)1.2. Optimization Problem We can now formulate the optimization problem as follows:

min

w,𝜉 ||w||22+C⋅n∑i=1𝜉isubject to: a

|  |  |
| --- | --- |
| (wTxi)yi+𝜉i | ⩾1 |
| 𝜉i | ⩾0 |

, 1⩽i⩽n The objective has a new term n∑i=1𝜉i which is the total penalty paid across all data-points. C is a hyperparameter that controls the trade-off between the width of the margin and the violations.  1.3. Hinge Loss Formulation Since we know the exact expression for 𝜉i, we can get rid of the constraints and move it into the objective:

min

w ||w||22+C⋅n∑i=1max(0,1-(wTxi)yi) The expression n∑i=1max(0,1-(wTxi)yi) is termed the hinge loss. We can interpret the two terms in the loss as follows: ||w||22⏠⏣⏣⏡⏣⏣⏢margin+C⋅n∑i=1max(0,1-(wTxi)yi)⏠⏣⏣⏣⏣⏣⏣⏡⏣⏣⏣⏣⏣⏣⏢penalty The first term controls the width of the margin, the second controls the total penalty levied on the data-points. These two terms work in opposite directions. That is: • If ||w|| is small, the margin is wide. If the margin is wide, the penalty paid by points will be generally high.• If ||w|| is large, the margin is small. If the margin is small, the penalty paid by points will be generally low. Visually:w1wT1x=1wT1x=0wT1x=-1w2wT2x=1wT2x=-1wT2x=0  • A very small value of C implies that we don't mind the penalties, which encourages wide margins. In the limit as C→0, the supporting hyperplanes run away to infinity.• For a very large C, we are very particular about small penalties, encouraging smaller margin. As C→∞, we approach hard-margin SVM. Visually: C=0C=∞Wide marginLarge penaltyNarrow marginSmall penaltyPerfectmarginZero penalty(if linearly separable)InfinitemarginPenaltyirrelavant  Alternatively, the soft-margin objective can be interpreted as the sum of a data-dependent loss and a regularization term (L2). 1C plays the role of the regularization rate. ||w||22⏠⏣⏣⏡⏣⏣⏢Regularization+C⋅n∑i=1max(0,1-(wTxi)yi)⏠⏣⏣⏣⏣⏣⏣⏡⏣⏣⏣⏣⏣⏣⏢Hinge Loss 1.4. Solving the Optimization ProblemWe will revisit the optimization problem in its original form:

min

w,𝜉 ||w||22+C⋅n∑i=1𝜉isubject to: a

|  |  |
| --- | --- |
| (wTxi)yi+𝜉i | ⩾1 |
| 𝜉i | ⩾0 |

, 1⩽i⩽n Introducing the Lagrangian function and Lagrange multipliers, we get an equivalent formulation. 1.5. Primal and Dual Primal

min

w,𝜉

max

𝛼⩾0,𝛽⩾0 ||w||22+C⋅n∑i=1𝜉i+n∑i=1𝛼i(1-(wTxi)yi-𝜉i)-n∑i=1𝛽i𝜉i Dual

max

𝛼⩾0,𝛽⩾0

min

w,𝜉 ||w||22+C⋅n∑i=1𝜉i+n∑i=1𝛼i(1-(wTxi)yi-𝜉i)-n∑i=1𝛽i𝜉i Solving the unconstrained optimization problem within the dual, we get: w=n∑i=1𝛼ixiyiand 𝛼i+𝛽i=C, 1⩽i⩽n As before, we can rewrite w=XY𝛼. Since both 𝛼i and 𝛽i are non-negative, we see that 𝛼i,𝛽i∈[0,C] for all data-points. The dual problem therefore becomes:

max

0⩽𝛼⩽C⋅1 𝛼T1-12𝛼T(YTXTXY)𝛼 This is nearly identical to the hard-margin form. The only change between the two forms is the constraints. As before, we won't solve the dual, but assume that there are solvers that would give us the optimal values for 𝛼\*. 1.6. Complementary Slackness and Support vectors

DefinitionA support vector is a point for which 𝛼\*i>0.

 The complementary slackness conditions are: 𝛼\*i[1-(w\*Txi)yi-𝜉\*i]=0, 1⩽i⩽n 𝛽\*i𝜉\*i=0, 1⩽i⩽n Let us also add the primal and dual constraints: Primal constraints𝜉\*i⩾0, (w\*Txi)yi+𝜉\*i⩾1We also know:𝜉\*i=max(0,1-(w\*Txi)yi) Dual constraints𝛼\*i⩾0, 𝛽\*i⩾0, 𝛼\*+𝛽\*i=C In the following tables, here is the naming convention:• Correct supporting hyperplane: wTx=1 for positive data-points and wTx=-1 for negative data-points.• Right side of the correct supporting hyperplane: wTx>1 for positive data-points and wTx<-1 for negative data-points.• Wrong side of the correct supporting hyperplane: wTx<1 for positive data-points and wTx>-1 for negative data-points. 1.6.1. Primal view

|  |  |  |
| --- | --- | --- |
| Situation | Inference | Interpretation |
| (w\*Txi)yi>1 | • 𝜉\*i=0• 𝛼\*i=0 | Points that lie on the right side of the correct supporting hyperplane are not support vectors. |
| (w\*Txi)yi=1 | • 𝜉\*i=0• 𝛼\*i∈[0,C] | Points that lie on the correct supporting hyperplane could be support vectors. |
| (w\*Txi)yi<1 | • 𝜉\*i>0• 𝛼\*i=C | Points that lie on the wrong side of the correct supporting hyperplane are some of the most important support vectors. |

 1.6.2. Dual view

|  |  |  |
| --- | --- | --- |
| Situation | Inference | Interpretation |
| 𝛼\*i=0 | • 𝜉\*i=0• (w\*Txi)yi⩾1 | Points that are not support vectors lie on or on the right side of the correct supporting hyperplane. |
| 𝛼\*i∈(0,C) | • 𝜉\*i=0• (w\*Txi)yi=1 | Points that are support vectors with 𝛼\*i≠C lie on the correct supporting hyperplanes. |
| 𝛼\*i=C | • 𝜉\*i⩾0• (w\*Txi)yi⩽1 | Points that are the most important support vectors may either lie on the correct supporting hyperplane or on the wrong side of it. |

  1.7. SVM ScenariosWe have the following possibilities:

|  |  |
| --- | --- |
| Type of Dataset | Type of SVM |
|  | Hard-margin, Linear SVM |
|  | Soft-Margin, Linear SVM |
|  | Hard-Margin, Kernel SVM |
|  | Soft-Margin, Kernel SVM |

 The kernel is also a hyperparameter. 2. Overfitting and Underfitting• Bias: This measures the accuracy of the predictions or how close the model is to the true labels. Smaller the error, lower the bias. As the complexity of the model increases, bias tends to decrease. High bias models tend to underfit.• Variance: This measures the variability in the model to fluctuations in the training dataset. As the complexity of the model increases, variance tends to increase. High variance models tend to overfit. Bias and variance work in opposite directions. Models with a low bias tend to have high variance. Models with a high bias tend to have low variance. Low Bias, Low VarianceHigh Bias, Low VarianceLow Bias, High VarianceHigh Bias, High Variance Examples of low bias, high variance models:• Deep decision trees• Kernel regression with a polynomial kernel of high degree Examples of high bias, low variance models:• Decision stumps and very shallow decision trees• Vanilla linear regression on a non-linear dataset 3. Ensemble TechniquesEnsemble techniques attempt to aggregate or combine multiple models to arrive at a decision.3.1. BaggingBagging or bootstrap aggregation is a technique that tries to reduce the variance. The basic idea is this: averaging a set of observations reduces the variance. Instead of averaging observations, we will be averaging over models trained on different datasets. There are two steps: 3.1.1. Bootstrapping We start with the dataset D and create multiple versions or bags by sampling from D with replacement. Each bag has the same number of data-points as D. Let us call the number of bags B. For example with B=3: 12345D124Bag-12524Bag-251324Bag-3535 Note that points can repeat in a given bag. 3.1.2. Aggregation We train a model on each bag. Typically, this is a high-variance model, such as a deep decision tree. We call this hi, the model for the ith bag. If there are B bags, we can aggregate the outputs of all these models.  • For a regression problem, the method of aggregation could be the mean:1BB∑i=1hi(x)• For a classification problem, the method of aggregation could be the majority vote:sign(B∑i=1hi(x)) 3.1.3. Distribution of points in a bagFix a bag and consider an arbitrary data-point, say (xi,yi). The probability that this point gets picked as the first point in the bag is 1n. The probability that this point doesn't get picked as the first point is 1-1n. The probability that this point doesn't get picked at all in this bag is (1-1n)n, since we are sampling with replacement (independence). Therefore, the probability that this point appears at least once in a bag is (gets picked at all):1-(1-1n)nFor a very large dataset, this is about 1-1e≈63%. Therefore, about 63% of the data-points in a bag is unique. 3.1.4. Random Forest Random forests bag deep decision trees with a slight twist. While growing each tree, at each split (question-answer pair), instead of considering all d features, it randomly samples a subset of m features to choose from. m is typically around d. In this way, the resulting trees are uncorrelated. Since the trees are grown independently on their own bags, the algorithm can be run in parallel. 3.2. BoostingA weak learner is a model that does slightly better than a random model. For example, a model that produces an error rate of 0.48 would be a weak model. An error rate of 0.48 would mean that the model produces misclassifies 48% of the data-point. Decision stump is an example of weak model.  In boosting, we combine weak learners, typically high bias models such as decision stumps, and turn them into strong learners, with a low bias. This is achieved by a sequential algorithm that focuses on mistakes committed at each step. 3.2.1. AdaBoost

AdaBoost(D, weak-learner)• D0(i)=1n, 1⩽i⩽n • Repeat for T rounds•  – ht←Train a weak learner on (D,Dt-1)–  – 𝜖t=error(ht)= ∑ht(xi)≠yiDt-1(i)–  – 𝛼t=12ln(1-𝜖t𝜖t)–  – Dt(i)=a

|  |  |  |  |  |
| --- | --- | --- | --- | --- |
| e𝛼t⋅Dt-1(i), |  | ht(xi)≠yi, |  | (mistake) |
| e-𝛼t⋅Dt-1(i), |  | ht(xi)=yi, |  | (correct) |

–  – Dt(i)=Dt(i)n∑i=1Dt(i)•  • Return sign(T∑t=1𝛼t⋅ht)

 Observations:• Mistakes are boosted by  e𝛼t and correct data-points are brought down by e-𝛼t.• If 𝜖t is high, then 𝛼t is low. That is, if the classifier in round t has a higher error, it is assigned a lower weight in the final ensemble. It can be shown that as the number of rounds increases, the training error keeps decreasing. The training error of the final classifier after T rounds is at most: exp(-2T∑t=1𝛾2t)where 𝛾t=12-𝜖t.