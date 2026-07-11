# **Machine Learning Techniques Professor Arun Raj Kumar Department of Computer Science & Engineering Indian Institute of Technology, Madras Introduction to Clustering**

(Refer Slide Time: 0:14)

Hello everyone, welcome back. So, far in this course, we have been looking at unsupervised learning. And specifically, we have been looking at representation learning problems in unsupervised learning, so representation learning. And in representation learning, we looked at the PCA algorithm, which is the principal component analysis algorithm, we also looked at a kernel version of it, which we call the kernel PCA.

What we are going to do now is look at another paradigm of unsupervised learning, which is called as clustering. So, this is what we are going to look at today. And this is also a popular unsupervised learning problem. So, what is the motivation for looking at clustering? Let us take a simple picture, two dimensional picture. And let us say we have a bunch of data points which are like this.

Let us say some points here, some points here and maybe some points here. Now, one thing we could do to represent this data in the way that we have seen so far is to do a PCA on this dataset. And if you do a PCA on this dataset, what we would get is the Eigen direction, which captures the maximum variance would be perhaps something around this direction along this direction. And once we have found the Eigen direction, what we typically do in PCA is find the proxies for these data points along the Eigen direction.

If we do that, then we are going to get points like this. I am not be exactly drawing it, but you get the idea. So, maybe there are more points here, here and then their corresponding proxies would be here, here. Now, the question is, have we really understood the underlying structure in the data? It is one thing to say that there is a line or a linear subspace that has most of the information that is present in the data.

But then in this case, that linear subspace happens to be this green line that I have drawn here. But there is more that you can say about this. So, it is not just the linear subspace, but then in the linear subspace, you still have some kind of information. So, the data points are what I would call as clustered together.

So, it is not that they are all over the place in the linear subspace that we are finding in PCA, let us say, but then even within the subspace, there is some more structure to be uncovered. The question that we lost today is, in general, if you are given a bunch of data points, how can you uncover these cluster based structure in the data.

(Refer Slide Time: 3:19)

So, the goal of the lecture is to understand let us say, we are given a bunch of data points as usual x1 to xn, all data points we are going to assume are in D dimension. Now, we want to partition the given data into K different clusters, K different partitions or clusters or groups. We can call them however we want. But that is the goal. So, we want to partition the data into K different, think of these as boxes, let us say.

So, here is an example. I mean, a simple example, let us say we just have a bunch of points, x1, x2, x3, x4, x5 and we want to partition them into, let us say, 3 boxes. Now, there are multiple ways you can group these things together. So, maybe there is one way which groups x1, x2, x5, in one box, x3 in one box and x4 in one box. Maybe this is a way to partition the data into 3 boxes or 3 clusters.

Here is another way, x1, x4 in this way, in this grouping group together, x2 stays separate, let us say x3, x5 group together. So, there are multiple ways you can partition a bunch of data points into boxes, K different boxes. In fact, in this case, if you want to argue how many ways are there to partition, 5 points into 3 boxes, naively speaking, each point, you take every point and then the point has 3 different options, 3 different boxes that it can go to.

And if you take the second point that also has three different options. So, if you naively compute how many ways you can put 5 points into 3 boxes, there are 3 into 3 into 3 into 3 into 3 in each point has 3 options. So, there are 3<sup>5</sup> possibilities. So, this also of course, includes possibilities which lead to empty boxes or empty clusters. But for the moment, even if you do not want that this will still be a very large number.

So, this is exponential in the parameters of interest, in this case, the number of data points and the number of points number of 2 boxes. So, this is something that we understand so that there are a lot of possibilities of putting points into a bunch of boxes. Now, we want to understand how do we, what is, what is a good way to do this.

That is the goal, which means that for each of these partitions, each of these ways of putting data points into boxes, we need to say, how good is that partition, we need to come up with a performance measure for a partition given a bunch of data points.

(Refer Slide Time: 6:14)

So, the next goal, what we want to do is what is a good performance measure for partitioning data points into clusters. Towards this, what we will do is we will first introduce some

notation. As usual, our data points are x1 to xn. So, these are data points. Now, we are going to say every data point is associated with a cluster indicator variable, which I am going to call as z. So, this is z1 to zn so these are cluster indicators, zi belongs to 1 to K.

Meaning every data point goes to one of these boxes, 1 to K. So, that is the problem. So, we need to put each point in one of the boxes, let us say if I put the tenth point in the fourth box, then x10 is the point data point and the corresponding z10, the variable corresponding to the cluster indicator for the tenth point which is z10, will now be 4.

So, now each of these values z1 to zn takes a value between 1 to K which indicates which cluster or which box, the corresponding point goes into, so this is a way to define a partition, if you will. So, once I give you z1 to zn then you know where each data point goes into. So, that is what this z1 to zn tells you and then that determines a partition. So, once we have this notation, then we ask the question given a cluster assignment, how good is it?

We want to understand how good a partition is? So, I can give you some cluster assignment and then I asked you how good is this assignment? Now, you need to objectively measure performance of goodness of a partition, which means that we need to associate a number to each partition, which means that if I tell you z1 to zn then you need to give me a number, which says how good is this way of partitioning x1 to xn via z1 to zn, how good is it?

So, let us call this a some function z1 to zn, of course, depends on x1 to xn also so I give you the partition partitioning of the data points into K clusters. I asked how good is this partition? So, now, you can one way to think about this, there are multiple ways you can define this function. One natural way you can ask is, you somehow want partitions to be homogeneous in the sense that if I say that I have clustered a bunch of data points into three different clusters, every cluster should somehow look alike.

Now, how can we measure alike looking alike of a cluster? Well, again, you can measure it in different ways. One natural way is to kind of look at how spread the data points are in this cluster. In other words, you can ask well, how different are these points from the mean or the center of this cluster.

So, you can measure the distance from of each point to its center and then sum it up over the set of points in the cluster and then that will give you some sense of how good is this cluster?

How homogeneous is this cluster, if the all the points are the same, then each point will suffer zero distance to the center. If the points are like, well apart, then they suffer a larger value.

So, we want to somehow formalize this intuition and say that the performance measure that we will be interested in is as follows. So, for every data point, you measure the distance of the data point xi to μzi. And I will tell you what μzi is and then this is an l2 squared distance. So, what is μzi, well, μzi is mean of mean meaning the average, mean or average of zi cluster.

Remember zi is a value between 1 to K, so it tells where which cluster xi goes to. So, how can we define μ’s, μk can be defined as follows μk is just the average of all the data points which go to the kth cluster according to z1 to zn. So, I look at z1 to zn each of these is a value between 1 to K and look at which of the data points have been assigned to the kth cluster. And then I compute the average for that set of points.

So, in notation, one way to put this would be to do the following. I say I am going to sum up all data points. But then not all data points have been assigned to the kth cluster. So, I will multiply this with a number, which is an indicator of whether the corresponding cluster to which the xi point has been assigned to is k.

So, this indicator value takes 1 if this is true, which means if the ith point is been assigned to the kth cluster, then this 1, otherwise, this is 0. So, basically, what I am doing is I am adding up all the points which have been assigned to the kth cluster. And then I am dividing it by the number of points assigned to kth cluster, which can be just got by summing up the indicators over all data point.

This would again be 1 indicator of some u is 1, if u is true and 0 otherwise. Which means all I am doing is it is just a notation to say that I am just looking at each box and then computing the average of that box. So, then what does this performance measure compute, it computes the distance between every point to the mean of the box distance square of every point to the mean of the box in which it is assigned. So, this is the performance measure with which we will work right now.

Just to make sure we all understand this perfectly well. So, here is an example. Let us say I have points x1, x2, x3, x4, x5 and then I have z1 is 1, z2 is 2, z3 is 1, z4 is 1, z5 is 2, in this case, let us say K is 2. I want to divide the 5 points into 2 boxes. And here is one way to

divide that, so I am saying x1 goes to the first box, x2 goes to the second box, x3 goes to the third box and so on, fourth to the one, fifth point to the second box.

So, what would be μ1? μ1 would be check which of the points have been assigned to box 1, in this case, x1 and x3 and x4, so this will be (x1 + x3 + x4) / 3, μ2 would be what is what are the points assigned to the second cluster x2 and x5 . So, this is going to be (x2 + x5) / 2.

So, this is basically an example of whatever we are saying here. So, the goodness of this partition itself would be (x1 - μ1)<sup>2</sup> + (x2 - μ2)<sup>2</sup> because 2 is the centers partition to (x3 - μ1)<sup>2</sup> + (x4 - μ1)<sup>2</sup> +( x5 - μ2)<sup>2</sup> and so on. So that is the way we are defining partitions.

And so now we have put down a specific measure or a metric to measure goodness of a partition. So, what would be our precise goal, our goal is now to minimize over all possible 𝑛 partitions, the measure that we just put down, which is ∑ (xi - μzi )<sup>2</sup> . So, this is our goal. 𝑖=1

So, when I want to find out this is to go over all possible partitions and then see, which one gives us the least value and we know that there are only a finite number of partitions. So, we could potentially imagine an algorithm where we will go over each partition and measure this and then pick the one that has the smallest value.

But what might be a problem with that algorithm. If you want to pause and think let me tell you the problem with that algorithm, now, the problem is there are too many partitions. There are too many possibilities to do this naive algorithm. In fact, the naive thing would be it will be K<sup>n</sup> . So, each data point has K possibilities if there are K clusters and there are n points.

So, there are potentially K power and ways to divide put points into boxes. Again, this is an upper bound because this also takes into account empty boxes, but then still, your actual value will not be 2, it will also grow exponentially. And that is a problem. So, computer scientists would say that this is an NP HARD problem.

In other words, it is not expected that we are going to get an algorithm to solve this, whose run time the amount of time it takes to run is polynomial in the parameters of interest, which is n and k in this case, maybe if there was something like N<sup>2</sup> into K<sup>3</sup> , that was your the amount of time if you came up with an algorithm, then that is a good algorithm because it runs polynomial in n polynomial in K.

But then right now we are saying the naive algorithm is going to take K<sup>n</sup> , where you look at go over all possible partitions and that is a big no, no. So, we simply cannot run this algorithm. Imagine even if K is 2 and the n is if you have 1000 data points. And this is saying the number of possible ways grow something like 2<sup>1000</sup> .

And that is like an astronomically large number to deal with. So, and we do not want to do that. So, then what can we do? So, if this is our goal, then how can we achieve this goal? We would not necessarily be able to achieve this goal exactly, but what we will do is we will come up with a very popular heuristic algorithm to kind of solve this problem. And we will see what this algorithm next.