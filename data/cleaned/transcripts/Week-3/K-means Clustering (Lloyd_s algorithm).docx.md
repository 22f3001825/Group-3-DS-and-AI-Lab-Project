# **Machine Learning Techniques Professor Arun Raj Kumar Department of Computer Science and Engineering Indian Institute of Technology, Madras K-Means Clustering (Lloyd’s algorithm)**

(Refer Slide Time: 0:14)

The algorithm that we are going to see is called as the Lloyd’s algorithm or sometimes also referred to as the K-means algorithm. Though this is a misnomer the problem is the K-means problem you are trying to find K-means, which represents the partitions. But sometimes the algorithm is also called as a K-means algorithm though it is the K-means problem for which the Lloyd’s algorithms a solution is a possible way to solve this problem may not be exactly but then a heuristic way to solve this problem. Anyway, so names aside. So, let us look at

what this algorithm is right now. So, it is very, very simple algorithm. So, it does the following.

So, the first step is initialization. We have a bunch of data points, which we need to first put in some boxes. So, we will talk about what are good ways to initialize a little later. But for now, for the moment, assume that we are starting with some way to put points in boxes, which means that we have z<sup>0</sup> 1<sup>,z0</sup> 2<sup>tillz0</sup> n<sup>everythinginbetween1tok.So,this0here</sup> indicates the iteration number. So, at initialization, you are saying each point has been assigned a cluster indicator, some value that you can get started with.

Now, what is the algorithm do? The algorithm essentially does two simple things. It runs until convergence. And we will talk about what it means to say the algorithm converges in a bit. But let me put down the algorithm first. The first step is compute the means step. This is step 1, which means what we do is for all k, we compute µk<sup>, which is the mean in the t th iteration</sup>

𝑛 as simply the way we defined earlier ∑ xi 1(zti = k). In the t th iteration does your partition 𝑖=1

𝑛 i look like put i th data point in the kth cluster divided by ∑ 1(zt = k). 𝑖=1

Well, every round, you are creating a new partition. That is the idea. And what we are saying is that once the partition is created points go into boxes and then you can compute the mean of each of these boxes. And these means we are just going to call them µtk<sup>to indicate that we</sup> are in the t th iteration. That is the easy point.

So, the main crux of the algorithm relies on this step that I will put down now it is called the reassignment step, which says how am I going to reassign the partition. So, which means that I start with some z’s, which is z<sup>0</sup> now in the next round, I need to change it to an updated cluster indicator values. How do I do that, so for all i for every data point, I need to say which cluster it goes to now, in the next step, so I am going to do the following. I am going to do reassign z<sup>i</sup> t + 1<sup>whichistheclusterindicatorfortheithdatapointinthenextroundasthe</sup> following.

So, basically, what I am doing is, I have a partition which means points are being put inside boxes every box has a mean now, I look at every point and then compare its distance to the mean to the box in which it is assigned to, to the mean of every other box. If I find a box, whose mean is strictly less than the distance to the mean in a different box is strictly less than

the distance to the current mean inside the same box. Then I assign this data point in the next round to that other box which means which is exactly what is happening here. I am saying z<sup>i</sup> t + 1<sup>theassignmenttotheithdatapointinthetplusfirstiterationisjustthatkthat</sup> minimizes the distance of the point to the mean of each of these boxes, which box has a mean whose distance I am who whom I am closest to.

So, this is assuming if the current assignment mean, so if the mean of current assignment is smallest, then don’t reassign. So, maybe you are in a situation where the current points, the current means distance is exactly the same as the distance or the mean to a different cluster. In that case, I do not want to jump, I will still be in the same box where I am. But if I find a box whose mean is strictly less than the current distance, so the current mean, then distance square to the current mean, then I will make this jump. So, that is what is the understanding. So, this is all the algorithm is.

Now we need to talk about a few things here. So, what does it mean to say, this algorithm converges? Well, what is happening in each round is that I am changing the partition from one to another. So, at some point, if I encounter a situation where no point wants to jump, partitions, jump boxes, so every point is happy with its own box, which means that the distance of each point to its own box’s mean is strictly less than any other box’s mean, then no jumping around happens and then the algorithm is said to have converged.

The question is, I have only put down what until convergence, which means that we need to first see if this algorithm converges at all, so it could happen that I am in a certain partition and then I change in round two to a different partition and then round three to a different partition, and the next round, I come back to the original partition, if that happens, I will be stuck in a loop. And then I will keep moving around and I will never change from one partition to another. I mean, I will never converge, the algorithm will never converge. So, I will keep changing partitions, but then I will never converge.

But then here, I am saying until convergence, which means that we need to first understand if this algorithm converges at all, so all this algorithm is saying that hoping that this is that I am in some partition and I hope that I go to a better partition after making this change. So, because intuitively, we want partitions to be to all look similar. So, every point should be closer to its own mean than any other mean. If that does not happen, then we make a jump. And we hope that this will eventually lead to a partition, which is a reasonably good partition.

But then that is a hope at this point, we need to argue why this algorithm will converge and so, I mean, will it converge, if so, how do we argue that? So, that needs an argument.

(Refer Slide Time: 8:31)

The fact is that Lloyd’s algorithm converges. And we will see why a little later but we can argue that this algorithm indeed converges. That is the good news. However, it could also happen that the algorithm does not necessarily converge to the optimal solution. So, the converged solution may not be optimal. Meaning it may not be necessarily the solution to the original problem that we put down, which was to, which was this np hard problem. Obviously, we do not expect to solve this original problem because it is known to be hard. So, whatever the algorithm results in may not necessarily solve this problem. So, that is the that is

something that we have to live with in some sense, but produces reasonable clusters in practice.

So in practice, this is a very popular algorithm and it kind of produces not so bad clusters. So, what we will do now is ask a couple of questions about this algorithm and then try to answer each of these questions. So, now I put down some algorithm. So, there are lots of questions that one needs to ask about, what kind of datasets where this algorithm will work well and there are many other questions. We will first list on some of the important key questions about this algorithm and we will try to answer those questions in the as we go long. So, here are some questions.

First question is about convergence, does is algorithm converge. The second question is, so let us say it converges, what kind of clusters does it produce, the nature of clusters. The third question on my task is, so there are some things which have not been specified clearly in the algorithm, one of the things is initialization. How do I initialize this algorithm?

And finally, so I have kind of side stepped this issue that we are assuming so far that given a set of points, we know the number of boxes that the points can have to be clustered into. But nobody is telling us that we are just given a bunch of points and then in an unsupervised way, we need to figure out some natural groupings, which means that what is the k that we should use that works well for this data set.

So, the choice of k is also question that one needs to ask. So, we will try to answer all these questions in the following part of this of this general discussion about the Lloyds and the K-means algorithm.