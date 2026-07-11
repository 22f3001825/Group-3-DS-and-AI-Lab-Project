# **Gaussian Mixture Model and EM Algorithm** 

✉ 23f1001171@ds.study.iitm.ac.in (Piush Das) 

### **Introduction** 

Till now everything we learned was deterministic, In this upcoming slides we will do some probabilistic assumption about the data. "There is some probabilistic mechanism that generates the data about which we don't know something. Given data, find / estimate what we don't know" 




Unknown Parameter<br>

### **Goal of Estimation** 

- Observe the data 

- Assume a probabilistic model 

- Estimate unknown parameters using the data 

✉ 23f1001171@ds.study.iitm.ac.in (Piush Das) 

##### **Example :** 

Observe the outcome of experiment 



**Estimate :** 



##### **The Assumption about the Observation are** 

##### **1. Independence** 

The outcome of one data point does not affect or depend on the outcome of another. 



##### **2. Identically Distributed** 

All data points come from the same probability distribution 





### **Maximum Likelihood Estimation** 

The likelihood of a dataset D under a distribution parameterized by θ is given below : 



- The likelihood is the "likelihood" of seeing the data if it is the result of drawing samples from the underlying distribution. 

- It takes this particular form if the points are assumed to be sampled independently and identically from the distribution. 

- The likelihood is a function of the parameter θ. It should not be confused with a probability distribution. 

- P could be a PDF or a PMF depending on the whether xi is discrete or continuous. 

##### **Bernoulli Distribution** 





✉ 23f1001171@ds.study.iitm.ac.in (Piush Das) 

**Estimate for** pml 



**Take derivate of** logL(p) **, w.r.t to p and equate it to 0 to get** 



✉ 23f1001171@ds.study.iitm.ac.in (Piush Das) 



### **Bayesian Estimation** 

Incorporate belief about parameters of interest into the estimation procedure. The Bayes theorem is a tool that allows you to update your belief about a situation using data. 

Posterior =<sup>Prior × Likelihood</sup> Evidence 

✉ 23f1001171@ds.study.iitm.ac.in (Piush Das) 

The prior encodes your prior belief about the situation before observing the data (evidence). 

- The likelihood tells you how well the data conforms to your prior belief. 

- The likelihood is multiplied with the prior and normalized with the evidence to give the posterior, the updated belief. 

- The evidence is a normalizing factor here. 

In the context of parameter estimation, Bayes theorem takes this form: 



- P(𝜃 | D) : Posterior probability of the parameter  given the data D 𝜃 

- P(D | 𝜃 ) : Likelihood of observing the data given the parameter 𝜃 

- P(𝜃) : Prior probability of the parameter , reflecting prior beliefs. 𝜃 

- P(D) : Marginal likelihood, which normalizes the distribution. 

✉ 23f1001171@ds.study.iitm.ac.in (Piush Das) 

##### **Beta Distribution (Prior)** 



✉ 23f1001171@ds.study.iitm.ac.in (Piush Das) 

##### **Bernoulli Distribution(Likelihood)** 

The Bernoulli Likelihood : 



##### **Posterior** 





The Beta distribution is a conjugate prior for the Bernoulli likelihood. A conjugate prior has a similar form as the likelihood simplifying the computation of the posterior. 

##### **Point Estimate** 

Often we would want a point estimate for the parameter. But Bayesian method return a distribution over the parameter. We look at two ways to exact a point estimate : 

##### 1. **Expectation of the Posterior** 



✉ 23f1001171@ds.study.iitm.ac.in (Piush Das) 

##### **2. Mode of the Posterior** 





The mode of the posterior is often called the Maximum Aposteriori estimate or MAP estimate, since the mode is nothing but the (arg)maximum of the posterior. 

✉ 23f1001171@ds.study.iitm.ac.in (Piush Das) 

### **Gaussian Mixture Model** 

**Given datapoints what will be the best model we can assume ?** 

**Is this a good model to represent the given data ?** 



✉ 23f1001171@ds.study.iitm.ac.in (Piush Das) 

##### **Is this a good model to represent the given data ?** 



✉ 23f1001171@ds.study.iitm.ac.in (Piush Das) 

##### **The Probabilistic mechanisms that generates the data are :** 

1. Pick which mixture a datapoint comes from ? 

Generate a mixture component among {1 , . . . . . , k} 





2. Generate data point from that mixture 



##### **Total Number of Parameters We Need to Estimate** 





Total parameters to estimate (𝜃) = [π, μ, σ]  = 3K - 1 



### **Maximum Likelihood of GMM** 







But it is not possibe to solve analytically because of summation inside log. For this we take help of jensen's inequality 

✉ 23f1001171@ds.study.iitm.ac.in (Piush Das) 

### **Jensen Inequality** 



log (𝜆1 x1 + 𝜆2 x2<sup>)</sup> ⩾ 𝜆1 log (x1) + 𝜆2 log (x2) condition : 𝜆1 + 𝜆2 = 1 



✉ 23f1001171@ds.study.iitm.ac.in (Piush Das) 

##### **Coming Back to The Original Problem** 



Introduce for every datapoints i , the parameter 𝜆1i , 𝜆2i , . . . . , 𝜆ki 





**By Jensen's Inequality** 



✉ 23f1001171@ds.study.iitm.ac.in (Piush Das) 

#### **Finally to Estimate the parameters(** 𝜃 **), we do the following: Fix  and maximise over (** 𝜆 𝜃 **)** 




- (xi - 𝜇k )2<br>n k 𝜋k . 1 e 2𝜎k2<br>i 2𝜋𝜎k<br>max𝜃 i ∑  = 1 k∑= 1 𝜆k . log 𝜆ki<br>

**Take derivative w.r.t to (** 𝜇 **) to get** 



**Take Derivative w.r.t to (** 𝜎 **) to get** 



✉ 23f1001171@ds.study.iitm.ac.in (Piush Das) 

**Take Derivative w.r.t to (** 𝜋 **) to get** 



**Fix  and maximize  for any i** 𝜃 𝜆 



Solving the above constrained optimisation problem analytically, we get 





✉ 23f1001171@ds.study.iitm.ac.in (Piush Das) 

## **EM Algorithm** 





## **Reference** 

**_Arun Raj Kumar, Lecture Slides for Machine Learning Techniques Karthik Thiagarajan, Machine Learning Techniques Github Notes. Indian Institute of Technology Madras , CS2007 Course Website Stanford University, CS229 Machine Learning Notes_** 

# **Thank You !** 

✉ 23f1001171@ds.study.iitm.ac.in (Piush Das)
