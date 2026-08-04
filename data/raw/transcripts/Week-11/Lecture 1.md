# Week-11 - Lecture 1


(Refer Slide Time: 00:00) Hello everyone, welcome back. We are looking at the support vector machine formulation and

(Refer Slide Time: 00:18) we said that the basic support vector machine formulation works well for linearly separable

(Refer Slide Time: 00:24) data sets. And then we asked the question what if there are outliers in the data, how do we

(Refer Slide Time: 00:30) deal with that? And we put down a different modified formulation for the support vector

(Refer Slide Time: 00:35) machine algorithm which we call the soft margin support vector machine algorithm which had the

(Refer Slide Time: 00:39) following formulations right. So, we wanted to minimize over W in R D of course, the length which

(Refer Slide Time: 00:47) corresponds to the margin plus some constant C which is a hyper parameter times sum over i

(Refer Slide Time: 00:55) equals 1 to n psi i which are slack variables associated with each data point which we talked

(Refer Slide Time: 01:01) about as bribes that each point pays to satisfy the constraint such that the following constraints

(Refer Slide Time: 01:07) satisfy W transpose x i y i plus psi i or epsilon i is greater than or equal to 1 for all i and

(Refer Slide Time: 01:20) epsilon i is greater than or equal to 0 for all i right. So, this is the modified formulation

(Refer Slide Time: 01:25) that we started looking at and we wanted to ask the question well this is a good formulation

(Refer Slide Time: 01:31) in the sense that now we can potentially handle outliers. But at this point in the way that is

(Refer Slide Time: 01:38) written right now this is the primal formulation it is not clear by looking at this formulation

(Refer Slide Time: 01:45) if you know this can be colonized. Why do you want to colonize this? Well now what this can handle

(Refer Slide Time: 01:51) is linearly separable data with outliers. But then it could so be the case that you might have

(Refer Slide Time: 01:58) quadratically separable data with outliers for example you could have a data set of this form

(Refer Slide Time: 02:05) you know maybe a two dimensional data where your positive data points where all somewhere here

(Refer Slide Time: 02:15) and your negative data points where all somewhere here and you also have some negatives on this

(Refer Slide Time: 02:22) side and some positives on this side right. So, now you want a separator which is something like

(Refer Slide Time: 02:28) this right. So, because any there is no linear separator for these data points however there is

(Refer Slide Time: 02:34) a quadratic separator if you treat these two points as outliers in some sense right. So,

(Refer Slide Time: 02:39) that is we want a formulation which not only uses which takes care of these outliers using this

(Refer Slide Time: 02:45) bribe or slack variables that we have been talking about but should also be amenable to

(Refer Slide Time: 02:50) colonization that is it should be able to handle structural non-linearity as well.

(Refer Slide Time: 02:55) The question is how or is it is this formulation the right way to look at that. So, the only way

(Refer Slide Time: 03:00) you can find out is by you know computing the dual formulation and seeing what happens.

(Refer Slide Time: 03:05) Let us go ahead and do that. So, how do we how do we write the dual form of this particular

(Refer Slide Time: 03:12) equation? Well we first write down the Lagrangian. Now, the Lagrangian well maybe I should have

(Refer Slide Time: 03:18) I missed the epsilon in this formulation epsilon is also this is also a variable. So, which means

(Refer Slide Time: 03:27) that if you write when I write the Lagrangian the primal variables are going to be W and epsilon.

(Refer Slide Time: 03:32) And now for this set of constraints for every data point there is corresponding you know Lagrangian

(Refer Slide Time: 03:39) variable and for every set of the second set of constraints for every data point also there is a

(Refer Slide Time: 03:45) variable. Now, the way I am going to think of this is that so, we are going to call the

(Refer Slide Time: 03:49) the variable associated Lagrange variable associated with the first set of constraints as alpha

(Refer Slide Time: 03:53) and the second set of constraints as beta. So, that every data point the i-th data point has

(Refer Slide Time: 03:59) two variables associated with it which is alpha i and beta i alpha i corresponding to this constraint

(Refer Slide Time: 04:05) and beta i corresponding to the other second constraint. So, what is the Lagrangian? Well,

(Refer Slide Time: 04:09) that is going to look like this you first write down your the original function as such

(Refer Slide Time: 04:16) epsilon i plus if you remember the Lagrangian from last time. So, this is going to be sum over i

(Refer Slide Time: 04:23) equals 1 to n alpha i which is the multiplier for the i-th constraint. Well, in the in the

(Refer Slide Time: 04:29) standard form the i-th constraint is going to look at look like the following 1 minus W transpose

(Refer Slide Time: 04:34) x i y i minus epsilon i. Well, that is the form where you write this less than or equal to 0.

(Refer Slide Time: 04:42) G i of W is less than or equal to 0 that is what the general constraint that we have been looking

(Refer Slide Time: 04:47) at and in that sense this will be the exact g i of W plus now you have an extra constraint which

(Refer Slide Time: 04:55) is sum over i equals 1 to n beta i which is again the variable associated with the i-th data point

(Refer Slide Time: 05:02) for the second constraint. Now, if you write it again in the standard form as some function less than

(Refer Slide Time: 05:07) or equal to 0 well that is going to be minus psi i because this is equivalent to minus psi i less than

(Refer Slide Time: 05:14) or equal to 0 and this is equivalent to 1 minus W transpose x i y i minus psi i is less than or equal

(Refer Slide Time: 05:21) to 0 that is why that those get multiplied here. So, now what is the dual problem? So, we have

(Refer Slide Time: 05:28) written down the Lagrangian we know what the dual problem is the dual problem is the following.

(Refer Slide Time: 05:34) It is exactly the same thing that we looked at earlier I mean the ideas are exactly the same

(Refer Slide Time: 05:40) just that we need to go over this so that we are very clear what we are trying to do. So, you want

(Refer Slide Time: 05:44) to minimize over W and epsilon maximize over alpha which is greater than or equal to 0 beta

(Refer Slide Time: 05:53) greater than or equal to 0 half norm W squared plus c sum over i psi i plus the whole thing

(Refer Slide Time: 06:03) essentially I am writing it again just copying whatever is there above plus sum over i equals 1 to

(Refer Slide Time: 06:15) beta i minus psi i. So, this is now the dual problem now we can ask the question well if I

(Refer Slide Time: 06:23) so remember what we did last time was there was only alpha there was no beta at that point and

(Refer Slide Time: 06:30) we asked the question if I fix some so we wrote the dual problem first as min max problem then we

(Refer Slide Time: 06:38) said that well because all the constraints and the functions are all convex we can write the min

(Refer Slide Time: 06:45) max problem as an equivalent maximum problem that is the first step. So, let us do that first step.

(Refer Slide Time: 06:49) So, the first step would be this is equivalent to max over alpha greater than 0 beta greater than 0

(Refer Slide Time: 06:57) you know min over W comma epsilon the same thing right. So, half norm W squared plus c sum over

(Refer Slide Time: 07:10) epsilon i plus sum over i phi and so on right. So, I am just writing this again and again for

(Refer Slide Time: 07:22) completion sake, but you get the idea. So, this comes because of duality this equivalence is

(Refer Slide Time: 07:32) because of duality in fact what is called as a strong duality. So, we have this now at our

(Refer Slide Time: 07:38) disposal so this is the problem that we could solve to get the same answer. Now, here what we did

(Refer Slide Time: 07:46) last time was what helped us was the fact that you know if I fix and Lagrange variable which is

(Refer Slide Time: 07:55) alpha last time and then I can minimize this in an unconstrained fashion which means that I can

(Refer Slide Time: 08:02) take the gradient with respect to W said it to 0 and we saw what happened. We can do the same thing

(Refer Slide Time: 08:07) now right. So, we can fix alpha and beta to be something and then if you take the gradient with

(Refer Slide Time: 08:11) respect to W right. So, what would happen well if I take let us call this if I take the gradient

(Refer Slide Time: 08:18) of this function which is the Lagrangian function right. So, this is L if I take the gradient of the

(Refer Slide Time: 08:24) Lagrangian with respect to W and say it to 0 what does that imply why am I doing that because I

(Refer Slide Time: 08:31) want to minimize this with respect to W at W star that minimizes this the gradient is going to be

(Refer Slide Time: 08:35) 0 and I am trying to see what that satisfies right. So, what would that mean that means that you

(Refer Slide Time: 08:41) know your W star with respect to some alpha and beta that you have fixed right. So, now you are

(Refer Slide Time: 08:47) fixing alpha and beta right. So, fix alpha come out beta and then you take the gradient with respect to

(Refer Slide Time: 08:52) W you get the following equation well this does not depend on W what this depends is exactly the

(Refer Slide Time: 08:58) same way in fact you are going to get the same answer here alpha i x i y nothing changes with respect

(Refer Slide Time: 09:06) to W star. So, this is let us call this one. So, if I take the gradient with respect to W star I

(Refer Slide Time: 09:15) still get the same thing. Now, there is another set of variables in the primal which is the epsilon i

(Refer Slide Time: 09:21) variables. So, now I can take the gradient with respect to that also right. So, if I take the

(Refer Slide Time: 09:25) gradient with respect to epsilon and say it to 0 then I can see maybe I will say it with respect

(Refer Slide Time: 09:31) to epsilon i and say it to 0. So, now let us see what happens. Now, this implies well the first

(Refer Slide Time: 09:36) term does not depend on epsilon the second term is c with respect to epsilon i that is just c

(Refer Slide Time: 09:43) plus well what do we get alpha i into minus 1 plus beta i into minus 1 is going to be 0

(Refer Slide Time: 09:53) which implies that at what optimality you are going to have alpha i plus beta i equals c right.

(Refer Slide Time: 10:01) So, which means that I mean whatever alpha beta that finally is the solution has to satisfy alpha i

(Refer Slide Time: 10:08) plus beta i equals c. Now, what we did last time was well we have this optimal W star's

(Refer Slide Time: 10:17) equation once you have fix an alpha. Now, we could do the same thing again we can back substitute

(Refer Slide Time: 10:23) W star into our Lagrangian and see what happens. Let us do the same thing here right. So,

(Refer Slide Time: 10:30) back substituting W star alpha beta into the Lagrangian.

(Refer Slide Time: 10:46) Well, if you do that and if you do some simplification you are going to get the following right. So,

(Refer Slide Time: 10:51) you will get maximize over alpha greater than or equal to 0 beta greater than or equal to 0 alpha

(Refer Slide Time: 11:04) plus beta equals c alpha transpose 1 minus alpha transpose y transpose x transpose x y alpha.

(Refer Slide Time: 11:16) So, this would be our tool problem. Now, the way I derived this is by using the fact that you

(Refer Slide Time: 11:30) substitute W star equals x y alpha because if you remember from last time right. So, W star alpha beta

(Refer Slide Time: 11:38) now this would be x y alpha it is exactly the same form and then you can substitute it back

(Refer Slide Time: 11:43) lot of things will cancel out and you can use the you can use the fact that alpha i plus beta

(Refer Slide Time: 11:49) equal c and then if you do the simplification you are going to end up with a dual problem which

(Refer Slide Time: 11:55) looks like this. Now, if you if you stare at this dual problem for a bit you will realize that well

(Refer Slide Time: 12:02) this is exactly the same thing that we have maybe there should be half here. This is exactly the

(Refer Slide Time: 12:07) same objective that we had for the dual problem in the hard margin support vector machine as well.

(Refer Slide Time: 12:14) So, the only thing that changes is that earlier we only had this condition alpha greater than

(Refer Slide Time: 12:19) or equal to 0. Now, we have a beta greater than or equal to 0 as well because there is a

(Refer Slide Time: 12:23) second set of variables and you have alpha plus beta equal c. What does that mean? That means,

(Refer Slide Time: 12:30) that alpha i plus beta i equal c for all i that is what I mean. So, in fact, if I have to be

(Refer Slide Time: 12:36) pedantic side should write this is c times the all one spectre. This just means that alpha i

(Refer Slide Time: 12:41) plus beta i equal c for all i that is the condition for this. Now, if you notice there is no beta here

(Refer Slide Time: 12:48) right. So, there is no beta term in the objective but then beta term appears in the optimization

(Refer Slide Time: 12:56) well what does that mean? That means, that we are saying alpha is greater than or equal to 0 but then

(Refer Slide Time: 13:02) alpha plus beta equal c which means that well beta is somehow restricting the range of alpha.

(Refer Slide Time: 13:08) Now, what range does it restrict alpha to alpha has to be greater than or equal to 0 but because beta

(Refer Slide Time: 13:14) is also greater than or equal to 0 and alpha i plus beta i equal c well that means, that well the

(Refer Slide Time: 13:21) only way only the only restriction that this imposes on alpha is that alpha has to be at most c

(Refer Slide Time: 13:28) right. So, that is what this is restricting. So, we can equivalently remove beta away and then

(Refer Slide Time: 13:34) say that this is the dual problem is just maximize over alpha is greater than or equal to 0 but

(Refer Slide Time: 13:40) then it is also restricted by by beta to be within c and the same objective. I can do this because

(Refer Slide Time: 13:47) beta does not appear in the objective it only appears as a restriction in the restriction in the

(Refer Slide Time: 13:56) you know constraint and so I can do this H transpose x y alpha. Now, this will be my problem that I

(Refer Slide Time: 14:05) want to solve. Now, this is very very similar to what we had for the hard margin support vector

(Refer Slide Time: 14:12) machine. Now, the only difference and interestingly the only difference between the hard margin support

(Refer Slide Time: 14:18) vector machine and the soft margin support vector machine happens to be the fact that now the alpha

(Refer Slide Time: 14:24) parameter which we are searching for in the dual problem is restricted to be you know is has

(Refer Slide Time: 14:31) an upper bound right. So, it is restricted to be within a value of c and remember c is a user

(Refer Slide Time: 14:36) defined hyper parameter to the problem. Now, let us do some sanity check to see if this matches

(Refer Slide Time: 14:43) our intuition. Now, what happens if c is 0? If c is 0 right so if c equals 0 then what does this

(Refer Slide Time: 14:55) condition tell us well z alpha has to be greater than or equal to 0 and alpha should be less than or

(Refer Slide Time: 15:00) equal to 0 as well which means the there is only one feasible alpha which is alpha is equals 0 right.

(Refer Slide Time: 15:07) So, and that has to be the optimal solution because there is only one feasible solution.

(Refer Slide Time: 15:11) Now, if alpha equals 0 which means 0 is a remember it is a vector and I mentioned alpha i is 0

(Refer Slide Time: 15:18) for all i well what does that mean that implies that well my w star is going to be just sum over alpha

(Refer Slide Time: 15:25) x i y i alpha star and if alpha star is 0 then w star is just linear combination of the data points

(Refer Slide Time: 15:33) and the only answer the w star will get is also 0 w star equals 0.

(Refer Slide Time: 15:38) Now, remember we argued the same thing when we put down our modified formulation that if c is 0

(Refer Slide Time: 15:47) then it means that the bribes do not cost anything if the bribes do not cost anything then you

(Refer Slide Time: 15:51) would focus on minimizing the length of w and the smallest you can get is 0 which is using w equal

(Refer Slide Time: 15:57) 0. Now, in the dual problem also this the same effect can be seen in a slightly different way

(Refer Slide Time: 16:03) in the sense that if c is 0 then alpha becomes 0 and so w becomes 0. So, that is a sanity check

(Refer Slide Time: 16:10) right. So, this this this takes the box that you know if c is 0 what we expected to happen in

(Refer Slide Time: 16:16) the primal also happens in the dual and it should happen just that we can convince ourselves

(Refer Slide Time: 16:20) easily. Now, if c is infinity then what happens is that you know well if c is infinity there is no

(Refer Slide Time: 16:27) upper bound for alpha if there is no upper bound for alpha then that means that you know this

(Refer Slide Time: 16:33) problem is exactly the same dual problem as the dual that we had for the hard margin S we have

(Refer Slide Time: 16:38) right. So, this is same as hard margin because the only condition there was max of alpha greater

(Refer Slide Time: 16:46) than or equal to 0 right. So, and if you remember from our argument for the hard for the modified

(Refer Slide Time: 16:51) formulation if c is infinity that is if the bribes are costing infinitely for every per unit

(Refer Slide Time: 16:56) then the only way you will get a non trivial solution is if you do not have to pay bribes at all

(Refer Slide Time: 17:01) and if you do not have to pay bribes at all and still if there is a w that means that the data set

(Refer Slide Time: 17:05) itself is linearly separable which means that you are back in the hard margin case right. So,

(Refer Slide Time: 17:10) which means this also checks out I mean our intuition as what we had for the primal problem even

(Refer Slide Time: 17:15) the dual problem great. So, now now this is good. So, we now have you know a very simple

(Refer Slide Time: 17:22) dual dual problem and the advantage is that this is still kernelizable right. So, because

(Refer Slide Time: 17:30) it is exactly the same problem and it appears in x transpose x just that the constraints are

(Refer Slide Time: 17:36) no longer just alpha greater than or equal to 0 alpha as an upper bound and these constraints

(Refer Slide Time: 17:40) are sometimes called as box constraints because you know your alpha sub is bound to be within a

(Refer Slide Time: 17:48) you know hyper cube of you know radius c it is a length c right. So, side length c I mean

(Refer Slide Time: 17:56) two dimension this just means that you know your alpha is within this box right. So,

(Refer Slide Time: 18:02) this is alpha 1 and alpha 2 and essentially you are searching for an alpha within this region.

(Refer Slide Time: 18:07) In high dimension this will become a cube it looks like a box and so it is called as a box

(Refer Slide Time: 18:11) constraint right. So, that is one point that I wanted to mention but the main interesting part

(Refer Slide Time: 18:16) is that we retain all the advantages that we had for this dual of the hard margin support vector

(Refer Slide Time: 18:24) machine it is still kernelizable and still the constraints are easy to solve right. So,

(Refer Slide Time: 18:29) projecting onto a box constraint is also easy if at some point if you see if you are doing a

(Refer Slide Time: 18:35) gradient based method and you observe that your alpha are going above c you can clip it to c

(Refer Slide Time: 18:40) and if it goes below 0 you can clip it to 0 right. So, projection is quite easy as well.

(Refer Slide Time: 18:47) Now, which means we have all the advantage of hard margins support vector machine but now we can

(Refer Slide Time: 18:52) also deal with outliers right. So, which means this makes it a very very powerful algorithm.

(Refer Slide Time: 18:57) Now, one other point that we had with respect to the hard margins of

(Refer Slide Time: 19:01) photo vector machine was that you know we argued using the complementary slackness conditions

(Refer Slide Time: 19:07) that the number of data points that really contribute to our W star or only can only be those

(Refer Slide Time: 19:15) that are on the hyper plane that supports our W at margin 1. Now, that was a very useful thing

(Refer Slide Time: 19:22) there because it told us that you know you are you are essentially compressing your data in

(Refer Slide Time: 19:31) some sense right. So, you you you have you might have billion data points but the ones that

(Refer Slide Time: 19:35) really contribute to W star are the ones that are right on the hyper plane right. So,

(Refer Slide Time: 19:42) the supporting hyper plane the remaining you can just throw away and what do you why do you have to

(Refer Slide Time: 19:46) throw away because especially when you are working with kernels we saw last time that if you

(Refer Slide Time: 19:49) had to make a you know prediction for a test data point you only need the similarity of the test

(Refer Slide Time: 19:56) data point with respect to each of the support vectors via the kernel and then you multiplied it

(Refer Slide Time: 20:02) with the corresponding alpha for the support vector and you are done right.

(Refer Slide Time: 20:07) Which was which was a very useful thing to have there because it led to sparse solutions.

(Refer Slide Time: 20:12) Now, here we have almost all the advantages of the hard margins of photoelectric machine we have

(Refer Slide Time: 20:18) kernelizability we have simple constraints but do we also have this sparsity notion still intact

(Refer Slide Time: 20:23) right. So, how can we find that out right. So, in other words I am asking the question well for

(Refer Slide Time: 20:28) the W star that you will get if you solve the primal is it true that the W star is still going to

(Refer Slide Time: 20:34) depend only on a small set of support vectors or because we allowed for these you know

(Refer Slide Time: 20:41) bribes and extra slack variables or things going to go wrong or you know I mean

(Refer Slide Time: 20:47) is it suddenly does it become that my W star is going to be a linear combination of all my data

(Refer Slide Time: 20:52) points in which case I cannot throw away data points I have to retain all my data points especially

(Refer Slide Time: 20:57) when I am using a kernel to make a prediction for the test data point right. So, that question

(Refer Slide Time: 21:02) we still have to answer and the way to answer that would be to take a look at the complementary

(Refer Slide Time: 21:07) slackness conditions for this modified support vector machine algorithm it is a soft margin case.

(Refer Slide Time: 21:14) So, what we are going to do next is going to look at the complementary slackness conditions

(Refer Slide Time: 21:19) and its implications for the soft margin support vector machine algorithm and that will give us some

(Refer Slide Time: 21:24) insights into you know which points are important and which points are not important in this

(Refer Slide Time: 21:28) particular formulation let us do that.
