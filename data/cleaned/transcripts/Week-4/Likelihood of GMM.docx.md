# **Machine Learning Techniques Professor Arun RajKumar Department of Computer Science and Engineering Indian Institute of Technology Madras Likelihood of GMM**

We are going to try maximum likelihood for the Gaussian mixture model which is called as GMMs, sometimes Max Gaussian Mixture model. Now, the likelihood function L is a function of a lot of things. So, it is a function of μ1 to μk, which we do not know, σ1<sup>2</sup> to σk<sup>2</sup> , which we do not know and π1 to πk, which we do not know.

And of course the data x1 to xn, which we have observed. It is a function of all these things. Of course, we are going to treat it as a function of the parameters, the data will act as a constant in this function and then we will maximize only with respect to the parameters like how we have always been doing. Nevertheless, let us put this term.

Now the i.i.d. assumption still holds, so every data point is generated according to the same 2 steps. The second data point, again, you go through the same 2 steps, which means that knowing the outcome of the first data point is not going to affect the probabilities of the second data point taking a certain value, independence still holds. And then it is the same process that generates each of the data points. So, identically distributed also holds, but then the distribution is going to be slightly different.

Now, what is that distribution? Well, because of independence, the first thing is we can write this as a product of i equals 1 to n. Now I am writing this, this pi is a big pi, it is not the pi,

which is a parameter, so it is just a product as usual. Now, there is some mixture distributions density, which is determined by where we have to see what is the density of observing xi when you have parameters μ1 to μk, σ1<sup>2</sup> to σk<sup>2</sup> and π1 to πk, small π1 to small πk. Well, what is this mixture density?

Now, because we have these 2 steps, what is the density of a point xi is determined by which mixture it comes from. Now which mixture it comes from is determined by the roll of the dice, which is determined by our probability vector π? So, I can write this density function

𝑛 𝐾 itself as ∏ [ ∑ πk. f (xi; μk,σk<sup>2</sup> ) ] What is happening here? What I am saying is, well, what 𝑖=1 𝑘=1

is the density of xi coming from this mixture distribution?

Now we are seeing, we do not know what was the coin what was the face on which the dice ended up in when the step 1 was performed? Because that is an latent variable. So, we do not get to see that. But then we are assuming that there is some probability πk that it would have come from cluster 1, the same point xi.

There is some probability π1 from cluster 1, π2 from cluster 2 and so on. It could have come from any cluster? So, we do not know that Apriori. So, we have to use the fact that well, it could have come from any cluster. So, I am weighing the chance that it is coming from a cluster by the probability that it comes from that cluster.

So, but we also know that if it comes from cluster 1, it cannot come from cluster 2. So, these are mutually exclusive events. Coming from cluster 1 is completely exclusive of coming from cluster 2. So, the chance of seeing this data point is a sum of these mutually exclusive events of coming from cluster 1, coming from cluster 2 and coming from cluster k. So, I can add these events chances up, but then what is the chance that it comes from cluster 1? Well, if it has to come from cluster 1, 2 things should have happened.

The first thing is that well, the dice should have fallen on face 1, which means the probability of that happening is π1 and this point should have been generated according to Gaussian with mean by μ1 and σ variance σ<sup>2</sup> 1.

So, now that is a product these 2 things have to happen together, that the point was chosen from cluster k and mixture k and then well, mixture k itself gives this point which is this density. So, now what density is this? Now, this is just a Gaussian density. So, this is a normal

density or Gaussian density, because that is our assumption. That is the Gaussian mixture model which we know how it looks like.

So, just to give some intuition here, so let us say the true density looked like this. This is a the true density, which means that is some mean. Let me put some numbers, maybe - 20. Maybe the mean of the second Gaussian was 0. Maybe the mean of the third Gaussian was 15. Let us say I saw x1 as - 15 which is a point here. Now, this does not mean that immediately that x1 necessarily came from cluster 1. Not necessary.

We follow 2 steps. Well, what could have happened is, of course, it cluster 1 could have been chosen and then this point came from cluster 1 according to this density value. Now, it could have very well been the case that cluster 2 was chosen when I rolled the dice.

Now, in that case, the density of this would be from the second Gaussian, which would be smaller value. So, because it is closer, more to cluster ones mean, of course, the density that of that cluster 2 explain this point is smaller. It could have come from cluster 3 also where the density is even smaller. So, it is super small, but then it is not 0. Gaussian will not give you 0 values for any point.

So, it could have come from any of these, so we cannot immediately dismiss the others, it could have come from any of these. In fact, it is not just the closeness to the means that determines this. It is also the π’s that determine this. So, it could be that π3 was 0.9, π1 was just 0.05 and π2 was just 0.05, in which case that though - 15 is very close to - 20, the chance that the first cluster was picked itself is only 5 percent. Whereas, the chance that the third cluster was picked this much higher.

So, in which case, it is not just how much density that the Gaussian has for this point, which depends on how close you are to the mean, that determines the density of seeing this point. But it is also the chance that such a cluster was picked.

All these are unknown variables at this point. So, we have to factor in all of these. And that is exactly what this equation is here. Let us go ahead now and then see what is the density and how we can do maximum likelihood here.

So, now, I am going to write the likelihood function. I am going to create, I mean, there are so many parameters, I am not going to keep writing all the parameters every time, let me just call it as θ. So, this is all parameters. So, μ, σs, and our π’s, it is all put together. I am just calling it as likelihood or as the parameters.

So, this is product of i equals 1 to n, because of independence. And now the ith point was generated according to k equals 1 to K πk into the Gaussian density that the kth cluster generates this, which we know is e<sup>-( (xi - μk)2/ 2 σk2 )</sup> / 2π σk.

So, this is the actual mixture, the likelihood function, which we are trying to maximize. Well, it is a likelihood function that is nothing stopping us from writing down a complicated likelihood function. That is the whole reason of going to likelihood functions. Because if it was always simple as sample mean and fraction of heads, I mean, why develop a theory? So, we are doing this because we want to solve complicated problems and we better be able to handle such complicated problems.

So, this is the likelihood function. Of course, this is a product of a bunch of things, it is easy to typically handle sums then products. So, our usual method would say that look at the log of the likelihood of theta. And how that looks like? Let us see that. Now that is going to be sum over i equals 1 to n, this product here becomes sum. You have a log. Now, here is where we hit a bottleneck in this very step.

Now what is happening is earlier, this logarithm, serves two useful purposes. One it converted products to sums. The second thing is that it simplified our density really well. So,

if there was a Gaussian, then it had a e power something. You did a log and the logs and the e’s cancelled. But now what is how happening is that is a log inside, I mean, there is a sum inside the log. So, this is a sum. And we do not know have nice ways to handle sums inside logs usually. We will somehow get to handling it in a minute. But it is not immediately obvious how to handle sums inside logs.

If it was a product inside logs, we know log will factor that in the sums, but then we have sum inside logs, which is where the problem comes from. Nevertheless, we will write this

term by 2π σk.

So, this is a complicated log likelihood expression. It is a a function of now we are going to treat this as a function of μ’s, μk’s, σk’s , πk’s and then try to maximize this. Well, what we can try is go over usual route and say that well, I will try to take the derivative of this with respect to each of the parameters of interest and then try to set it to 9 and see what happens. There are multiple problems with that.

So, the first problem is and you can try doing this, but then it is not possible to solve this analytically. When I say analytically, there is no equation that we will end up with, like μ<sup>^</sup> ML<sup>,</sup> earlier was just the average of the data points. So, that was a nice equation for μ<sup>^</sup> ML<sup>. It is not</sup> possible to solve this analytically. So, if you take the derivative with respect to μ and try to set it to 0, there is no closed form solution for the μ’s.

If you take the derivative with respect to π, that is a bigger problem, because π’s not just are not free variables. So, they are constrained by the fact that all the π’s should sum to 1. So, it is not a unconstrained optimization problem. It is a constrained optimization problem that is an even bigger problem. So, we have to take care of all that, if you are taking the derivatives and trying to set it to 0. And in general, it is not possible to solve this analytically.

Of course, for people who have seen some kind of optimization methods before, there are some gradient based approaches that you can use to write down the gradient and then do a gradient ascent, because this is a maximization problem and then try to solve this. So, that is like, common general purpose method, which works for any function and then we are trying to apply it to this particular log likelihood function, which we want to maximize with respect to some parameters. That is one way you can do it. Nobody is stopping us from doing that. You will get some estimates, μ hats σ<sup>2</sup> and π.

Instead, what we want to do is, we somehow want to use the power of the structure that is there in this problem. The structure that is there in this problem is that there are well defined 2 steps that generate the data. That is the structure. So, first, you have a cluster indicator, and then you generate the data according to this. But if you are using a general purpose optimization method, it does not necessarily exploit the structure variable. So, the question is, can we come up with an alternate way to solve this, which exploits the structure in a better way?

So, what we want is we need an alternate way to solve this efficiently. So, what do we want to solve? We of course want to solve the maximization of log likelihood with respect to the parameters, all the three key parameters that we wrote down earlier. What I want to do is do take a very quick detour now, and then we will discuss a few ingredients, which will be helpful for us to solve this optimization problem.

Once we see the ingredients, then we will try to see how we can apply to this particular likelihood function. So, let me call this likelihood function star. We will come back and revisit star in a while. But what we are going to do now is take a quick detour and talk a bit about convex functions, and we will see how that will be helpful in solving this problem. Once we go over that discussion.