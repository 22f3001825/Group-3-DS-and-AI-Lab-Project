# **Machine Learning Techniques Professor Arun Raj Kumar Department of Computer Science and Engineering Indian Institute of Technology Madras Maximum Likelihood Estimation**

(Refer Slide Time: 00:13

So, the question is, is there a principled way to get estimators from data and the way one could do this, is by looking at what is called as the likelihood function. The likelihood function looks as follows. So, let us take the example. It is easy to explain a smaller example. Let us say 1, 0, 1, 1 was our data.

Now, now we are going to say the x axis goes from 0 to 1. And it is all choices of P, that could have possibly generated the data that we see, which is 1, 0, 1, 1. Now for every value of

P, we ask the question, well, I see I have seen this data, if the true P was this, what is the chance that I would have seen the state? So and now we can plot that chance. So, this is the probability that your first random variable, which is the first outcome was 1, the second outcome is 0, third outcome is 1 and the fourth outcome is 1.

Now you can plot this. So, for every value of P, you can ask, what is the probability that I observed this data and that is what we are calling as likelihood here. And if we plot this and you could try plotting this for this example. And I tried this and then it looks something like this. So, the curve looks something like this. So, basically, it, we know that at t = 0, there is no chance that I could have generated 1, 0, 1, 1, the probability that I see the data is 0 at t = 1 also it is 0, we already know that.

For the remaining we can calculate these probabilities and then I can plot this and what I get here is something of this form. And now I can see, where does this curve peak? In other words, which is the value of P, for which the chance of seeing the data is highest? So, the data is most likely for which parameter of P, which choice of P, so and that choice in this particular case, in this example, if you try it would have been three fourths. So, which is exactly the guess that we made which is while looking at the fraction of ones.

But why should this happen? In general, I mean, what is the method here is a question to ask. So, then we will see about that in a minute. So, what we want to then do is we have a bunch of potential parameter values, which could have generated the data. And then our goal now is to pick one of those values and say, this is what I am going to bet on. This is my guess. And the way we are going to do that is by saying that, I will look at the probability that my data is generated given this the truth is this parameter and whichever P maximizes that would be my guess.

So, and this method was is quite old. So, it has been there since the fifties. And this was proposed by Fisher and it is called Fisher’s principle of maximum likelihood. This might be familiar for some of you this think of this as a review, for estimation, if you have seen this before, otherwise, this is still precursor to what is going to come later. This is Fisher’s principle of maximum likelihood.

So, what does that principle say? Well, it says that you write down what is known as a likelihood function L, which is a function of two things. One, the parameter that you are trying to estimate and it also depends on the data, x1, x2,..,xn. So, I see the data and I want think of this as a function of the parameter because for every value of P, I am going to ask what is the chance that I see this data? Now, how do I write this? I will write this as the probability of seeing x1, x2,..., xn. When I write this, it means that specific value that each of these x1 to xn takes.

So in the case, it would be x1 = 1, x2 = 0, x3 = 1 and x4 = 1 and so on. So if the true value is P, so if the underlying parameter is P, this is the underlying parameter. Now, how can so this is a joint distribution. So, this is the probability that all these things happen together, that

the first toss is x1, second toss is 0, third toss is 1 and the fourth toss in 1, so the probability that all four events happen together.

But because we have assumed independence, that one event does not affect the probability of the other. I can write this as P(x1,p). P(x2,p)....P(xn,p). I can do this and what lets me do this is independence. This is independence.

And now I will I also know that each of these coins was from the same P, so I know that. And so I can write this whole thing, as in a simplified way as product and this is the sign for product, 丌<sup>n</sup> i = 1<sup>(p)xi (1 - p)(1 - xn). This is just a compact way to write this thing.</sup>

So, basically, what does this tell me, if xi is 1, so, this term is what does it, when you observe a value of 1, now, if the true probability of seeing 1 as p, then I should multiply it with P. So which means that this if xi = 1, it’s value is P<sup>1</sup> (1 - P)<sup>(1-1)</sup> , 0, which is simply p.

On the other hand, if xi = 0, this implies this is P<sup>0</sup> .(1 - P)<sup>(1-0)</sup> , which is 1 - P, which is what we want. So, which means in for example, in this particular case, if x1 = 1, x2 = 0, x3 = 1 and x4 = 1, this would be p for this x1 into 1- p into this p into this p, which is p<sup>3</sup> into 1 - p. So, essentially, the plot that I have done here is that of the curve p<sup>3</sup> into 1 - p. So, that is precisely what we have here, in general.

Okay so, now what is the estimator, so this is the likelihood function. And now we want to define our estimator, which is our guess for p and that is where you put a hat on top of p to say to emphasize that it is a guess. And the guess comes from the maximum likelihood principle. And so this is called as an ML, so I am also writing this as ML is that argument of p that maximizes my likelihood function, which is, in this case, just  丌<sup>n</sup> i = 1<sup>(p)xi (1 - p)(1 - xn).</sup>

So, this is what I, this is the function that I want to maximize to get my guess for P. Well, this is a function which has a lot of products. Typically, it is easy to deal with sums then product. So, what you could do is you can take the logarithm of this function and in fact, you can look at arg max p, log( 丌<sup>n</sup> i = 1<sup>(p)xi (1 - p)(1 - xn) )</sup>

Now, remember, this is fine, because logarithm is a monotonically increasing function, which means that if there is a p<sup>^</sup> , which maximizes the original function, that means that the functions value at p<sup>^</sup> is greater than the functions value at any other point.

Now, if I take the logarithm of it, because it is of its monotonicity the log of the functions value at p<sup>^</sup> will be greater than the log of the functions value at any other point. And so it is

okay if I either maximize the original function or the logarithm of it, the point where the maximum occurs does not change, So, because log is monotonic function, increasing function I can do this.

Now, things become simpler. Now, this becomes arg max p ∑<sup>n</sup> i = 1<sup>and that is the power of log</sup> products become sum this becomes xi log p+ (1- xi) log (1- p).

Now, this function happens to be a nice concave function. Do not worry if that you have not seen that term that is fine. So, this is a function which has no you can maximize this by taking the derivative and setting it to 0.

So, now, this is take this as an exercise take derivative of this function, treat this as a function of p, derivative of L (p). In fact, log L (p), treat this treat the likelihood functions is the log likelihood function, set it to 0 to get our guess p<sup>^</sup> ML<sup>= 1/n ∑n</sup> i = 1<sup>xi. If you did that, if you had</sup> taken the derivative, set it to 0 and I urge you to try that out, you would get that the answer as simply the average of my data points.

This looks like the average but then it also has a simple interpretation because my xi is just 0 or 1 heads or tails out of the sum, what contributes to the sum, it is just the ones not the zeros. So, basically, the sum counts the number of ones in my data. So, this is simply the fraction of ones.

So basically, here is a method which is called the principle of maximum likelihood, which seems to give us reasonable guesses. So, my guess for the true p, by looking at the data is that value of p which maximizes the chance that I observed this data. And that has led us to guessing the fraction of ones as the, which was also our intuitive guess. But remember, we have implicitly used two important facts, one is independence of the trials. The other is identically distributed nature of the trials. So, now this is one example.

Now, one thing to keep in mind, when we are doing this is the following. So, let us say we now have data for different form. We still have x1 to xn, but x1, xn are no longer zeros or ones, let us say xi belongs to real numbers for all i. Let us say I collect the height of a bunch of 100 people. And then I want to reason about that in a probabilistic sense.

Now, the height cannot necessarily be 0 or 1. So, it can be any value. And so I cannot use the previous model. If I use the previous model the box with a coins inside that, that is not going to be useful for explaining this data, because that box can explain only data which has zeros and ones. So, I need a different box to explain this data, which means I need a different probabilistic model that I need to assume to explain this data.

And the natural model, in this case, would be something like assuming the box is still have a box, you still have a box with a button. And then our data comes from it. But because our data can be any real value, in this case, we want a box that can explain real numbers, when we are going to assume the most simplest thing would be to assume that the box has a Gaussian random variable with some mean μ and some variance σ . So, that is I am assuming xi is Gaussian with mean μ and variance σ<sup>2</sup> for all i. That might be another reasonable assumption to explain this data.

Now, if I do that and if I now let us say we again, write the likelihood function like how we had written earlier, which is now for simplicity, let us say, we know the variance that generates the data. It is not true in general. So, if you have a bunch of data points, you would not know anything about the data. But let us make it even simpler and say that we know the variance. So, the only thing that we do not know is the mean. So, let us say mean is the parameter that we are trying to estimate. So, mean is unknown. Say variance σ<sup>2</sup> is known.

So, now what is the likelihood function look like? Well, it is a function of μ, σ<sup>2</sup> , the parameters. I mean, one parameter is known, one is unknown, but still, it is a function of these two, these two and of course, the data x1 to xn. I see a bunch of data points. Now, what is this likelihood? Well, the way we have put down likelihood earlier is that this is the probability that the joint distribution of x1 to xn parameter is by μ and σ<sup>2</sup> . So, of course, I can write this as a product by independence of i = 1 to n P (xi ; μ1,σ<sup>2</sup> )

Now, what is this probability? So, let us say x1, the first height that I measured was 162.53 centimeters. Now, let us assume some Gaussian distribution with mean 150 let us say. So, let us say this is the Gaussian PDF, here is 150, some variance that I know, now I am trying to get the mean. So, let us say I start with my guess as 150.

Now and I am asking, what is the chance that if I draw a sample, according to Gaussian distribution with mean 150, what is the chance that I am going to get 162.53? That is the question that we are asking here. So, if we define our likelihood like this. But if you remember, Gaussian is a continuous distribution. So, you can, if you ask for the chance that a

random variable that you sample according to a Gaussian distribution falls in an interval a to b, then we know that that chance is just given by the area under this curve of the PDF.

So this PDF, if you remember, is e<sup>-(xi-μ)2/2σ2.1/</sup> 2Πσ , all that should we know. So now, this is the chance for an interval, but then we are asking what is the probability of a specific value that we have observed. So, I stopped, the person, asked for his or her height and then I got the value is 162.53.

Now, I want to ask the probability that I see this particular value with some Gaussian with some mean μ. Now, because Gaussian is continuous, this value is going to be 0 for any individual point or a bunch of points. So, only intervals will have non-zero values for continuous distributions. And so no matter what my μ is, this is always going to give me a zero value. Because I am asking for the probability of a bunch of points to be generated according to any μ any Gaussian with any μ however, away, it might be from the data, or close it might be to the data, it is still going to be 0.

In other words, this function, the way that it stands now as a product of probabilities, will give me 0 value for all possible choices of μ, which means this is not able to distinguish one μ from another, so it does not have the capability to distinguish one μ from another. So, it might not be useful in making good guesses. So we cannot really, there is nothing to maximize here, because every μ gets a value of 0. So, all μ’s are equally bad. So, you cannot really use this function to make a guess.

And the problem arises because of the fact that Gaussian is continuous and individual points get 0 probabilities. So, Fisher’s proposal was to not use the probabilities. And instead, replace the probabilities not to this and instead define the likelihood of the parameter in this case, as not the product of the probabilities, but then instead the product of or in general, the value that these parameters take these observations take is given by the PDF of the distribution that generates the data. So, you replace probabilities with PDFs.

In other words, you want to replace the x probabilities with the joint PDF x1 to xn of x1… xn parameterize by μ1 , σ<sup>2</sup> . Now, PDFs behave similarly with respect to probabilities for a lot of cases. In fact, if the data points are independent PDFs will factorize.

So, this can be written as i = 1 to n, f of xi parameterize by μ and σ<sup>2</sup> . What does this mean? This means that I am looking at the Bell curve’s value at xi. So, I am not asking for the probability. The probability of seeing this point is 0. But then the value that this point x has given me the PDF is not 0. That is some non-zero value. It may not even be between 0 and 1, but it is some non-zero value that I can use as a proxy in some sense for the probabilities. That is the proposal of Fisher.

And in fact, what is this going to be we know what this is, so, for the Gaussian. So, this is asking if the true mean is μ and the variance σ<sup>2</sup> , what is the density at a particular value i and we know that by definition is .1/ 2Πσ e<sup>-(xi-μ)2/2σ2</sup> . So, the same μ and 2 σ<sup>2</sup> but then you are multiplying it over different xi’s. So, that is what this essentially means. So, this is our new modified likelihood function.

In fact, that is why we call it to the likelihood. So, we do not call it the probability function. If it was always using probabilities, why give it a different name? You giving it a different name because it is not strictly probabilities, so of observing the data, it is the likelihood of observing the data. That is what Fisher called it. And we want to maximize this likelihood function.

Now you do the same drill. This is a product of a bunch of things. So, you take the log of the likelihood function of μ σ<sup>2</sup> x1 to xn. I will just do this for completion only one example. So,

𝑛 this is ∑ log (1/ 2Πσ) . Now, this is logarithm to the base e. So, you can do this as -(xi -μ)<sup>2</sup> , 𝑖=1

the logs in the exponential cancel. And this looks like this.

Of course, we are trying to maximize this with respect to μ because we want to find that value of μ that maximizes the likelihood. So, this term does not have mu, so I can remove this term. It is not going to contribute to my maximize, in other words, I could might as well

𝑛 maximize ∑ -(xi -μ)<sup>2</sup> . I can even remove 2σ<sup>2</sup> because that is I am assuming as a constant 𝑖=1

rate, so that does not really affect my maximization.

So, I want to find that arg max, over mu, which is μ<sup>^</sup> ML<sup>.So,thatisgoingtobemyguess,</sup> which is an arg max μ, the negative of this, which again you can take the derivative, set it to

𝑛 0. And please do that. Try that out. It is just two steps. This again, happens to be 1/ n ∑ xi. 𝑖=1

What does this tell us? This tells us that if you have a bunch of data points and this is the important part that if you assume that this data is generated according to a Gaussian, with certain unknown mean mu, then the best guess, according to the maximum likelihood principle for this unknown mean, mu, is the sample mean.

Now, it might feel that well, what is the big deal. So, we could have any way taken the sample mean and it would have been a good guess for the unknown parameter. But this is a good guess, the sample mean happens to be a good guess only, or not I should not say only, in this case, where we are assuming that the underlying data comes from a Gaussian.

If I change that assumption, to a different distribution, maybe I have some domain knowledge, which makes me believe that the data is not coming from a Gaussian, but then it comes from, let us say, a Laplacian distribution, for example. That is a different probability distribution, which looks like a Gaussian, but then it is more sharp at the peak.

Then if we do a principle of maximum likelihood, it is no longer going to give me the sample mean. It will give me something else. So, in fact, it will give me the sample median which means to say that you are estimator is very closely tied with the probabilistic model that you assume that generates the data.

So, it is always the sample mean, may not be a good guess. It depends on what model you believe generates this data. If you believe in a different model, the guess is going to be different. And our method adjusts to the model, so because the method essentially tries to use the PDF of the model that generates the data. And so it works well for the model that we use. So, that is the point that I just wanted to mention.

And in general, this is a very general purpose method. So, it does not make it is a simple idea. So you put down a model, whatever model it might be, you put down that model, right down this PDF of that model, or the, if the discrete distribution, the probability of that model and write down the likelihood function of the parameters maximize it. So, it is as simple as that. It is not just a simple it is as general as that that is more important. So, it is super general, in the sense that once you have the model, you have a method to get an estimator.

So, these estimators may not necessarily be very intuitive apriori. In this case, perhaps it is intuitive. In the previous case of the coin toss, it was perhaps intuitive. It is good that it matches our intuition when we do have intuition about what might be a good guess. But even if we do not have intuition about what might be a good guess, the method is robust enough

that it can give us some estimates and that is why this is a very super popular method in general, in statistics and machine learning. Now, so this is one side of the story.

So, this is the summary so to say of the principle of maximum likelihood. Now, of course, if you are in a statistics course you will try to understand why is this a good estimator? Maybe somebody smart, tomorrow might come back and say that, hey, I have another estimator, which is a better estimator. And then you have to argue why maximum likelihood is a better estimator than what they might have and so on. And that is what a statistics course will do. So, they will try to argue good properties of the maximum likelihood estimator and in cases where it can be in general it will give you very good estimators.

So, and in some cases, you can argue that you cannot get any better than a maximum likelihood estimator. So, in certain well defined ways, it might, you can argue that it is the best that you can ever get and so on. But because this is not really a statistical course, we are not going to dwell deeper into the specific properties of the maximum likelihood estimator itself, we will agree that it is a good estimator, it typically is estimated that gives you reasonable guesses. And what we want to use is somehow ask the question.

So, this is a good estimator given data, it gives me good estimators. Is there something else that might be typically available in practice? And if so, is the maximum likelihood estimator still the best thing to do or is there something else that one can do? Of course, I am being vague here. So, let me make that a little bit more precise. And then we will try to see how you can potentially come up with different estimators, which might be in some cases better than the maximum likelihood estimators.