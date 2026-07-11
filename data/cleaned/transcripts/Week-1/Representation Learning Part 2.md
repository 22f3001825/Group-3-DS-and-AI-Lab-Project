# **Machine Learning Techniques Professor Arun Rajkumar Department of Computer Science & Engineering Indian Institute of Technology, Madras Representation Learning: Part 2**

(Refer Slide Time: 0:13)

Here we are seeing if we know that, well, four points are on a line. And the fifth point is not
on the line, then how can we find the proxy for the fifth point along the line that has the four
points. But in practice, nobody is going to come and tell us that, hey, these points are on the
line, these points are not on the line. So, now you can find the proxies for the points not on
the line along the line, nobody tells us that.
We are just given a dataset, which has a bunch of points. So, which means that we need to
find that line on to which you need to project these data points as well. So, that is also
something that we need to find. So, now there are multiple lines. So, we need to somehow
find that line, right. So, that is what we are going to do next, we are going to use the fact that
given a line, we know how to find the proxy for a data point on this line, to actually find that
line itself. Let us see how we can do that.

Here we are seeing if we know that, well, four points are on a line. And the fifth point is not on the line, then how can we find the proxy for the fifth point along the line that has the four points. But in practice, nobody is going to come and tell us that, hey, these points are on the line, these points are not on the line. So, now you can find the proxies for the points not on the line along the line, nobody tells us that.

We are just given a dataset, which has a bunch of points. So, which means that we need to find that line on to which you need to project these data points as well. So, that is also something that we need to find. So, now there are multiple lines. So, we need to somehow find that line, right. So, that is what we are going to do next, we are going to use the fact that given a line, we know how to find the proxy for a data point on this line, to actually find that line itself. Let us see how we can do that.

(Refer Slide Time: 1:15)

So, now just to make this goal a little bit more precise. So, this is our goal now. So, we want
to develop a way to find of course, a compressed representation of data, when data points do
not necessarily fall along the line. So, we are not going to assume that all the data points are
along the line, just that one or two points are not on the line.
So, this is not an exception. So, this is almost a rule. So, it is never going to be the case that
we are going to find almost all points on a line, but then just one or two points not on the line,
is more like a rule not really an exception. What do I mean by that? Let us say if I if there
was a class of 100 people, and then I measured the height and weight and try to plot them, we
might get some values like this. So, of course, as the height increases, the weight increases.
Now, we may want to represent this dataset using this line, but as you can see, I mean, only
one or two points actually perhaps fall on this line, maybe none of the points fall on this line,
yet we want to represent this data points using this line. So, which means that the fact that
there is an exact linear relationship between the features is a myth. So, that is never going to
happen. That is, very, very rare.

So, now just to make this goal a little bit more precise. So, this is our goal now. So, we want to develop a way to find of course, a compressed representation of data, when data points do not necessarily fall along the line. So, we are not going to assume that all the data points are along the line, just that one or two points are not on the line.

So, this is not an exception. So, this is almost a rule. So, it is never going to be the case that we are going to find almost all points on a line, but then just one or two points not on the line, is more like a rule not really an exception. What do I mean by that? Let us say if I if there was a class of 100 people, and then I measured the height and weight and try to plot them, we might get some values like this. So, of course, as the height increases, the weight increases.

Now, we may want to represent this dataset using this line, but as you can see, I mean, only one or two points actually perhaps fall on this line, maybe none of the points fall on this line, yet we want to represent this data points using this line. So, which means that the fact that there is an exact linear relationship between the features is a myth. So, that is never going to happen. That is, very, very rare.

So, physical loss might satisfy something like that. But then your real world data will perhaps never satisfy that. So, which means that we are always going to find proxies for data points along the line. So, you will have to find these proxies. Now, if I know that the red line is the best line, then I know how to find proxy for each of these data points. But nobody gives us the red line. So maybe it is not the red line, maybe it is the blue line.

So, now how do we know? So, because for given a line, I can always find a proxy  along that line for any data point so, I could have found proxies for all these purple data points along the blue line as well. So, by finding, by projecting them along the blue line, now the brown points would act as the proxies, and I can still compress them.

Now both are going to give me the same amount of compression. There is no doubt about that, because once I found proxies along the line, I can find the representative for this line and one  coefficient for each of the data points both are good ideas. But one line is still better than the other, not in terms of the amount of compression you achieved.

But in terms of what, think about that. Let me tell you what it is. So, it is obvious that why the red line is better than the blue line, though both give us 50 percent compression, the red line is a better line because if you had to reconstruct this data set, then the amount of error that you suffer with respect to the original data set with respect to the red line is much lesser than the blue line.

So, the reconstruction error is lesser for the red line, not the compression ratio, the reconstruction error is less for the red line than the blue line. So, which means we have to find that line to represent our data that gives us the least reconstruction error. Now how do we find that is the question.

(Refer Slide Time: 5:09)

So, now we have a very, very precise goal to tackle. So, now our modified goal, or rather not a modified goal, our specific goal now is find the line, given a data set, of course, I am not

writing that again, find the line that has the least reconstruction error. This is what we want to find.

(Refer Slide Time: 5:40)

So, Let us do this. Now, Let us say you have a data set. As usual, we have unsupervised data
set, which is{ , …. }. Where  . Now, how do I define the error for a given line
with respect to the data set? Well, basically, what you need to do, you need to kind of sum up
the errors for each of the data points. So, your data set has a bunch of N data points.
So, you  sum up the error incurred by each of these data points  along the line. So, this is for a
given line, if I give you a line, you can measure the performance of the line as the error that
the dataset incurs on this line. So, by counting, by summing up the error for each of the data
points, but what is the error of a particular data point on a line?
Well, that is just the length squared of this line, which we are going to think of as being
represented by some  , which is just we know . Now, remember, when I say line,
I am going to represent using, this line is going to be represented using   such that the length
of   is 1, So,   or   is 1.
That is how we are going to think of lines, so among all possible lines represented by vectors
in the unit circle, I want to find the best line so, given a line, which means I give you a

So, Let us do this. Now, Let us say you have a data set. As usual, we have unsupervised data set, which is{ , …. }. Where . Now, how do I define the error for a given line with respect to the data set? Well, basically, what you need to do, you need to kind of sum up the errors for each of the data points. So, your data set has a bunch of N data points.

So, you  sum up the error incurred by each of these data points  along the line. So, this is for a given line, if I give you a line, you can measure the performance of the line as the error that the dataset incurs on this line. So, by counting, by summing up the error for each of the data points, but what is the error of a particular data point on a line?

Well, that is just the length squared of this line, which we are going to think of as being represented by some , which is just we know . Now, remember, when I say line, I am going to represent using, this line is going to be represented using such that the length of is 1, So, or is 1.

That is how we are going to think of lines, so among all possible lines represented by vectors in the unit circle, I want to find the best line so, given a line, which means I give you a . And I asked what is the error, and that would be the sum of the errors for all the data points along the line. Now, what is the length squared?

Well, we know the length is just . For any vector, let us say we take a vector, the = , so dot product of a vector with itself is just its length squared. Now if you do that, so then this is going to be just

# . This is what we want to minimize.

And if you want to minimize this, we can well, this is the error of a given line given with respect to the data set. And our goal is to find that that minimizes this, so we can think of this as some function of , which is just the sum of the errors, . This, so now you want to minimize this function.

Now, a couple of things that we will do here, so we will think of this as the average error instead of the sum of their that does not really change the . So, if some minimizes the sum of the errors, it is the same that will also minimize the average error. So, I can think of this as function as that that minimizes the average error as well.

We will see why we can think, I mean, the whole derivation would go through even if you think of the sum. But in terms of interpretability, we will see why the average is a better thing to look at later, so now this we know, the length squared is just of a vector. Remember, this is a vector is in R<sup>d</sup> , is in R<sup>d</sup> . This is in R. So, this is a scalar times , this is the proxy for along the line .

And then you are looking at the difference vectors. Difference is a vector and we are looking at its length. And because is a vector, the length squared is just the transpose of the vector with itself. So, I can write this as . That is still. Well, I should

write everywhere I should use i. Sorry about that. Because this is the ith data point, .

(Refer Slide Time: 9:55)

So, now I can expand this. I am sure. I mean, anybody who has done an MLF for linear algebra course will know how to do this expansion, I will do this nevertheless. So, this is minus times , that is a square minus, again, into , which is same as.

. And the last term is plus , the scalars multiply themselves that is . Now the vectors will dot themselves . Well, that is , but we know that the ’s that we care about have length 1, so that is just multiplied by one. So, if you do, again, some simplification, these will cancel out. And we are just going to have .

### Timestamp: 11:03

Now if you think about this, we are after that that minimizes this value. So, but if you look at the first term that does not have a , so, that is a constant that you are adding to each of these terms. So,  it will not affect your , even if you remove that constant. So, equivalently,

I can minimize a different function without that constant, which would simply be .

So, the constant can go away and then the, whichever minimizes g(w)is also the 1 that minimizes f(w). If you are not convinced about this, pause and think about why this constant does not matter in finding . So, now this isg(w), which has a negative sign. Of course, we want to minimize over all such that or is 1.

So, that is, the goal. But instead of holding on to this negative sign, we can write this as instead, max over W such that, is 1, without the negative sign, I can write this as

So, we will see why we are doing this simplification.

So, now I can write this objective as . It is the same thing, So, is

same as , I am squaring this. So, I can write this as product of two terms. And why am I doing that?

Well, that is because I can now write this as now remember, is a vector in R<sup>d</sup> , So, which means transpose can be thought of as like a 1 x vector. is a x1 vector is a 1x vector, is a x1 vector. So, vectors are all column vectors. By default, the transposes will be row vectors.

Now I can write this whole thing as , I have just changed the brackets. So, that is still. Because everything is linear, I can do this as well. This is just matrix multiplication. So, it does not matter. I mean, the same trimetric. I mean, I can do whichever way I want. I am not like commuting it.

So, remember that I am just changing the brackets, the order in which the multiplication happens is still the same. Now, note that does not depend on i. So, I can bring outside and say that this whole thing is

. Now, let me note this, that this, what object is this?

So, if you have not, if you are not already seeing it, pause and think about what kind of an object is it? Is it a vector? Is it a scalar? Is the matrix what is it? I will tell you what it is. So, this is a x matrix. It is an average of a bunch of x matrices. 1 x matrix per data point. You take all the data points, find their average matrix. So, that is what this is. So, Let us give this matrix and name this matrix. Let us call this C.

### Timestamp: 14:50

So, essentially, then what we are saying is that equivalently. The problem that we can solve, to achieve our objective is the following, So, we can maximize over such that is 1, , where C is . What we are saying is that finding that line that passes through the origin which best represents the data, in terms minimum reconstruction error is same as finding that that maximizes this quantity with respect to a matrix that you can generate from your data.

This is a x matrix. And some of you might already recognize what this matrix is. We will talk about this matrix a little bit detail later, but this matrix is nothing but the covariance matrix. So, this matrix is called the covariance matrix of the data set. And basically what we

are trying to find is that we want to find a direction which maximizes this bilinear form which is for the covariance matrix.

Again, for those who have done linear algebra course, already, you would immediately recognize that the solution to this problem is is the Eigen vector corresponding to the maximum Eigen value of C, the covariance matrix. Basically, your line which best represents the data in terms of error minimization of reconstruction is same as the line which maximizes the as C is the covariance matrix and this line is given by the Eigen vector corresponding to the maximum

the data in terms of error minimization of reconstruction is same as the line which maximizes
the  as C is the covariance matrix and this line is given by the Eigen vector
corresponding to the maximum
Eigen value of the covariance matrix. We will talk about this covariance matrix in a little bit
more detail a little later. For now, imagine that, well, this is not a hard problem to solve. So,
that is the main takeaway at this point. We will understand this covariance matrix and what
does it mean to say, where did the covariance come into picture while we are doing error
minimization and all that a little later, but for now, assume that well, this problem has a well-
known, well understood solution in terms of the Eigen vectors of a certain matrices
associated with the dataset.

Eigen value of the covariance matrix. We will talk about this covariance matrix in a little bit more detail a little later. For now, imagine that, well, this is not a hard problem to solve. So, that is the main takeaway at this point. We will understand this covariance matrix and what does it mean to say, where did the covariance come into picture while we are doing error minimization and all that a little later, but for now, assume that well, this problem has a wellknown, well understood solution in terms of the Eigen vectors of a certain matrices associated with the dataset.