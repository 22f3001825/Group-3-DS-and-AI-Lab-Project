aWeek-8Karthik Thiagarajan[1. Discriminative and Generative modeling](#n0.14332213768754642) [2. Generative models](#n0.4672805932765369) [3. Naive Bayes](#n0.23642051207913717) [4. Linear Discriminant Analysis (Gaussian Naive Bayes)](#n0.9519121431958606) 1. Discriminative and Generative modeling Generative model Learn the joint distribution between features and labels: P(x,y)=P(y)P(x | y) Data generation can be understood as a two step process: • Choose a class: this is governed by the prior P(y)• Sample a data-point from the class-conditional distribution P(x | y) Generative models are powerful if the distribution chosen closely matches the true process generating the data. Discriminative model Learn the conditional distribution of the label given the data-point: P(y | x) Discriminative models do not worry about how the data-point is generated. It is sufficient to "discriminate" between the two classes. 2. Generative models Binary classification Consider a binary classification problem with binary features: xi∈{0,1}d, yi∈{0,1} If the class-conditional independence is not assumed, the number of free parameters is given by: 2×(2d-1)+1Visually: Class-1Class-22d faces If the class-conditional independence is assumed, the number of free parameters is given by: 2×d+1 Visually, d coins, one parameter per coin: ⋯⋯Class-2Class-1 Multi-class classification, discrete feature set In general, if we have C classes: xi∈{0,⋯,k-1}d, yi∈{1,⋯,C} If the class-conditional independence is not assumed, the number of free parameters is given by: C×(kd-1)+(C-1) Visually:  Class-1Class-Ckd faces⋮ The number of parameters is exponential in the number of features. If the class-conditional independence is assumed, the number of free parameters is given by: C×d(k-1)+(C-1) Visually: ⋯Class-1⋯Class-C⋮ ⏠⏣⏣⏣⏣⏣⏣⏣⏣⏣⏡⏣⏣⏣⏣⏣⏣⏣⏣⏣⏢d featuresk faces3. Naive Bayes Notation Binary features, binary classification: xi∈{0,1}d, yi∈{0,1} xij=a

|  |  |  |
| --- | --- | --- |
| 1, |  | feature j is present in sample i |
| 0, |  | feature j is not present in sample i |

 Parameter for the prior probability of the label: p=P(Y=1) Parameter for feature j under class y: pyj=P(Xj=1 | Y=y) ⋯Class-1Class-0p01p02p0d⋯p11p12p1d MLE For one-data point (xi,yi): pyi(1-p)1-yid∏j=1(pyij)xij(1-pyij)1-xij For the entire dataset: L(𝜃;D)=n∏i=1[pyi(1-p)1-yid∏j=1(pyij)xij(1-pyij)1-xij] where 𝜃 is the collection of all parameters. Log-Likelihood l(𝜃;D)=n∑i=1ayilogp+(1-yi)log(1-p)1-yi+ d∑j=1xijlogpyij+(1-xij)log(1-pyij)a Estimates p=n∑i=1I[yi=1]n pyj=n∑i=1I[yi=y]xijn∑i=1I[yi=y] Smoothing • pyj=0 when no data-point in class y has xij=1. Alternatively, every data-point in class y has xij=0. This will create problems during prediction. To fix this, you add a data-point where all the features are 1 to both the classes.• pyj=1 when no data-point in class y has xij=0. Alternatively, every data-point in class y has xij=1. This will create problems during prediction. To fix this, you add a data-point where all the features are 0 to both the classes. You end up adding four data-points to the entire dataset, two in each class. This method is called Laplace smoothing. The numerator increases by 1 and the denominator increases by 2. Prediction Using Bayes' rule: P(y=1 | xtest)=P(y=1)⋅P(xtest | y=1)P(xtest) P(y=0 | xtest)=P(y=0)⋅P(xtest | y=0)P(xtest) If we only need to find the predicted label and not the actual probability, we just need to compute the numerators and compare their magnitudes: y=a

|  |  |  |
| --- | --- | --- |
| 1, |  | P(y=1)⋅P(xtest | y=1)⩾P(y=0)⋅P(xtest | y=0) |
| 0, |  | otherwise |

 Decision Boundary P(y=1 | x)P(y=0 | x)=1 The decision boundary is linear: wTx+b=0 where: a

|  |  |
| --- | --- |
| wj | =log[p1j(1-p0j)  p0j(1-p1j)] |
|  |  |
| b= | log(p  1-p)+d∑j=1log(1-p1j  1-p0j) |

 4. Linear Discriminant Analysis (Gaussian Naive Bayes) This is a generative model where all the features are continuous. We assume that the data for a given class is drawn from a multi-variate Gaussian. The two classes are assumed to share the same covariance matrix. Class conditional density x | y=0∼N(𝜇0,Σ)  P(x)=1(2𝜋)d|Σ|exp[-12(x-𝜇0)TΣ-1(x-𝜇0)]  x | y=1∼N(𝜇1,Σ) P(x)=1(2𝜋)d|Σ|exp[-12(x-𝜇1)TΣ-1(x-𝜇1)]  Estimates from MLE 𝜇1=n∑i=1I[yi=1]xin∑i=1I[yi=1], 𝜇0=n∑i=1I[yi=0]xin∑i=1I[yi=0] Σ=1nn∑i=1(xi-𝜇yi)(xi-𝜇yi)T Decision Boundary wTx+b=0 a

|  |  |
| --- | --- |
| w | =(𝜇0-𝜇1)TΣ-1 |
|  |  |
| b | =1  2[𝜇T1Σ-1𝜇1-𝜇T0Σ-1𝜇0+logp  1-p] |

 The decision boundary is linear.