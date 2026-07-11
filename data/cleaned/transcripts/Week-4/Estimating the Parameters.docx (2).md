# **Machine Learning Techniques Professor Arun Rajkumar Department of Computer Science and Engineering Indian Institute of Technology Madras Estimating the parameters**

So, let’s let’s try that. So, let’s go back to our maximum likelihood function that we had written earlier. Let me recall that, recall this was I noted down this a star earlier. So, the 𝑛 𝐾 likelihood function looked like this, the log likelihood function looks like this, ∑ log( ∑ πk 𝑖=1 𝑘=1

e -(xi - μk )2 / 2σ𝑘2. 1 / 2π σk. This was a complicated looking log likelihood function.<br>

And the problem that we had was that there is a summation sitting inside the logarithm. Now, what we can do is, well, I want to think of this as a sum of a bunch of things. Now, Jensen's is telling us that well, it is not just a sum of a bunch of things, it is sum of a combination of a bunch of things that can be written in a form where you can remove the sum outside, pull the sum outside and then you will get an inequality.

So, we need some combination of the sums, so it is just a bunch of numbers sitting here, I am going to think of these as a bunch of numbers. And then there is a sum here. Now, if now I do not have this combination set.

So, what I am going to do is, I am going to introduce this combinations artificially and make it a problem with more parameters. I mean, it looks counterintuitive at first glance, but then we will see the power of this method.

Now, what we are going to do is we are going to introduce for every data point i what we are going to do is we are going to introduce some parameters. And let us call them λ<sup>i</sup> 1<sup>, to λi</sup> k<sup>. So,</sup> every data point gets K μ parameters. And what are these well, such that, what should happen is for every data point i that the λs that we are introducing should be, should have this notion

𝐾 of probability. So, they have to sum to 1. So, ∑ λ<sup>i</sup> k<sup>should be 1, that is 0</sup> ≤ λ<sup>i</sup> k ≤ 1, for all k, 𝑘=1 all i and k, actually.

So, what is this? What does it mean to say introduce suddenly new parameters? Let us, see

𝑛 𝐾 what that means. So, we have log L(θ).And this is ∑ log ∑ . And this is where we want to 𝑖=1 𝑘=1 introduce and then let me just bluntly, put this λ<sup>i</sup> k<sup>,whichistheparameterthatIam</sup> introducing, there is 1 for every data point i and for every data point i there are k of them, capital K of them, and the small kth parameter is λ<sup>i</sup> k<sup>.</sup>

Now I am just multiplying it, which means that the sum that I am thinking of cannot change, so then I am looking at a different function. So, to do that, what I am going to do is let me write down what the sum was earlier. So, the sum earlier was πk. e<sup>-(xi-μk</sup> )2 / 2σ𝑘2. 1 / 2π σk, which is exactly the density of the Gaussian, but because I have multiplied it by λ<sup>i</sup> k<sup>,Iwill</sup> divided it by λ<sup>i</sup> k<sup>, now it is just multiplication and division.</sup>

So, it is still exactly the same log likelihood but then I am just artificially introducing these parameters I multiplying and dividing by parameter remember, for every i and every k there is a λ<sup>i</sup> k<sup>, what does that mean? That means that for every data point, now I am saying there is a</sup> distribution over all K’s, all clusters will try to interpret these λ<sup>i</sup> k<sup>s later on for now in to think</sup> of them has some artificial parameters that I am introducing into the picture.

The moment I do this, now, I observed that, well this is a log of a sum of, a weighted combination of a bunch of points. So, the logarithm is evaluated at the sum of λ<sup>i</sup> k<sup>timesa</sup> bunch of things. So, which means I can write use my power of Jensen's, so now by Jensen's I can write this log L(θ), which is exactly this quantity, as greater than a different function, it is not the same function.

So, because the function changes, and then that is why you have an inequality. And let me just call that as a modified log likelihood function, log likelihood of θ. Now this θ were the earlier parameters. Now you have this extra parameters λ, which have been introduced.

Now I am creating a new function, which is a modified log likelihood function, which not only has θ and then λs. But then what is this modified likelihood function? Well, it is basically the log likelihood function with Jensen's applied to it, the moment I apply Jensen's the summation comes out.

𝐾 So, this becomes ∑ λ<sup>i</sup> k<sup>,letmeretainthecolorforλi</sup> k<sup>.So,thatweseethatthoseare</sup> 𝑘=1

parameters we have introduced into the method. Now, you have log πk e<sup>-(xi - μk</sup> )2 / 2σ𝑘2. 1 / 2π σk /λ<sup>i</sup> k<sup>.</sup>

The equations might look complicated, but then what is exactly happening is we had a log likelihood function, which was hard to maximize, but then we observed that there is a log of sum sitting inside it. Now we are introducing these extra λ parameters and then writing it as a sum of logs. And that is just by Jensen's by noting that log is a concave function. That is all has happened so far.

Now, why is this any easier? So, why should this be any easier to solve? First of all, I mean, is it easier to solve this model maximizing this modified logarithm log likelihood function, because it first of all, it is not the thing that you wanted to solve, so it is not the log likelihood function, it is a different function.

The second thing is that it has more parameters, we have introduced all these λ<sup>i</sup> k<sup>’s for each i</sup> and each k, which means we have introducing n into k parameters essentially extra into the system into the equation. So, it should be worth it.

So, that something should be super simple, something become should become really simple. Otherwise doing all this is not worth it. Now, we will see why this is worth the effort. Now, first thing we note is that note that the above modified log likelihood gives a lower bound. For the true log likelihood at θ, I wanted to maximize the true log likelihood at θ, the function that I care about is to log likelihood at θ. Now if you give me a set of parameters θ, then I can evaluate the true likely log likelihood at θ.

But now if I evaluated the modified log likelihood, now it is going to give me a lower bound. That is what Jensen's tells me and this lower bound. And the interesting part is that this low this is a lower bound for any choice of λ.

So, Jensen's holds no matter what your λ is, as long as λs sum to 1 λs are between 0 and 1. So, for any choice of λ, when I say λ, when I say again, just to be clear, when I say θ, it means that I mean, μ1 to μk , σ1<sup>2</sup> to σk<sup>2</sup> , π1 to πk. When I say λ, I mean λ1 to λ1k, λ2k, to λ2k,...,λn1 to λnk. And that is what I mean by saying we are introducing this extra parameter λ.

So, no matter so you give me a θ, which is a bunch of μ σ s and π 's. Now, I do not I mean, I do not want to evaluate the log likelihood. Instead, let me say I want to evaluate the modified log likelihood. Now I can put any value of λ, I will get a number and then give it to you. And that number will be a lower bound for the actual log likelihood at the θ that you gave me.

So, I will use your θ, I will use my own λs. And then I will compute the modified log likelihood it will be a lower bound. That is simply by Jensen's but the question is what are we gaining. So, this is a lower bound. So, all that is good, but what are we really gaining? By introducing this, we need to understand that.

And here is the key insight why this is such a beautiful method, so the key insight is the following. And that is why it works, we will see later. Now, I originally wanted to maximize my likelihood function with respect to θ. Now I have a new method new function, which is a modified log likelihood, which is a function of 2 different parameters, one is θ, and one is the artificial introduced parameter λ.

Now, the great advantage we gain by looking at this modified likelihood is the following. And we will justify this in a minute. Now, the advantage is that if we fix some λ, it is easy to maximize with respect to θ. So, for a given value of λ, it is super easy to maximize with respect to θ.

Similarly, we will see if we fix θ, it is easy to maximize with respect to λ. This is the perhaps the most important thing we should take away from here. So, now, originally we had a problem which had only one set of parameters θ, and we do not know how to maximize that in a nice efficient way.

Now, we are saying we are introducing another set of parameters. And now we are saying that if we fix some value for that parameter, I can maximize this modified likelihood with respect to θ very easily. And if we fixed θ, then we can maximize with respect to λ very easily.

So, how, how is this useful to come up with an algorithm we will see in a bit, but then let us first convince ourselves that this key insight is true. And what does it mean to say it is easy to maximize with respect to θ and λ by fixing the other thing? And then we will actually put down an algorithm.

So, now what does it mean to say? We will fix λ and maximize over θ? Let us first do that. So, fix λ and maximize over θ. So, what is the actual function? Well, this is maximize over θ,

𝑛 𝐾 2 when I say θ, again, the set of parameters that we are looking at ∑ ∑ [λ<sup>i</sup> k<sup>log (πke-(xi - μk</sup> ) / 𝑖=1 𝑘=1

> 2σ𝑘2. 1 / 2π σk) /λ<sup>i</sup> k<sup>]. Now, we are going to when you say we fix λ, we are going to treat λs as</sup> constants.

𝑛 𝐾<br>So, what does that help? How does that help us? Well, this guy is same as max θ ∑ ∑ λ i k log<br>𝑖=1 𝑘=1<br>

, Now, I can think of this as there is a product sitting inside the log.

So, that will become a sum over log. So, this will become log over πk. Now, the second term will, things will cancel out with respect to the E, so this will become -λ<sup>i</sup> k<sup>(xi - μk)2 /2 σk2- λi</sup> k log 2πσk.

The next term I can ignored because this is λ<sup>i</sup> k<sup>log,Imean-λi</sup> k<sup>log λi</sup> k<sup>. But then this I am kind</sup> of treating it as a constant λs constant, because that is what saying fixed λ means. So, this is

equal into maximizing only with respect to these 3 terms, because the real parameters here are πk,µ, σ , and so on. So, only these 3 terms matter.

Now, the advantage of looking at this is that, if you now take the derivative of this function, where you are treating λ as constant with respect to the parameters θ, that is with respect to µ, σ<sup>2</sup> , and π 's, all of them have a closed form. And let me put down those closed forms.

So, now if you can take derivatives, I would not do the derivation here. And please try that. And that is a very insightful exercise to try that take derivatives with respect to µ’s, and σ to ^ get the following. µ, I am gonna call this a modified maximum likelihood, it is not the mean maximum modified likelihood.

So, it is not, we are not maximizing the original likelihood, we are maximizing a modified 𝑛 𝑛 function, the kth value is going to look like ∑ λ<sup>i</sup> k<sup>.xi/</sup> ∑ λ<sup>i</sup> k<sup>.Wehaveaclosedform for</sup> µ<sup>’s.</sup> 𝑖=1 𝑖=1

So, if you fix λ and try to maximize the modified likelihood function with respect to θ,

similarly, σ^2 kmml , will just be ∑𝑛 λ<sup>i</sup> k<sup>.(xi -</sup> µ^ kmml )2 / ∑𝑛 λ<sup>i</sup> k<sup>.</sup> 𝑖=1 𝑖=1

We will talk about the π 's in a minute. But let us let us look at this and understand what this means. This means that there is some λs which I am fixing. So, I can arbitrarily fixed this λs. And then if for instance, if I had fixed λ<sup>i</sup> k<sup>.Thewaytothinkofλi</sup> k<sup>isasfollows. So, you can</sup> treat λ<sup>i</sup> k<sup>astheprobabilitythatthe,ithpointgrowsintothekthcluster,whatdoyouthinkis</sup> the probability because we are fixing it arbitrarily at this point.

So, let us say I put each point into one cluster. So, I want to assume that every point comes from the same single cluster. So, which means λ<sup>i</sup> k<sup>willbe1foraparticularclusterindicator</sup> value k, and then it will be 0 every where else. If that happens, then what is this essentially ^ mml telling us is µ k , is simply the mean of the data points assigned to a particular cluster. And ^ 2 mml i the σ k is just the sample variance of data points assigned to a particular cluster if our λ k<sup>’s</sup> are 0 for all case, except 1, for which it is value is 1, but then we are not constrained to put λ<sup>i</sup> k<sup>’s like that.</sup>

Now, then you can think of λ<sup>i</sup> k<sup>’s as somehow, starting with a soft clustering of the data points,</sup> which means what do we mean by soft clustering? For every point, I am kind of telling, what is the chance that this point comes from each of the clusters? Now, we do not know earlier how to get this chance.

But then let us say we initialize it with some values, then what is these estimators are telling us is that, well, it is going to give you a weighted mean and weighted sample variance where the weights are given by these chances that we are fixing.

That is all this is. So, basically, once I fixed λs, then maximizing the modified likelihood is very easy. It is like saying, I am telling how important is every data point for each cluster. So, I am just going to simply, weigh these points by their importance for each cluster. And, and that will give me the clusters best mean and the clusters best variance. That is exactly in equations, these things that you are seeing.

Now you can, you have to be slightly careful when you are maximizing with respect to π's because π's have this constraint that they have to sum to 1, nevertheless, we can do the maximization you can do maximization of π1, to πK.

Now, if you again, go back to your likelihood and see which are the terms which depend on π , it will simply be some, there will be just only one term and that is also not too complicated

term λ<sup>i</sup> k<sup>log  πk such that π 's are not free variables such that</sup> ∑ πk = 1, such that πk ≥0. 𝑘

Now, you see that you observe that well, there is a λ<sup>i</sup> k<sup>for each i. For every i, we are deciding</sup> on a distribution over the data points, sorry distribution over the clusters? λ<sup>i</sup> k<sup>tells me what is</sup> the chance that the ith point comes from the kth cluster? Intuitively, that is what it is meant to mean.

So, now, here, this is a sum over i equals 1 to n and something which sum over K. Now, we are trying to maximize with respect to πk’s. Now what we can do is we can solve I mean of

course, there is a constraint here, which is what will typically cause an issue, but you can solve this by using standard constrained optimization techniques.

If you have seen some constrained optimization techniques, you may be familiar with the method of Lagrange multipliers otherwise, take it at this point that this can be solved in closed form easily. So, this can be solved using the method of Lagrange multipliers to give us

^ 𝑛 the following quantity π kmml is going to be simply ∑ λ<sup>i</sup> k<sup>/ n.</sup> 𝑖=1

Now, what does this intuitively mean? Well, this intuitively means that well, remember λ<sup>i</sup> k kind of tells us what is the chance that we think ith point goes to the kth cluster? And now, we are asking what is the chance that a, some point will come from the kth cluster? Well, it is the, you are basically how to average the chance of each point going to the kth cluster.

Now, if each point was hard clustered that it will only go to one cluster, which means λ<sup>i</sup> k<sup>’s</sup> ^ where we are taking values either 1 or 0. Then this simply means that π, our best estimate is just the average of the number of points or the fraction of points that went into that particular cluster. So, if  λ<sup>i</sup> k<sup>’s were 0’s or 1’s, then well, for each data point, you are counting λi</sup> k<sup>.</sup>

So, then it will be 1 only for those points which have been assigned to cluster k. So, you are just looking at the fraction of points assigned to cluster k. But then if you do a soft clustering if λ<sup>i</sup> k<sup>’sorbetween0’sand1’s,thenthisiskindoftellingyouonanaverage,whatisthe</sup>

chance that a point belongs to a cluster K, that is what this is. So, basically, putting everything together, so, what we have is that we have the following.

So, fixing λ we get the following if we maximize with respect to θ, we get the following. I ^ will just summarize this as µ kmml is just the weighted mean, where the weights are given by these λs that we are assuming λ<sup>i</sup> k.<sup>σ^2k</sup> mml<sup>istheweightedsampleistheweightedsample</sup> variance.

𝐾 But again, the weights are given by λ<sup>i</sup> ’s that λ<sup>i</sup> k<sup>’sthatweareassuming</sup> ∑ λ<sup>i</sup> k<sup>,andπ'sare</sup> 𝑘=1

again, the weighted version of what you would standard expecting, if it is just the weighting of each points chance that belongs to cluster k and then averaged. So, this is good. So, this kind of tells us that Well, I have a problem with 2 sets of parameters θ and λ. I fixed λ. I can maximize easily with respect to θ.

Now, the other way should also happen easily. So, you need to fix θ and maximize with respect to λ. And let us see if that is easy also. And once both of these we convince ourselves that these are easy by looking at the actual closed form solutions, then we can put down an algorithm that can be efficiently used to solve this problem.

So, how would this look like? So, now, we are fixing θ and then maximizing with respect to λ, which means again, let me recall the likelihood function every time I would have to write this, but it is worth doing that because it will reinforce what we are trying to do in a better way, ik divided by λ<sup>i</sup> k<sup>thiswasthelikelihoodfunction.Now,Iwanttomaximizethiswith</sup> respect to λ treating all the other parameters µ’s, π 's, σ ’s as constant.

Now, I can, I mean, do some simplification and then only pull out the terms which are non constants. And that will look like this λ<sup>i</sup> k<sup>.AndyoucantrythisthisonestepIamskipping,</sup> but then you can try this out for yourself. So, λ<sup>i</sup> k<sup>someconstantand they will write what this</sup> constant is -λ<sup>i</sup> k<sup>logλi</sup> k<sup>, where this constant that I am thinking of is ik e power minus basically</sup> the density of Gaussian. So, 2 σk<sup>2</sup> 1 / 2π σk.

So, now remember, we want to maximize this with respect to λs. So, and then there are k λs for each data point i. Now, if you look at this, equation itself, it is a sum over data points, and then for each data point I have a bunch of K parameters. So, then I am adding these things up. So, because the parameter, so the function is not, does not have any cross terms, so, the λ<sup>i</sup> k and λ<sup>j</sup> k<sup>do not appear together at all in the function.</sup>

So, I can actually maximize these separately for each data point i, and then that would actually the separate maximize that should actually also, maximize the entire function because it is just a sum of a bunch of functions, which depend on i separately, but then there are no variables shared between these the inner summation.

So, I can optimize this separately, which means that we can fix any i and then maximize over

𝐾 that λs have to satisfy ∑ λ<sup>i</sup> k<sup>=1and0</sup> ≤ λ<sup>i</sup> k ≤ 1, it is a constrained optimization problem, 𝑘=1 nevertheless, not a hard one to solve.

So, you can still maximize this in closed form using the method of Lagrange multiplier can be solved to enclose form analytically. When I say analytically, all I mean that can write ^ down a formula for the answer to get the following formula λik<sup>ofthemodifiedmaximum</sup> likelihood looks like the following.

𝐾 So,(1 / 2π σk. e<sup>-(xi-μk</sup> )2 / 2σ𝑘2) . πk / ∑ (1 / 2π σl e<sup>-(xi-μl</sup> )2 / 2σ𝑙2) . πl. So, this looks like a 𝑙=1

complicated formula, but it is not.

So, this is all this is saying is that, well, what is this. So, I am I am trying to ask, well, if I fixed the parameters, if I tell you what are the means, what are the variances what are the π ^ 's? Then what is the, what is the best guess λik<sup>?</sup>

^ What is λik<sup>representingitisrepresentingtheprobabilitythattheithpointgoestothekth</sup> cluster, I tell you what the ith point is and then ask what is the chance that this goes to the kth cluster. Now, well, if I know all the parameters, then basically what I am asking is, I am asking something like what is the probability that zi, which is remember from our step one that this is the cluster indicator is k given xi.

So, given a point xi, say I am asking what is the chance that this goes to the K cluster? And ^ that is what I am going to think of as λik<sup>, as to represent. Well, I know by Bayes theorem, this</sup> is just P( xi | zi = k) . P( zi = k) /  P (xi).

This is my base theorem. So, this is what my Bayes theorem tells me. And now if I have the parameters µ’s, σ<sup>2</sup> and π 's, then you can verify that this is simply probability of xi given zi equals k, because this is the chance that xi comes from the kth cluster.

This is simply P (zi = k) this is the step 1 chance that the kth cluster is chosen. And this is summation over like all possible ways of generating xi. P(xi | zi) into P(zi) which is just P(xi) itself. This is just base theorem.

So, it is so, nice that this turns out to be exactly what you get, if you had applied Bayes theorem and try to estimate P (zi = k | xi), that is what is the chance that the xi point goes to the kth cluster? And that once the parameters are given, you will simply use the Bayes theorem to estimate that, that is exactly what comes out as the as your maximum likelihood estimator also.

So, now what we now have is we have solved for λs if the parameters are given similarly, we have solved for the parameters if the λ are given an all of these are just simple formulas. So, given once you fix λs you get a weighted mean, weighted variance and then a weighted fraction for µ, σ<sup>2</sup> and π respectively and if you fix µ, π, σ<sup>2</sup> respectively and then see what is the best λ then that is simply by your Bayes theorem then estimate for P (zi | xi).

So, all of these are simple now, so, all of these are closed form solution. So, which means we can actually write down an algorithm for this for solving for θ. So, remember our original goal was to maximize the log likelihood now, by adding these extra parameters λ we are saying that you can fix λ solve for θ you can fix θ solve for λ efficiently that we have seen how. Now we will use this to come up with an iterated algorithm to solve the problem.