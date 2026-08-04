# Week-12 - Lecture 3

### Timestamp: 00:00

 So, perceptron I will kind of point out what perceptron does. So, if you remember what

### Timestamp: 00:23

 perceptron was doing perceptron was doing this update rule Wt plus 1 was Wt plus X well

### Timestamp: 00:32

 let us call this the point that we get is Xt Yt at the T at iteration and let us say

### Timestamp: 00:38

 we make a mistake and this is the update that we did right.

### Timestamp: 00:42

 Now, this update rule should remind you of a very I mean this is this looks very close

### Timestamp: 00:49

 to a standard gradient descent based update rule right. So, where you you have a guess

### Timestamp: 00:54

 for the current parameter of interest and then you take a gradient step in the negative

### Timestamp: 00:59

 gradient step right. So, that is a gradient update rule that people typically use.

### Timestamp: 01:04

 Now, if you use a hinge loss right. So, let us think of using a hinge loss as usual well

### Timestamp: 01:11

 hinge loss is something that we discovered from SVMs which is loss of a particular W for

### Timestamp: 01:17

 a given data point X Y is just max of 0 comma 1 minus W transpose X into Y. This is my

### Timestamp: 01:24

 hinge loss remember it looks like this right it looks like this.

### Timestamp: 01:31

 Now, if you look at the let us say hinge L hinge if I take the derivative of L hinge

### Timestamp: 01:41

 or the gradient of L hinge with respect to W or yeah. So, with respect to W or maybe

### Timestamp: 01:51

 this I can just try this as the gradient with respect to W. Now, how would that look

### Timestamp: 01:56

 like well that looks like. So, this is a piecewise linear function right. So, this is this

### Timestamp: 02:04

 is W transpose X into Y and this is the loss this is this is linear till 1 and then it

### Timestamp: 02:11

 is still linear, but then it is a different linear function from 1 onwards. So, if you

### Timestamp: 02:15

 look at the hinge loss is gradient right. So, if W transpose X into Y is strictly less

### Timestamp: 02:22

 than 0 then it is this linear piece whose slope is just W right. So, so whose slope is

### Timestamp: 02:30

 just X into Y which means that minus X into Y. So, because there is a 1 minus W transpose

### Timestamp: 02:36

 X into Y. So, that is what this linear function is. So, in fact, this when this is less

### Timestamp: 02:41

 than 0 the slope would just be minus X into Y that would be your gradient. On the other

### Timestamp: 02:47

 hand if it is greater than strictly greater than 0. So, then this is a constant which means

### Timestamp: 02:56

 that the gradient is going to be simply 0 at that point we do not have to care about

### Timestamp: 03:01

 the gradient there there is no gradient object there. Now, at 0 sorry at when W transpose

### Timestamp: 03:11

 X into Y is at 0 then what happens is the question well this is actually less than 1 for the

### Timestamp: 03:18

 hinge loss, but if you if you can kind of think of this as yeah. So, at so this values

### Timestamp: 03:27

 1 this values 1. So, now if W transpose X into Y exactly is 0 equal to 0 right. So, then

### Timestamp: 03:40

 actually let me make a small change here. So, this is going to be just this function right.

### Timestamp: 03:49

 So, it is going to be minus X Y if W transpose X into Y is less than 0 this is a modified

### Timestamp: 03:54

 version of hinge it is going to be 0 if W transpose X Y is greater than 0 and at W transpose

### Timestamp: 04:01

 X into Y is 0. So, this function is not you know differentiable at this point because

### Timestamp: 04:07

 it is an intersection of 2 piecewise linear functions. So, this we have to look at sub

### Timestamp: 04:12

 gradients at this point and sub gradients at this point can be any value between you know

### Timestamp: 04:18

 the slopes these 2 slopes and these 2 slopes can be you know minus 1 to 0 I can pick any

### Timestamp: 04:26

 value between minus 1 to 0 for example, this is a sub gradient this is a sub gradient

### Timestamp: 04:31

 and so on at this point right. So, sub gradient is a line that kind of completely is below

### Timestamp: 04:35

 this function at that point and there are multiple lines that you can do I mean you can

### Timestamp: 04:40

 take a slope of between minus X into Y till 0 any value is till a sub gradient. So, this

### Timestamp: 04:47

 would be a sub gradient now in our definition of perceptron right. So, now perceptron I

### Timestamp: 04:54

 can if you do a sub gradient descent then you could pick any one sub gradient from this

### Timestamp: 05:00

 set minus 1 comma 0 into x y and what perceptron does it is makes a choice it chooses minus

### Timestamp: 05:09

 X into Y right. So, it chooses the value minus 1 as the sub gradient. So, which means

### Timestamp: 05:14

 that even if W transpose X into Y is 0 this is going to be minus X into Y right. So,

### Timestamp: 05:20

 which means that now what happens is you know when a new point comes in and you observe

### Timestamp: 05:28

 that you do not make a mistake which means that W transpose X into Y is greater than

### Timestamp: 05:33

 0 then you do not do an update which means that you are moving in the gradient direction

### Timestamp: 05:37

 but then the gradient is 0 which means that you are not really making an update. On the

### Timestamp: 05:41

 other hand if you make a mistake which means W transpose X is less than 0 or W transpose

### Timestamp: 05:46

 X equal to 0 then you are assumed to make a mistake right. So, when mistake right so,

### Timestamp: 05:52

 then mistake comma 0 otherwise right. So, then what perceptron does is it the gradient

### Timestamp: 06:01

 is minus X into Y which means that then the gradient update rule would be W T plus 1 is

### Timestamp: 06:07

 W T minus usual gradient update rule would be something like this loss at W T. This would

### Timestamp: 06:14

 be the usual gradient update rule but then for perceptron you know this is minus X T

### Timestamp: 06:23

 Y T now which means that the gradient is minus X into Y which happens when in fact you make

### Timestamp: 06:29

 a mistake this is the mistake case right. But then E T T is said to 1 in case of perceptron

### Timestamp: 06:36

 what I am essentially trying to say is that now having seen this we can interpret perceptron

### Timestamp: 06:50

 as if it is doing it is looking at one point at a time from my data set and doing a gradient

### Timestamp: 06:57

 descent or a sub gradient descent if there is no differentiability at the point that you

### Timestamp: 07:02

 have but it is taking a fixed step size of 1 right. So, this is the step size which is

### Timestamp: 07:09

 fixed to 1 in perceptron's case if I fixed the step size to 1 and if I take the gradient

### Timestamp: 07:15

 and if I imagine my loss as this modified hinge loss where you know you do not have this

### Timestamp: 07:20

 as actually you do not have this 1 minus basically right. So, this is the modified hinge

### Timestamp: 07:25

 let us call this modified hinge which looks like this.

### Timestamp: 07:29

 Now you can interpret perceptron as if it is doing a sub gradient descent on the modified

### Timestamp: 07:36

 hinge loss where I am just taking a gradient step with the constant step size equal to

### Timestamp: 07:43

 1 right. So, this is one way to you know integrate I mean interpret perceptron right.

### Timestamp: 07:50

 So, let me put that down so perceptron can be interpreted as you know well because data points

### Timestamp: 08:07

 comes one at a time you can think of this as a stochastic gradient descent problem where

### Timestamp: 08:11

 instead of taking a gradient with respect to the entire data set you are only taking it with

### Timestamp: 08:15

 respect to 1 data point which can be randomly drawn let us say. So, it is a stochastic gradient

### Timestamp: 08:20

 descent problem and then you are moving in the gradient direction that is dictated by

### Timestamp: 08:24

 this point right. So, with you know this modified hinge loss with step size equal to 1 right.

### Timestamp: 08:43

 So, this is an interpretation right. So, all we are saying is that we are kind of backfitting

### Timestamp: 08:48

 this right. So, we put down perceptron algorithm in a different using a different motivation

### Timestamp: 08:54

 what we are saying is that because SVM's minimize hinge loss. Now you can kind of look at that

### Timestamp: 09:00

 loss and see what perceptron does with respect to that loss and what we can also think of

### Timestamp: 09:05

 perceptron as it is doing trying to minimize the hinge loss, but not the 1 minus w transpose x,

### Timestamp: 09:12

 but then just max of 0 comma minus w transpose x, y, but it is not minimizing the loss as an

### Timestamp: 09:19

 optimization problem over all data points it is taking 1 data point at a time which is equivalent

### Timestamp: 09:24

 to doing a stochastic gradient descent and it is moving in the gradient direction, but then

### Timestamp: 09:31

 it is also doing a constant stochastic right. So, with all these caveats we can treat perceptron

### Timestamp: 09:37

 also as a loss minimization algorithm, but that is just in some sense reverse fitting

### Timestamp: 09:44

 thing right. So, you are kind of force fitting what perceptron does in the framework that you

### Timestamp: 09:48

 are actually trying to think about, but that is a good thing to also know because at the end of

### Timestamp: 09:53

 the day it is doing something with the hinge loss because this update rule x, t, y, t naturally

### Timestamp: 09:59

 you know fits with the hinge loss update right. So, this is minus x, t, y, so that is a w, t plus

### Timestamp: 10:05

 x, t, y, t that perceptron does yeah. So, this is one way to think of this. Now,

### Timestamp: 10:11

 similarly we can also interpret the boosting algorithm as if it is doing some kind of optimization

### Timestamp: 10:19

 on what is called as an exponential loss. Again we want really going to the details of how this

### Timestamp: 10:24

 exactly does here the loss can be thought of as for boosting because we did not prove the

### Timestamp: 10:38

 correctness of boosting in this course it would be hard to you know explain why this motivate

### Timestamp: 10:43

 this loss without proving the correctness. Nevertheless you can we can give some high level

### Timestamp: 10:48

 motivation right. So, boosting can be thought of as the loss of a particular h on a data point x

### Timestamp: 10:53

 come away can be thought of as e power minus y into h of x right. So, this is what is called as

### Timestamp: 11:00

 an exponential loss it looks like the logistic loss it is though it is not the logistic loss

### Timestamp: 11:09

 exponential loss. Now, you can view boosting as if you know you are trying to add a new classifier

### Timestamp: 11:21

 that kind of minimizes this exponential loss in every round right. So, basically it is what is

### Timestamp: 11:28

 called as a coordinate descent algorithm we want really bother about that too much in this course,

### Timestamp: 11:32

 but all I want to say here is that you can also put boosting in this framework with some caveats

### Timestamp: 11:38

 like how we had we kind of force fit perceptron in this framework with some caveats.

### Timestamp: 11:43

 But the more natural thing that to understand and to appreciate is that you know these conclusions

### Timestamp: 11:49

 that we do which is that you know the standard algorithms like you know logistic regression

### Timestamp: 11:55

 SVMs and not really the regression we never use regression for classification, but then logistic

### Timestamp: 12:01

 regression and SVMs can be neatly interpreted as as if you are using a convex surrogate in place

### Timestamp: 12:08

 of the 0 1 plus. So, these are all convex surrogates right. So, I would like to conclude this

### Timestamp: 12:15

 discussion by saying that this is these are all convex surrogates the reason we why we want

### Timestamp: 12:19

 convexities because you know we somehow want a function which has only one minimizer minimum

### Timestamp: 12:25

 and it is easy to find that minimum convex functions have only one minimizer and it is easy to

### Timestamp: 12:31

 find them and so they act as natural surrogates choices for surrogates right. So, and then different

### Timestamp: 12:38

 convex functions can be used and then depending on which convex function you get different algorithms.

### Timestamp: 12:43

 Of course, these are not the only convex surrogates there are several other losses that you can come

### Timestamp: 12:48

 with and people have come with different losses for example, there is something called as a

### Timestamp: 12:51

 Hoobert's loss and so on and so forth which also leads to different types of algorithms right.

### Timestamp: 12:59

 But there is another class of problems where you a class of algorithms where you do not

### Timestamp: 13:06

 you kind of give up on this convexity and you are you are still ok to end up getting a local

### Timestamp: 13:13

 minimum and in practice such algorithms also perform you know comparably well with this

### Timestamp: 13:21

 class of algorithms like SPMs and logistic regressions and these algorithms are called as neural

### Timestamp: 13:27

 networks right. So, which does not have a convex surrogate it is a completely a non convex problem

### Timestamp: 13:34

 but still works well in practice and in fact, it is also inspired by the perceptron algorithm.

### Timestamp: 13:41

 So, in fact and it also has led to major advances in in a subfield of machine learning called

### Timestamp: 13:49

 deep learning which we are not looking at in this course, but future course I mean would cover

### Timestamp: 13:55

 something like that especially if you are in this you know online BSE program.

### Timestamp: 14:03

 So, what we are going to see next is going away from this convex surrogates and briefly discuss

### Timestamp: 14:08

 this idea of neural networks the goal is not to completely cover neural networks because that will

### Timestamp: 14:13

 be covered in a different course like from bottom up, but just to give perspective with respect to

### Timestamp: 14:19

 whatever we have seen so far you talk a bit about neural networks which deal with the NP hardness

### Timestamp: 14:25

 in a slightly different way right. So, which which go away from convexity and what exactly

### Timestamp: 14:32

 are neural networks how do they you know deal with this problem of binary classification is

### Timestamp: 14:38

 something that we will start looking at next. Thank you.