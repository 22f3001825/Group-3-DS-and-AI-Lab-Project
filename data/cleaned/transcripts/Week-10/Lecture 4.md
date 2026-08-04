# Week-10 - Lecture 4

### Timestamp: 00:00

 Let us go back to our problem and see what our problem was.

### Timestamp: 00:16

 It is our problem was the following.

### Timestamp: 00:18

 We have to remember half norm w squared such that w transpose x i into y i is greater than

### Timestamp: 00:27

 or equal to 1 for all i equals 1 to 10.

### Timestamp: 00:32

 This was our original problem.

### Timestamp: 00:35

 First question is does this min max swap that we will do later would it apply to our problem?

### Timestamp: 00:40

 It would apply because what kind of a function is this of w?

### Timestamp: 00:44

 Well, this is a quadratic function of w.

### Timestamp: 00:46

 So, there is a squared term.

### Timestamp: 00:48

 So, this is quadratic in w and what kind of functions or constraints of w will be the

### Timestamp: 00:53

 linear linear in w is quadratic in w.

### Timestamp: 00:59

 So, both f and g g i's are all convex for our problem and so we can apply the min max swap

### Timestamp: 01:07

 in our case.

### Timestamp: 01:08

 So, let us try to do that.

### Timestamp: 01:10

 But before we do that, we have to bring these these guys into standard form.

### Timestamp: 01:13

 The g a of w is less than or equal to 0.

### Timestamp: 01:16

 So, what is the standard form?

### Timestamp: 01:18

 So, this is equal and 2.

### Timestamp: 01:20

 1 minus w transpose x i into y i is less than or equal to 0 for all i equals 1 to 10.

### Timestamp: 01:27

 This is exactly the same as this.

### Timestamp: 01:29

 So, just writing this as in the form, now this would be my g i of w which is less than

### Timestamp: 01:35

 or equal to 0.

### Timestamp: 01:37

 So, what does this tell us now?

### Timestamp: 01:40

 So, now this is the original problem I wanted to solve.

### Timestamp: 01:43

 So, now I will write the Lagrangian of w comma alpha.

### Timestamp: 01:47

 I am going to write this as alpha, but then the meaning of this alpha is alpha 1, alpha

### Timestamp: 01:52

 2 dot dot dot alpha n because there are n constraints for our case.

### Timestamp: 01:56

 So, each of these constraints will have a corresponding alpha associated with it and

### Timestamp: 02:00

 I am going to think of the whole vector as I am going to indicate it using alpha just

### Timestamp: 02:05

 to you know a d clutter notation.

### Timestamp: 02:08

 So, what is the Lagrangian going to look like?

### Timestamp: 02:12

 Well, I will first write f of w which is half norm w square plus it is going to be alpha

### Timestamp: 02:17

 1 times g of g 1 of w plus alpha 2 times g 2 of w dot dot dot which can be written as

### Timestamp: 02:22

 sum over i equals 1 to n alpha i g i of w, but g i of w in this case it is just 1 minus

### Timestamp: 02:31

 w transpose x i into y i.

### Timestamp: 02:33

 This is 1 to be k.

### Timestamp: 02:35

 So, this is our Lagrangian.

### Timestamp: 02:39

 So, now what we are saying is that we can either you know minimize over w maximize over

### Timestamp: 02:47

 alpha greater than or equal to 0 and by which I mean this just mean alpha 1 greater than

### Timestamp: 02:53

 or equal to 0 dot dot alpha n greater than or equal to 0.

### Timestamp: 02:56

 That is what this means.

### Timestamp: 02:59

 You want to minimize max this half norm w square plus sum over is 1 to n alpha i 1 minus

### Timestamp: 03:08

 w transpose x i into y i.

### Timestamp: 03:11

 This is equivalent to max over alpha greater than 0 mean over w the same thing half norm

### Timestamp: 03:19

 w square plus sum over i is 1 to n alpha i 1 minus w transpose x i away.

### Timestamp: 03:26

 It is exactly what we did in general for f and g.

### Timestamp: 03:30

 Now I have applied it to our problem we still are not sure why this is going to help but

### Timestamp: 03:35

 let us see why it is my problem.

### Timestamp: 03:38

 Now, the reason why this problem on the right hand side might help us is because of the

### Timestamp: 03:47

 following fact.

### Timestamp: 03:48

 So, earlier we had a if I give you a w, right.

### Timestamp: 03:52

 So, if I fix a w and try to evaluate the max problem now that is a maximization over

### Timestamp: 03:59

 alpha greater than or equal to 0.

### Timestamp: 04:01

 So, on the other hand in the right hand side now if I fix an alpha greater than or equal

### Timestamp: 04:08

 to 0 and I try to minimize and I try to minimize this over w now here there are absolutely

### Timestamp: 04:14

 no constraints on w.

### Timestamp: 04:17

 So, for any fixed alpha now this w's minimization is an unconstrained problem which means I know

### Timestamp: 04:25

 how to do unconstrained minimization, right.

### Timestamp: 04:27

 So, what I will do is I will take the gradient of this function with respect to the w the

### Timestamp: 04:31

 higher order analog of derivative and then try to set it to 0 and see what happen I can

### Timestamp: 04:35

 do that, right.

### Timestamp: 04:36

 So, let us try that for this particular problem and see what happens, right.

### Timestamp: 04:40

 So, what I am trying to do is I am going to try to solve the right hand side problem

### Timestamp: 04:47

 to understand the right hand side problem let us say fix some alpha greater than or equal

### Timestamp: 04:53

 to 0 arbitrarily alpha greater than or equal to 0 and then ask the question well maybe if

### Timestamp: 04:58

 you have three data points maybe alpha is 1 5 7, right.

### Timestamp: 05:01

 So, some factor that I am just fixing right.

### Timestamp: 05:04

 So, arbitrarily I am fixing some vector alpha and then I am asking what is minimization

### Timestamp: 05:10

 over w of norm w spread plus sum over i equal to 1 to n alpha i 1 minus w transpose

### Timestamp: 05:17

 x i y i.

### Timestamp: 05:19

 What is the minimizer what is this value going to be, right.

### Timestamp: 05:23

 So, can I get a hold on this value.

### Timestamp: 05:25

 Now, because this is an unconstrained optimization over w now I can take the derivative of this

### Timestamp: 05:30

 whole thing or the gradient of this with respect to w and try to set it to 0 and so that

### Timestamp: 05:35

 is where the minimization is going to happen.

### Timestamp: 05:37

 So, what is the gradient of this whole thing is going to be with respect to 0, well the

### Timestamp: 05:42

 gradient will solve the following right.

### Timestamp: 05:44

 So, half norm w square is gradient it is just w.

### Timestamp: 05:48

 So, that is let me write this as w plus sum over i equals 1 to n there is an alpha i w

### Timestamp: 05:57

 transpose minus w transpose x i y i gradient it is just minus x i y i with respect to w.

### Timestamp: 06:03

 Now, this is the gradient at any w at the optimal w this value is going to be 0 right.

### Timestamp: 06:10

 Now, this is for any alpha that I have given right.

### Timestamp: 06:13

 So, this w star when you say w star this is the w star this is the best for the alpha

### Timestamp: 06:18

 that I gave you right.

### Timestamp: 06:19

 So, you pick some alpha and with respect to that alpha maybe I can even say this is w

### Timestamp: 06:23

 star alpha just to indicate that there is a dependence on alpha k right.

### Timestamp: 06:27

 So, what is w star alpha then will w star alpha then is going to be just sum over

### Timestamp: 06:33

 i equals 1 to n alpha i x i y i.

### Timestamp: 06:38

 Now, what is this telling us this is telling us the following right.

### Timestamp: 06:43

 So, we wanted to solve this maximum problem right here.

### Timestamp: 06:48

 Now, the moment I pick an alpha the w has a functional form that depends on this alpha

### Timestamp: 06:56

 and what is this functional form the functional form is a nice functional form which just

### Timestamp: 07:00

 is of the form you know the w that that is best for the alpha that I give you is just

### Timestamp: 07:06

 you know linearly combining my data points with alpha right.

### Timestamp: 07:09

 So, it is just sum over i equals 1 to n alpha i x i.

### Timestamp: 07:12

 Well, remember what is what are these guys right.

### Timestamp: 07:14

 So, alpha's are all greater than or equal to 0 that is some fixed quantity y i is plus

### Timestamp: 07:20

 or minus 1 x i you know where is r d right.

### Timestamp: 07:25

 So, which means w star alpha is also going to be some vector in r t right.

### Timestamp: 07:28

 So, if I give you alpha then the best w is is the linear combination of your data point

### Timestamp: 07:34

 x i y i is with alpha that is what this is saying right.

### Timestamp: 07:37

 So, which means that I now have to find that alpha which is which is kind of the which

### Timestamp: 07:42

 maximizes this quantity with respect to all possible alpha greater than or equal to 0.

### Timestamp: 07:46

 But what is this quantity now here we have maximum is over alpha minimized over w there are

### Timestamp: 07:52

 two variables.

### Timestamp: 07:54

 But now what this argument is telling us is that if I fixed alpha the w the best w is just

### Timestamp: 07:59

 a nice function of alpha right.

### Timestamp: 08:01

 So, it is just a linear combination using alpha which means that I can actually find this

### Timestamp: 08:07

 minimum value by back substituting this value that for w in the original objective itself

### Timestamp: 08:13

 right. So, I can do that right.

### Timestamp: 08:14

 So, let me try to do that.

### Timestamp: 08:16

 So, to find the minimizer so, what I am going to do is I am going to substitute

### Timestamp: 08:21

 substitute back value of w star alpha in the objective.

### Timestamp: 08:34

 So, we can do this or to do this first I will make a note that you know w star alpha

### Timestamp: 08:41

 can actually return in matrix notation as x y alpha where x is just you know a matrix which has

### Timestamp: 08:54

 our data points as columns x 1 to 10 and y is just another matrix which has our labels in

### Timestamp: 09:03

 as diagonal the diagonal matrix all that is 0 the labels are all in tag null and alpha is as

### Timestamp: 09:09

 you should the alpha that I actually input to the input to this x 1 i fix some alpha that is

### Timestamp: 09:14

 this alpha. So, the reason why we are writing this is because it is easy to you know deal with

### Timestamp: 09:20

 matrix notation then you know keeping graph of the sum over i and so on and so forth right.

### Timestamp: 09:24

 So, verify that this is exactly same as what we had earlier right. So, this sum over i alpha i

### Timestamp: 09:31

 x i y i is exactly same as what have written here right. So, why because these two guys will

### Timestamp: 09:36

 multiply to x 1 y 1 x 2 y 2 by any mean column and this alpha is the kind of multiply to

### Timestamp: 09:43

 multiply each of the column and we will get for you. So, just to just to be sure right. So,

### Timestamp: 09:50

 this is like a d cross n matrix this is an n cross n matrix when this is an n cross 1 vector.

### Timestamp: 09:56

 So, that these product will be a d cross 1 vector which is our w right. So, let us let us back

### Timestamp: 10:02

 substitute this quantity into our original problem. The original problem was this right. So,

### Timestamp: 10:08

 the objective was half non w square plus sum over i equals 1 to n alpha i 1 minus w transpose x

### Timestamp: 10:15

 i y i now substitute w star alpha equals x y alpha into n to this right. So, if you do that right.

### Timestamp: 10:33

 So, on simplification I am not going to do the algebra here on simplification we will get

### Timestamp: 10:39

 something that does not have w because wherever there is w we are substituting it as x y alpha

### Timestamp: 10:44

 on simplification what you will get is the following right. So, you will get this term is equal to

### Timestamp: 10:51

 alpha transpose 1 minus half x y alpha which is our w transpose x y alpha this is what you would get

### Timestamp: 11:05

 where 1 is just the vector of all ones. This is the n dimensional vector of all one

### Timestamp: 11:13

 and this is this is the quantity right. So, that is which means that if it fix a value of alpha

### Timestamp: 11:18

 this is what the minimization over w evaluates and then I want to maximize this over all possible

### Timestamp: 11:23

 alpha greater than or equal to z right. So, so which means that the dual problem that we can

### Timestamp: 11:30

 alternatively solve is the following right. So, now maximize over alpha greater than or equal to 0

### Timestamp: 11:39

 is quantity which is alpha transpose 1 minus half. Now, I will write this in open of this

### Timestamp: 11:48

 transpose like this alpha transpose y transpose x transpose x y alpha.

### Timestamp: 11:57

 Now, this is the dual problem. Dual to what? Dual to the original problem that we wanted to solve

### Timestamp: 12:03

 which was minimize over w half norm w squared such that w transpose x i into y i greater than or equal to

### Timestamp: 12:16

 you can take this as the primal problem. Now, what I am saying is the following right. So,

### Timestamp: 12:21

 I can either solve the primal problem or I can solve the dual problem both will give me the same

### Timestamp: 12:25

 answer right. So, but the question is you know what have you gained by solving the dual problem

### Timestamp: 12:32

 by looking at the dual problem right. So, that is if if it is if you have not really gained much

### Timestamp: 12:37

 then why do we bother doing the dual problem at all right. So, so we need to be clear what we are

### Timestamp: 12:41

 gaining here. So, let us just let us see what we have gained. What have we gained?

### Timestamp: 12:48

 So, the first point is that you know the dual variable time mentioned right. So, if you are

### Timestamp: 13:06

 solving the dual problem you are solving a problem with searching for alpha right. So, you might do

### Timestamp: 13:10

 again gradient based techniques to solve this let us say, but you will search for alpha. But where

### Timestamp: 13:15

 is where are you searching for your search for alpha in R n plus right. So, R n plus means

### Timestamp: 13:22

 you are searching for alpha greater than or equal to 0 in n dimension. There are there is one alpha i

### Timestamp: 13:27

 corresponding to each each data point and then you are trying to find a vector alpha in n dimension

### Timestamp: 13:34

 which has greater than or equal to 0 while while the primal problem or dimension is what.

### Timestamp: 13:49

 Well in the primal problem what I am solving I am trying to find a w where is this w this w is in R t

### Timestamp: 13:57

 it is a d dimensional vector that I am searching for I am searching for something in d dimensional

### Timestamp: 14:01

 space in the primal problem where it is a dual problem and searching for something in the n

### Timestamp: 14:04

 dimensional space which means that if it so happens that your d is much much larger than n then

### Timestamp: 14:10

 it might be better to solve the dual problem than the primal problem because you are searching in a

### Timestamp: 14:14

 smaller space. So, right. So, and if your algorithm for instance you are using a gradient based

### Timestamp: 14:19

 technique or something like that which depends whose rate of convergence depends somehow on the

### Timestamp: 14:25

 dimensionality of the space where you are searching for then smaller the dimension better will be your

### Timestamp: 14:30

 algorithm and so it might be better of solving the problem in a smaller dimensionality than a larger

### Timestamp: 14:35

 dimension space. But then this will happen this will be useful only if these larger than n these

### Timestamp: 14:40

 much much larger than n. So, this is but nevertheless this is one good thing to note that you can

### Timestamp: 14:46

 solve the problem in n dimension the number of points dimension as I put to the number of you know

### Timestamp: 14:51

 feature dimension. First point the second point is that dual constraints

### Timestamp: 15:01

 are you know easier in terms of what do I mean by that I mean the following right. So,

### Timestamp: 15:08

 here if you are solving the primal problem you have to search for a w with satisfy these

### Timestamp: 15:12

 constraints and there are n such constraints where w transpose x i y i has to be greater than

### Timestamp: 15:18

 or equal to these are linear constraints but still these might be slightly more complicated

### Timestamp: 15:22

 constraints especially when you are doing projections on on to the space that satisfy these

### Timestamp: 15:27

 constraints and so on. I mean if you are doing a gradient based algorithm you might take a

### Timestamp: 15:31

 gradient step but then you might go out of this constraint space you may want to projected back

### Timestamp: 15:36

 into this constraint space where you have to have a hold on how these constraints set is and so

### Timestamp: 15:42

 on and so forth. Whereas in the dual problem the constraints are super simple it is just

### Timestamp: 15:46

 alpha greater than or equal to 0 it is still a constraint optimization problem remember you still

### Timestamp: 15:50

 have to do some kind of projection on to this set but then that projection might be much easier

### Timestamp: 15:55

 because this space in which you are projecting is just the positive quarter for the non-negative

### Timestamp: 16:00

 quarter right. So, projections might be easier and so the dual problem might be easier to solve again.

### Timestamp: 16:05

 Now both these advantages that we are talking about comes from the fact that you know by looking

### Timestamp: 16:11

 at this part that one alpha is in R n dimension and so it might be easier. The second is if D

### Timestamp: 16:17

 is larger than n and the second is alpha greater than or equal to 0 might be a simpler constraint to

### Timestamp: 16:23

 tackle than W transpose x i y is greater than or equal to 1 for all n. However these two are you

### Timestamp: 16:30

 know in some sense auxiliary benefits that we get out of this the major benefit of the main

### Timestamp: 16:35

 benefit that we get by looking at the dual problem is the fact that if you stare at the dual

### Timestamp: 16:42

 problem the objective of the dual problem you will observe something very very interesting that

### Timestamp: 16:48

 the objective depends on x transpose it right. So, the objective now depends on the dot product

### Timestamp: 16:58

 matrix x transpose x is the R n cross n matrix which is the dot product matrix it captures the

### Timestamp: 17:04

 dot product between every pair of data point and immediately some you know some things should

### Timestamp: 17:10

 light up right. So, what why is this a useful thing to do because the moment you have expressed

### Timestamp: 17:16

 your optimization problem in terms of dot product you know what can happen right. So, we have already

### Timestamp: 17:20

 seen this multiple times in this course. So, more importantly more importantly

### Timestamp: 17:30

 dual depends on x transpose x and so can be now you will have to complete the sentence

### Timestamp: 17:45

 the from whatever you see in the sports hall and yes and can be what can be fertilized

### Timestamp: 17:52

 which means now by looking at the primal problem it is not at all clear that if the data was not

### Timestamp: 18:01

 linearly separable but then was quadratically separable I do not know how to solve the problem

### Timestamp: 18:05

 because I am looking for a line with the margin 1. Now, what I am saying is that the dual problem

### Timestamp: 18:11

 reveals the fact that if what is really important is the dot products between the path of data

### Timestamp: 18:16

 and so the moment we can write the same problem as the equal and form which depends on x transpose x

### Timestamp: 18:23

 now I can replace this with some matrix k kernel matrix k right. So, where the dot products are

### Timestamp: 18:31

 in some high dimensional space and all the all our discussions about you know mapping from

### Timestamp: 18:36

 low dimension to high dimension and taking the dot product will apply here that is you can now solve

### Timestamp: 18:42

 the problem in a quadratics and for a cubic sense depending on what kernel is or Gaussian kernel

### Timestamp: 18:47

 radial basis function kernel whatever we want right. So, you can do all that right. So,

### Timestamp: 18:51

 this is this is something that is very very important. So, so these are three main advantages

### Timestamp: 18:57

 of solving the dual problem. So, this is the first point that I wanted to make. So,

### Timestamp: 19:01

 second point that I wanted to make is by by looking at the solution w star itself right. So,

### Timestamp: 19:10

 the w star for the best possible alpha that we will get right. So, for alpha star is going to look

### Timestamp: 19:16

 like this. Some over i equals 1 to n alpha star i x i by i right. So, so which means so why is this

### Timestamp: 19:25

 true because if you remember whichever alpha that I fixed right. So, the w star corresponding to

### Timestamp: 19:31

 that is it is a linear combination with respect to that alpha which means that the whatever if I

### Timestamp: 19:35

 solve the dual problem and I find that alpha star is the solution of the dual problem

### Timestamp: 19:39

 then the w star corresponding will be of the form some over i alpha star i x i y i right. So,

### Timestamp: 19:45

 that is that is the that is the way it will be because that is what we derived right. So, we are

### Timestamp: 19:51

 taking the variance setting into 0. So, now, this state is that this state is

### Timestamp: 19:56

 optimal w w star is a linear combination of the data points where importance of a data point

### Timestamp: 20:18

 given by alpha star i for i f data point i f data point right. So, that is what this means right.

### Timestamp: 20:42

 So, for your optimal w how much does a point x i contribute is given by the corresponding alpha

### Timestamp: 20:50

 star and if alpha star is 0 then it means that that point does not contribute at all and if alpha

### Timestamp: 20:55

 star is positive then that point contributes something to w star right. So, because if alpha star

### Timestamp: 21:00

 is star 0 then this x i y a does not contribute to w star. So, the question is then you know question is

### Timestamp: 21:07

 question is where are the important points that is points for which alpha star i is greater than

### Timestamp: 21:33

 this. We know alpha star is always greater than or equal to 0 because that is the space where

### Timestamp: 21:38

 we are searching for but it does not mean that they have to be always greater than 0. There

### Timestamp: 21:43

 might be some points for which it is 0 for some points it might be greater than 0. The question

### Timestamp: 21:46

 that we are asking is where are those points for which it is strictly greater than 0 can we

### Timestamp: 21:51

 somehow characterize these points that will tell us you know how many points overall contribute

### Timestamp: 21:57

 to w star and how many points do not contribute to w star. So, we would like to understand that.