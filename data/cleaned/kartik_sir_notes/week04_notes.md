aWeek-4Karthik Thiagarajan[1. Estimation: Introduction](#n0.3258430873283915) [2. Maximum Likelihood Estimation](#n0.3355767526845632) [2.1. Bernoulli](#n0.7646399686835019) [2.2. Gaussian](#n0.4582616052248769) [3. Bayesian methods](#n0.6306451241307149) [3.1. Bernoulli with Beta prior](#n0.8791102751723499) [3.2. Point estimate](#n0.8099598093234013) [4. Gaussian Mixture Models](#n0.7186865983310531) [5. GMM and MLE](#n0.3556715585761875) [6. EM algorithm](#n0.9519613760251677) [7. (\*) Proof of Correctness](#n0.27746030125296806) [8. References](#n0.9635305381625096) Starred (\*) section may be mathematically heavy. Handle with care.1. Estimation: Introduction So far, we have seen two unsupervised learning problems, dimensionality reduction and clustering, and the corresponding algorithms for them, PCA and K-means. In both these situations, we weren't worried about how the data was generated. We did expect the dataset to satisfy certain assumptions and proceeded from there. For example, in vanilla PCA we wanted linearity and in K-means we wanted the data to lie in Voronoi regions. In this week, we start modeling the data generation process. One can also treat this as an introduction go probabilistic generative models. We assume that there is an underlying probability distribution over the features. The dataset then becomes a collection of points, where each point is sampled from this distribution. For example, consider a dataset with one feature, say {1,-0.3,5,0.2,-0.1}. We could assume that this came from some normal distribution with mean 𝜇 and variance 𝜎2, where 𝜇 and 𝜎2 are parameters of the distribution that are fixed, but unknown to us. Understanding the dataset then turns into a process of estimating the parameters of the distribution given the dataset.  In the rest of the document we will look at various methods of parameter estimation and take up specific distributions to understand their applicability. 2. Maximum Likelihood Estimation The first method is maximum likelihood estimation (MLE). Likelihood We assume that the data-points are drawn i.i.d from the distribution. Recall that i.i.d stands for independent and identically distributed. The likelihood of a dataset D under a distribution parameterized by 𝜃 is given below. L(𝜃;D)=n∏i=1P(xi;𝜃) A few points concerning the likelihood: • The likelihood is the "likelihood" of seeing the data as the result of drawing samples from the underlying distribution. That is, it is a measure of how likely it is to observe a collection of data-points drawn from a distribution with parameter value 𝜃.•  • It takes this particular form if the points are assumed to be sampled independently and identically from the distribution. The independence allows us to multiply the individual probabilities/densities. The identical nature allows us to use the same PMF/PDF.•  • The likelihood is a function of the parameter 𝜃. It should not be confused with a probability distribution. The dataset D remains fixed. As 𝜃 changes, we get different values for the likelihood.•  • P could be a PMF or a PDF depending on the whether xi is discrete or continuous. Log-likelihood l(𝜃;D)=n∑i=1logP(xi;𝜃) Since product of probabilities would result in a very small number, we move to log-space to avoid underflow. Maximizing the log-likelihood We now look for the parameter value that maximizes the likelihood:

max

𝜃 L(𝜃;D) Since logis a strictly increasing function, we can maximize the log-likelihood instead:

max

𝜃 l(𝜃;D) We will take up two examples. In both cases, the dataset has n data-points. 2.1. Bernoulli Consider a dataset where each data-point xi∈{0,1}. We can think of this as tossing a coin, where 1 corresponds to heads and 0 to tails. Now, let X be a random variable with support {0,1} that follows the Bernoulli distribution with parameter p, where p=P(X=1). The PMF of X is given by: pX(x)=a

|  |  |  |
| --- | --- | --- |
| p, |  | x=1 |
| 1-p, |  | x=0 |

 This can be compactly expressed as: pX(x)=px(1-p)1-x Note that pX(1)=p and pX(0)=1-p as expected. The likelihood of the dataset as a function of p is given below: a

|  |  |
| --- | --- |
| L(p;D) | =n∏i=1pxi(1-p)1-xi |
|  |  |
|  | =pn∑i=1xi(1-p)n∑i=1(1-xi) |
|  |  |
|  | =pnh(1-p)nt |

 where nh is number of heads and nt is number of tails. Note nh+nt=n. The log-likelihood now becomes: l(p;D)=nhlogp+ntlog(1-p) To get the MLE, we differentiate the log-likelihood with respect to p and set it to zero: a

|  |  |
| --- | --- |
| dl  dp | =nh  p-nt  1-p=0 |
|  |  |
| ⟹ | p=nh  n |

 We usually denote the MLE of a parameter by adding a   above the parameter. Therefore, the maximum likelihood estimate is given by:

p=nhn

 This is just the mean of the data-points.

Estimator vs Estimate: If Xi is the random variable corresponding to the ith sample, then p=1nn∑i=1Xi is an unbiased estimator for the parameter p. An estimator is a function of the n random variables and is itself a random variable. When we have the realizations x1,⋯,xn, the actual dataset, then we have p=1nn∑i=1xi, which is an estimate. It is a realization of the estimator and is a deterministic value. We will stick to the estimate in this document.

 2.2. Gaussian Now we turn to the Gaussian distribution. Let xi∈R. We can model this using a continuous random variable that follows a Gaussian distribution with parameters 𝜇 and 𝜎2. That is, X∼N(𝜇,𝜎2). The PDF is given by: fX(x)=12𝜋𝜎2exp[-12(x-𝜇𝜎)2] Once again assuming i.i.d, the likelihood is expressed as: L(𝜇,𝜎2;D)=n∏i=1fX(xi) Note that L is now a function of two parameters, 𝜇 and 𝜎2. Turning to the log-likelihood as before: a

|  |  |
| --- | --- |
| l(𝜇,𝜎2;D) | =n∑i=1logfX(xi) |
|  |  |
|  | =n∑i=1-1  2log(2𝜋𝜎2)-1  2𝜎2(xi-𝜇)2 |

 Since this is a multivariable function, we need to work with the partial derivatives: a

|  |  |
| --- | --- |
| ∂l  ∂𝜇 | =n∑i=1(xi-𝜇)=0 |
|  |  |
| ⟹𝜇 | =1  nn∑i=1xi |

 We see that the MLE for 𝜇 is the sample mean: 𝜇=1nn∑i=1xi Next, we go for 𝜎: a

|  |  |
| --- | --- |
| ∂l  ∂𝜎 | =n∑i=1-1  𝜎+1  𝜎3(xi-𝜇)2=0 |
|  |  |
| ⟹𝜎2 | =1  nn∑i=1(xi-𝜇)2 |

 Plugging in the value of 𝜇, we get: 𝜎2=1nn∑i=1(xi-𝜇)2 This is nothing but the sample variance. Putting the two together, the MLE estimates are:

𝜇=1nn∑i=1xi, 𝜎2=1nn∑i=1(xi-𝜇)2

  3. Bayesian methodsIn a Bayesian setting, probabilities are viewed as beliefs. The probability P(A)=0.3 indicates that we are about 30% confident that event A will occur. Contrast this with the frequentist interpretation in which we repeatedly run an experiment and claim that event A occurs 30% of the times. Both are valid approaches to interpret probabilities. In this section, we will look at the Bayesian framework. Bayes Theorem The Bayes theorem is a tool that allows us to update our belief about a situation using data. One way of presenting it is given below: Posterior=Prior×LikelihoodEvidence • The prior encodes our prior belief about the situation before observing the data (evidence).•  • The likelihood tells us how well the data conforms to our prior belief.•  • The likelihood is multiplied with the prior and normalized with the evidence to give the posterior, the updated belief. The evidence is a normalizing factor here. Since the evidence is a constant, we can also express the relationship as: Posterior∝Prior×Likelihood The prior belief when modified by the likelihood results in the posterior. In the context of parameter estimation, Bayes theorem takes this form: P(𝜃 | D)=P(𝜃)⋅P(D | 𝜃)P(D) We have a certain prior belief about the parameter 𝜃 of the underlying distribution describing the data. The likelihood of observing the data given this parameter then modifies the prior belief multiplicatively to give us the updated belief about the parameter 𝜃 given the data, which we call the posterior. A note on the type of objects in the Bayes theorem: Posterior=Prior×LikelihoodEvidencefunctionscalardistribution • The prior and posterior are probability distributions of the parameter 𝜃.• The likelihood is a function of the parameter 𝜃 for the given dataset.• The evidence is a scalar value that acts as a normalizing constant. We will look at an example of Bayesian estimation for a binary dataset in {0,1}n modeled using a Bernoulli distribution with parameter p and a Beta prior for p. 3.1. Bernoulli with Beta prior Consider a dataset D in which each xi∈{0,1}. As before, we will model this using a Bernoulli distribution. Let X∼Bernoulli(p), where p is the parameter of the distribution. In MLE, we estimated p by maximizing the likelihood. In a Bayesian setting, we start with a probability distribution over p that encodes our initial belief. The Beta distribution is a suitable choice since its support is [0,1] which coincides with the range of values p can assume. Beta Prior Beta(𝛼,𝛽)=1𝛣(𝛼,𝛽)p𝛼-1(1-p)𝛽-1 Here: • 𝛼,𝛽>0 are parameters of the distribution.•  • The support is [0,1].•  • 𝛣(𝛼,𝛽), called the Beta function, is a normalizing constant that ensures that Beta(𝛼,𝛽) is a valid PDF. Let us take a quick look at some of the shapes that the Beta distribution can assume as we vary the parameters 𝛼,𝛽. Each one can model a different belief. 101210121012101210121012Beta(2,5)Beta(5,2)Beta(3,3)Beta(0.5,3)Beta(3,0.5)Beta(0.5,0.5)To link this with a practical experiment, we can think of a biased coin whose probability of landing heads is p. We will compare some of these shapes and connect them with the corresponding prior beliefs about the nature of the coin:

|  |  |  |
| --- | --- | --- |
| Belief | Prior | Shape |
| We believe that the coin is more or less unbiased. | Beta(3,3) | 1012 |
| We believe that the coin is considerably biased towards heads. | Beta(5,2) | 1012 |
| We believe that the coin is heavily biased, but have no clue about the direction of the bias. | Beta(0.5,0.5) | 1012 |

 Now we get back to the problem. The Bernoulli likelihood should be quite familiar by now. If we have nh heads and nt tails, with nh+nt=n, then the likelihood is: pnh(1-p)nt Which brings us to the posterior: Posterior We have:Posterior∝Prior×Likelihood Plugging the prior and likelihood: a

|  |  |
| --- | --- |
| Posterior | ∝p𝛼-1(1-p)𝛽-1pnh(1-p)nt |
|  |  |
|  | ∝p(𝛼+nh)-1⋅(1-p)(𝛽+nt)-1 |

 The quantity on the RHS has the form of the Beta distribution! It is just a scaled version of the Beta distribution with parameters 𝛼+nh and 𝛽+nt. It will become a distribution once we normalize it. Fortunately, we needn't worry about the normalization factor here and we can directly express the posterior as:

Posterior=Beta(𝛼+nh,𝛽+nt)

 The Beta distribution is said to be a conjugate prior for the Bernoulli likelihood. A conjugate prior has a similar form as the likelihood thus allowing us to simplify the computation of the posterior. If we didn't have this conjugate prior-likelihood pair, then we would have to compute the normalizing constant by explicitly integrating the product of prior and likelihood over the support of the parameter, a task that might prove to be difficult, if not impossible. There is an interesting interpretation of this update: Beta(𝛼,𝛽)→Beta(𝛼+nh,𝛽+nt) • We can view 𝛼 and 𝛽 as pseudo-observations. It is as though we already have observed 𝛼 heads and 𝛽 tails and then go on to observe the dataset D with nh heads and nt tails. • We have to be careful to not take this interpretation too literally since 𝛼,𝛽 are not necessarily integers. 3.2. Point estimate Often we want a point estimate (a single number) for the parameter. The MLE was a point estimate. However, Bayesian methods return a distribution (posterior) over the parameter. We look at two ways to extract a point estimate: • expectation of the posterior•  • mode of the posterior For this Beta prior-Bernoulli likelihood, the expected value of the posterior is:

𝛼+nh𝛼+𝛽+n

 This has a clean interpretation as the proportion of heads after including the pseudo observations while acknowledging the caveat that 𝛼,𝛽 are not necessarily integers. The mode of the posterior for 𝛼+nh>1,𝛽+nt>1 is:

𝛼+nh-1𝛼+𝛽+n-2

 In this context, the mode of the posterior is also called the Maximum A Posteriori estimate or MAP estimate, since the mode is nothing but the (arg)maximum of the posterior. In a general setting: 𝜃MAP=

argmax

𝜃 f(𝜃 | D)

Remark: In general, for a Beta distribution with parameters 𝛼,𝛽, the expectation is 𝛼𝛼+𝛽. The mode is a bit tricky and has to be defined in a piecewise manner depending on the range of 𝛼 and 𝛽. When 𝛼>1 and 𝛽>1, the mode is given by 𝛼-1𝛼+𝛽-2.

 4. Gaussian Mixture Models For more complex datasets, we turn to what is called a Gaussian Mixture Model. A GMM is a probability distribution. It is a mixture of K Gaussians, each of which is called a component. Once again we let X denote the random variable and xi∈R, i=1,⋯,n, the data-points that are sampled i.i.d from the distribution governing X. If fX(⋅) denotes the density of the GMM, we have: fX(x)=K∑k=1𝜋k⋅N(x;𝜇k,𝜎2k) where K∑k=1𝜋k=1 so that fX is a valid PDF. Here: • fX is the PDF of the GMM.•  • N is the PDF of a Gaussian distribution with mean 𝜇k and variance 𝜎2k•  • 𝜋k the "prior" contribution of the kth component. Collectively, the 𝜋ks are called the mixture probabilities. A GMM is a latent variable model. That is, we can view the data-generation process by introducing a latent (hidden) variable zi for each data-point. Generating xi can then be explained as follows: • First sample a component k by setting zi=k with prior probability 𝜋k•  • Sample a point from the corresponding Gaussian; the conditional density associated with this is N(x;𝜇k,𝜎2k) To be a little more rigorous, we now introduce the random variable Z to denote the component indicator. Z has support {1,⋯,K} with the following PMF: pZ(k)=𝜋k Recall that we use capital letters for random variables and small letters for realizations. The joint density of generating the point x from component z becomes: fX,Z(x,z)=pZ(z)⋅fX | Z(x | z) For a specific realization xi and k, we have: fX,Z(xi,k)=𝜋kN(xi;𝜇k,𝜎2k) Next, to get the density of the GMM, we marginalize over the random variable Z: a

|  |  |
| --- | --- |
| fX(x) | =K∑k=1fX,Z(x,k) |
|  |  |
|  | =K∑k=1pZ(k)⋅fX | Z(x | k) |

 This leads us to: fX(x)=K∑k=1𝜋k⋅N(x;𝜇k,𝜎2k) This is the density of the GMM as obtained earlier but seen through the lens of latent variables. Note that the latent variables are not explicitly observed. Only the dataset D is observed. However, the introduction of the latent variables will prove beneficial as we will soon see. 5. GMM and MLE Once we have a distribution, we can follow the established recipe of estimating its parameters using MLE. For a GMM with K components, we need to estimate 3K-1 free parameters: • K-1 mixture probabilities•  • K means•  • K variances Since K∑k=1𝜋k=1, we only have K-1 free variables for the mixture probabilities. The parameters are collectively referred to as 𝜃=[𝜋,𝜇,𝜎]. The log-likelihood of the GMM can now be written as: a

|  |  |
| --- | --- |
| l(𝜃;D) | =n∑i=1logfX(xi) |
|  |  |
|  | =n∑i=1logK∑k=1𝜋k⋅N(xi;𝜇k,𝜎2k) |

 The difficulty here is that it is hard to optimize l(𝜃;D) directly. We will not get a closed-form expression for the parameters. One of the problems is the sum inside the log. One way to convert a log of sums into a sum of logs is provided by the Jensen's inequality.

Jensen's Inequality: For 0⩽𝛼1,𝛼2⩽1 and 𝛼1+𝛼2=1 and for all x1,x2>0, we have: log(𝛼1x1+𝛼2x2)⩾𝛼1logx1+𝛼2logx2 To understand this better, consider: log(12⋅2+12⋅5)⩾12⋅log2+12⋅log5Visually:11.522.533.544.55log2log512(log2+log5)log(2+52)log is a concave function and is dome shaped. To remember the inequality, use the mnemonic that the "dome is always above the lines across its surface". In general, for 0⩽𝛼1,⋯,𝛼n⩽1 and 𝛼1+⋯+𝛼n=1, and for all x1,⋯,xn>0, we have: log(𝛼1x1+⋯+𝛼nxn)⩾𝛼1logx1+⋯+𝛼nlogxn This can also be viewed in terms of the expectation of some random variable whose support is {x1,⋯,xn} and the PMF being pX(xi)=𝛼i. Therefore, Jensen's inequality becomes:

log(E[X])⩾E[logX]

 Equality occurs when X is a constant.

 Back to the log-likelihood:a

|  |  |
| --- | --- |
| l(𝜃;D) | =n∑i=1logK∑k=1𝜋k⋅N(xi;𝜇k,𝜎2k) |

 Since K∑k=1𝜋k=1, we could apply Jensen's inequality right away. However, that won't take us very far. It turns out that it helps to introduce certain intermediate variables denoted as 𝜆ik into the equation. Specifically: • i: corresponds to index of the data-point•  • k: corresponds to index of the component • 0⩽𝜆ik⩽1– K∑k=1𝜆ik=1 for all i•  • There are Kn such variables out of which n(K-1) are free Multiplying and dividing each term inside the log by the appropriate 𝜆ik, we have: a

|  |  |
| --- | --- |
| l(𝜃;D) | =n∑i=1logK∑k=1𝜆ik⋅𝜋k⋅N(xi;𝜇k,𝜎2k)  𝜆ik |

 Now, we can apply Jensen's inequality to get: a

|  |  |
| --- | --- |
| l(𝜃;D) | =n∑i=1logK∑k=1𝜆ik⋅𝜋k⋅N(xi;𝜇k,𝜎2k)  𝜆ik |
|  |  |
|  | ⩾n∑i=1K∑k=1𝜆iklog𝜋k⋅N(xi;𝜇k,𝜎2k)  𝜆ik |

 Denoting the new quantity on the right hand side as lB(𝜃,𝜆;D), we have: l(𝜃;D)⩾lB(𝜃,𝜆;D) lB(𝜃,𝜆;D) is a lower-bound for every choice of 𝜃 and 𝜆 as long as 𝜆 satisfies K∑k=1𝜆ik=1 for each i. This is often called the [Evidence Lower Bound](https://en.wikipedia.org/wiki/Evidence_lower_bound) (ELBOW). It seems as though Jensen has only complicated things. But we will see how this simple algebraic trick pays off in the next section. 6. EM algorithm If we can't maximize the log-likelihood explicitly, we can at least try and maximize its lower bound. If that proves to be a tractable approach, then we have a reasonable comprise. Expectation-Maximization is an iterative algorithm that takes this approach towards parameter estimation for latent variable models. We will stick to EM algorithm applied to GMMs in this document. As stated earlier, the parameters are collectively referred to as 𝜃=[𝜋,𝜇,𝜎] and the intermediate variables are collectively referred to as 𝜆. We revisit the lower bound: l(𝜃;D)⩾lB(𝜃,𝜆;D) where: lB(𝜃,𝜆;D)=n∑i=1K∑k=1𝜆ik⋅log[𝜋k⋅N(xi;𝜇k,𝜎2k)𝜆ik] We start with an initial guess for 𝜃, denoted 𝜃(0), and keep bettering our estimate in each iteration of the algorithm. An iteration consists of two steps: • Expectation-step or E-step: estimate the values for 𝜆 using the current values of 𝜃(t-1) • Maximization-step or M-step: update the values for 𝜃(t) using the newly found values of 𝜆 The sequence of steps can be visualized as follows: 𝜃(0)→𝜆→𝜃(1)⏠⏣⏣⏡⏣⏣⏢iteration-1→𝜆→𝜃(2)⏠⏣⏣⏡⏣⏣⏢iteration-2→⋯→𝜃(T-1)→𝜆→𝜃(T)⏠⏣⏣⏡⏣⏣⏢iteration-T The value of 𝜆 computed in the E-step doesn't get carried over from one iteration to the other. Hence, we have dropped the iteration counter superscript for it. As for convergence, the log-likelihood can be shown to be monotonically increasing from one iteration to the next, that is: l(𝜃(t+1);D)⩾l(𝜃(t);D) When successive iterates become smaller than some 𝜖, we can terminate the algorithm. Therefore, one termination criterion could be: ||𝜃(t+1)-𝜃(t)||<𝜖 We now specify the pseudocode first and then expand on each of the steps after that: a

|  |  |
| --- | --- |
|  | EM(X,𝜖) |
| 1 | 𝜃(0)←initializeParams(X) |
| 2 | do |
| 3 | 𝜆←eStep(X,𝜃(t)) |
| 4 | 𝜃(t+1)←mStep(X,𝜆) |
| 5 | while ||𝜃(t+1)-𝜃(t)||⩾𝜖 |
| 6 | return 𝜃(t+1) |

 Initialization A common practice is to use K-means to initialize 𝜃(0). We run K-means with K equal to the number of components in the GMM, that is, as many clusters as there are components in the mixture model. Once that is done, let zis denote the indicators of the final clusters. Then, we can initialize 𝜋(0), 𝜇(0) and 𝜎(0) as follows: a

|  |  |
| --- | --- |
| 𝜋(0)k | =n∑i=1I[zi=k]  n |
|  |  |
| 𝜇(0)k | =n∑i=1I[zi=k]⋅xi  n∑i=1I[zi=k] |
|  |  |
| 𝜎2k(0) | =n∑i=1I[zi=k]⋅(xi-𝜇(0)k)2  n∑i=1I[zi=k] |

 Note that 𝜇(0)k is just the mean of the kth cluster. 𝜋(0)k is the fraction of the data-points in that cluster and 𝜎2k(0) is its variance. This acts as a very natural initialization for EM. E-step In the E-step, we use the current parameter values to estimate 𝜆ik.  a

|  |  |
| --- | --- |
| 𝜆ik | =P(Zi=k | X=xi) |
|  |  |
|  | =pZ | X(k | xi) |

 𝜆ik is the posterior probability of observing component k given xi. That is, given that xi is observed, it reveals the probability of observing component k. Alternatively, 𝜆ik is the contribution of the kth component to the point xi given that we have observed the point xi. Using the Bayes' theorem, we can express this as: a

|  |  |
| --- | --- |
| 𝜆ik | =pZ(k)⋅fX | Z(xi | k)  fX(xi) |
|  |  |
|  | =pZ(k)⋅fX | Z(xi | k)  K∑l=1pZ(l)⋅fX | Z(xi | l) |
|  |  |
|  | =𝜋k⋅N(xi;𝜇k,𝜎2k)  k∑l=1𝜋l⋅N(xi;𝜇l,𝜎2l) |

 Note that 𝜋k,𝜇k,𝜎2k are the values at time-step t. The superscript has been ignored for simplicity. M-Step Next, we use the values of 𝜆ik obtained in the E-step to update the values of 𝜋k,𝜇k,𝜎2k. The updates take the following form: 𝜇k=n∑i=1𝜆ik⋅xin∑i=1𝜆ik, 𝜎2k=n∑i=1𝜆ik⋅(xi-𝜇k)2n∑i=1𝜆ik 𝜋k=n∑i=1𝜆ikn This has quite an intuitive interpretation. The mean 𝜇k is a weighted average of all the data-points, where the weight is 𝜆ik. This weight indicates the contribution of the data-point xi towards the formation of the mean of component k. A similar interpretation holds for the variance of each component.  Similarity with K-Means The trend of the overall algorithm becomes clearer when we compare this with K-means. 𝜆ik can be seen as the affinity of xi to component k. In K-means this affinity is binary -- a point either belongs to a cluster or it doesn't, it represents a hard assignment. In the case of EM, this affinity is a number between [0,1], a soft assignment. The E-step is analogous to the cluster reassignment step in K-means. The M-step is analogous to the updates for the cluster centers in K-means. We display this correspondence in the table below:

|  |  |
| --- | --- |
| EM Algorithm | K-Means |
| E-step: 𝜆ik=pZ | X(k | xi) | Reassignment-step:  𝜆ik=a  |  |  |  | | --- | --- | --- | | 1, |  | xi is closest to 𝜇k | | 0, |  | otherwise | |
| M-step:𝜇k=n∑i=1𝜆ikxi  n∑i=1𝜆ik 𝜎2k=n∑i=1𝜆ik(xi-𝜇k)2  n∑i=1𝜆ik 𝜋k=n∑i=1𝜆ik  n | Update means:    𝜇k=n∑i=1𝜆ik⋅xi  n∑i=1𝜆ik |

 For this reason, EM can be viewed as doing a soft-clustering instead of a hard clustering. The 𝜆ik values contain this information. 7. (\*) Proof of Correctness We now look at the algorithm in a little more detail to understand how we got here. The lower bound of the log-likelihood obtained using Jensen's inequality is the key result. Recall that: l(𝜃;D)⩾lB(𝜃,𝜆;D) where: lB(𝜃,𝜆;D)=n∑i=1K∑k=1𝜆ik⋅log[𝜋k⋅N(xi;𝜇k,𝜎2k)𝜆ik] As stated before, this inequality holds for all 𝜃 and all 𝜆 that satisfies K∑k=1𝜆ik=1. The idea is to maximize the lower bound. For a given 𝜃(t), a natural tendency is to look for that 𝜆 which will push lB(𝜃(t),𝜆) to its maximum value. Since lB lower bounds l, the best case scenario would happen if we can find a 𝜆 with: lB(𝜃(t),𝜆)=l(𝜃(t),𝜆) Can this ever happen? Indeed it does when 𝜆ik=pZ | X(k | xi), this is precisely our E-Step! The proof is quite straightforward. Assuming that 𝜃(t)=[𝜋,𝜇,𝜎]: a

|  |  |
| --- | --- |
| lB(𝜃(t),𝜆;D) | =n∑i=1K∑k=1𝜆ik⋅log[𝜋k⋅N(xi;𝜇k,𝜎2k)  𝜆ik] |
|  |  |
|  | =n∑i=1K∑k=1𝜆ik⋅log[𝜋k⋅N(xi;𝜇k,𝜎2k)⋅1  𝜆ik] |
|  |  |
|  | =n∑i=1K∑k=1𝜆ik⋅log[𝜋k⋅N(xi;𝜇k,𝜎2k)⋅K∑l=1𝜋l⋅N(xi;𝜇l,𝜎2l)  𝜋k⋅N(xi;𝜇k,𝜎2k)] |
|  |  |
|  | =n∑i=1K∑k=1𝜆ik⋅log[K∑l=1𝜋l⋅N(xi;𝜇l,𝜎2l)] |
|  |  |
|  | =n∑i=1log[K∑l=1𝜋l⋅N(xi;𝜇l,𝜎2l)]K∑k=1𝜆ik |
|  |  |
|  | =n∑i=1log[K∑l=1𝜋l⋅N(xi;𝜇l,𝜎2l)] |
|  |  |
|  | =l(𝜃(t);D) |

 Visually, here is what we are doing if we consider time step t (credits-Bishop). The red curve is the log-likelihood. The blue curve is the lower bound that we get as a result of the E-step. lB(𝜃,𝜆;D)l(𝜃;D)l(𝜃(t);D)lB(𝜃(t),𝜆;D)E-step𝜃(t) Once the E-step is done, we turn to the M-step, where we maximize the lower bound with respect to 𝜃. The updated value 𝜃(t+1) lies at the peak of the lower bound. This is a conventional optimization problem, where we take partial derivatives of lB(𝜃,𝜆;D) with respect to each parameter, set it to zero, and arrive at the resulting estimates. Visually, this is the result of the M-Step: 𝜃(t+1)lB(𝜃,𝜆;D)l(𝜃;D)l(𝜃(t);D)𝜃(t)l(𝜃(t+1);D)M Step We now keep alternating between these two steps.  Finally, we come to the question of convergence. We have to show the following: l(𝜃(t+1);D)⩾l(𝜃(t);D) This is nicely captured in this chain of inequalities/equalities given below. Here, 𝜆 is the value obtained in the E-step in iteration t. l(𝜃(t);D)=lB(𝜃(t),𝜆;D)⩽lB(𝜃(t+1),𝜆;D)⩽l(𝜃(t+1);D) The chain has to be read from left to right: • l(𝜃(t);D)=lB(𝜃(t),𝜆;D) is true because of the E-step. The choice of 𝜆 ensures that the lower bound is strict at 𝜃(t). • lB(𝜃(t),𝜆;D)⩽lB(𝜃(t+1),𝜆;D) is true because of the M-step. Once 𝜆 is fixed, 𝜃(t+1) is the value that maximizes the lower bound. • lB(𝜃(t+1),𝜆;D)⩽l(𝜃(t+1);D) is true because lB is anyway a lower bound for the log-likelihood. 8. References Outside of our lectures, the following references were used: • Pattern Recognition and Machine Learning, Bishop.•  • CS229 Lecture Notes, Stanford, Andrew NG, updated by Tengyu Ma