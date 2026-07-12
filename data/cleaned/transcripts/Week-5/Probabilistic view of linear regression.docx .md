# **Machine Learning Techniques Professor Arun Rajkumar Department of Computer Science and Engineering Indian Institute of Technology, Madras Probabilistic View of Linear Regression**

(Refer Slide Time: 0:17)

Now, what we are going to see is a probabilistic view of linear regression. What happens when you think of linear regression as if there is some probabilistic model that generates our labels. So, that is what, that is what we are going to look at. So, we have already looked at estimation, in general in an unsupervised setting where we have seen maximum likelihood Bayesian methods and so on. But now, we are going to think of our linear regression also as in some sense an estimation problem, which means that there should be some probabilistic mechanism that we are going to assume that generates something that we have seen.

### Timestamp: 01:04

So, what is that we are going to assume? Well, in the linear regression problem, you have the data points in d dimension, the labels are in real numbers and of course, you have a dataset which I can write as {(x1,y1),.., (xn,yn)} this is the dataset. Now, the probabilistic model that we are going to assume is as follows, we are going to assume that the label is generated as follows the label given the data point is generated as w<sup>T</sup> x + ε.

What does this mean? This means that I do not I am not trying to model how the features themselves are generated, I am just trying to model the relationship between features and the labels in a probabilistic way, and what is the probabilistic mechanism that generates the labels if I give you x, well, what we are going to posit or hypothesize is the following.

So, if I give you a feature, then there is an unknown but fixed w which is not known to us, so, this is the parameter of the problem. So, this is unknown, but fixed and this is an Rd and whenever a feature is seen you do a w<sup>T</sup> x, but then your y is not exactly w<sup>T</sup> x. So, this is the structure part of the problem.

Now, we are going to explicitly say there is also a noise part to the problem. So, we are adding some noise to this w<sup>T</sup> x and that is this ε. So, this ε is noise and this noise is we are going to assume is a Gaussian distribution with 0 mean and some known variance σ<sup>2</sup> .

So, this is Gaussian, Gaussian. So, so, now, what we are saying is that our data set every yi was generated according to this process somebody was gave us xi and then to get the yi there is an unknown but fixed w using which w<sup>T</sup> xi was generated and then a noise got added and we are only seeing the noisy version of w<sup>T</sup> xi whereas we know that the statistics of this noise is 0 mean and some (va) known variance  σ<sup>2</sup> , all that is known.

So, but the only thing that is unknown for us is w we do not know w so, which means now, we can view the whole thing as an estimation problem.

### Timestamp: 03:48

So, now we can view we can view this as an estimation problem, what are we trying to estimate? Well, we are trying to estimate the w which after adding noise affects our labels. So, once we have put down a model as to how the data is generated, at least the y is given x is generated, and we have an unknown parameter.

Now, we already know what some methods to estimate come up with estimators and the simplest method that we have already seen. The solution approach to this problem is, as you must have already guessed, is just the maximum likelihood approach. So, now I want to understand the same problem, but then in a maximum likelihood context and see what comes out of it.

### Timestamp: 04:50

So, which means the standard maximum likelihood problem, I am going to write the likelihood, so the likelihood function is going to look like this. Let us call this x. Now, what is the parameter of interest, well the parameter of interest is w, but then the likelihood function also depends on the data x1 to xn and y1 to yn, because this is the observed data points, we are observing this and then we are treating this as if it is a function of w.

Though, it is also a function of the data points and the labels, but then we are going to treat it as a function of w and then we will try to find that w that maximizes our likelihood of seeing this, but then before that, what is this likelihood itself.

Now, as usual, the i.i.d. assumptions hold in a probabilistic model that is x1 y1 is independently generated. So, y1 is independently generated of y2 and so on and they are all from the same Gaussian distribution. So, basically, this is going to be product of i equals 1 to n. Now, what is the chance that I see a particular yi for a given xi? Well, we know that every yi given xi is generated according to w<sup>T</sup> xi, which is a fixed quantity, there is nothing random there and then you add a random noise.

But this noise is 0 mean noise with a certain variance. So, if I add a constant fixed quantity w<sup>T</sup> X site to the 0 mean Gaussian, just the mean gets shifted, the variance spread is is fixed, but just the mean moves around by adding a constant, let us say we have a 0 mean Gaussian, I add 5 to it, it becomes a Gaussian with mean 5, the variance is still the same. So, it is exactly the same thing here.

Now, I have added w<sup>T</sup> xi to this 0 mean Gaussian for the ith data point. So, now, that would be a Gaussian distribution with mean w<sup>T</sup> xi and variance σ<sup>2</sup> , which we are assuming is known.

### Timestamp: 06:48

So, now this would then be the likelihood can be written as the density of e, which looks like e power, w<sup>T</sup> xi, which is the mean, minus what I observed, which is yi squared by 2σ<sup>2</sup> and of course, with 1 /√2π σ. Though let us content it does not really matter in our in our maximization as we will see.

So, once we have put down this likelihood, I can now do the log likelihood log L (w, x1 to xn, y1 to yn). We want to do the logarithm because it is hard to deal with products, easier to deal with sums. So, this is Σ<sup>n</sup> i=1<sup>,thelogcancelsthe exponential. So, this is minus, (wTxi- yi)2 / 2 σ2 . 1/√2π</sup> σ. Now, remember, we want to think of this as a function of w, x is our constant, σ is our constant, everything else, y is our constant, so it is only a function of w.

### Timestamp: 08:05

And we want to see which w maximizes our likelihood or log likelihood, which means I can equivalently equivalently w star, I mean, to get the best w. I could have maximized. So, the mean, I want to maxw Σ<sup>n</sup> i=1<sup>,Iamgoingtoremove,Idonotcareaboutthesevariables,these are</sup> just constant scalings, these are known σ<sup>2</sup> is assumed to be known. So, these are constants, I do not care about them. I will just hold on to the other guys.

So, this is just (w<sup>T</sup> xi-yi)<sup>2</sup> , of course, the minus is there. Now, this is equivalent to minw Σ<sup>n</sup> i=1<sup>(wT</sup> xi- yi)<sup>2</sup> . Now, this minimization problem is something that we have already encountered. So, this is exactly the linear regression problem with squared error that we already put out, which means we know the solution to this.

### Timestamp: 09:12

So, so basically, what is the solution to this? Well, then, the ŵML as an estimator is exactly same as our w*, which we already know is (xx<sup>T</sup> )<sup>✝</sup> xy from our previous discussion about linear regression. Now, it is great that we started with a completely different technique of looking at things which is by thinking of a probabilistic mechanism for generating y given x and then did the most natural thing which is to look at a maximum likelihood approach and outcomes solution, which is exactly same as the linear regression solution.

So, what is the conclusion and it merits separate writing here because in some interesting points can be made the conclusion is that maximum likelihood estimator assuming this is the most important part 0 mean, Gaussian noise is exactly same as linear regression with and again, this is the important part with squared error.

We could have either solved the linear regression part with squared error, or we could have treated this problem as a maximum likelihood problem with Gaussian noise with 0 mean Gaussian noise and these both are exactly equivalent. These both are equivalent is is an important thing to understand, because what exactly makes them equivalent is the choice of squared error when we started by looking at linear regression where we did not really justify a squared error that much, we just said that, well, we will start with squared error because it looks like an intuitive thing to do do do, I mean, look at.

Now, we are saying, well, more than just intuition, it has a very well probabilistic backing as well. So, we are saying that if we chose squared error to solve the linear regression problem, it is as if we are implicitly making the assumption that there is a Gaussian noise 0 mean that gets added to our labels that corrupts our labels.

Now, these two are both important to understand. So, if I had changed my noise, if there is reason to believe that my noise was not Gaussian, then it would not be the same as solving the linear regression problem is squared error.

So, the noise statistics are the density that you are assuming about the noise impacts, essentially, the loss function, or the error function that we are using in our linear regression. That is the connection that I want you to make here.

So, for example, if I had given a different noise, for instance, if there if I tried a different noise, like laplacian noise or something like that, so I am just giving you an example, then no longer you would end up with a linear regression with squared error, these two will not be equivalent anymore, it would be equivalent to a different loss function.

Let us say in fact, and if if I mean just for completions sake, if you use a laplacian noise, then it would be as if you are, you are looking at the absolute difference between w<sup>T</sup> xi and yi and then summing up over them and that would be the problem that you are actually trying to solve.

So, because the laplacian PDF has an absolute value sitting at the top of exp e<sup>-abs(wTxi-y)i</sup> , it it it kind of falls down sharper than the Gaussian distribution but that that is not the important point. The important point is that choosing a noise means implicitly choosing an error function and vice versa, choosing an error function means implicitly choosing a noise, so that is the first connection that we want to make, which is which is important so, good so, we have made that connection.

The question is, is this the only thing that we gain, or are we gaining anything else by looking at this from a probabilistic viewpoint, well, the answer is yes, this is an important conclusion that we are drawing that if you view your w as an estimator, then you can connect the noise and the loss.

### Timestamp: 13:50

But now what else have we gained? So, what else, what else have we gained, by viewing this in a probabilistic way, well, the most important thing that we might have (perf) perhaps gained is that now we can study properties of estimator especially to ŵML. So, this is an important gain that we have when we view learning as a probabilistic mechanism, because the moment you put probabilistic learning becomes estimation and once you have an estimator, then you can bring in all the machinery that we know about understanding estimators. We have already seen some kind of understanding what are good estimators and whatever perhaps not.

So, now, what we are going to see is can we somehow use this notion of estimators that somehow can we use some properties of these estimators or some other way of trying to do estimation to understand this problem of linear regression better and that is what we will do next.