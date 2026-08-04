# Week-12 - Lecture 2

### Timestamp: 00:00

 So, so this is a bad loss right. So, basically what I am saying is that the light blue curve

### Timestamp: 00:19

 is a bad way to approximate the dark blue curve. So, we need a better ways to do this.

### Timestamp: 00:25

 Let us see if there are better ways to do this. So, for towards that let us start maybe

### Timestamp: 00:33

 examining the support vector machine algorithm. So, if you remember the support vector machine

### Timestamp: 00:48

 algorithms formulation the soft margin support vector algorithms formulation it was minimize

### Timestamp: 00:54

 over w and psi half norm w squared which is you know proxy for the margin plus sum over i c times

### Timestamp: 01:06

 sum over i equals 1 to n psi i such that w transpose x i into y i plus psi i is rather

### Timestamp: 01:21

 greater than or equal to 1 and psi i is greater than or equal to 0. This was the formulation

### Timestamp: 01:28

 we came up with this formulation after detailed discussion about support vector machines.

### Timestamp: 01:34

 Now one way to rewrite this formulation would be as follows because we want to understand

### Timestamp: 01:39

 this from a loss functions point of view. I can rewrite this as equivalently you know minimize

### Timestamp: 01:49

 over w and psi I am not doing major modifications here I am going to bring it in some standard

### Timestamp: 01:57

 form. I want to understand of this psi i better right. So, psi i is greater than or equal

### Timestamp: 02:02

 to 1 minus w transpose x i y i and psi i is greater than or equal to 0. Now, which means

### Timestamp: 02:11

 that if I put these two things together then it means psi i is greater than or equal

### Timestamp: 02:16

 to 0 psi or epsilon i. So, epsilon i is greater than or equal to 0 epsilon i remember is the

### Timestamp: 02:22

 bribe that the data point i pays or the slack variable to get to the right side of the line

### Timestamp: 02:27

 right. So, that should be greater than or equal to 0 and it should be greater than or equal

### Timestamp: 02:32

 to 1 minus w transpose x i y i which means that it should be greater than or equal to the

### Timestamp: 02:37

 maximum of 0 comma 1 minus w transpose x i y i right. So, so equivalently I can write

### Timestamp: 02:46

 this as you know half norm w square plus c times sum over i is 1 to n psi i where psi

### Timestamp: 02:52

 i is greater than or equal to this. Now, this is equivalently I can write this as equivalently

### Timestamp: 03:01

 minimize over w half norm w square right. So, remember the bribe that you can that you will pay

### Timestamp: 03:10

 is either 0 if the w actually correctly classifies your x i with margin 1 or you will exactly pay 1

### Timestamp: 03:19

 minus w transpose x i y you would not pay extra unnecessary by right. So, which means that this

### Timestamp: 03:24

 can be written as c times sum over i equals 1 to n well psi i is at optimality psi i is

### Timestamp: 03:31

 going to be like exactly the maximum of 0 and 1 minus w transpose x i y i which means

### Timestamp: 03:38

 that I can directly write this as max over 0 comma 1 minus w transpose x i y i right.

### Timestamp: 03:48

 So, this is an equivalent formulation where I am just trying to find the w in r d such

### Timestamp: 03:53

 that you know you have some term here which which the motivation for this was maximizing the

### Timestamp: 03:59

 margin plus some other term here. Now, remember this term depends on data right. So, data dependent

### Timestamp: 04:07

 term why because the x i and y i appears only in this picture here whereas, this is model dependent

### Timestamp: 04:14

 right. So, this depends only on w that we are trying to learn. Now, we can now view this as

### Timestamp: 04:21

 if this guy is a regularizer if you remember from ridge iteration we had a loss function which is a

### Timestamp: 04:30

 squared loss and then we added half norm w squared as a regularizer. Now, this half norm w squared

### Timestamp: 04:36

 serves the same purpose right. So, there it was a lambda by 2 norm w squared but then that lambda

### Timestamp: 04:43

 say factor is got using the c somehow we were trying to balance two terms using a lambda here

### Timestamp: 04:48

 that balancing happens on the other side but that does not really matter you can bring it this side

### Timestamp: 04:52

 as well right. So, so now this half norm w squared is the regularizer now this data dependent term

### Timestamp: 04:59

 is the loss right. So, this is the loss how much loss that a particular w suffers on my data set.

### Timestamp: 05:06

 Now, in our notation right. So, this w transpose x i is what we are calling as g of x i right. So,

### Timestamp: 05:12

 this is in general this could be any g if it is linear then this is w transpose x which means

### Timestamp: 05:18

 that what is exactly the loss that we are learning well now let us go back and see how this loss

### Timestamp: 05:25

 fits into our picture of original picture. Now, remember this is the picture that we had where we had

### Timestamp: 05:34

 this 0 1 loss 0 1 loss we also had squared loss which was g of x minus 1 squared this this guy is

### Timestamp: 05:53

 g of x into y this is my loss. Now, I want to understand the SVM's loss SVM's loss looks like

### Timestamp: 06:03

 the following max of 0 comma 1 minus g of x into y. So, this is the loss per data point now that

### Timestamp: 06:14

 loss is summed up over n different data points right. So, for a single data point it is max of 0

### Timestamp: 06:19

 comma 1 minus w transpose x into y which is g of x into y right. So, remember the most important

### Timestamp: 06:25

 thing is that this loss depends on the product right. So, of whose that once you learn the w using

### Timestamp: 06:31

 this product then you will find the sign of this to make a prediction. So, now how does this picture

### Timestamp: 06:38

 look like right. So, as a function of g of x into y if you think of this as a variable now max of

### Timestamp: 06:44

 0 comma 1 minus that variable let us call that z right. So, this was z so this is just max of 0 comma

### Timestamp: 06:49

 1 minus z. So, how does that picture look like here well one is somewhere here this is 1 this is

### Timestamp: 06:59

 where this guy becomes 0 square loss becomes 0. So, this is 1 so this is where 0 1 loss takes value.

### Timestamp: 07:06

 Now, if my g of x into y is greater than 1 now what would happen well 1 minus g of x into y will

### Timestamp: 07:14

 become less than 0 because g of x into y is greater than 1. So, that will be a negative value.

### Timestamp: 07:20

 So, the max of 0 comma negative value will be 0 which means that if it is anything greater than 1

### Timestamp: 07:26

 is going to get a 0 value right. So, there is no loss. On the other hand if g of x into y is less

### Timestamp: 07:34

 than 1 that is we make a prediction with margin less than 1 this Vms interpretation. Then we suffer

### Timestamp: 07:41

 a loss which is max of it will never going to be 0 because if g of x into y is less than 1. So,

### Timestamp: 07:48

 1 minus this is always going to be positive. So, you are always going to suffer a positive loss.

### Timestamp: 07:53

 So, it is not going to be 0. So, 1 minus z is just a linear function right. So,

### Timestamp: 08:00

 it is going to look something like this especially when 0 x into y is 0 this value will be 1.

### Timestamp: 08:06

 So, which means that at 0 this will be 1 and then at 1 this will be 0 and this will be a linear

### Timestamp: 08:12

 function right. So, this is a line maybe I should draw this carefully. So, this is a line

### Timestamp: 08:24

 and at 1 it becomes 0 and then it continues to say 0. Now, as you can see even if g of x into y

### Timestamp: 08:32

 is a large positive quantity the loss that I get is still 0 whereas, in squared loss it kind of

### Timestamp: 08:38

 started increasing because because we are essentially that is tuned for a regression problem whereas,

### Timestamp: 08:43

 this loss is tuned for a classification problem. On the other hand it is still not the same as the

### Timestamp: 08:49

 0 1 loss of course, it cannot be the same as 0 1 loss. Now, what you can think of is right. So,

### Timestamp: 08:55

 the nice property of the orange line which is the SVM's loss is that it is in some sense the best

### Timestamp: 09:04

 convex approximation of the 0 1 loss you can think of it that way right. So, this orange line is

### Timestamp: 09:10

 convex function of g of x into y. The blue line is the light blue line is also a convex function,

### Timestamp: 09:16

 but then it is not a great approximation for the dark blue line. On the other hand the

### Timestamp: 09:21

 orange line is a convex function which is why solving the problem is easier and is also a good

### Timestamp: 09:26

 approximation for the dark blue line right. So, and that is why this performs much better than

### Timestamp: 09:31

 just using a regression problem to solve classification right. So, this loss has a name

### Timestamp: 09:38

 in literature. So, this loss is called as the hinge loss right. So, this is called as the hinge

### Timestamp: 09:47

 loss. Basically now, you can view your SVM problem itself as if it is solving a hinge loss,

### Timestamp: 09:55

 it is trying to find a w which minimizes a hinge loss plus regularization.

### Timestamp: 10:04

 Like how the rigid regression was solving the squared loss plus regularization L2 regularization.

### Timestamp: 10:11

 Now, SVM can be thought of as solving minimizing the hinge loss plus L2 regularization right.

### Timestamp: 10:17

 So, the regularizer of course, we can play around with regularizer thus you wish,

### Timestamp: 10:21

 but then if you want good easy solvability then using an L2 regularizer typically helps

### Timestamp: 10:28

 and hinge loss is basically trying to approximate the 0 1 loss. So, that you know you take

### Timestamp: 10:35

 get rid of the NP hardness somehow. Good. So, now we have put two different algorithms in

### Timestamp: 10:43

 the same perspective. Let us go ahead and see if we can put other algorithms also under this

### Timestamp: 10:47

 perspective right. So, that kind of will give us a feel for how different algorithms are different

### Timestamp: 10:53

 with respect to dealing with the NP hardness problem. Okay. The next algorithm that which is

### Timestamp: 10:59

 another popular algorithm that we have seen is the logistic regression algorithm.

### Timestamp: 11:04

 So, what was the logistic regression algorithms problem? Well, we were trying to maximize a

### Timestamp: 11:19

 likelihood problem there where we assumed that p of y given x is some logistic function on

### Timestamp: 11:27

 w transpose x right. So, if I remember if you remember this from our discussion of logistic

### Timestamp: 11:32

 regression, we were maximizing the likelihood function over w where we had product of i equals

### Timestamp: 11:40

 1 to n because the points were assumed to be iid the labels. So, now so we used let us say

### Timestamp: 11:49

 some sigma of w transpose x i which sigma is the logistic function.

### Timestamp: 11:57

 Power you know z i into 1 minus sigma of w transpose x i power 1 minus z i right. So,

### Timestamp: 12:06

 where sigma of z sigma of a is 1 by 1 plus a power minus a. This was the logistic function

### Timestamp: 12:14

 that we used and z i in this case I am using z i instead of y i because z i was 0 or 1 but then

### Timestamp: 12:20

 the way we are trying to deal with the losses here is with y i as 1 or minus 1. So, we need to

### Timestamp: 12:26

 kind of map this to the 1 or minus 1 world a little bit later right. So, z i is 1 the label is 1

### Timestamp: 12:33

 if y i is 1 plus 1 and z i is 0 if y i is minus 1 right. So, because there when we discuss logistic

### Timestamp: 12:43

 regression we assume that the labels were 0 or 1 and that is why this formulation came about.

### Timestamp: 12:48

 So, now just to note that I mean we can treat the data set as having labels as plus 1 or minus 1

### Timestamp: 12:55

 just that there is a direct relation between z i and y i which we need to use.

### Timestamp: 13:00

 So, what does this give us? Well, this gives us so, this is the likelihood function within

### Timestamp: 13:06

 we then take the logarithm of this and then we will say that we will maximize over w sum over i

### Timestamp: 13:12

 equals 1 to n z i log sigma w transpose x i plus 1 minus z i log 1 minus sigma w transpose

### Timestamp: 13:25

 x i and then we looked at its gradient and all that when we are discussing logistic regression.

### Timestamp: 13:30

 This is equivalent to minimizing over w sum over i equals 1 to n z i rather minus z i

### Timestamp: 13:39

 log sigma w transpose x i I am writing this is a minimization problem because we want to understand

### Timestamp: 13:49

 everything as a minimization problem with respect to some parameter of interest in this case w

### Timestamp: 13:54

 and then we see what is the loss function that comes about right. So, plus z i minus 1 log

### Timestamp: 14:01

 1 minus sigma w transpose x i. Now, let us see so, this is the loss over n different data points

### Timestamp: 14:13

 that we have. Now, let us see what is the loss for a single data point

### Timestamp: 14:24

 when let us say z i equals 1 of course, there are two cases z i can be 1 or minus 1 let us say

### Timestamp: 14:29

 when z i is 1 now what happens if z i is 1 then this is the contribution of the loss

### Timestamp: 14:37

 of i th data point, but then if z i is 1 the second term 0. So, that does not contribute

### Timestamp: 14:42

 this case 1. So, which means that this value is just minus log of let me write this in

### Timestamp: 14:49

 the same color is minus log of sigma w transpose x i right. So, because this is 1 assume if this is

### Timestamp: 15:00

 1 then this is the contribution which is just minus log of what is sigma of w transpose x i which

### Timestamp: 15:07

 is just 1 plus e power minus w transpose x i which is log of 1 plus e power minus w transpose x i.

### Timestamp: 15:17

 Now, if z i is 1 that also means that in our notation y i is plus 1 right. So, which means

### Timestamp: 15:24

 that I can equivalently write this as log of 1 plus e power minus w transpose x i into y i right.

### Timestamp: 15:32

 So, it is the same basically what I am saying here is that for every point in the data set where

### Timestamp: 15:38

 the label is 1 now the loss of a particular w that you want to choose with respect to that data

### Timestamp: 15:45

 point it can be written like this right. Similarly, what happens when loss is loss for a single point

### Timestamp: 15:59

 when z i equals 0 z i equals 0 in our notation is y a equals minus 1 z i equals 0 would mean what.

### Timestamp: 16:07

 So, again let us go back to the loss well if z i is 0 the first term does not contribute anything

### Timestamp: 16:12

 only the second term contributes is the second term what does it contribute it contributes minus 1.

### Timestamp: 16:19

 So, it contributes minus log of 1 minus sigma of w transpose x i which is minus log of

### Timestamp: 16:33

 1 minus 1 by 1 plus e power minus w transpose x i this is just algebra nothing major going on here

### Timestamp: 16:40

 which is minus log of if you play around with this you will get that this is just e power minus

### Timestamp: 16:46

 w transpose x i by 1 plus e power minus w transpose x i which is equivalent to minus log of let

### Timestamp: 17:01

 us say what I do here is I divide both the numerator and denominator by e power minus w transpose x i

### Timestamp: 17:12

 divided by I can do that because it is always going to be a positive term which would not be negative

### Timestamp: 17:19

 so sorry 0. So, division is still ok the reason why I am doing this will be apparent in a minute.

### Timestamp: 17:25

 So, this numerator will become 1 the denominator will become you know the first term will be

### Timestamp: 17:30

 e power w transpose x i the second term will be 1. So, now this itself can be written as log of

### Timestamp: 17:40

 1 plus e power w transpose x i this is also same as log of 1 plus e power minus w transpose x i

### Timestamp: 17:54

 into y i. Why because now we are looking at the case where z i is 0 which means y i is minus 1

### Timestamp: 18:01

 which means the w transpose x i can be written as minus w transpose x i into y i this is minus y i

### Timestamp: 18:06

 is also minus 1 right. So, I can write it like this now now as you can observe that in both the

### Timestamp: 18:11

 cases I have managed to write my loss for a single data point as exactly the same depending on

### Timestamp: 18:19

 log of 1 plus e power minus w transpose x i y which means what does it mean it just means that

### Timestamp: 18:26

 my logistic regression can be equivalently thought of as right. So, equivalently minimizing over

### Timestamp: 18:33

 w sum over i equals 1 to n log of 1 plus e power minus w transpose x i y right. So, if I have the

### Timestamp: 18:44

 data set if I represent my labels as 0 and 1 then I can I would rather write this as in this way

### Timestamp: 18:52

 right. So, that would be the logistic functions probability of the maximum likelihood formulation

### Timestamp: 18:58

 or if I represent it as plus 1 minus 1 then I can simplify it and put it in this way both are

### Timestamp: 19:04

 exactly equivalent because the loss with respect to every data point depends on whether y is

### Timestamp: 19:08

 plus 1 or minus 1 or z i is 0 or 1 and then we just derived that in both the cases you can

### Timestamp: 19:14

 represent the loss contribution of the data points to the loss can be written in this form.

### Timestamp: 19:20

 Now, this helps us because now what we have done is we have written it in terms of w transpose x i

### Timestamp: 19:25

 into y a now this is just our g of x in x i into y a which means that we can put this guy now in

### Timestamp: 19:32

 the picture that we already have right. So, earlier it was not possible now because we have

### Timestamp: 19:37

 written it this way we can put it in our picture of loss for a single data point let us do that and

### Timestamp: 19:43

 see what comes out right. So, again just to refresh I mean it is good thing to refresh these things

### Timestamp: 19:50

 especially if you are seeing the first time we have the 0 1 loss as usual

### Timestamp: 19:55

 in 2 y yeah we have we saw the squared loss and we also saw the hinge loss

### Timestamp: 20:14

 now ok. So, let me put this all right. So, this is g of x into y minus 1 squared squared loss

### Timestamp: 20:28

 0 1 loss indicator of g of x not into y less than 0 hinge loss max of 1 minus g of x into y

### Timestamp: 20:45

 from a 0 now we have the fourth loss which is the logistic regression loss which is log of 1 plus

### Timestamp: 20:54

 e power minus g of x into y right. So, this of course x x is g of x into y the y axis is loss.

### Timestamp: 21:08

 How does this look like in this picture well this is another way to deal with our NP hardness

### Timestamp: 21:13

 how does this look look like in the picture well I may not be able to try to scale but then

### Timestamp: 21:19

 if I do a reasonable approximation of this this and of course down like this right. So,

### Timestamp: 21:30

 it never becomes 0 of course, because you have a 1 plus log of 1 is 0, but then log of 1 plus

### Timestamp: 21:36

 something which is never going to be 0 because it e power something. So, this this loss is never

### Timestamp: 21:44

 0, but then it keeps getting lower and lower as g of x into y increases right. So, and this is

### Timestamp: 21:51

 another way you can think of as dealing with the with the NP hardness. Now, this is a convex

### Timestamp: 21:57

 function now this can be minimized efficiently right. So, like how SVM deals with NP hardness

### Timestamp: 22:02

 using hinge loss logistic regression deals with you know this green loss and just as a name

### Timestamp: 22:08

 is called as the logistic logistic loss right. So, this is how logistic regression can be

### Timestamp: 22:18

 interpreted as dealing with the NP hardness of 0 1 problem right. So, basically what we are saying

### Timestamp: 22:23

 is that different algorithms use different convex surrogates to minimize

### Timestamp: 22:30

 instead of the 0 1 loss and depending on how good this surrogate is in representing the original

### Timestamp: 22:37

 0 1 loss we get you know different performances and so on. So, both right. So, so the conclusion that

### Timestamp: 22:45

 we finally draw using this picture let me put the down. So, the conclusions here are as follows.

### Timestamp: 22:53

 So, 0 1 loss is hard to minimize

### Timestamp: 22:57

 first point the second point is different algorithms

### Timestamp: 23:07

 use different surrogates surrogate loss.

### Timestamp: 23:22

 Surrogates are convex and hence easy to minimize. This is the main area right. So, this is the reason

### Timestamp: 23:42

 why we have so many algorithms for classification as opposed to regression because in regression what

### Timestamp: 23:48

 we cared about is the squared loss which is already convex and so we did not have to look further.

### Timestamp: 23:56

 Then we did the regularization and so on right. So, which is a separate point of discussion

### Timestamp: 24:02

 now here even the loss that we care about is not convex. So, these different surrogates deal with

### Timestamp: 24:08

 it in different ways and now of course in each of these cases you can also do a regularization

### Timestamp: 24:14

 so you can for instance SVM does this regularization implicitly right. So, where the goal itself was

### Timestamp: 24:20

 to maximize margin which gave us the regularization effect. In logistic regression implicitly there

### Timestamp: 24:26

 is no regularization but in practice you always run logistic regression with the regularization

### Timestamp: 24:31

 term right. So, it is as easy as running the logistic regression I mean anyway you are if you are

### Timestamp: 24:36

 using gradient based methods to solve it it is not too hard to solve this. So, this is a this is a

### Timestamp: 24:43

 high level view we can put down for instance perceptron we can think of perceptron also in this

### Timestamp: 24:52

 framework is not it would not be as clean as this but we can do that and I will talk a bit about

### Timestamp: 24:58

 that in a minute we can also put boosting in this framework where you will use something called

### Timestamp: 25:02

 as an exponential loss right. So, let us talk briefly about that before we end this discussion.