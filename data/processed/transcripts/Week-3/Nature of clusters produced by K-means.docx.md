

# **Machine Learning Techniques Professor Arun Rajmar Department of Computer Science & Engineering Indian Institute of Technology, Madras Nature of Clusters Produced By K - Means** 

(Refer Slide Time: 0:15) 



So, the next thing we are going to look at is what kind of clusters are being produced by the Lloyd’s algorithm? So we know that the algorithm converges, but what can we comment on the type of clusters that that results from this algorithm? 

So to take a simple case, let us look at the case first, when 𝐾 equals 2, when you have a bunch of data points, you just want to divide them into two buckets or two clusters. So let us say Lloyd's algorithm is run with just 𝐾 equals two and Lloyd's algorithm produces 2 clusters. It will converge and it will produce two clusters with means, let us say µ and µ . 1 2 

(Refer Slide Time: 1:30) 



Let us say the algorithm converges and then we, in the converged partition clusters, we look at the average of cluster 1 and cluster 2, and it turns out to be µ and µ . Now, the question 1 2 is, what can we say about the points assigned to these clusters assigned to cluster 1 and cluster 2? Let us say cluster 1. Let us say we focus on cluster 1, the argument for cluster 2 

will be similar. 

(Refer Slide Time: 2:10) 





Can we say something about how do the points look like? Well, by algorithm’s construction and the convergence argument that we did earlier, we know that when the algorithm said, the partitions have converged, it means that everybody, every data point is happy with their own mean. What does that mean? 

Well, for if you look at cluster 1, then it means that each data point that has been assigned to cluster 1 is closer to µ than µ in terms of distance squared that is what it means, right? So it 1 2 2 2 means that for cluster 1, for points in cluster 1, ‖𝑥−µ ‖ ≤‖𝑥−µ ‖ . Where 𝑥 is of 1 2 course, a point a generic point in cluster one, right? 

So its distance squared to µ should be at most, the distance square to µ . Now, what does 1 2 this mean? I mean, how do we understand this? So we can think of this as µ , this as a µ , let 1 2 us say I just give you µ and µ . And they ask where could be these clusters? Now, we know 1 2 that points assigned to cluster 1 satisfy this equation. 

But what does this equation, let us unravel this equation a little bit and see what happens? So, 2 2 𝑇 2 2 𝑇 this is just ‖𝑥‖ + ‖µ ‖ −2𝑥 µ + ‖µ ‖ −2𝑥 µ , of course, we can cancel 1 1 ≤‖𝑥‖ 2 2 certain terms and what would result is the following. I can bring the last term to the other side. 

2 2 𝑇 ‖µ2‖ −‖µ1‖ So that would mean 𝑥 (µ2 −µ1)<sup>≤</sup> 2 , what is this? So this is for all 𝑥 in cluster 1, it must be the case that this is satisfied. Simply because the distance of this points to µ is less 1 than µ , what does this mean? So pictorially what are these points? That is something that we 2 want to understand. 

So, if this is µ and µ , how can we say where are the set of points which are, which satisfy 1 2 this equation, this as you can already observe, this is an equation of the form, you know, 𝑇 𝑥 ≤𝑏. So it is, it is, it is linear in 𝑥 that is what we observed. So, which means we should expect some kind of linear division and let us see what that is? 

# (Refer Slide Time: 5:19) 



So here is a picture we have µ , let us say this is µ . And we want the equation is 1 2 2 2 𝑇 ‖µ2‖ −‖µ1‖ 𝑥 (µ2 −µ1)<sup>≤</sup> 2 ~~.~~ Well, basically the dot product of your cluster point 𝑥 with respect to µ minus µ is at most something that is what this is saying. But let us look at 2 1 where is the vector µ minus µ , well here is the vector µ . 2 1 2 

So, this is µ , this is µ where is in this case? Let me just confirm the order, one order here, 2 1 sorry, yeah, this is correct. So where would be µ . So, µ is what you would add to 2 −µ1 2 −µ1 

µ to get to µ , which means it is this. So, this is what you would add to µ to get to µ that is 1 2 1 2 your µ . So, which means the actual vector is from the origin pointing in this direction. 2 −µ1 

So, that is my µ vector, this is where the vector that vector is. Now, we know where are 2 −µ1 the set of points which make us 0 dot product with this vector. Well, that would be 𝑇 somewhere here. So, this would be set of all 𝑥 such that 𝑥 µ<sup>=0</sup> . But our condition ( 2 −µ1) 

2 2 𝑇 ‖µ2‖ −‖µ1‖ says that 𝑥 (µ2 −µ1) is at most 2 ~~.~~ . 

So, now, whether that value is positive or negative will depend on which length is bigger 2 2 2 ‖µ ‖ length is bigger or ‖µ ‖ length is bigger, at least in this picture, it looks like ‖µ ‖ 2 1 2 2 length is larger than ‖µ ‖ square length so, this seems to be a positive quantity. So which 1 𝑇 means if I want extra, if I asked the question, where is 𝑥 µ is less than or equal to ( 2 −µ1) 2 2 ‖µ2‖ −‖µ1‖ instead of less than or equal to if I put the equal to and ask where is it equal to 2 . 2 2 In other words, if I ask whether the set of all 𝑥 which satisfy𝑥𝑇(µ2 −µ1)<sup>=</sup> ‖µ2‖ −‖µ2 1‖ , well, because we are thinking of this as a positive quantity, that means that I have to move the green line parallel in this direction. So, that would give me a line let us say like somewhere like this. 

2 2 𝑇 ‖µ2‖ −‖µ1‖ Now, this could be the line which is 𝑥 (µ2 −µ1)<sup>=</sup> 2 ~~.~~ So then, where is our cluster 1? It says that any 𝑥 that is in cluster 1 should satisfy something, is it has to be less than or equal to this, which means that it has to be in this region. So left of the orange line. This is the region for cluster 1, cluster 1 region. Now, this is one way to think of this, directly from the picture. 

Now we can also ask, well, how much did they move on to the right? So I did not move the green line parallely to the right. So, how much did I move? Well, can we find a point which satisfies this equation, then we will know. So, one point that satisfies this equation is like take 

µ1+µ2 𝑥= 2 which is the average 𝑥, so average of the means. 

𝑇 2 2 µ1+µ2 ‖µ2‖ −‖µ1‖ So now then 2 (µ2 −µ1), you can verify will equal 2 , which means that the ~~(~~ ) average of the means is actually here. So the average of the means is exactly this point. This µ1+µ2 point is essentially then saying this is 2 ~~.~~ 

2 2 So this is just ‖µ2‖ −‖µ2 1‖ , which means this point, which is the average of, which is between 

µ1 and µ2 actually falls on this line. So, which is in fact, this is µ1+µ2 2 ~~.~~ So, another way to think about this is to simply say that, well, I have two points. And then I want to, I want to understand the set of all points which are closer to one point than the other 

Well I connect the line between these two points, look at the perpendicular bisector of this line, and then say that every point that falls on one side of the perpendicular bisector or closer to that point, and which is exactly what we kind of argued, in the general sense in high dimension as well. 

So this is good so this just means, what happens in two dimension? So even K equals 2, let me just make sure that, well, if this is cluster 1, well, where are cluster 2 data points, cluster 2 on this side. So, basically what has happened is that, so your K means algorithm or the Lloyd’s algorithm is going to give you clusters, if K equals 2, you just separate it by a line that is what this means. So it has to happen. This simply comes from the convergence criteria for algorithm, so that implies this. 

(Refer Slide Time: 11:38) 



So now what happens when K equals 3? That is an actual question we can ask. And we will see that and that might give us some more intuition as to how these clusters look like. In 𝐾= 3, the algorithm is going to converge with not just 1 mean, but then 3 means sorry, not just 2 means but then 3 means. 

Let us call these means µ , µ , and µ , let us say again, the data is just two dimensional data, I 1 2 3 mean, all of whatever we are saying works for high dimensional data also, but then it is easy to visualize the two dimensional data that is why we are doing this. So now, what is the question we are asking, where are the points which are assigned to cluster 1? That is the first thing that we like to understand. 

Now, we know that by the convergence criteria of Lloyd's, every point that is assigned to cluster 1 is closer to µ than µ or µ . So, both of them, I mean, if I compare even if I find one 1 2 3 of the others, µ , µ as being closer, then I would have jumped the algorithm would not have 2 3 converged. So that cannot be these µs cannot be the final µs. 

Because the algorithm has converged, every point assigned to cluster 1 necessarily should have distances to µ closer than both µ and µ . So how does that look in picture? Well, first, 1 2 3 where are the set of points which are closer to µ than µ ? Well, we already argued that that is 1 2 going to be simply, let us say, if I put this imaginary line that joins µ and µ , then that is just 1 2 going to be in the left hand side of the perpendicular bisector of µ and µ . 1 2 

Now, µ need not be on this line, µ could be somewhere here also, right? So this line is like 3 3 this. But we are also saying just for consistency, I am going to use the green color here. So, anybody on the left hand side of the green line is closer to µ than µ , but that is not enough 1 2 to say that point can be assigned to cluster 1. 

So, it is also necessary that the point should be closer to µ than µ also, which means that I 1 3 need to also look at the perpendicular bisector of the line joining µ and µ and that may be 1 3 somewhere like this and it can go further, further is not that necessary. But now it means that well, the points assigned to µ or on the left hand side or the direction that I am drawing here 1 with respect to µ and should also be on the left hand side that is the direction I am drawing 3 here with respect to µ . 1 

Which means if I had to shade that region where the points are in cluster 1, it will be an intersection of these two regions, which will exactly be this so, it will be the boundary would be something like this. Now what about µ and µ . So where are the points in cluster 2 and 2 3 cluster 3? Well, for that we need to draw one more perpendicular bisector, which connects µ 2 and µ and that would some be, somewhere like this. 3 

And that would tell us those assigned to cluster 2 are going to be in this region. So this would be my boundary, it is closer to both, I mean, it is closer to µ than both µ and µ so, it should 2 1 3 be in the blue region. Naturally, whatever remains is the ones that are for µ region which is 3 this region. 

So, as you can see, what has happened is that you know, you have three different separators one for each pair of means, µ µ separator, µ µ separator and µ separator and then the 1 2 1 3 2 µ3 points assigned to µ or closer to µ than µ via the µ µ separator and µ than µ via µ 1 1 2 1 2 1 3 1 µ3 separator. 

So, essentially what we are doing is that, we are dividing the entire space in this case 𝑅 which is where the data points are into 𝐾 different regions using you know intersection of half spaces. Basically, when I say half space, it means that in two dimension you draw a line and anything on one side of the line is what is called as a half space, it is dividing the entire 

space into two parts, a half is on one side of the line the other half is on the other side of the line. 

So there are for every data point, so for every cluster, now, your region would be an intersection of 𝐾−1 half spaces, if you have K clusters to begin with, because every point is going to get compared with, every mean is going to get compared with 𝐾−1 other means and then it should attract point towards itself. 

So it will be an intersection of half spaces. So cluster regions are intersection of half spaces. So this argument works even for high dimension with visualizing in 2d, but then it is true for high dimension as well. 

(Refer Slide Time: 17:20) 



And these type of intersection of half spaces they also have a name, this is called as Voronoi region. So basically, what that then tells us is that if you run the Lloyd’s algorithm then the clusters can be, you know, imagined as if they are falling in different Voronoi regions. Basically, your Lloyd’s algorithm is trying to find the best, in some sense, Voronoi partition that will lead to, in some sense, the best cluster, right? 

So you necessarily, the partition, the points assigned to each cluster should be part of a Voronoi region. That is what this argument finally says this. So this is the comment that I wanted to make about the nature of clusters. 

(Refer Slide Time: 18:25) 



Let me also, at this point, make a comment about something that we perhaps will not discuss in this course. But then it is interesting to know also. So for example, if I had data in 2 dimension like this, so let us say I had data around a circle, like this, and I had some more data points in a smaller circle. 

Now, the number of clusters in this dataset naturally looks like two clusters and one cluster, which are in the outer concentric circle, and the other cluster are the points in the inner concentric circle. Now let us say I give you this dataset, and I asked you to run the Lloyd’s algorithm with 𝐾= 2. Of course, it is going to converge, we know that, but what kind of partitions would it result in? 

In other words, where would these points get clustered? How would these clusters look like? Now if you think about that, we know from the previous argument that the clusters necessarily have to be in Voronoi regions, if 𝐾= 2, then it means that there is a line that divides cluster 1 from cluster 2. 

Now, if the points are in the circles, maybe you might get a line something like this. It is not necessarily that it has to be a slant line, it could be a vertical line, I mean that the exact line depends on the exact spacing of these points and so on. But irrespective of how the points are spaced, it is going to be a line which means that I am going to say anybody on this side is in cluster 1 and all the points are on the other side or in cluster 2. 

Which means we did not recover the real clustering that we want, which was the inner concentric circles should become one cluster, the outer concentric circle should become 

another cluster, your K-means algorithm in the way that we have described, it will never be able to recover such a partition, because the nature of clusters or Voronoi partition. 

So, if your data set, if you do not believe that if your data set has a nice Voronoi like structure, where the partitions, where the cluster sit, then perhaps your K-means algorithm is going to fail there. So it will not be able to recover. Now, how to fix this, so how to fix? So, we will not do this in detail in this course, but let me at least give you some pointers, which you can perhaps if you are interested, you can go ahead and read about these things. 

So, like how we argued in PCA that, if your features are non-linearly related, then you can use this notion of kernels to go from low dimension to high dimension. And in the high dimension, you learn a linear relation, which translates to nonlinear relationships in the lower dimension. 

Similarly, you can, there is a way to, you know, kernelize K - means it is called the Kernel K means algorithm and it has interesting relationships to other types of popular clustering algorithms also, which we are not seeing in this course, for example, something called a spectral cluster which is, which has a lot of relation to PCA as well. So, in simple terms, you can understand this as if, you know, maybe there are no Voronoi regions in the low dimensional space, that gives me natural clustering of this data. 

But then if I map it to some high dimensional space, then it would, it would kind of, you know, the natural clusters would kind of separate out into different Voronoi regions. And in the high dimensional space, I can do a simple Lloyd’s algorithm that is the basic idea. So to go to this high dimensional space without really, the problem of computational efficiency and so on, inefficiency, and so on, we use the kernel trick, and you can Kernelize K- means also. 

Let me leave it at that without dwelling into depth about how to do this Kernelization. But it is good to know that you can kernelize K means also. And this kernel version of K means has a lot of relation to, you know, computing the eigenvectors of your Kernel matrix and then using them somehow as some representation of these data points to do further cluster. We will not look at that in this course, but it is good to know. 

So that is all I want to comment about the nature of clusters that Lloyd’s algorithm produces. We have two more issues that we need to talk about. One is the initialization issue. What, 

how do you initialize Lloyd’s algorithm? Well, and the second is the issue of how do you choose the number of clusters? First, we will talk about the initialization issue. 

