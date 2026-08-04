# Week-12 - Lecture 1

(Refer Slide Time: 00:00) Hello and welcome back. So, far we have looked at several algorithms for binary classification,

(Refer Slide Time: 00:20) specifically supervised learning problems. We have I mean under supervised learning we

(Refer Slide Time: 00:25) have looked at regression and then specifically binary classification and for binary classification

(Refer Slide Time: 00:29) we have looked at several algorithms which includes let us say logistic regression,

(Refer Slide Time: 00:34) support vector machines boosting as a non-sample method which we saw recently and even per

(Refer Slide Time: 00:40) sub-tron and things like that. Of course, we have also seen other methods like you know decision

(Refer Slide Time: 00:45) trees, canary, rest neighbors and so on. So, what we are going to ask and answer today at a

(Refer Slide Time: 00:51) high level is why are there so many methods right. So, for instance when we spoke about the

(Refer Slide Time: 00:57) problem of regression, we just came up with the single method which was linear regression and

(Refer Slide Time: 01:03) then we looked at a regularized version of linear regression. There were different types of regularization

(Refer Slide Time: 01:09) that we could do that led us to different algorithms like RIDG and LASO. But then the underlying

(Refer Slide Time: 01:14) algorithm was still a variant of regression only. So, where we use the squared loss and we try to

(Refer Slide Time: 01:21) minimize it plus a regular reset. Whereas, the case of classification we seem to have all these

(Refer Slide Time: 01:27) different algorithms and how do we understand all of these algorithms in a single unified framework

(Refer Slide Time: 01:33) right. So, and why are there so many different algorithms right. So, this is what we are going to

(Refer Slide Time: 01:38) kind of explore in today's lecture. So, what do we really want to do in a classification problem

(Refer Slide Time: 01:46) right. So, if you think about that we want. So, we are given a dataset as usual x1y1

(Refer Slide Time: 01:58) dot dot dot xn yn x i's are in RIDG. Now, y i's are in let us say plus 1 minus 1 and if you

(Refer Slide Time: 02:12) remember our goal was to learn some H which will map RD to plus or minus 1. Now, how do we measure

(Refer Slide Time: 02:23) the performance of H? Well, what is the most intuitive way to measure performance in a classification

(Refer Slide Time: 02:29) problem? Well, what I can do is I can look at performance measure which is the error performance

(Refer Slide Time: 02:38) measure. I can measure the performance of a particular H as by looking at sum over i equals

(Refer Slide Time: 02:48) 1 to n indicator of H of x i not equals y i right. So, what does this indicator mean? Well,

(Refer Slide Time: 02:58) this indicator means that indicator of sum z this is a function which takes a value 1 if z is true

(Refer Slide Time: 03:07) we have seen this before and 0 otherwise. This just then comes the number of mistakes that H

(Refer Slide Time: 03:13) is making on the training set. So, of course, we know that we cannot let all possible H's

(Refer Slide Time: 03:21) learn from all possible H's because then this we can always find a H that has 0 training error

(Refer Slide Time: 03:26) but then it would have ended up minimizing sorry, it could have ended up memorizing from data

(Refer Slide Time: 03:31) but not really learn from data. So, what we typically do then is we assume that H comes from some

(Refer Slide Time: 03:37) class of functions and then we only look at which H minimizes this in this class right. So,

(Refer Slide Time: 03:43) we have seen this before as well. So, we kind of now look at minimization of H belongs to let us

(Refer Slide Time: 03:48) say H linear which is the most natural class of functions you might want to minimize the error

(Refer Slide Time: 03:56) indicator of H of x i not equals y. Well, what does H linear mean? H linear means that you know

(Refer Slide Time: 04:04) that is sum w such that H of x is w transpose x or w transpose x plus some constant c which means

(Refer Slide Time: 04:13) that this is equivalent to minimize over w in r t sum over i equals 1 to n indicator of well I can

(Refer Slide Time: 04:21) also add bias term which is w transpose x plus p x i plus p indicator of sin of w transpose

(Refer Slide Time: 04:33) x i plus p not equals y. So, my H is now the sin of w transpose x i plus b

(Refer Slide Time: 04:41) well now I want to learn the best w and b such that this is mean so far in all the algorithms

(Refer Slide Time: 04:47) that we have seen we have only used w we have not explicitly stated the b learning the b

(Refer Slide Time: 04:52) but then it is very simple right. So, all the algorithms that we have seen you can easily

(Refer Slide Time: 04:56) extend it to the case where you have b as well that does not really change what we are trying to do

(Refer Slide Time: 05:01) here so much it just says that you know your your line does not necessarily pass through origin

(Refer Slide Time: 05:07) but then it can be anywhere which is more natural to ask for one way to think about

(Refer Slide Time: 05:14) you know how to get this in a general form is let us say you have an x in r d now you can kind of

(Refer Slide Time: 05:24) make a new feature new dataset where you have x also under extra 1 which is added as you know

(Refer Slide Time: 05:33) padded as a feature now this becomes this is a vector in r d plus 1 let us say this is my new

(Refer Slide Time: 05:39) dataset now if I just learn a w line that passes through the origin right. So, now that w would have

(Refer Slide Time: 05:46) w 1 till w d and then w d plus 1 because now the data points are in d plus 1 dimension now I will

(Refer Slide Time: 05:54) have a d plus 1 dimension w and then now let us call this x dash right. So, this is w dash which

(Refer Slide Time: 06:03) can be thought of as w and this w d plus 1 which I am let us say calling as b right. So, now w dash

(Refer Slide Time: 06:10) transpose x dash which is you know just the simple dot product in one extra dimension is equivalent

(Refer Slide Time: 06:18) to w transpose x plus b because this guy is always 1 and the last value is this what I am

(Refer Slide Time: 06:25) calling as this bias right. So, which means that you know you do not lose anything by saying that

(Refer Slide Time: 06:30) you know you are just learning a w just that you can change your dataset by adding this one extra

(Refer Slide Time: 06:35) feature and then we can you know for instance we can without loss of generality think of this as

(Refer Slide Time: 06:41) our problem also of course, now d is this padded dimension right. So, you also have this extra dimension

(Refer Slide Time: 06:47) and that is what we are going to call as t anyway. So, that is not the main point I am trying to say

(Refer Slide Time: 06:51) here the main point I am trying to say here is that well this is what this is how we are going to

(Refer Slide Time: 06:55) measure performance of a w and then we want to find this best w that minimizes this error in our

(Refer Slide Time: 07:00) training set and we said before that this is a hard problem right. So, this is what is called as an

(Refer Slide Time: 07:06) NP hard problem which you know intuitively means that we do not expect to have a polynomial time

(Refer Slide Time: 07:14) algorithm which will solve this of course, if you assume that the dataset is linearly separable

(Refer Slide Time: 07:20) then we know that this can be solved using perceptron, support vector machine and so on and so forth.

(Refer Slide Time: 07:25) But if the dataset is not linearly separable then finding the best w that minimizes the

(Refer Slide Time: 07:31) accurate error in this way that I have written is an NP hard problem. Now,

(Refer Slide Time: 07:36) this is the fundamental reason why we do not have a single algorithm for binary classification

(Refer Slide Time: 07:42) because we do not know how to solve this problem right. So, it is not expected to I mean we do not

(Refer Slide Time: 07:48) expect to have a solution to this problem which runs in polynomial time. So, we need to deal with

(Refer Slide Time: 07:55) this somehow right. So, one line of thought would say that you make assumptions about the data

(Refer Slide Time: 08:01) and then deal with it somehow which is what our generative models for example, do and once you

(Refer Slide Time: 08:08) make those assumptions maybe you can get the best w and so on or even in perceptron's case we make

(Refer Slide Time: 08:14) the assumption that linear separability with gamma margin is how our dataset is generated under

(Refer Slide Time: 08:20) that assumption this problem is still easy to solve. But a general problem it is NP hard to solve.

(Refer Slide Time: 08:26) So, how do we deal with this right. So, now the way different algorithms are dealing with it will

(Refer Slide Time: 08:33) become apparent if we take what is called as a loss function view.

(Refer Slide Time: 08:43) What is this loss function view? Well, this is the loss function view right. So, now how much loss

(Refer Slide Time: 08:53) does a single point suffer single x comma y in the training set suffer with respect to an underlying

(Refer Slide Time: 09:02) h right. So, for example, the so let us say we have an x comma y and then we have an h which is

(Refer Slide Time: 09:11) R d 2 plus or minus 1. Now, how much loss does this point suffer with respect to this h? Well,

(Refer Slide Time: 09:21) it suffers a loss of either 0 or a loss of 1 depending on whether h correctly predicts x or not

(Refer Slide Time: 09:28) right. So, x is again in R d y is in plus or minus 1. So, depending on whether h of x equals y or

(Refer Slide Time: 09:36) h of x not equals y we say that the loss for this particular data point is either 1 or 0.

(Refer Slide Time: 09:43) Now, one other way to say this is right. So, this is indicator of h of x not equal to y right.

(Refer Slide Time: 09:50) So, this takes either value 0 or 1. Now, this is same as saying indicator of h of x

(Refer Slide Time: 10:00) into y right is less than 0 right. So, or in the case well h can now I can even say if it is

(Refer Slide Time: 10:13) linear function I can even say w transpose x into y is less than 0 right. Now, what does this

(Refer Slide Time: 10:21) mean? This means that why is this true right. My h is now I am assuming my h is sign of w transpose

(Refer Slide Time: 10:28) x h of x is sign of w transpose x and now I can either define my loss for a single data point as

(Refer Slide Time: 10:37) indicator of h of x not equal to y or equivalently I can say that it is same as indicator of w

(Refer Slide Time: 10:43) transpose x into y is less than 0. Why why are these two things same? Well, if w transpose x

(Refer Slide Time: 10:50) is positive and y is also positive plus 1 right. So, if this is greater than 0 and if this is

(Refer Slide Time: 10:58) plus 1 then the product is positive which means that this indicator will evaluate to 0.

(Refer Slide Time: 11:04) But why is the what does it mean to say that the product is positive that is I mean if this is

(Refer Slide Time: 11:08) greater than 0 and this is plus 1 which means that the sign if I look at the sign to make a prediction

(Refer Slide Time: 11:13) because this is greater than 0 I am going to predict plus 1 and y is also plus 1 right. So,

(Refer Slide Time: 11:18) so I will not make a mistake on this data point. On the other hand if the other way this can

(Refer Slide Time: 11:24) become positive is if this is less than 0 and y is minus 1. In which case because this is less

(Refer Slide Time: 11:31) than 0 the sign of this is I am going to predict it as you know minus 1 and the label is also

(Refer Slide Time: 11:38) minus 1. So, even in that case I do not make a mistake which means that the product in that case

(Refer Slide Time: 11:44) is also positive. On the other hand if the product is negative that means that you know either

(Refer Slide Time: 11:49) w transpose x is greater than 0 but then I have a minus 1 in the y or w transpose x is less than 0

(Refer Slide Time: 11:57) or and I have a plus 1 for the y. These are the cases when w transpose x is sign does not match

(Refer Slide Time: 12:02) with y sign and so we have a mismatch here which will lead to my which will lead to a loss

(Refer Slide Time: 12:10) a loss of 1. So, which means that I can plot this and see how this looks like right. So,

(Refer Slide Time: 12:15) if I plot this as a function of let us say w transpose x into y or let us say I am going to call

(Refer Slide Time: 12:27) this some g of x into y where my h of x is just sign of g of x. Typically if you are learning from

(Refer Slide Time: 12:39) linear functions your g of x is going to be a linear model. Let us say you are learning a

(Refer Slide Time: 12:44) quadratic function g of x could be a quadratic model no matter what it is I am going to take

(Refer Slide Time: 12:48) sign of it and then I am that is what I am going to make a prediction with. But then the sign of

(Refer Slide Time: 12:52) what right. So, the g of x is going to determine whether I suffer a loss or not which means that

(Refer Slide Time: 12:58) if I plot my loss as a function of g of x into y well how is it going to look like well if the

(Refer Slide Time: 13:07) product is positive then I do not suffer any loss. If the product is negative then I suffer a

(Refer Slide Time: 13:13) loss which means that whenever the product is negative I suffer a loss of 1 and if the product

(Refer Slide Time: 13:20) is positive I do not suffer a loss or if it is 0 then let us say we can decide that we do not

(Refer Slide Time: 13:25) suffer any loss. So, now this is the loss of a single point right. So, this is loss let me

(Refer Slide Time: 13:35) make it is clear. So, this is loss of h on the point x come away right where h is defined as sign

(Refer Slide Time: 13:42) of g of x for some function g which can be a linear function which can be a quadratic function

(Refer Slide Time: 13:46) depending on what function we are trying to learn right. So, now let us look at this loss. Now,

(Refer Slide Time: 13:52) what what do we do this is the loss for a single point and then our actual loss that we are trying

(Refer Slide Time: 13:56) to minimize is the sum of the single points loss over all the points in the training data right.

(Refer Slide Time: 14:03) So, sum over i equals 1 to n indicator of g of x i into y i is less than 0 right. So,

(Refer Slide Time: 14:13) this is what we are trying to find the best g right. So, g is linear we are trying to find the best

(Refer Slide Time: 14:18) w g is quadratic we are just find trying to find the best quadratic fit for the data that minimizes

(Refer Slide Time: 14:25) this loss. So, because this is a sum we can just look at the individual loss right. So, for individual

(Refer Slide Time: 14:32) data points and see and already see where the problem lies right. So, why is there an NP hardness?

(Refer Slide Time: 14:38) The reason why it is NP hard is because right. So, of the nature of this loss function right. So,

(Refer Slide Time: 14:46) this loss function kind of abruptly jumps when when you when when this quantity g of x into y

(Refer Slide Time: 14:52) becomes less than 0 right. So, it suddenly jumps from 0 to 1 right. So, it is it is discontinuous

(Refer Slide Time: 14:58) that is the first thing and this is not convex right. So, if this was convex then you know this

(Refer Slide Time: 15:06) function would if this was convex this is not, but if this was convex then you can when you

(Refer Slide Time: 15:11) sum it up over n different data points it would be a sum of n convex functions and sum of convex

(Refer Slide Time: 15:16) functions is known to be convex and convex functions are easy to minimize right. So, we will be

(Refer Slide Time: 15:23) able to find the best possible solution in polynomial time. Whereas, here that is not the case right.

(Refer Slide Time: 15:29) So, here the problem is this is not a convex function and so, this is an NP hard problem in general

(Refer Slide Time: 15:35) and so we have to somehow deal with this NP hardness and different algorithms deals with it

(Refer Slide Time: 15:40) differently. Now, let us see how each of these algorithms actually deals with it and that will

(Refer Slide Time: 15:45) kind of give us very good insight about this whole picture from a loss functions point of you.

(Refer Slide Time: 15:51) So, let us understand the let us start with an algorithm which is a bad algorithm, but nevertheless

(Refer Slide Time: 15:57) can be put in this framework the algorithm is as follows right. So, the algorithm is you know using

(Refer Slide Time: 16:04) algorithm one let me call this algorithm one you know using regression for classification.

(Refer Slide Time: 16:15) So, what does use regression for classification mean well that there the loss of you know some

(Refer Slide Time: 16:28) function with respect to some function g with respect to data point or let me say yes with respect

(Refer Slide Time: 16:36) to data point x comma y is going to look like what well it is going to look like

(Refer Slide Time: 16:42) some over well for a single data point it is going to look like g of x minus y square this g

(Refer Slide Time: 16:51) could be w transpose x if it is linear regression this is just w transpose x right. So, this is how

(Refer Slide Time: 16:56) we define the loss to find a good function g or find a good w right. So, and now once you have

(Refer Slide Time: 17:04) defined the loss for a single point then you add it up over all points and find the best possible g

(Refer Slide Time: 17:09) right. So, now, but the problem is in a general linear regression problem this y can be any

(Refer Slide Time: 17:16) real values, but then here y is just you know plus or minus 1 right. So, and that is why we said that

(Refer Slide Time: 17:21) this is a bad idea to use regression to solve the classification problem of course, our h remember

(Refer Slide Time: 17:27) our h is finally going to be h of x is going to be sign of g of x right. So, that is always the case

(Refer Slide Time: 17:35) right. So, this this is the final classifier, but then to find the g we are going to use a linear

(Refer Slide Time: 17:40) regression problem we know that this can be solved you know efficiently in polynomial time.

(Refer Slide Time: 17:45) If it is linear regression it is just matrix operations will give you the answer.

(Refer Slide Time: 17:49) And now, once you get that w from linear regression then you will use sign of w transpose x to make

(Refer Slide Time: 17:54) a prediction right. So, now how do we think of this in the previous picture that we have put down.

(Refer Slide Time: 18:02) So, we can see that this is exactly equivalent to so, let us see g of x into y minus 1

(Refer Slide Time: 18:13) square. I claim that these two things are the same and we will see why writing it in this form

(Refer Slide Time: 18:17) is a good idea right. So, now, y remember can take only values plus 1 or minus 1 right.

(Refer Slide Time: 18:23) So, if I expand this guy out so, this is just g of x square plus y square minus 2 g of x

(Refer Slide Time: 18:31) into y right. So, now this is g of x square as usual y square is always going to be 1 because

(Refer Slide Time: 18:43) y is just plus or minus 1. So, this is 1 so, this is minus 2 g of x into y. Now, let us look at

(Refer Slide Time: 18:50) this quantity now this quantity is equal to g of x into y square plus 1 square which is 1

(Refer Slide Time: 18:58) minus 2 g of x into y. But then again g of x into y square is g of x square into y square

(Refer Slide Time: 19:05) which is just g of x square plus 1 minus 2 g of x into y. This is 2 this is 1 right.

(Refer Slide Time: 19:16) 1 and 2 1 equals 2 which means that I can either view the laws when y is plus or minus 1 not in

(Refer Slide Time: 19:23) general with when y is plus or minus 1 which is the problem that we have g of x minus y square

(Refer Slide Time: 19:29) is same as g of x into y minus 1 square. Now, this means that let us go back to our picture and

(Refer Slide Time: 19:36) see what this means this means the following right. So, we had this picture earlier where we had

(Refer Slide Time: 19:46) the 0 1 laws which is right. So, the blue is what is called as the 0 1 laws it takes a value

(Refer Slide Time: 19:52) either 0 or 1 where the x axis is g of x into y and the y axis is you know laws.

(Refer Slide Time: 20:03) Now, we are seeing the regression problem right. So, if you solve the regression problem

(Refer Slide Time: 20:09) it means that you are inherently using the following laws what laws are we using we are using

(Refer Slide Time: 20:15) the following laws that g of x into y minus 1 square which means as a function of g of x into y

(Refer Slide Time: 20:23) right. So, that is the variable if you can just think of g of x into y as the variable that is what

(Refer Slide Time: 20:27) our x axis is. Now, minus 1 square which means that there is a 1 somewhere here and now that laws

(Refer Slide Time: 20:33) is going to look like the following right. So, it is going to go like this right. So, this is

(Refer Slide Time: 20:48) just a function g of x into y minus 1 square that is the regression laws or what is usually called

(Refer Slide Time: 21:00) as the square laws. Now, what is this telling us what is this picture telling us this picture is

(Refer Slide Time: 21:09) telling us that we originally wanted to measure goodness of a particular h which comes via g

(Refer Slide Time: 21:19) for a single data point using the dark blue laws. On the other hand if you use a regression

(Refer Slide Time: 21:25) problem to solve classification then you are pretending that well the dark blue is equivalent to

(Refer Slide Time: 21:32) the light blue which is the regression laws. Instead of minimizing the dark blue laws which

(Refer Slide Time: 21:38) is n p hard in general we are using the surrogate laws which is the light blue laws which is the

(Refer Slide Time: 21:44) regression laws. Now, then as you can see right. So, this the dark blue and the light blue are

(Refer Slide Time: 21:51) widely different right. So, so why is this widely different why because you know the white blue laws

(Refer Slide Time: 22:00) right. So, even if my g of x into y is correctly predicting the sign of g of x into y even if it

(Refer Slide Time: 22:07) is correct with respect to what the label true label is right. So, which means that when if this

(Refer Slide Time: 22:13) value is positive then that means that the sign of g of x h of x which is what the classifier would

(Refer Slide Time: 22:19) actually correctly predict for y still that point would suffer a increasingly large laws if the

(Refer Slide Time: 22:25) value g of x into y is large right. Because this is a regression problem right. So, you are just

(Refer Slide Time: 22:31) trying to minimize g of x minus y squared and y is plus 1 or minus 1 if g of x is large but then

(Refer Slide Time: 22:39) even if it is positive the difference squared is what is contributing right. This point is

(Refer Slide Time: 22:44) contributing so much to the laws and this difference can be positive even if the sign of g of x

(Refer Slide Time: 22:52) is matching y. So, which means that you know in this region right. So, as you move in this direction

(Refer Slide Time: 23:00) this is going to make larger errors even for points where h of x would actually correctly

(Refer Slide Time: 23:06) predict with respect to the dark blue 0 1 laws and that is why this is a bad idea right.

(Refer Slide Time: 23:12) So, especially when you have outliers that means that the outlier is going to be somewhere here

(Refer Slide Time: 23:15) maybe you are predicting it correctly I mean h of x will predict it correctly but then your g

(Refer Slide Time: 23:21) which you are trying to learn would give a large loss to it and so it is a bad algorithm in general

(Refer Slide Time: 23:27) right. So, so this is a bad loss right. So, basically what I am saying is that the light blue curve

(Refer Slide Time: 23:33) is a bad way to approximate the dark blue curve. So, we need a better ways to do this.

(Refer Slide Time: 23:39) Let us see if there are better ways to do this.