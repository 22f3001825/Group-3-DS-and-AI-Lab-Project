# **Machine Learning Techniques Professor Arun RajKumar Department of Computer Science and Engineering Indian Institute of Technology, Madras Introduction to Binary Classification**

Welcome back everybody, we are around at the midpoint of this course, around 6 weeks are over now. And so far, we have looked at unsupervised learning methods, we have looked at supervised learning, we have started to look at supervised learning, specifically we have looked in detail the problem of regression including linear regression, the non-linear version of it and then several variants including ridge regression and lasso.

(Refer Slide Time: 0:57)

And what we are going to do from now on is look at another important paradigm in machine learning which is also supervised learning paradigm, but then the problem that we are going to look at is much more popular and I mean much more applied. And this is the problem of classification and this also falls under supervised learning as we have seen earlier. So, we will start looking at the problem of classification.

As we saw the classification problem can be posed in two different ways, one is the standard binary classification where you only have two classes or the multi-class classification where you have several classes. So, what we are going to do in this course is look at binary classification because that is the most basic and important form of classification and once we understand binary classification well then we will see how ideas from binary classification can also be used most of the time seamlessly to solve the multi-class classification problem as well.

So, our focus for the next couple of weeks is going to be on binary classification. So, what is the problem of binary classification? You have a data set x1,...,xn which is a bunch of features as usual all xi's are in d dimensional features but in addition because it is supervised learning we know that we will also have labels which is y1 to yn.

And because it is a classification problem as opposed to a regression problem which we have dealt so far. Now, our labels are going to be either you can think of it as 0, 1 or you can think of it as -1, 1. So, essentially you have some features and then you want to box it into two different, two different classes.

So, you can call these class as 0 or 1 or -1 or 1 does not really matter most of the times I mean depending on some mathematical convenience in some algorithms we will think of it as 0, 1, some other, some other algorithms we might think of it as -1, 1. But absolutely it does not matter because it is just a number that we are assigning to these classes.

So, for example your problem could be something like given an email you want to figure out if the email is spam or not in which case your classes are just spam or non-spam and now you can without loss of generality say spam is 0, non-spam is 1 or spam is 1, non-spam is 0 or spam is 1, non-spam is -1, does not really matter. So, the main point is that there are two classes and hence it is called binary classification.

So, what is the goal? The goal now is to do the following like in the regression case we still want to learn some function which maps Rd which is the feature space to let us I mean for this purpose of discussion let me just say 0 to 1. So, you want to learn a function from data which maps a new feature, any given feature to 0 or 1.

Now what is the loss or the error that we are interested in. Remember in the regression problem the error that we were interested in is was the squared error and then we justified it in different ways. So, what might be an error that we might be interested in the classification case?

(Refer Slide Time: 3:59)

This is a common on very intuitive loss or error of a given function which could be as the 𝑛 following. So, loss of h, so this is the loss or error of h, we can think of it as ∑ maybe I will 𝑖=1

do an averaging indicator of h(xi)≠yi, where the indicator function takes some argument z and outputs 1 if z is true and 0 otherwise.

So, which means that basically what we are measuring is what is the fraction of points in the training set that our h gets wrong. So, when it gets it wrong you penalize it by value of 1, if it gets it right you do not penalize it the value is 0, so that is what this indicator is capturing and then we are dividing it by n, so we are basically counting the fraction of errors in our data set.

So, this is a much more reasonable loss function than a square loss simply because what we really care about is whether you are doing it correctly or incorrectly. So, that is the main goal of classification to get as much data points correctly as possible in the test set. So, as a proxy we are going to measure it in the training setup.

Of course, the same issue as regression would come in, so if you let all functions, if you let we are searching in the space of all functions then we will always be able to make this error 0 but then we would, we would have perhaps fit the noise as well which is the same argument we have made for regression.

So, we should not be searching in the space of all functions, we should search in a space of restricted functions. And like linear, like regression where we said that the restricted class is a linear class, we can try to do the same thing for classification as well. So, what we could do is

we can then ask well I restrict my space of functions to just the linear functions and then my goal would be to, my algorithm would be to do the following.

Minimize over h in H linear and I will tell you what H linear in this case means it is slightly

𝑛 different from your usual regression case because of the nature of prediction, ∑ 1(h(xi) ≠yi). 𝑖=1

What is H linear here? What do I mean by H linear?

h linear, by H linear I mean the following. So, H linear is the set of all hypothesis functions or the classifiers h such that h of x, hw let us say it is characterized by some w such that hw(x) is the sign of w<sup>T</sup> x. So, where the sign is just our usual function which says sign of w<sup>T</sup> x or in general sign of any input z is going to be 1 if z ≥ 0 and 0 otherwise.

So, basically you are still linearly combining the features by doing w<sup>T</sup> x and then asking well what is the sign of this quantity. So, you are thresholding it at 0, if your sign ≥ 0 then we are saying that it is the class that we will predict that h will predict is positive otherwise it is negative.

So, in pictures this is going to look like the following. So, you have some w, so this corresponds to this gives rise to a function hw which is going to predict +1 if the for every x such that w<sup>T</sup> x is positive. But where are those x? We know where those x's are so those x's are in here.

So, on the right hand side so to say of our hyper, hyperplane or in this case the line. So, this is the set of all x such that w<sup>T</sup> x ≥ 0. And similarly, you have the set of all, the other side is the set of all x such that w<sup>T</sup> x ≤ 0 which we have seen already, so this is just the set of all x such that w<sup>T</sup> x ≤ 0.

And here is where this h will predict negative and the yellow region is where the h is going to predict positive. Of course, what happens if a point lies on the line it does not really matter because you can either predict positive or negative by but our definition says that we are going to predict it as negative without loss of generality.

In some sense you can, if you want to switch the definition you can do that also, you can think of on the line you want to say positive as opposed to negative does not really matter or you can toss a coin, you can break dice somehow. So because, I mean w<sup>T</sup> x = 0 means it is tied, both the classes are tied and then you can decide it however you want.

(Refer Slide Time: 9:32)

So, now the question comes how do we solve this problem? Remember again, in the, going back to the regression case what we did was we said that we are going to find that w which minimizes our squared loss and then we started taking the derivative and then setting it to 0 and all those things we did.

Now, the question is, now we have changed the loss, it is no longer the square loss, it is the, it is what is called as a 0-1 loss let me give this loss a name this loss is called the 0-1 loss because it takes, it gives a loss of either 0 or 1 depending on whether h correctly predicts x or not with respect to the y in the training set.

Now, how do we minimize this? Unfortunately, this problem is an NP-hard problem in general, in general. What do I mean by in general? In general, for a general data set so we will see cases where this is easy to solve but then in general if I give you a data set xi, yi and ask you to find that test line which suffers the minimum loss with respect to this data it is hard to solve, so it is an NP-hard problem, we do not know if there is an efficient algorithm to find such a w at all.

So, while in the regression case it was very easy, we could just take the gradient, set it to 0 and solve the problem, here it is not so easy. So, that is because of the nature of the loss itself, regression was giving like a continuous loss function. So, depending on how much you are away from the label yi which is a real number there your loss kind of takes any possible value from 0 to infinity.

Here the loss can take only two values, discrete values, so either 0 or 1 and this nature of, this discrete nature of this loss makes this loss function itself non differentiable and non-continuous and so we suffer this problem. So, this becomes like in some sense a discrete search problem and so it becomes NP-hard in general.

So, we cannot solve this problem, so we have to give up on this. So, we have to look for, though this is what we want to do we have to look for alternate ways to solve the binary classification problem. So, how can we solve that? The first thing that immediately comes to our mind is well we already know how to solve the regression problem.

So, in regression the labels could take any real value, here the labels are constrained to take 0 or 1 so it appears so that we have solved a more broader problem in the regression case, why cannot we simply use that idea to solve this problem. So, that is the question we are going to ask next and see if that will be of any use at all.

So, can we use let us say linear regression to solve classification problems. By which what do I mean? I mean the following, so you are given a data set (x1, y1),...,(xn, yn), you input the data set to a linear regression model and what you get is a w, so in the standard linear regression this is equivalent to the maximum likelihood and all that, we know that.

So, let us say you get some w in Rd and now you use the w to get hw by thresholding w at w<sup>T</sup> x = 0, hw is from Rd to 0-1. Is this a good idea that is the question we are asking? So, now of course this is not solving the 0-1 loss, this is solving a square loss, so for now let us think of

this as a vanilla version where we do not have regularization, adding regularization would not change our argument so much.

But let us say for the moment we assume that this is a non-regularized linear regression, the standard version, where you are just minimizing for the square loss. So, what is going to happen here? So, that is the question we are asking. You could do this but there is a problem.

Now, just to illustrate this problem let us take this data set. So, here is a data set which has bunch of let us say positive labels which I am calling as, which I am marking using the red dots and let us say we have a point, some points here which are green dots, which are negative labels, so all the labels y, yi = - 1 here and yi = +1 for these points, these are two dimensional data.

Now, if you solve the regression problem let us say you get some w which looks like this, now what does that mean, that means that well this is the hw that you are going to get and anybody on the right hand side is going to be positive, anybody on the left hand side is going to be negative, it looks good. So, this is an in fact a good way to separate the positives from the negatives and your regression might give you this.

Now, let us say I add a bunch of extra points. So, I add maybe a bunch of points here. So, now the moment I add these points in terms of classification these points are not, should not really bother our line here that we have found out, because these points are still on the correct side of the line so if you had run an algorithm, a classification algorithm it might still get you the same line, so which separates the positives from the negatives.

But now regression is going to not just minimize the 0-1 loss, but then it is trying to minimize the average deviation between w<sup>T</sup> x and the corresponding y, the y for all of these are going to be +1 but then if I use this w, the w<sup>T</sup> x is going to be large. So, it is going to be positive but then regression does not just look at the sign, it is going to look at the exact value and these guys will have a large w<sup>T</sup> x and so w<sup>T</sup> x - the label 1 square will be large for these.

And so to balance this, to minimize the loss function what it is going to do it is kind of going to tilt my w, so maybe the w that I will get will get slightly tilted and it might become something like this. So, my w might tilt in this direction or maybe I will use a different color or I will use a dotted version of the w, maybe my w will tilt in this direction and then I might get some line like this. So, now let us say if you had some points here as well.

So, now what is happening is that your w gets tilted back and forth just because there are these points which are far apart from the line, from the line, from the separator. So, now for a classification point of view it does not really matter if my point is far apart from the line as long as it is on the correct side of the line.

So, but from a regression point of view you are trying to minimize the average prediction minus the label square. So, the label you are going to think of it as some real number it so happens in this data regression will think that it so happens in this data the labels the real numbers are happened to be +1 or -1 and so it will try to match +1 or -1 as much as possible and so it will try to shift the predictor itself.

And that is a bad thing, that might lead us to some line which might actually make errors on the data set while you can actually find a line which makes no errors in this case in terms of the 0-1 loss. But whereas the line that minimizes the squared loss may end up making some errors.

In other words, the main point is that your least squares or the regression problem. So, conclusion that we draw from this is that regression is sensitive to the location of the data points and not just, I am loosely writing, not just the “side” of on which the data points lie with respect to the separator.

So, by side I mean that the w<sup>T</sup> x, the sign (w<sup>T</sup> x) is what should matter whereas it is actually looking at the value of w<sup>T</sup> x, so that is the problem with regression. So, it is not a great idea to directly take regression and apply to classification and hope that it will give you good results in the test set.

So, now how do we solve this? So, then it so we are stuck, seems like we are stuck because we put down loss function which is the most natural loss function for classification, we said that the original problem is NP-hard to solve, we cannot use regression also, so we need to come up with alternate algorithms.

And one of the main reasons why we have so many algorithms for binary classification that we will see throughout this course is simply because of the fact that this problem, original problem that we want to solve is actually hard. So, you somehow have to get around this hardness in different ways by making different assumptions and that will lead us to different different algorithms, so that is the main idea why you have so many classification algorithms,

whereas you have like a very standard regression algorithm which is the least squares regression.

So, what we are going to do in the next couple of classes, the next couple of lectures is going to look at a lot of classification algorithms. But just to warm up we will start with the simplest possible classification algorithms and then we will make it slightly more complicated not just for the sake of making it complicated but because it will become more and more principled as we go along in this course. But for now what we want to do is start with the simplest possible classification algorithm.

So, here is a question for you, so pause and think, forgetting all that we have discussed so far if you had to do a classification problem, solve a classification problem, you have a data set, you are given a new data point. What is the simplest way that you will use to make a prediction of +1 or -1 or 0 or 1 for this new data point that I give you. Think about this and then we will come and I mean we will start discussing this problem now.