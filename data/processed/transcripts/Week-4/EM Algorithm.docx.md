

**Machine Learning Techniques Professor Arun Rajkumar Department of Computer Science and Engineering Indian Institute of Technology Madras EM Algorithm** 

(Refer Slide Time: 00:14) 







And here is the Algorithm. So, the first thing you do is you initialize some value for θ naught. So, 0 here is iteration basically, it is an iterative algorithm. So, initially, you basically that means that you are initializing some means μ, μ<sup>0</sup> to μ<sup>0</sup> k, some variances, σ1<sup>2</sup> to σk<sup>2</sup> , and then some π1 to  πk. 

Now, the algorithm thus as follows, now, until convergence and the way we are going to think of convergence here is that well our parameters θ<sup>t+1</sup> - θt, so the norm difference is not too much. So, this is some tolerance parameter that we are allowed to tolerate. If your parameter estimates do not change too much, then you stop the algorithm. 

So, this is some tolerance parameter, it could be 10<sup>-3</sup> or 10<sup>-2</sup> depending on what you want to run. Now, what we will do is, because we have initialized with some θ, we will solve first for λ, λ<sup>t +1</sup> is just arg max λ modified log L( θt , λ) and treating λ as the parameter. 

So, you are fixing θt and treating λ as the parameter and then maximizing, we know how to do that. That is a simple problem that we already solved. Now, the second step is once you have λs, you update your θ’s, θ<sup>t+1</sup> , again, using the simple formulas that we have put down, which is arg max over θ, the modified log likelihood. Here, you are going to, treat this as a parameter optimization over θ, where you are fixing λ to be the 1 that you got in the previous one, λ t plus 1. And that is it. That is the algorithm. 

So, the key insight is that by introducing this new parameters and using the power of Jensen's you can split the problem into 2 parts, where fixing one solving for the other is easy, fixing 

the other solving for other one is easy, and you will now do this, iteratively keep going back and forth. 

(Refer Slide Time: 02:55) 







Now, this algorithm has a name. So, this is a, this is an instance of a very famous algorithm called the EM algorithm, where E stands for expectation and M stands for maximization. And basically, it has two steps. And the first step this is called as the expectation step. And this step is called as the maximization step. It is called an expectation step, because you can write this modified maximum likelihood as some kind of an expectation of quantity. 

And that is what eventually we end up getting as λ<sup>t+1</sup> , you can express λ<sup>t+1</sup> as some kind of an expectation. And so it is called the expectation step. We would not worry about writing the generalized version in this course, but you can solve this in general also, I will make a comment later, but there are only 2 steps and because these 2 steps do this E and M steps alternatively until convergence, this algorithm is called the EM algorithm. 

This was developed in the 1970s and still prevalently used I think it it was known in different avatars even before this, but then it was Dempster in his, several paper, put down this algorithm and called it the EM algorithm. And it has been, popular ever since. 

(Refer Slide Time: 04:33) 



So, all this is fine. But, and we can also argue that this algorithm will converge. So, all this is fine. But how can we understand this algorithm, what is exactly going on in this algorithm. We know the equations are easy to solve and all that, but intuitively. What is it? What is it essentially trying to do? The first thing to understand is that you can somehow try to maybe I should put this here on you so, you can try to relate this to our K-means or the Lloyd’s algorithm. You can think of EM as if it is producing soft clustering. Where as Lloyd's produces hard clustering. 

In other words, you can interpret lamda ik that comes out of this as the chance that every data point goes to a particular cluster, λ<sup>i</sup> k<sup>’sisachancethatithdatapointgoestothekthcluster,</sup> which means that the end of this algorithm, you are going to be not just left with parameters μ’s, σ<sup>2,</sup> s and π's, you are also going to be left with some optimal λs and now, you can use these λs you can interpret these λs as some kind of clustering use this to clustering. 

So, remember Lloyd's also had 2 steps, in the first step you would compute the means, and the second step you would do a reassignment you can even try to interpret these 2 steps as analogous to those steps. So, here we are not just computing means. So, once an assignment is given fixed, then what we are computing is well, when I say assignment is fixed here, it means that λs are fixed, we are maximizing over not just means, but then means variances and π's. 

So, there are more parameters that we are maximizing over nevertheless, it can be treated as analogous to the finding the means in K-means, now, once the means are fixed in K Means we were doing a reassignment step, which means that we were changing the cluster indicators Zi’s in a hard sense. 

Now, here, it is done in a soft sense, in the sense that we are trying to see what is the how does the probabilities of points going to clusters change, once the means and variances and π's have changed. And that is your λ expectation step where the λs change. So, it is exactly the analogous algorithm to what we already have seen, but then in a more, full fledged probabilistic setting where you have more parameters. 

So, it is not just the means you also have variances. And that is another point. So, EM also takes variances into account. Whereas, well, variances in the sense that in higher dimensions, especially when variances will become co-variances, your Gaussian will have a co-variance. And then you will estimate the covariance matrices, you might be able to estimate structures, which are slightly in a slightly better way than the Lloyd's algorithm. 

For example, in 2 dimension, well, if you have 2 means here, Lloyd's kind of tries to assume that, there is a variance that you are trying to measure as the goodness of the cluster itself. But then it could be so that the data points in the first cluster might have a variance in a different direction, whereas the data points in the other cluster might have variants in a slightly different direction. 

Now, Lloyd's will perhaps not be able to do so well in clustering points in this region, where these clusters overlap. Whereas, EM algorithm might be able to better understand that when there is a shape variance in a certain direction for one cluster, and a certain direction for other clusters simply because it is estimating the variance, along with the means, so there are more parameters you are estimating. 

So, that is one advantage, you can think of this. And of course, if you want to do a clustering, using this, you can do a clustering. So, how would you do that? Well, you will start with your standard, you will run this algorithm, you will get your λs. Now, for every data point, you see what is the chance that this point belongs to every cluster. 

And you if you want you can convert this into a hard clustering by assigning the data point to the cluster, which has the maximum chance of this point being, so for every i, you look at λ<sup>1</sup> k<sup>,</sup> 

λ<sup>2</sup> k<sup>,..,λi</sup> k<sup>,andthenseewhichoftheseishighest.Andthenyouputyourpointinthat</sup> particular cluster, that particular box, that way you can get hard clustering out of EM soft clustering that it produces, if you wish to cluster them in a hard sense. 

And now this clusters need not necessarily be voronoi regions, so because you are calculating variances and so on, EM clusters need not be voronoi regions, so well, even if you do not have voronoi regions, especially places where clusters overlap. EM does a much better job of assigning points to clusters even if you do the hard clustering, than your perhaps your Lloyd's algorithm. So, these are some ways to understand the EM algorithm itself. So, this is one point I wanted to talk about. And we will talk about one more aspect of EM and then finish this discussion. 

(Refer Slide Time: 10:06) 



And that point is, well, all this is fine. So, we have put down this algorithm which has these nice two steps. And it resembles our K-means a Lloyd's algorithm and all that is fine. But how does this, compare to the log likelihood which we want to maximize at the first place. 

Because we started with a parameteric probabilistic model, which had means variances and π's, we wrote down the log likelihood, and then we use Jensen's to completely avoid the log likelihood, but then use a different function, which is a modified log likelihood. And we are trying to solve for the modified log likelihood. 

Now, of course, we are arguing that this algorithm will converge. We would not prove that, but then we can argue that this algorithm will converge and all that. But how does this relate to the original problem, which we wanted to solve, which was to maximize the log likelihood. 

(Refer Slide Time: 11:04) 



Now, if you think about that, the following picture, remember this? If I, loosely, I mean, try to explain this picture. So, let us say this is our parameter space, so, θ, which is the parameters over which we want to maximize the log likelihood. Now, if I drew, if it simply tried to plot the log likelihood go, it might look something like that. While for simple models, like Gaussian models, or Bernoulli, models, this likelihood would be a nice concave function, and then maximizing it would be easier. 

In the Gaussian mixture model, the log likelihood is much more complicated function. So, maximizing this is hard. That is the biggest problem. So, in technical terms, we are saying there is a sum sitting inside log and all that but then end of the day, this is a complicated landscape where you are trying to find that θ* that maximizes this in fact, what you really want is this guy. So, you want this θ* where this likelihood function is maximized. 

Now, what is exactly happening in in EM algorithm is the following. We are starting at some, let us say θt. So, we are in some θt, which has a certain likelihood value here. But now we are not working with the log likelihood, we are working with the modified log likelihood. 

But then Jensen's is telling us that the modified log likelihood for any choice of λ is going to lower bound the log likelihood function. That is something that we already saw. Which 

means, if I plotted the modified log likelihood at θt as a function of λ, then that might look something like this. 

This is a nice function. That is the biggest advantage. This is a nice function. And it always stays below the original log likelihood for no matter what choice of λ. So, now, what I can do is what is this function? Well, this function is the modified log likelihood, θ and some λ. 

So, I find λ<sup>t+1</sup> , given a θ<sup>t</sup> I found λ<sup>t+1</sup> , the first step, which is the best λ<sup>t+1</sup> , and then if I plot this as a function of θ, because I am plotting everything as a function of θ, now, it looks like a nice function. So, for any fixed value of λ<sup>t</sup> , this will be a nice function, but then we are fixing that best value of λ<sup>t</sup> , and then trying to see how this looks like. And now maximizing this is easier, which means that I can maximize this modified likelihood and get my θ<sup>t+1</sup> . 

Now, what would I what would happen? Well, the modified log likelihood, again, I will try to find the best λ<sup>t</sup> , and then try to find the modified log likelihood of with respect to θ at λ<sup>t+2</sup> , which might look something like this, maybe I will use a different color. So, maybe it will look something like this. 

Now, at this point, what might happen is that maximizing this will make me converge and this function is just modified log likelihood of θ at λ<sup>t + 2</sup> . So, once I have found θ<sup>t +1</sup> , I find the corresponding λ<sup>t+2</sup> , and then I write this as a function, draw this as a function of θ and try to maximize this at this point. 

And then I am kind of stuck here. So, what might be the solution that EM would give me is this, EM’s converge, converged solution. Basically, you are trying to, go make better and better guesses in this complicated landscape. Now, you might, and in practice, you typically will, converge only to a local maxima of this, of the original likelihood function, that is a guarantee that you can do. 

So, while you may not be able to maximize the original log likelihood function using the E M algorithm, in fact, you cannot do it with any known algorithm, what you can do is what you can guarantee using EM algorithm is EM algorithm. And this is the conclusion with which we will end this discussion is EM converges to a local maxima of log likelihood. While you really wanted to maximize the log likelihood function, which means that you wanted θ*, what you will eventually get is only a local maximum, you may not get here, it will converge to a local maxima. 

So, in practice, it now kind of clearly says that how well you initialize this algorithm will kind of take you to which maximum you end up in. So, if I start with a very bad initialization here, maybe I will only reach this maximum. So, which might be much worse than the actual maximum that they want to reach. So, initialization will become an important thing. 

And typically, what people do to initialize EM is that, while you are given a bunch of data points, you have a K, which is the number of mixtures, run your Lloyd's, get a hard clustering using Lloyd's, and use that hard clustering the means and the variances and the π's that you can derive from this hard clustering as your initialization for EM. 

How do you get that well, once you have the hard clustering, you can look at each cluster compute the sample mean sample variance that will give you the π's μ’s and the σ<sup>2</sup> for each of the cluster and then to get the π's you just look at the fraction of data points that are there in each of these clusters. So, that would be your θ<sup>0</sup> . 

(Refer Slide Time: 17:18) 



So, this θ naught usually comes from Lloyd's. So, to summarize everything, what we are saying is, we have put down, a latent variable model, where we wanted to understand slightly complicated data, which has some cluster structure where the latent variable is a cluster indicator, and maximizing the log likelihood was a hard problem. 

And so, we came up with a different algorithm, which exploits the structure of this log likelihood function using Jensen's inequality, to introduce new variables, such that you can do what is called as alternate maximization by fixing one set of variables maximizing rather and 

the other way around. And if you want to initialize this new algorithm, which is called the EM algorithm, you start with the Lloyd's, get hot clustering, initialize it and then do this alternate maximization, typically in practice, you might get better estimates. 

Now, you can do later again, use this to convert it into a clustering or you can use these estimates in whatever way you want to use. So, that is up to what is the task that you do after unsupervised learning. But for doing estimation, this is a very, very powerful technique, it converges really fast in practice, and typically produces very good parameter estimates. 

So, this is whatever we have seen is in the context of Gaussian mixtures. But the general principle of EM algorithm is very broad. We will not do that in this course, but it can work for any reasonable latent variable model. 

As long as you have some kind of nice structural separation that you have in the log likelihood, you can apply this EM algorithm, not just for the Gaussian model for the Gaussian model, we actually wrote down the algorithm, but this can be applied in a variety of other situations as well. 

So, with this, we come to an end of our discussions about unsupervised learning problems, we looked at various methods of unsupervised learning, including representation learning, clustering, and now estimation. 

And specifically in estimation, we have looked in detail, maximum likelihood Bayesian models. And now one very interesting practical application of maximum likelihood to the problem of estimating mixture models, specifically the Gaussian mixture model. From next time, we will start looking at different paradigm of machine learning, which is a very popular paradigm of machine learning, called supervised learning. Till then, take care goodbye and I will see you soon, thanks.