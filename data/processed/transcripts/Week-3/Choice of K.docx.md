

# **Machine Learning Techniques Professor Arun Raj Kumar Department of Computer Science and Engineering Indian Institute of Technology, Madras Choice of K** 

(Refer Slide Time: 0:13) 





So, the next thing we are going to look at with respect to the Lloyd’s algorithm is how do we choose 𝐾? In practice, you are not going to be given this 𝐾, you are just going to be given a bunch of data points. And typically, you do not know how many natural clusters are there in the dataset. So, which means we need to come up with a method to automatically figure this out. 

So, what I am going to give you today is some broad principles as to how you can potentially get this choice of 𝐾, the specific methods, who will perhaps see it in a tutorial session. But what I wanted to just show you is a high level idea. And, all of what we will see are typically heuristics. So, and there are several other heuristics also, which we would not be able to cover completely in this short time. But the way to think about this is similar. So, that is what we will try to understand. 

So, how do you choose 𝐾? So, let us first ask the question, what happens? So what is the goal? So, we have an objective function, which you want to minimize, which is 𝑛 2 𝐹(𝑍1,... 𝑍𝑛) = ∑ ║𝑥𝑖 −µ𝑥 ║ . This is our standard function that we have been dealing with 𝑖=1 𝑖 

so far. Now, I can choose any 𝐾 for this potentially, let us say I choose 𝐾 as 𝑛. But 𝑛 is the number of data points, then how does this objective behave in that case? Well, if you have the number of clusters equal to the number of data points, then it means that every data point is its own cluster. So, then what happens to this objective? You can pause and think it is not too hard to see that this objective will simply be 0. Which means though, we want to minimize this objective, that is for a fixed 𝐾, if you want to allow for any choice of 𝐾 and ask which choice of 𝐾 minimizes this objective, then naturally 𝐾 equals 𝑛 would do that, because that would give you 0, and that would be the smallest that this objective can take. So, that does not really make sense. Because we do not want the 𝑛 clusters for our data points. We do not want to say that each data point is a separate cluster. I mean, that is not really much of clustering is it? 

So, which means what we want is, you know, we want 𝐾 to be smaller, we want to understand the data in a compressed form, which means we want 𝐾 to be smaller. So, making 𝐾 larger will reduce the objective value, definitely. But then that is not enough for us. So, that is not the goal, the goal is not achieved there. 

So, we want 𝐾 to be as small as possible. But does not mean that we are completely letting go of the objective function also. So, because for a given 𝐾, we still want to find that partition that minimizes this objective or gets close to minimizing this objective as much as possible. That is our goal. But to choose 𝐾, we should not only rely on this objective function that is the main thing. If you only rely on this objective function, then we will just end up with 𝐾 equals n, which is useless. We want 𝐾 to be small. So now, how can we do this? 

One way to do this would then be to say that, well, I saw who can run this algorithm for multiple 𝐾s, but then there are two different things that I need to measure. One is, if I run the algorithm with a specific 𝐾, I get a partition as the output of the algorithm. How, what is the objective value for this partition? That is something that I can measure. But that is not just enough. Now, I do not want larger 𝐾s, I want smaller 𝐾s, which means what we also want to measure is, how big is this 𝐾? In other words, what I am saying is we need to somehow penalize large 𝐾s, large values of 𝐾 and this is the basic idea. 

(Refer Slide Time: 4:53) 



So, we want somehow a 𝐾. So, broadly put, we want to find a 𝐾 that has the smallest not just the objective value, because if I only rely on that, then I know 𝐾 is 𝑛, objective function value, it is important, the objective function value is also important. But then it is not just the objective function value, we also want to introduce some kind of penalty for 𝐾. 

It is just a function of 𝐾 and depending on what your function is, you are kind of thinking of how much, you are penalizing for asking for one more cluster, you can think of it that way. So, if I move from 𝐾 equals to 5 to 𝐾 equals to 6, I might reduce the objective function by a certain amount, naturally, because I have more clusters. So, points will get the cluster sizes will typically become smaller, and so the distance to the means will become smaller. 

So, my objective function might reduce, but I am paying something for adding one more cluster into my data set. So, from going from 5 to 6, I have to pay some penalty. So, which is equal to penalty of 6 minus penalty of 5. So, that is the extra penalty that I am paying to 

purchase a cluster, if you will. But if that is that purchase worth it, well, it is worth it if the objective function drops by a lot. 

For example, if you start with 𝐾 equals 1, that objective function might be really large, because there is no real clustering happening, you are thinking of all points as a single cluster. But then, the moment I make one extra cluster, of course, I am paying something for this extra cluster. But that payment is worth it, because the amount of reduction that I get in the objective function is large. But then as I keep adding more and more clusters, I have to pay more and more. 

So, because my penalty is going to increase with the amount of 𝐾, but then the amount of decrease in the objective function is not going to be that much. And so there is going to be a balance that I will strike for some choice of 𝐾. That is the basic idea. 

(Refer Slide Time: 7:12) 



So, you can think of, if you want to think of this as a plot, it is going to look something like this. So, let us say the x-axis is just 𝐾 as one 𝐾 equals 1, 2, 3, 4, ..., 𝑛 if you will. Now, if I just compute the objective value, well, that is going to kind of go down, so it will go down with my, as I increase my 𝐾, and it will, in fact, treat 0 when I hit 𝐾 equals 𝑛. I mean there is no interpolation happening here, I am just showing this picture, the case discrete and just showing this so that the trend is visible. So, this is the objective function. Now, penalty of 𝐾 is up to us to decide, so we can choose any penalty we want, we can choose something like this, maybe this is a penalty function that we want to pick for 𝐾 penalty of 𝐾. 

So, this gives a very low penalty for 𝐾 equals 1 and as penalty increase, as 𝐾 increases, the penalty increases. Now this of course, now what I am going to plot is objective plus penalty. If I plot that, which is what I care about, so then that is going to look something like this, it will go down and then after a point the penalty will take over and then it will start increasing. So, this is my objective plus penalty. 

* Now, which means there will be some choice of 𝐾 , where the sum of the objective on the * penalty will be as small as possible, and that 𝐾 will be my choice of 𝐾. So, the only thing so basically, this means that I have run it for different choices of 𝐾 for each choice of 𝐾, you can try out different initialization you can get, you can run your K means++, doesn't really matter. 

Whatever you, whatever we want to do, or you can do uniform initialization, run it multiple times. But then finally, the best partition that you get for that 𝐾. The objective function corresponding to that is what we are considering here. And you run it for different choices of 𝐾 and at some point you will find a 𝐾 where this objective plus penalty is as small as * possible. So, and then you choose that choice of 𝐾 . This is one way to think about how to choose 𝐾. Do not think that I have kind of left unspecified is this penalty, penalty function 

itself? 

(Refer Slide Time: 9:55) 



So, this objective plus penalty in general people look at different criterion for choosing this, some common criterion for choosing these are the following. One is called as the AIC criterion and one is called as the BIC criterion. So, this is Akaike information may be seeing 

the name, perhaps incorrectly. But this is a Bayesian information criterion you will perhaps see in more detail some of these criterion, at least in some more detail in the tutorials. But this * criterion just says that you look at a function like this 2𝐾−2𝑙𝑜𝑔𝐿θ . And they will tell [ ( ( ))] you what that means at a high level now, and then we will see that later in more detail. This * says something like 𝐾𝑙𝑜𝑔𝑛( ) −2𝑙𝑜𝑔𝐿θ . [ ( ( ))] 

So, in some sense, these methods are giving you some way to, you know, quantify goodness of your partition by using two things like how we discussed. One is the objective value somehow has to come into picture, the other is the dependence on 𝐾 itself. So, with respect to dependence on 𝐾, one criteria, the Akaike information criteria, says it has to go linearly with 𝐾. The second one also says linearly 𝐾, the Bayesian information criteria, it says K times logarithm of n. Again, so these criteria are optimal for different ways you assume as to how the data itself is generated in a probabilistic fashion. 

So, so far we have not talked about data being generated in a probabilistic fashion at all. So, it might not, this might not perhaps be the best place to talk in detail about what these criterion are. Nevertheless, I just want to say at this point that people typically make some assumptions about how the data is generated and then try to argue if this assumption is true, then the best choice of 𝐾 should be something that minimizes this quantity, which depends on 𝐾, which is okay. But then the way it depends on data is via a slightly different way of looking at the objective function, which is because we assume more things about how the data is generated, you can do something much more nuanced by asking what is called as the likelihood of seeing this data given some parameters that you would estimate from data and so on. 

At this point, we won’t dwell deep into this because we have not spoken too much about estimation, problem of estimation, which we will talk about later. But when once you understand estimation and how it fits into the broader context of, in this case, model selection, then we will perhaps revisit this and then try to tie things together where you will understand this in a much better way. But if you have already understood likelihoods and probabilistic way of generating data, then you can think of this as the objective function appears in terms of a likelihood term here and then the dependence on 𝐾 of course, is linear, as you increase 𝐾, then you pay more and more price in a linear fashion. 

In one case, it is just simply depends on 𝐾 and other case it also depends on 𝑛. Again these are not just the set on stone. So, there are several other things that people use something 

called as an elbow method and there are other choices are also prevalent in practice to choose 𝐾. Again, the goal is not to completely look at all these methods, but then just to give a flavor for how people typically do this. Usual idea is run it for different sizes of 𝐾 and then use some criteria which balances objective one penalty to pick the best. So, with that, we have kind of completed our the main discussion about the Lloyd’s algorithm and I will summarize this and that will be the end of the clustering part of our course. 

So, for the Lloyd’s algorithm, we put down four different questions. One question was about convergence and the answer to this is yes, the algorithm does converge. But it might converge to a local optima. The second question is what were the nature of clusters that the algorithm produces. And the answer to this we saw is basically voronoi regions. And I also mentioned that well, you can make this clustering algorithm work using a kernel trick, where you might get voronoi regions in a high dimensional space and so on. 

The third point is initialization. We looked at one interesting way of initialization, which is called as the K-means++ algorithm, which does initialization in a much more nuanced way, which can lead you to some kind of guarantee about how good the algorithm itself is. And finally, now, we have seen the choice of 𝐾 and the broad idea here is that you look at objective plus some penalty for 𝐾 and then pick that 𝐾 that minimizes this. So, with this, we have come to the kind of end of our discussion about clustering algorithms. 

So, broadly, we have looked at non supervised learning so far in the course, we are at a place where you looked at representation learning, we also looked at clustering and some examples of popular clustering algorithms. We will continue a little bit our discussion about unsupervised learning, but then using certain method called as an estimation next time, which will not only be applicable to unsupervised learning, but then we will see later on is also applicable to supervised learning, but then it kind of acts as a bridge. And that is what we will see the next time. So, with that, we will end this discussion and I hope to see you all next time soon. Thank you.