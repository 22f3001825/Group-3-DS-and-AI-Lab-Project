# Week-10 - Lecture 5

### Timestamp: 00:00

 So, to answer this question, we like to do some work right. So, and we will do that now.

### Timestamp: 00:19

 For that we have to revisit our Lagrangian formulation right. So, now we will we will try

### Timestamp: 00:24

 to answer this question in a minute and that will be this something very interesting.

### Timestamp: 00:28

 For that we will have to one small leader which we will do now. So, we will be visiting the Lagrangian.

### Timestamp: 00:38

 Let us do the follow right. So, remember we know that min over

### Timestamp: 00:46

 so, we know the following right. So, because of duality we know that min over w max over alpha

### Timestamp: 00:55

 greater than 0 f of w plus g of l plus alpha g of w is equivalent to max over alpha greater

### Timestamp: 01:06

 than or equal to 0 min over w about w plus alpha g of w if f and g are convex which is what we are

### Timestamp: 01:14

 assuming now. Now, this is the primal problem and this is the dual problem.

### Timestamp: 01:22

 Now, let us say if I solve the primal problem somehow and I got my solution as w star is

### Timestamp: 01:30

 the primal solution. So, this is the minimization problem in w star is the primal solution let us say.

### Timestamp: 01:39

 And let us say I solve the dual problem and I got alpha star is the dual solution.

### Timestamp: 01:44

 So, let us say I solve the primal problem and I solve the dual problem.

### Timestamp: 01:54

 Now, let us so, let us say I try to plug in the value of the primal solution into this right.

### Timestamp: 02:01

 So, which means that I want to find out what press the primals at the primal solution what

### Timestamp: 02:06

 does this value look like? M x of alpha greater than or equal to 0 f of w star plus alpha g of

### Timestamp: 02:12

 the dual solution. This is what this will look like. Here I can plug in the dual solution

### Timestamp: 02:18

 and then I will I can ask well this will be min of w f of w plus alpha star g of the this is what

### Timestamp: 02:27

 the dual solution at dual optimality if I plug in that alpha star. So, this is the value that I will

### Timestamp: 02:34

 that I will get. Now, what can we comment about this one? Well, we already argue that this value

### Timestamp: 02:41

 because w star is the primal solution it will satisfy the constraint g of the mu star

### Timestamp: 02:46

 reflection of equal to 0. And for whenever a point satisfies the constraint this Lagrangian

### Timestamp: 02:52

 will actually evaluate to the functions object to evaluate that point which means that this

### Timestamp: 02:57

 is going to evaluate to f of w star you know these two things are equal this is going to evaluate

### Timestamp: 03:02

 to f of w star. Now, this is going to evaluate it to let us say it evaluates to some value which

### Timestamp: 03:10

 min of w f of w plus alpha g of alpha star g of w right. So, and these two these two guys are

### Timestamp: 03:21

 equal that is what duality theory tells us. Now, what I can do is that well because this is a

### Timestamp: 03:29

 minimization over all w I can actually plug in the w star and then argue that when the minimum

### Timestamp: 03:36

 value has to be less than or equal to what w star would have given you where w star is the

### Timestamp: 03:42

 primal solution which means that this is going to be less than or equal to any w evaluated at any

### Timestamp: 03:47

 w and in particular at w star right. So, which means that this value is going to be less than or

### Timestamp: 03:52

 equal to f of w star plus alpha star g of w star. Now, this implies f of w star is on the left hand

### Timestamp: 03:59

 side on the right hand side this is thing this is less than or equal to f of w star plus alpha

### Timestamp: 04:03

 star g of w star. Now, this implies alpha star g of w star is greater than or equal to 0 because

### Timestamp: 04:10

 I can cancel out the f of w star and then this has to happen. But we already know something right.

### Timestamp: 04:18

 So, but we already know already know alpha star has to be greater than or equal to 0 and g of

### Timestamp: 04:27

 w star has to be less than or equal to 0. Why? Because they are primal opt if I mean they are

### Timestamp: 04:33

 feasible points in the primal in the primal problem and feasible points in the dual problem.

### Timestamp: 04:38

 So, which means that optimal point has to be a feasible point also which means that

### Timestamp: 04:42

 it has to satisfy this constraint for the primal, it has to satisfy this constraint for the

### Timestamp: 04:46

 dual which means if this is a non additive quantity and this is a non push of you quantity

### Timestamp: 04:51

 the product of this has to be alpha star and the g of w star has to be the product must be less

### Timestamp: 04:58

 than or equal to 0 because this guy is less than or equal to 0 this is greater than or equal to 0.

### Timestamp: 05:02

 there is no way that this can be a positive strictly positive point right. So, so this is also

### Timestamp: 05:09

 true, but our argument here says all first R into g of W star is greater than or equal to

### Timestamp: 05:14

 C 2. So, this is 1, this is 2 if both 1 and 2 are 2 then the only way that both of these can

### Timestamp: 05:20

 be true is because 1 and 2 implies then alpha star into g of W star equals C. The only way both

### Timestamp: 05:30

 these can be reconciled if alpha star into g of W star is actually equal to 0 right.

### Timestamp: 05:37

 So, this condition of the primal duality primal optimal solution multiplied by the

### Timestamp: 05:43

 constraint at the dual from the primal opt- to the constraint at the primal optimal solution g

### Timestamp: 05:49

 of W star multiplied by the dual optimal value alpha star is equal to 0 this is called as

### Timestamp: 05:55

 sometimes called as a complementary slackness condition.

### Timestamp: 06:02

 Well essentially it says that there if 1 slack that is if 1 is strictly positive,

### Timestamp: 06:07

 alpha star is strictly positive that is there is a slack between 0 and strictly positive there

### Timestamp: 06:13

 is a positive quantity then the other one has to be 0. See similarly g of W star is strictly

### Timestamp: 06:19

 less than 0 then alpha star has to be 0 right. So, they are complementary in some sense.

### Timestamp: 06:24

 So, that is why it is called as complementary slackness condition for multiple constraints

### Timestamp: 06:28

 something similar holds right. So, because we always have to deal with multiple constraints.

### Timestamp: 06:39

 What happens is that you know alpha i star g i of W star will be equal to 0 for all

### Timestamp: 06:49

 right. So, for every constraint there is a corresponding multiplier alpha star i and so the

### Timestamp: 06:53

 product of these two will be equal to 0. The argument will be very similar we can do the argument

### Timestamp: 06:57

 yourself, but this has to hold for multiple constraints. So, this is also known as complementary slackness.

### Timestamp: 07:05

 So, why is this helpful for us right. So, we are revisiting the Lagrangian to understand

### Timestamp: 07:10

 some property of optimal solution of dual and primal optimal, but how is this going to be helpful

### Timestamp: 07:15

 for us. Let us try to understand what this means in our set up right. So, in our problem

### Timestamp: 07:24

 what is this means that alpha i star into g i of W star if you remember this 1 minus W star

### Timestamp: 07:39

 transpose x i into y i this is the this is g i of W star right. So, this product has to be 0

### Timestamp: 07:51

 for all i that is if I take any point i the corresponding constraint 1 minus W star transpose x i

### Timestamp: 07:59

 y i has multiplied by the corresponding Lagrangian multiplier alpha star has to be 0 right. So,

### Timestamp: 08:05

 that is what complementary slackness takes right. So, this is this by complementary slackness.

### Timestamp: 08:11

 Now, it is still not clear why this is going to be helpful right. So, but then we are we are

### Timestamp: 08:22

 almost there right. So, now which implies if a point positively contributes to W star that is

### Timestamp: 08:30

 if alpha star i is strictly greater than 0 that is where it positively contributes to the point

### Timestamp: 08:38

 alpha star then this implies by complementary slackness let us call this c s right. So, c s for

### Timestamp: 08:44

 complementary slackness this implies that 1 minus W star transpose x i into y i has to be equal

### Timestamp: 08:52

 to 0 only then the product will be 0. Now, this implies W star transpose x i into y i equals 1

### Timestamp: 09:01

 that is whenever if you solve the dual problem and you find a particular data point i has its

### Timestamp: 09:07

 corresponding alpha star e is strictly greater than 0 then the corresponding point will satisfy

### Timestamp: 09:14

 W star transpose x i y i equals 1. Now, what is it mean to say the corresponding point will

### Timestamp: 09:20

 satisfy W star transpose x i y i equals 1 right. So, now here something very interesting happens

### Timestamp: 09:26

 in picture right. So, let us say we have points like this which are plus

### Timestamp: 09:39

 there are lot of negative points here. Now, let us say this is our W star that we got as answer

### Timestamp: 09:51

 by solving the problem and now we observe that you know of course, this is the this is the

### Timestamp: 10:00

 separated actually draw this hard line.

### Timestamp: 10:05

 So, the corresponding margin lines are going to look like this right.

### Timestamp: 10:27

 So, this is the set of all x such that W star transpose x into y where y equals 1 equals 1

### Timestamp: 10:42

 margin 1 with positive guys and this is the set of all x such that W star transpose x into

### Timestamp: 10:50

 minus 1 equals 1 or W star transpose this is the y that I am talking about for the negative points.

### Timestamp: 10:58

 Now, what is the thing well if alpha star if I solve the dual problem and if I find alpha

### Timestamp: 11:05

 star is greater than 0 that is it positively contributes to my W star then it means that W star

### Timestamp: 11:11

 transpose x i y equals 1 which means that it has to be either on this line or it has to be on this

### Timestamp: 11:18

 line specifically right. So, this means that all these points right. So, every other point here

### Timestamp: 11:28

 is not going to necessarily contribute it is not going to contribute to my W star at all right.

### Timestamp: 11:32

 So, all these points which are not on the line if the point is not on the line then

### Timestamp: 11:41

 it implies alpha star is not greater than 0, but then alpha star has to be greater than or equal

### Timestamp: 11:46

 to 0 which means that for all the circuit points right. So, alpha star i equals 0 that is they

### Timestamp: 11:53

 do not contribute to my W star at all. So, the only guys who contribute to W star only possible

### Timestamp: 11:59

 guys are those that are on this line right. So, it might so happen that there are points on this

### Timestamp: 12:04

 line which do not contribute also, but then which might have alpha star 0 that we are not saying

### Timestamp: 12:10

 because the implication is saying that if alpha star is greater than 0 then it has to be on

### Timestamp: 12:15

 this line right. So, which means that there are very small subset of points which are really

### Timestamp: 12:22

 going to contribute to your W star right. So, now essentially what then we are saying is that

### Timestamp: 12:27

 this algorithm automatically gives you a way to pick the most critical points from billion points.

### Timestamp: 12:34

 You might have billion points, but then there are only going to be like hundreds hundreds of points

### Timestamp: 12:39

 you even tens of hundreds of points on these supporting hyperplanes and those points are the only

### Timestamp: 12:44

 ones that really matter for your W star. Everybody else that is not really matter. So, which means

### Timestamp: 12:49

 you can throw away the rest of the points on only work with these points right. So, if you want a

### Timestamp: 12:53

 W star you can only use these points to get that W star and especially this is important because

### Timestamp: 12:59

 when you have a kernel right. So, you are never going to reconstruct your W star in a high

### Timestamp: 13:03

 dimension exactly. You will only do a dot product with the new test point and when you are when

### Timestamp: 13:09

 you have to do that you only have to retain these small set of points you can throw away the rest of

### Timestamp: 13:15

 the points right. So, and that is why these this algorithm is so elegant in the sense that it

### Timestamp: 13:22

 takes that it is automatically gives you a way to compress your data set into small set of points.

### Timestamp: 13:27

 Now, all the points which are relevant to our W star right. So, let me make that comment

### Timestamp: 13:35

 only the point that are on the supporting hyperplane and this is supporting hyperplane these two

### Timestamp: 13:53

 lengths with margin 1 are contribute to W star and contribute to W star right. So, now these

### Timestamp: 14:07

 points necessarily I mean their special points these special points by the fact which of the

### Timestamp: 14:17

 fact that they are on the supporting hyperplane we are good to call them support vector

### Timestamp: 14:29

 because they are on the supporting hyperplane right. So, and this algorithm because it relies so

### Timestamp: 14:35

 much on the support vector right. So, they essentially find the support vector is called as a support

### Timestamp: 14:42

 vector machine machine is just a fancy word but the main idea is that uses the support vector right.

### Timestamp: 14:55

 So, this was this algorithm was developed mainly by Baphne-Cönn-Kolli in the 90s right.

### Timestamp: 15:05

 So, so essentially the biggest advantage that we get here that your W star is a sparse combination

### Timestamp: 15:16

 sparsling a combination of the data point right. So, again so in the in the kernel version right.

### Timestamp: 15:32

 So, now you can also kernelize this by looking at the dual right. So, you will solve the dual problem

### Timestamp: 15:35

 get these alphas now how would you solve the x test point right. So, you you need an x test

### Timestamp: 15:43

 given x test in the kernel version what would you want to do you want to calculate W star transpose

### Timestamp: 15:49

 x test but you know W star transpose x test is just somewhere i equals 1 to n alpha star i x i y i

### Timestamp: 15:57

 transpose x test which is somewhere i equals 1 to n alpha star i y i x i transpose x test.

### Timestamp: 16:09

 There is a dot product involved here. So, in the corresponding kernel version you will have

### Timestamp: 16:14

 given x test you want to calculate W star transpose phi of x test where W star is the higher

### Timestamp: 16:20

 dimensional W star which will be equal into sum over i equals 1 to n alpha star i y i the kernel

### Timestamp: 16:29

 at x i comma x x. Now, to evaluate this if you have a billion data points what is the advantage

### Timestamp: 16:36

 that we get here is that you know your alpha i star are only going to be positive for a small set

### Timestamp: 16:42

 of data point which means that you are only going to retain those alpha star in their corresponding

### Timestamp: 16:46

 y i. So, now your test for a given test point you can make a prediction only based on a small set

### Timestamp: 16:53

 of support vectors right. So, this is going to be greater than 0 only for support vectors.

### Timestamp: 16:59

 And so, you know you can maintain very small set of data points even if you are a billion data

### Timestamp: 17:04

 points maybe you can maintain just 100 data points and you will be able to make plus peak and

### Timestamp: 17:08

 really really easy that is the power of this matter right. So, this is this is the support vector

### Timestamp: 17:12

 machine algorithm. Now, at this point you know we have a very solid algorithm which can be

### Timestamp: 17:22

 kernelized and is also has the attractive properties of sparsity in terms of W star.

### Timestamp: 17:29

 But there are several lingering questions still that remind right. So, let me put on these

### Timestamp: 17:33

 questions and then we will answer these next. So, what are the questions that still remind?

### Timestamp: 17:39

 So, first question is you know how to adapt the support vector machines which is sometimes

### Timestamp: 17:51

 called as the SVM algorithm support vector machine algorithm let me point that out here itself

### Timestamp: 17:57

 as SVM how to adapt the support vector machine algorithm when data as how clear.

### Timestamp: 18:15

 Remember we are still assuming that the data is linearly separable or when you are using a

### Timestamp: 18:20

 kernel you are assuming that the data is quadratically separable, cubicly separable or in some

### Timestamp: 18:24

 high dimensional phase it is linearly separable. So, in you might have a dataset which is you know

### Timestamp: 18:33

 non-linearly separable in the following sense right. So, you might have a data like this where

### Timestamp: 18:38

 you might have plus plus plus plus minus minus minus minus minus but then there is a plus on this

### Timestamp: 18:45

 side and a minus on this side. So, now this is not linearly separable. So, I cannot run my

### Timestamp: 18:51

 support vector machine algorithm here because the algorithm needs a W which kind of correctly

### Timestamp: 18:56

 classified as all my data point there is no such W it will look for a W among all W's which

### Timestamp: 19:01

 classified is correctly separate this correctly it will look for the one that has the smallest

### Timestamp: 19:06

 length that is what the algorithm is but then here there is no such W. So, the algorithm will just

### Timestamp: 19:11

 put it front up and say there is no feasible W. Now, of course, we can imagine that you know you can

### Timestamp: 19:18

 perhaps map it to some high dimensional space where this is linearly separable but then there is

### Timestamp: 19:24

 a there is a problem with that right. So, you can use current this right. So, one I mean one

### Timestamp: 19:29

 might immediately think well this algorithm can be analyzed you know then why can't I deal with

### Timestamp: 19:34

 this outliers by pushing it to some high dimensional space. But it is not the right approach

### Timestamp: 19:43

 right way to solve why do I say that because what is the idea of kernels? The idea of kernels

### Timestamp: 19:53

 is to the hypothesis is that your data actual separator is not linear in the load dimension

### Timestamp: 20:00

 but it is linear in a high dimension right. So, which means that the data has some non-linear

### Timestamp: 20:05

 separator right. So, maybe it is a quadratic boundary if you be boundary whatever it is but it is

### Timestamp: 20:09

 a non-linear separator the structure is non-linear right. So, the separating structure is non-linear

### Timestamp: 20:15

 this assumption whereas, in this problem the structure is still linear you still I mean you

### Timestamp: 20:20

 still want a linear separator from this data set just that these outliers these two points here

### Timestamp: 20:28

 are are making an issue right. So, in this particular case there are only two points in general

### Timestamp: 20:32

 that will be many but the outliers are is what causing the algorithm to give up saying that there

### Timestamp: 20:39

 is no feasible W. But it is not a structural problem it is a problem of noise right. So, outliers

### Timestamp: 20:45

 are typically a problem of noise. So, to solve a problem of noise we cannot adapt our techniques to

### Timestamp: 20:53

 like a kernel kernel technique which is used to solve the problem of structure right. So, if the

### Timestamp: 20:58

 structure is different not linear structure non-linear structure then you use kernel. But if the

### Timestamp: 21:03

 structure is still linear but then if you have noise then using kernels and you might not get

### Timestamp: 21:08

 get best accuracy if you if you if you try to do that right. So, so then the question is how can

### Timestamp: 21:15

 I you know adapt my support vector machine algorithm itself when data has inherent out there.

### Timestamp: 21:21

 So, this is the question that that we are going to ask and this will lead us to one of the most

### Timestamp: 21:26

 powerful variance of support vector machine which is called as a soft margin support vector

### Timestamp: 21:32

 machine algorithm and that comes up with I mean the basic idea there is to make a small

### Timestamp: 21:38

 modification to our original problem that will lead to you know profound no consequence.

### Timestamp: 21:43

 And what is the small modification that we have to do and how does that help us we will see next.