

# **Machine Learning Techniques Professor Arun Raj Kumar Department of Computer Science and Engineering Indian Institute of Technology Madras Bayesian estimation** 

So, this is a good estimator given data, it gives me good estimators. Is there something else that might be typically available in practice? And if so, is the maximum likelihood estimator still the best thing to do? Or is there something else that one can do? Of course, I am being vague here. So, let me make that a little bit more precise. And then and then we’ll try to see how you can potentially come up with different estimators, which might be in some cases better than the maximum likelihood estimators. 

And to do this, let us again, go back and revisit our simple example of coin toss. So, our model is still the coin toss model. You observe data, which is 0 and 1. And you are going to make an assumption that it comes from a box with a coin with some unknown bias P, of generating heads and you press it n times, you get the coin. And you get n data points, n observations all that is the same. 

(Refer Slide Time: 01:22) 





But now, the extra thing, piece of information that you have is that somebody comes and says. So, let us put me this topic, consider the coin example. By the way, the coin tosses are called as Bernoulli trials. So, it like how Gaussian. So, the corresponding random variable in the coin are called as Bernoulli trials. 

So, you have a coins x1 to xn. So, this is basically all my xi’s or Bernoulli that is what means with some parameter P, this is the probability of xi = 1 for all i and it is the same setup. We have this in addition, let us say somebody came and told you the following statement, “I believe the bias p is somewhere is close to 1.” Let us say someone said this. 

Now, imagine a situation where you have this box. And the box has a coin inside about which at this point, you do not know anything. Let us say you have not even seen the data. But then somebody walks in and says, I believe that the bias p is somewhere close to 1. Now, you have this extra piece of information, which is an English sentence. So, somebody says that they believe that p is close to 1, that is an English sentence. Nevertheless, it is a statement that gives you some information about the coin inside the box. And this is what we will call as, in general domain knowledge, let us say. 

So, the statement could be anything. It could be closer to 1 not maybe they are saying something like, I know, it is small, the p is either small or either too high. But then I am sure that it is not close to 0.5. That is also a statement somebody could make it. So, all these are statements that people could make or you might have as a practitioner from your experience, you might have what I am going to call, as hunch about data about the parameters. Not the data about the parameters. We may have a hunch about the parameters. 

So, remember, these hunches have nothing to do with the data. So, we have not even seen a single data point it. Even before seeing the data points in the previous case of maximum likelihood estimators. If I did not give you data and then I asked you, well, what would be your guess for the underlying model that generates the data? You go blank. So, because there is no way you could make a guess, because your method depends only on data. Only if you give me data, I will be able to see what might be a good guess. 

If there is no data, there is no other information that I have. Maximum likelihood estimator depends completely on data. But in practice, you might have something more than the data, which is the hunch that I am talking about here. And now, it might be good and it will be very good if we had a principled way to incorporate our hunch into our estimation process. So, is there a way we can somehow codify our hunch into mathematically more precise mechanisms that can be incorporated into our estimation procedure itself. If so, how can we do this? 

So, this is what we are going to see next. And this will take us to what is known as a Bayesian modelling approach. Again, for people who have seen this, this might be a recap, otherwise, this can be thought of as a primer in Bayesian modelling. So, the goal is to incorporate these hunches that we have that we might have. So, how can we do that? So, that is the question. 

(Refer Slide Time: 05:44) 



So, goal incorporate hunch or belief about parameters of interest into the estimation procedure and how do we do this? The way we are going to think of this is as follows. 

(Refer Slide Time: 06:26) 



So, the approach that we will take to do this is as follows. So, we are going to think of the parameter that we are trying to estimate as a random variable. And I will tell you what that means, intuitively, but that is the, that is the approach that we are going to take. So, basically, we have this hunch. So, earlier we were thinking of the parameter as some μ or some p. So, this is what we were trying to estimate. 

Now, we are seeing. So, we are going to not, in some sense, we are going to encode our hunch as a distribution over this underlying parameter. So, earlier, this is what our goal was to get a μ or now we are going to say I have some hunch, which is to say that, well, if I say, for example, for the case of p, let us look at the case of p I know that the value of p can take any value between 0 and 1. 

Now, if I if somebody said that, well, I think I believe that the value, true value of p is somewhere close to 0.9 or something like that, or it is close to 1, I might potentially put a hunch like this. So, what is this tell us ? This tells us that I believe even before seeing the data, that my true value of P is most likely around 0.9 or closer to 1. So, in this case, I am saying 0.9. I mean, that is just an example. So, this could be 0.9. Depending on our hunch, we can modify this. So, this might be one way to encode your hunch, or a statement of the form, well, I know that the p is not close to 0.5, it is either too small or too big. 

So, maybe you want a hunch that encodes that, maybe you would put a distribution like this. So, this is still between 0 and 1. This is 0.5. And essentially, you can think of it as putting weights on each of these values of p. So, because p can take in this case, any value between 0 

and 1, you can encode these weights in terms of a distribution itself. So, which means I can treat this hunch itself as a random variable as a parameter itself as a random variable, which has some associated distribution with it. 

Now, what does the distribution tell me? Well, without seeing the data, it kind of tells me that it gives me what is the chance, I believe, before seeing the data that my true parameter falls in a particular interval. That is what these things are encoding. So, for p it could be like this. For μ, you could say that well, I think the mean μ, the parameter I am trying to estimate is probably around -12.5. So, maybe that is the guess that I want to encode. Maybe I will encode that something like this. 

So, it is around 12.5. It could be other things also, but then I believe it is more around 12.5 than anything else, if that is what I believe, then this is a way I could have encoded that hunch, before I see the data. 

(Refer Slide Time: 10:09) 



So, now, what happens is, so, what are we saying? We are saying that we have a hunch, which is what I am going to call as codified using a probability distribution over θ. Let us say θ is the parameter that I am trying to estimate. Let us not fix μ or p specific values or specific parameters. But in general, it is some parameter θ, which means that there is some p of θ. What is p of θ give me? Well, if θ is a continuous parameter, like your p or μ, then it means that it is a continuous probability distribution, where the support the values that θ can take or any values that you could have potentially guessed. 

For p, this could be any value between 0 and 1 and the shape of this p, the PDF determines, what is our belief about this the parameter of interest even before we see the data. So, the hunch that we have can be codified using a probability distribution over θ, which can be said as P(θ), which simply tells us that, if θ is takes value in a continuous range. For example, like the p that we were trying to estimate in case of Bernoulli random variables, then this P(θ) would actually be a PDF. So, it tells us that what do we believe about this underlying p in terms of probabilities. 

In other words, if I did not see the data and I asked you, well, what is the chance that this p takes a particular value in a particular range, for else takes a value in a particular range, then you can integrate this PDF and then give me the probability and so on. So, essentially, we are treating θ as a random variable. That is what it means. 

Now, what do we do with this hunch? Well, of course, we see the data next. So, after this, we have the data. And once we see the data, our belief system needs to be updated. So, we may believe that the p is around 0.9, which means that we believe that, the chance of heads is much higher than the chance of tails. 

But then if we observe 1000 data points and it so happens that, 900 of them are tails, then it is against our belief system. So, our belief system said that we are expecting 90 percent heads, but then we actually are seeing 90 percent heads on average, but then we are actually seeing, let us say 90 percent tails, which means that we have to update our belief system accordingly, as how the data dictates. 

Also, if, our data adheres to our belief system, then that strengthens our belief system. So, then, we might still want to update our belief system where we might be more confident about our guesses and so on. So, in any case, we after looking at this data, we need to move from hunch to an updated hunch. So, this needs to happen. And how can we codify the updated hunch? Well, this can be codified using again a probability distribution, but then what distribution is this? This is no longer p(θ), but then it is p(θ) given data. 

So, this idea of going from what is called as prior distribution over θ to what is called as a posterior distribution of θ, but then after observing data, is what is called as the Bayesian way of doing things. So, you have a hunch, you see data, you update your hunch. So, this is the Bayesian modeling. 

(Refer Slide Time: 14:15) 





But then what is so Bayesian about it. So, where is Bayes coming into the picture? Well, that is that precisely happens to describe how you go from p(θ) to p(θ |data). So, where is the base coming in? So, if you remember the Bayes law, or the Bayes theorem, now, we know that P (A | B) is from high school, we know that this is P(B| A) . P (A) / P(B). So, this is our standard Bayes Rule, which says that A conditioned on B the probability of a condition on B can be gotten as with using P(A), P (B) and P (B | A). So, if we know these three things, I can get P ( A | B). 

Now how does this help in our case? We are going to think of a as parameters, so, which is simply our θ and B as our data, so, which is x1 to xn. So, which means simply by using the Bayes law, we can do the following, we can see that p (θ | {x1,.., xn}), which is our updated 

hunch, after seeing data can be written as P (B | A), which is P({x1,..., xn}). The data given the parameter into P (A), which is the parameter divided by the data P({x1,..., xn}). This is just exactly analogous to our Bayes law. 

And now, if you notice this, it gives you an excellent way to go from your prior to your posterior. And what Bayes theorem is saying is simply the following. So, you have some initial belief about your prior distribution. Now, to go to a posterior distribution, you have to review your prior distribution. You have to make a multiplicative update to this prior and that multiplicative update is given by this specific term, which also is something that we have encountered earlier. 

So, now, at least the numerator is something that should be familiar to you. Think about what the numerator is. The numerator is saying, well, if I give you θ, we told you what the parameter is, what is the chance that I see this data? Now, this is what we have been calling as the likelihood. So, this is something that we already have seen. 

Now, the denominator is something that is independent of θ. So, this does not depend on θ. So, this is the technical term for this is called as evidence, this is the chance that you actually observe the data itself, but then notice that it does not depend on θ. So, which means that you can think of your posterior as proportional to your likelihood times your prior. So, you are re-weighing your previous belief, using the likelihood and then that will give you the posterior. So, that is what Bayesian modelling essentially is telling. 

(Refer Slide Time: 17:20) 



So, for example, I might have a hunch, like this. Example. Maybe I had a hunch somebody came and told me that be that I am trying to get data from is close to 0.9, then I could have, incorporated that hunch by using a PDF. Let me draw this carefully. So, PDF something like this. So, which peaks at 0.9, let us say. Now I see my data. And let us say my I say 10 data points, which are many of them are 0, let us say. So, eight of them are 0 and two of them are 1s. Again, all of these representative images, it is not exact numbers that I am plotting, but then just to give a feel. 

So, now the data is kind of the likelihood is kind of telling me suggesting me that, the p value should actually be 2 by 0.2 whereas my belief is saying it is 0.9. So, now, if I somehow combine these, what I might get is something like this. So, I might get something like this as the updated hunch. So, this is my hunch. This is my updated hunch. It might peak somewhere, perhaps at 0.27, I do not know. These are just numbers that I am making up. But you get the idea. 

So, you start with some distribution over your possible parameter values. You see the data and then you get a new distribution, which is perhaps a different distribution. Now, if I had a different set of data points, now, this is a case where the, the data does not know correspond to my hunch. 

On the other hand, if I had the flipped version of this data, let us say something like this, where you had nine 1s and one 0. Now, in this particular case, the same hunch might translate to an even sharper rise at 0.9. So, I am believing in 0.9, even further, strongly, so, because my data also in some sense corresponds to my hunch. So, this is the idea of Bayesian modelling. 

(Refer Slide Time: 19:41) 





Now, let us take one simple example, to talk about Bayesian modelling. And then we will move on to other types of setups. So, again, we will talk about how to encode a hunch when data is setup is data as Bernoulli, which is the coin toss example, Bernoulli of p. So, this is the basically when the assumption that we are making about the data is that it is Bernoulli of p. So, there is a box with a coin, all the things that we have discussed. So, the likelihood is Bernoulli. 

Now, what is a good prior? Which means, P(θ)? In this case, θ is just P, which means how can I encode my prior? Well, of course, here I have been drawing pictures, but then mathematically how can we encode this prior? One way to encode a good way to encode this 

prior is using what is called as the beta distribution. It is called a beta prior. And we will see why this is a good way to encode prior. 

Basically, you want some continuous distribution whose values are between 0 and 1. We cannot use a Gaussian here. So, because Gaussian can give me any value between -∞and ∞, but then the parameter I am trying to estimate which P, I know takes value between 0 and 1, so any distribution that I use as a prior to encode my prior knowledge should be supported only in 0 and 1. And a good choice is what is called as a beta prior. 

So, once I say a beta prior, I should put down the density of this distribution. So, the density of the beta distribution looks like as follows. The density is defined for every value of p between 0 and 1. And like the Gaussian is parameterized using the mean and the variance, the beta distribution is parameterized using two values, α and β, which are both positive numbers. And it is given something like this. 

So, this is p<sup>(α-1)</sup> . 1 - p<sup>(β - 1)</sup> for all p is 0 , 1. Of course, divided by some normalizing constant z, which does not depend on p, such that this is a PDF, it integrates to 1 and so on. That is not so important for us, what is more important is the functional forms, how it depends on p. 

So, what can this beta prior do? Let us, take some examples and see what kind of PDF this looks like. So, if you take 0 to 1 which is the value of p and then if I use, let us say p as α as 2, 1 beta as 2, I get something like this. So, this is my PDF, when α = 2 and β= 2, meaning my this is essentially the function p . (1- p) divided by some normalizing constant such that the area under this curve is 1, because it has to be a probability distribution. And we know p . (1 - p) looks something like this. So, this is the case α = 2 and β = 2. 

Now, when α is, let us say 2 and β = 5, it looks something like this. Again, these are representative images, this is α = 2, β = 5. It kind of says that when you have small α and big β, then you are kind of believing that you are true p is somewhere closer to 0 than 1. If α = 2 and β = 2, then it is like I am still believing that the coin is pretty much unbiased. I mean, my highest value is 0.5, but then I am spreading out my bets, so to say. 

Now, for a different choice, for example, if α = 0.5 and β = 0.5, then this picture actually looks something like this. This function looks like this. It is a very flexible distribution. Now, this is a case where I can encode my belief that well, my p is either small or large. But it is definitely not close to 0.5. So, it is a biased coin. So, it is a skewed coin that much I know. 

So, now that can be encoded using the choices of α = 0.5 and β = 0.5. So, this can capture different types of intuition. Let us, say there is some intuition that we have, which can be put down using some choice of α and β. 

(Refer Slide Time: 24:11) 





So, now what do we do with this prior? Well, of course, we need to write down the posterior now. So, we need to write down the well, we need to write on p ( θ | data). And we said that well, this is proportional to p ( data | θ) p (θ). And all this prior is telling us is like is the PDF for p (θ). 

Now, how does the p ( θ | data) look like if your data comes from a Bernoulli likelihood, that is what we want to find out. In other words, we want to find out the PDF of p given data at 

some value of p. Now this is proportional to the Bernoulli likelihood, which we know looks 𝑛 like ∏ p<sup>xi</sup> . (1-p)<sup>(1-xi)</sup> . You have already seen while we discuss maximum likelihood that this 𝑖=1 

is our Bernoulli likelihood. So, this is our likelihood function, our foreseeing, of course, the data x1 to xn and p (θ), we are saying can be encoded as p<sup>(α - 1)</sup> . (1 - p )<sup>(θ - 1)</sup> . 

So, this is our prior. So, this is prior, this is likelihood. And if I multiply this I should get, of course, I have to divide by the evidence, but then I am that is why I am not saying equal to but then proportional to what I would get as the PDF of the posterior. 

Now, the interesting thing that you might already be noticing is that the prior and likelihood both have the form p power or something into 1 - p power something. So, they look similar, at least functionally. So, which means I can somehow combine this and say that this is proportional to p power sum over xi, this guys, p<sup>(∑xi + α - 1)</sup> . (1 - p)<sup>(∑(1 - xi) + (β - 1))</sup> . So, this is what my PDF of my posterior looks is proportional to. 

So, it is just a simplification of this thing. Of course, I am seeing proportional to because there is some normalizing constant, which is needed to make this a real PDF, it has to integrate to 1 and so on. But we will see that that is not so important, as we will see in a minute. So, what does this tell us? So, the very interesting thing that this tells us is that f ( p) was of the form p power something into 1 - p power something. Our prior shape was of the form p<sup>(α - 1)</sup> (1- p)<sup>(α - 1)</sup> . 

Now our posterior also, this distribution also has the same functional form. So, same and that does not happen for all choices of prior. I will comment about that in a minute. So, this is some functional form, same functional form as the prior. So, the posterior also has the functional form p power something into 1 minus p power something, which means that we know that the posterior distribution is also a beta distribution. 

Now, the parameters are no longer α and beta. For the prior it was α and beta. But now the posteriors parameter are not α and beta. They depend on the priors parameter α and beta. But then they also depend on the data. It is a beta distribution but then the parameters have not changed. It is as if you are only updating the parameter of the distribution. And you do not have to exactly calculate the density for at all values of p. You do not have to completely calculate the entire function, so, entire density. If you know the parameter, then you get the function for free. 

So, interestingly, this has not happened by for all choices of priors. So, if I did not choose a beta distribution, if I had chosen some other complicated distribution between 0 and 1 that encoded my prior knowledge, it is not necessary that if I multiply it with the Bernoulli likelihood, I will get a beta posterior. That is not at all necessary. So, you will still get a posterior. It might be useful and all that, but it is need not be convenient in the sense that your prior and the posterior of the same functional form. 

(Refer Slide Time: 28:35) 



In this particular case, it happens. So, we start with the beta prior, which means we have some parameters, α and β . And now, after seeing data, the updated hunch is a beta posterior, it is also beta and the data is Bernoulli, so, Bernoulli. Now, what are the parameters of this posterior? Well we pause and think about it, I will tell you now. So, this is just α + ∑xi , β + ∑(1 - xi). Now, one way to think about ∑xi is just the number of heads and nh number of heads in my data and ∑(1 - xi) is the number of tails. 

So, what is this kind of tells us? It tells us that if I started with some value, α and β, I observed in nh tails and nh heads and nt tails in my data. Then my updated belief about the parameters looks like a beta distribution with parameters, number of heads + α and number of tails + β. 

Now, if you had used a simple maximum likelihood, then it would be only number of heads and number of tails which would have determined our guess. So, it would be nh /nh + nt, which is just the n. So, nh / n would be our guess which is what we saw as our guess for the maximum likelihood estimator. Now here we are seeing, one way to guess, after getting this 

better posterior could be guessing as α plus nh divided by one possible guess. Guess could be to look at α + nh / α + nh + β + nt, which is α + nh / α + β + n, nh + nt is just n. 

Now, this might be our guess. If you had to commit to a single guess, then we might commit to this guess. And in fact, this turns out for this particular case to be the expected value of the posterior. So, is expected value of any beta distribution with parameters α and β is α / α + β. In this case, the posterior is a beta with (α + nh , β + nt). And the expected value of this turns out to be exactly this value. 

Now, this is kind of telling us essentially that, let us think about this for a second. So, we have some data which have nh tails and the nt, nh heads and nt tails. If you had to do a maximum likelihood estimator, we would have said that number of heads by n that is our estimate. 

Now, we are saying number of heads + α / n + α + β . It is as if we are saying that we have our data. And we also have this extra ghost data, which have α heads and β tails. If we had our data and an extra α +β data points where we had α heads and beta tails, well, then we would have guessed our maximum likelihood estimator as α + nh / α + β + n, which is exactly what is the expected value of the posterior. 

Now, what does this tell us, this tells us that in this particular example, the prior using the beta prior can be thought of as if thinking that we did some ghost experiments or pseudo experiments, which are not real data, but then these pseudo data ghost data which have α+β data points, out of which α showed up heads and β should up tails that is what is giving us our beliefs. So, it is as if somebody came and said, I did 100 experiments, 80 of them happened to be heads, 20 of them happen to be tails. 

Now, if somebody told us that, then we converted that into a hunch using a beta prior with α as 80 and β as 20. Now, it is as if we can once we do this, the posterior will take into account these ghost data samples also and then will give us a maximum likelihood estimator, it could be thought of as that way. So, that is that is one way to interpret what is going on here. 

So, in general, you could, this might be one way to make a single guess from the posterior, which is using the expected value of the posterior. There are other ways you can make guesses, which is what is called as a map estimator. Which is to say that well, in maximum likelihood, we wrote down the likelihood function and we pick the value which maximizes the likelihood. 

In the map estimator, which is a maximum Aposteriori estimator. We look at the maximizer of the posterior distribution. So, now you have a posterior distribution. Now, you look at which value has the maximum PDF. So, PDF value or the likelihood and then you make that as your guess. So, that is typically called as p<sup>^</sup> MAP<sup>. And in this case, it will be slightly different</sup> from α by α + β. So, the point is that now you have an updated hunch, which gives you belief system over all possible values that your parameter could take. Not committing to a single value. 

If you want to commit to a single value, you can either take the mod of this distribution, which is the maximum Aposteriori estimator. You can take the expected value. You can take whatever you want. So, you can take some samples, average them, everything is possible, because you have an entire distribution in your hand. So, this way of modeling things is what is called as a Bayesian way of modeling things. 

So, to summarize, at a very high level, we have looked at two different types of estimation procedures. One is called as the maximum likelihood procedure, which just writes down the likelihood function and then tries to maximize it to get a point estimate. The Bayesian world starts with a hunch about our parameter to estimate and then converts that hunch into an updated hunch via the data and using the Bayes theorem. 

And once you earn a updated hunch, which is a distribution over all possible choices our parameters can take. Then you can either convert that into a single estimator if you want by taking the Aposteriori maximum Aposteriori estimate or you can take the expected value or you can do whatever you want. So, these are two broad ways of doing estimations. 

Now, this is all you know basic statistical ideas. What we are going to do next is use these ideas specifically the principle of maximum likelihood and see how that can be used for a very, very specific unsupervised learning problem, which will give us a probabilistic twist to a clustering algorithm that we have already seen, which is the K-means algorithm. So, for K-means functions did not assume any probabilistic model for data. 

So, now, if you assume a reasonable probabilistic model for data, can you come up with a probabilistic version or a probabilistic counterpart to clustering algorithm? Or can we come up with a probabilistic counterpart to the representation learning algorithms? So, these are the type of questions we are going to ask next. And that will give us the real power of using all these techniques that we have learned here including maximum likelihood or even Bayesian 

methods, when we want to apply it to specific unsupervised learning machine learning problems like representation learning or clustering. 

And the next thing that we will see is how to use this for estimation ideas for coming up with a probabilistic version of the clustering algorithm. We will see that next time. Hope you enjoyed this video. Thank you. 

