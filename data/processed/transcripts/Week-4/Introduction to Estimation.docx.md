

# **Machine Learning Techniques Professor Arun RajKumar Department of Computer Science and Engineering Indian Institute of Technology Madras Introduction to Estimation** 

(Refer Slide Time: 00:14) 



Welcome back, everyone. So, far we have been looking at unsupervised learning. And specifically, we have been looking at two main paradigms of unsupervised learning specifically, one is representation learning and the other is cluster. So, we have looked at representation learning. And in representation learning, we have looked at PCA as one way to learn good representations, when the features have some linear relationships among them. We also looked at kernel PCA as a means to learn nonlinear relationships among data points via the use of kernel trick. 

So, another possible way to look at unsupervised learning is via the idea of clustering, which is also something that we have looked at and in clustering, we have looked at the Lloyds or the K-means algorithm. Now, in both these ways of looking at unsupervised learning, one thing that we have not done is that we have not assumed any model for data. By which I mean that we have not assumed any probabilistic model that generates the data. And we will see what that means as we go along. 

The goal of this video and a few other videos to follow is to look at a different type of unsupervised learning paradigm, which is not just for unsupervised learning we will see how methods we use are actually useful even for supervised learning later on. But the idea is, we 

are going to look at something called estimation where the basic difference between what we have seen so far and what we will see in this video and the few following videos, is that we are going to make some probabilistic assumption about the data. 

So, we will see what it means to make some probabilistic assumption about data, it is still going to be in an unsupervised fashion. So, we are still in the unsupervised world. But then we are going to move away from the deterministic methods that we have looked at so far and then look at a more flavor of probability involved when you have some probabilistic model for data. 

(Refer Slide Time: 02:55) 



So, what does it mean to say, there is a probabilistic model, basically, our hypothesis is the 

following. There is some probabilistic mechanism that generates the data. So, this is the assumption that we work with. Now, what else about this probabilistic mechanism that we have to look at? Is that, about this mechanism about which we do not know something, so, we do not know something. So, it is not that we are completely aware of the details of this probabilistic mechanism, there is something that we do not know and I will make it clear what this something is. 

And the goal is given data, find or estimate what we do not know. I am trying to put this in a very high level view of what estimation means and we will make it more precise as we go along. So, the first question we ask is, what does it mean to say that there is a probabilistic mechanism that generates the data? For that let us start with a simple example. The way I would like to think of this is as follows. Let us say you have a box and the box is box which 

is a black box, let us say which you do not know what is inside it. But then there is a button on the top of this box. 

For the moment, we will assume that the inside the box there is a coin and this coin is not necessarily an unbiased coin. In other words, it has a head and tail on either side. But then the chance that if you flip this coin, head will occur is not necessarily 0.5. It could be 0.7, it could be 0.9, it could be some value p, which you do not know. And that is this coin inside this box. 

(Refer Slide Time: 05:08) 



And what happens is that every time you press this button. This coin gets flipped inside this bias potentially biased coin gets flipped inside. And what you observe is the outcome of this experiment. In this case, let us say its head. Now, let us say head is head means 1, maybe I press this again, I get a tail, tail mean 0 and then I press it again, I get ahead. Let us say head is 1, I press it the fourth time again, I get ahead, let us say head is 1. And I can let us say I have a bunch of such, what I am going to call as observations. 

Now, these observations according to us are generated according to this probabilistic mechanism, where the probability is completely specified by this coin and its bias. Now, you can think of it this way. So, there is this side, which is known to us or observed and this is what we see. So, this is what is given to us. Now, once this is given to us, we are assuming and then and let me highlight this word assuming that we are assuming that there is some mechanism that has generated this data. It may or may not be true in real world, but we are going to make some assumptions and then work with such assumptions. 

How good are these assumptions and so on, we will talk about later? But for the moment, let us say we make some assumption. In this case, I, you can think of it as I view a bunch of data, which are all zeros and ones. And my assumption about how this data is generated is the story that I build to explain this data is that there is a box with a coin. And then every time I press the box, I get an observation that is how these four observations were generated. So, this is an assumption that I am making. 

And remember that this assumption, this part of the picture is what is unknown to us? So, in specifically, so this P is what is unknown. So, this is an unknown parameter. And you can think of this unknown parameter as what is a compressed representation of the data? So, I might have 1000 points, 1000 values, 0, 1 values, but then, to explain these 1000 data points, which are all zeros or ones, there is only a single number, which is the bias of this coin. So, if I know the bias of this coin, I can explain how this data is generated, I have the story. So, it is like I am tossing this coin 100 times, 1000 times and then getting the data. 

So, you can view this parameter as a compressed representation of the data observed data that you see. But of course, we do not know what this parameter is. And so the goal of estimation itself is the following. So, you observe some data and you assume and again, I cannot stress this enough, you assume a model, in this case, a probabilistic model that generates data. So, there is some model that generates data. And under this model, you want to estimate what you do not know about this estimate, what you do not know about this model. 

So, I have assumed that there is a coin. And that coin has some bias. But if you do not know what this bias is. The proxy for understanding this bias, this value P, this unknown parameter is just my data. So, I see this data, I have made this assumption about the model, I do not know what the value of P is. I want to estimate unknown parameters using data. So, this is the general idea of estimation. 

(Refer Slide Time: 09:09) 





Now, let us take a simple example, with again, with the coin toss, but then not just four data points. Let us say we have more data points. The first thing is you observe, so you observe, let us say, 12 or let me make it 12. So, 1, 0, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1. Let us say this is the data that you observed. 

Now, I want you to the model that I am assuming is, of course, that there is a box and then every time I press a box, a 1 or 0 gets generated and the box has a coin with some bias P when they say bias to just to make this very, very precise. This bias is just the probability of some random variable x taking value one = P and the probability that x = 0 is 1 - P. So, that is what it means to say there is a probabilistic mechanism that generates the data. 

So, and from this mechanism, I am assuming this. So, I am observing this data is the assumption. So, now what would be a good estimate for this particular data? So, it is a good exercise to pause and think what would you estimate if you are given this bunch of data points. So, pause and think about this and then I will probably try to guess what you might have guessed. So, basically, if you counted the number of ones in the data, so there are 9 ones if I have written this correctly and there are 3 zeros out of 12 observations, 9 of them are heads and 3 of them are tails. 

So, my estimate could be something like 9 over 12, which is three fourth. So, this could be my estimator for the underlying P. Now, what do I do with this estimator? Once I have a once I believe that I know what the true P is or I made a guess for the true P. Now I have my own box. So, now I have this box, where there is a coin and then I am saying the coin has bias three fourths. 

Now, once this is there, now, I know I can play god. So, I can create data if I want to, so I do not need the data anymore, because I understood the mechanics of how this data is generated. And that is all there is to this data. This data only contains information about the underlying mechanics, which I am assuming that generates is and once you know the mechanics in this case, which is to know the P, then I do not need the data anymore. So, I have the box and then I have put the values for the parameters. And I am happy. 

If we want, I want to generate as many data points as I wish from this box. So, I can do that. So, but remember, what you have, is still a guess. So, this is a guess, this may or may not be the truth. So, the true P may not necessarily be exactly the same as your guess. In fact, in the moment we introduce probabilities, we are never going to be 100 percent sure that we know the true P that generates the data. So why is that? Well, if you think about this, well, what about a guess which is not three fourths, but then let us say two thirds. 

In other words, can there be a coin with probability P as two thirds which could have generated this data. Think about this. So, if the true P of this coin is two thirds, could I have gotten this data. Or is there absolutely no way I could have gotten 9 ones out of 12 tosses? The answer is you could have gotten this data. So, even with two thirds probability, there is a chance that you could have gotten this data that is nothing I mean, rejecting the possibility that the truth could be two third. 

Well, can the true P 0.0001, can this be the probability of seeing heads? Well, what would you think? So, if you think about it, well, I cannot simply rule out this probability. So, this value of P. There is still a nonzero chance that I could have seen this data, if the true P is 0.0001. Of course, my data is not representative within course, the word representative of this model, where P is 0.0001, which means that I must have had an extremely unlucky day that I see 9 heads out of 12 when the chance of falling heads is 0.0001, 1 and what, 10,000. 

So, that is a very rare event, but that does not mean that it cannot happen it could have happened. So, which means, both two thirds and 0.0001 are still possibilities. Now, what about P equals 0? Is this possible case? Well, we are saying this is this could have generated data, this could have generated data. What about P equals 0? 

Now, if you think about it, P equal to 0 means what? So, the probability of seeing heads is 0. Which means, if I toss that coin 12 times I should have seen only tails, but then I see both heads and tails in my data which means that P equal to 0 is simply not possible. This cannot happen. So, my true P could not have been 0, I am sure about that. 

Similarly, my true P cannot be 1, I am sure about that because with 1 you could not have generated this data you would have got an all heads but then we see a tail as well. So, the only thing that we are sure about is that the true P cannot be either 0 or 1. Everybody else between 0 and 1 is a potential contender for the true P that could be possible. So, there is a chance. 

Now in this case, we still somehow guess three fourths, when every P is a possible candidate for the true P. Now, why did we guess that? So, in general, what went in our minds when we guessed this? So, were there some implicit assumptions that we made before making this guess? In fact, we must have made some assumptions in our head before we guess three fourths? And what are these assumptions? So, let us think about what these assumptions are for a moment. 

So, the assumptions that one typically works with in when we deal with data are the following. So, let me put it here assumptions. Well, so in this simple case, you have this box with the unknown parameter P and then you get let us say, x1, x2 till x n. So, n data points each of these 0 or 1 and then you have n of them. 

Now, there are two basic assumptions we are making about this data. And these are very common, the assumptions are as follows. The observations are first thing is, I will put an 

assumption and then explain what they are, are independent. And the second assumption is that they are identically distributed. 

So, what do these assumptions mean? Well, independence simply means, in this case, this is a probabilistic independence, which means that the probability that x i equals 1, or rather in general x i take some value given x j takes some value is same as the probability that x i takes that value for all i comma j, so, I naught equals j. 

What does that mean? That means that, if I told you that the third toss was a head, then that does not change my uncertainty about my fourth toss. So, the information that the third toss was a head does not affect the probability that the fourth toss is going to be ahead or tail. So, that is when we call these tosses as independent tosses. And this happens for any set of any pair of observations that you see. And you can also argue that n I mean, P of x i, given any set of other random variables here is still same as P of x. So, they are completely independent of each other. So, that is the first point. That is something that we are assuming implicitly. 

The second assumption is that identical distribution. What does that mean? Well, that means the following. That means that P of x i equals 1 equals P of x j equals 1 equals P for all i comma j. That simply means that I mean, in pictures or in words, it means that we are using the same coin every time. So if I, tossed the first coin, it fell heads. And in the second toss, if we pick a different coin and toss it, well, these two coin tosses are still independent. So, because the first toss being head does not tell me how the second coin toss would be head or tail, but then they are not identically distributed, because these two coins might have different biases. 

But here we are saying that well, you are essentially pressing and then getting the same coin gets flipped, all n different times. So, the distribution that determines the outcome, it is the law that determines the outcome that you observe in a probabilistic sense is exactly the same every time. So, that is what it means to say the data points are identically distributed. So, basically, you can think of it as saying there is only one box. So, there is one box and then you press the same box, every time. 

So, now, let us come back to our question of there are all these guesses, which are possible, but then we still made a guess three fourths. Now, we are assuming that the data of has these two, satisfies these two assumptions that they are independent and identically distributed. Now under this assumption, now, is there a way to say one guess is better than another guess? 

Is there a more principled way to say two thirds is a better guess than let us say 0.0001 or three fourths is a better guess than any other guess? If so, then yes, guessing three fourths might make sense in a certain way. 

So, otherwise, these three fourths seems to be arbitrary. So, it is intuitive that you should guess the chances, the number of heads in your data fraction of heads in your data. But it is not at very principled. So, the question is, is there a principled way to get estimates from data? 




data?<br>
