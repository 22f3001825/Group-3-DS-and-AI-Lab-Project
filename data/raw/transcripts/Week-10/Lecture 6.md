# Week-10 - Lecture 6


(Refer Slide Time: 00:00) Welcome back. So far we have seen the support vector machine algorithm when you have linear

(Refer Slide Time: 00:19) separability and when you have perhaps linear separability in a higher dimension where

(Refer Slide Time: 00:23) you can use a kernel in the dual power. What we finally said was one shortcoming of the

(Refer Slide Time: 00:30) formulation that we have so far is the fact that you cannot handle how players in a clean

(Refer Slide Time: 00:35) manner. This is because when you have outliers using a kernel it is not the best possible

(Refer Slide Time: 00:39) idea. So then the question is how can we adapt or modify our formulation for support vector

(Refer Slide Time: 00:44) machine to deal with outliers. So towards this let us first start by taking a look at

(Refer Slide Time: 00:51) the original formulation of the support vector machine which is selected. So this was the original

(Refer Slide Time: 01:01) formulation of the support vector machine where you wanted to find a w that minimizes the length

(Refer Slide Time: 01:05) squared or maximizes the width when you have when you fix the margin when you ground the margin

(Refer Slide Time: 01:12) to be 1. So this was the original problem and now if you have a data set which is not linearly

(Refer Slide Time: 01:17) separable which has some outliers then this algorithm will not run because it is only looking

(Refer Slide Time: 01:24) for w's which have w transpose x i y i is greater than or equal to 1. You need a w to satisfy

(Refer Slide Time: 01:31) w transpose x i y greater than or equal to 1 for all data points only then that w comes into

(Refer Slide Time: 01:36) play and among those w's that satisfy this we are trying to fix the fixed w that has the

(Refer Slide Time: 01:41) least length. So the problem is not all w's are going to be feasible right. So now somehow we

(Refer Slide Time: 01:51) have to fix this problem and you have outliers and the way we are going to fix this is using the

(Refer Slide Time: 01:55) following idea right. So this is the inside. Now we are going to make every w please.

(Refer Slide Time: 02:04) Earlier only w's which correctly classified that separated the first two from the negatives were

(Refer Slide Time: 02:14) feasible. Now we are going to make every w please. Now how can we make that how can we achieve

(Refer Slide Time: 02:20) that objective of making every w feasible well the way we are going to do it is as follows right.

(Refer Slide Time: 02:25) So I mean intuitively let us say we fix some w fix any w you know w classifies

(Refer Slide Time: 02:35) some point correctly and misclassify some point.

(Refer Slide Time: 02:48) Now earlier if a w misclassifies any point then we will not allow the w right. So we won't take

(Refer Slide Time: 02:55) that w into consideration because you want the w to classify all points correctly but such a w may

(Refer Slide Time: 03:00) not exist and that is why the problem comes. So now we are saying we will take a w and observe that

(Refer Slide Time: 03:05) this w classify some points correctly and it misclassifies some other points. For the points it

(Refer Slide Time: 03:10) classified correctly there is no problem for the points that are misclassified or incorrectly

(Refer Slide Time: 03:16) classified. So you are going to do the following the incorrect points.

(Refer Slide Time: 03:21) Incorrectly classified points the idea is loosely speaking right. So we will say the incorrectly

(Refer Slide Time: 03:33) classified points can face some bride to become to go to the correct side right. So to go to the

(Refer Slide Time: 03:43) correct side. So I have to quantify what these things mean I do that.

(Refer Slide Time: 03:49) So somehow we are allowing the capability of points to pay bride to make the w that we care

(Refer Slide Time: 03:56) about feasible. What does this mean? So this means one way to achieve this is as follows right.

(Refer Slide Time: 04:02) So what we are going to do is the following right. So we are going to do a modified formulation

(Refer Slide Time: 04:08) modified formulation. So you want to minimize over w up from w squared nothing change is there

(Refer Slide Time: 04:21) so far. Such that earlier you want a w transpose x i into y i to be greater than or equal to 1.

(Refer Slide Time: 04:28) This is what you wanted for all i. Now what I am going to see is that well I fix a w if the w

(Refer Slide Time: 04:35) satisfies this condition for a point x i y i I am happy. If it does not satisfy this condition

(Refer Slide Time: 04:42) now I am going to allow this point to face some bride epsilon i such that this condition is

(Refer Slide Time: 04:51) satisfied. Now why you was that condition earlier not satisfied because w transpose x i y i was

(Refer Slide Time: 04:55) less than 1 but you want it to be greater than 1 which means that you need some extra push right.

(Refer Slide Time: 05:01) So you need some extra num value to be added to this point it need to make it greater than or equal

(Refer Slide Time: 05:05) to 1 and that quantity is what I am calling as bride that the point i face to satisfy this

(Refer Slide Time: 05:11) condition. Now the bride that each point face is greater than or equal to 0 right. So

(Refer Slide Time: 05:17) you cannot pay a negative bride you are paying either a 0 bride if the point is already class

(Refer Slide Time: 05:22) by charity I do not have to pay any bride otherwise I will pay a 0 I will pay a positive

(Refer Slide Time: 05:26) bride to make this equation satisfied. Now I also have to decide how much bride each point face

(Refer Slide Time: 05:34) right. So it means that I need to minimize this over the bride epsilon i as well right. So

(Refer Slide Time: 05:39) epsilon i is the bride that the i of theta point face. Now this might be a potential modified

(Refer Slide Time: 05:45) formulation but now if you if you stare at this formulation for a second you will realize that

(Refer Slide Time: 05:52) is something lacking about this formulation. Now what is lacking here is the problem.

(Refer Slide Time: 05:57) Now if we solve this problem what would happen is that our goal is to minimize the

(Refer Slide Time: 06:03) length of w and now I am the moment I add this bribes or possibility of points giving bribes.

(Refer Slide Time: 06:10) Now I am allowing every w to be p is equal w right. So earlier only w's which were class paying

(Refer Slide Time: 06:17) correctly separating the point plus from the negative where p is equal now all w's are p is equal.

(Refer Slide Time: 06:23) Now let us say I take the w which is the w with all 0's right. So that is also a w valid w.

(Refer Slide Time: 06:31) Now is that a feasible w because all w's are feasible that is also be a feasible w. Why will

(Refer Slide Time: 06:36) that be a feasible w because you know for the w which is all 0's this value is always going to be 0

(Refer Slide Time: 06:42) but then each theta point can pay a bribe of 1 to satisfy this equation. Now that bribes of

(Refer Slide Time: 06:49) course greater than or equal to 0's so now you you have all 0's which is also a feasible w

(Refer Slide Time: 06:55) and now you want to minimize the length over all feasible w's right. So that is what your your

(Refer Slide Time: 07:01) goal is but now you cannot minimize the length less than or equal to 0 which means that if I solve

(Refer Slide Time: 07:05) this problem I am just going to get all 0's as my solution but then something really wrong is

(Refer Slide Time: 07:11) going on here right. So what is going on wrong right. So pause and think about this I will tell

(Refer Slide Time: 07:16) you what the answer is for this now. What is going on wrong here is the fact that it is not the

(Refer Slide Time: 07:21) fact that we allowed points to pay bribes but but what we did not do is that we did not penalize

(Refer Slide Time: 07:30) right. So we do not want points to pay bribes as much as possible which means that

(Refer Slide Time: 07:34) it points are paying bribes well they better pay it with a cost right. So you cannot come for free

(Refer Slide Time: 07:40) right. So earlier I mean in this formulation that you are seeing right now there is no you know

(Refer Slide Time: 07:45) penalty for a point to pay bribes right. So which means that if there is no I mean restriction

(Refer Slide Time: 07:51) everybody is going to pay bribes and then get their job done right. So they will satisfy that

(Refer Slide Time: 07:55) this equation every point will do that. So which means that we have penalized this bribes.

(Refer Slide Time: 08:00) We want to pay at least bribes possible and still be able to satisfy this equation.

(Refer Slide Time: 08:06) How can we do that well where can we penalize we can only penalize in the objective right.

(Refer Slide Time: 08:10) So because objective is where we want to you know determine how good a w is. Now the moment I fix

(Refer Slide Time: 08:17) a w the bribes are fixed but then how much bribes should also be a part of goodness of a w.

(Refer Slide Time: 08:24) So what we will do is that we will add the amount of bribes each data point paid as part of the

(Refer Slide Time: 08:31) objective itself. Now what would happen is that you know the vector w which is all zeros will

(Refer Slide Time: 08:39) have to pay a lot of bribes because each point will pay a bribes of one unit and so then

(Refer Slide Time: 08:44) total bribes that is paid by the vector w to zero is m right. So and that might be too large

(Refer Slide Time: 08:50) and so that may not be the optimal solution. Now one small thing to note here is that

(Refer Slide Time: 08:57) now we are our objective has changed our objective is some of two terms. On the one side we have

(Refer Slide Time: 09:05) half number w square which is the length of w the other side which we have some more i epsilon i

(Refer Slide Time: 09:12) which is the amount of bribes that each data point pays with respect to that w. Now these two are

(Refer Slide Time: 09:19) not necessarily compatible units right so one is in length one is in amount of bribes that

(Refer Slide Time: 09:26) pay right so the units of these things are completely different. So we have to kind of balance

(Refer Slide Time: 09:31) these two different quantities carefully and so we need a balancing factor here and let us

(Refer Slide Time: 09:37) call that balancing factor c. Now how important is this c we do not know a prior right so it depends

(Refer Slide Time: 09:45) on the data right so how noisy is the data how many outlets of that in the data will determine

(Refer Slide Time: 09:50) how much bribes necessary and how the bribes in the length kind of kind of balance of each

(Refer Slide Time: 09:55) of that right so now the c is some value which is greater than or equal to zero and this is

(Refer Slide Time: 10:02) typically a hyper parameter. Now we will you will try different values of c and see which one works

(Refer Slide Time: 10:13) using cross validation you have seen how cross validation works earlier we use the same procedure

(Refer Slide Time: 10:17) to find out c right so now this would be the modified formulation and this formulation is

(Refer Slide Time: 10:25) sometimes called as the you know the soft margin formulation

(Refer Slide Time: 10:33) because we not only care about the margin via this length we also care about you know the outliers

(Refer Slide Time: 10:43) and so this is called as the soft margin formulation. Now let us talk a little bit about the c

(Refer Slide Time: 10:49) right so so let us look at the case when c equal zero what happens when c is zero well if c is zero

(Refer Slide Time: 11:01) then what is c telling us c is telling us how much one unit of bribes cost right so that's what c

(Refer Slide Time: 11:07) says now c is zero then it means that bribes don't cost which means what is the solution that we

(Refer Slide Time: 11:16) will get we will get a w equal to zero as the solution this is the argument that we did earlier

(Refer Slide Time: 11:23) it is if the bribes are not costly you are just going to minimize the length and w equal zero

(Refer Slide Time: 11:28) as a feasible point so that will be the optimal on that's what on the other hand if c is

(Refer Slide Time: 11:32) infinity right so if every unit of bribes is infinitely more important than the length then

(Refer Slide Time: 11:40) what would happen well the only way you can even get a feasible w is when you don't pay bribes

(Refer Slide Time: 11:47) at all right so which means that if there will I mean the only way this problem gets solved is

(Refer Slide Time: 11:53) that is the w that actually classify is your data point correctly which means that you see is

(Refer Slide Time: 11:58) infinity we are back to our linear separability right so linear separability which means if there

(Refer Slide Time: 12:06) is no linear separable to acid fire then all w's are equally bad they are going to cost

(Refer Slide Time: 12:11) infinite right so so that's a useless setup right so only if linearly separable then you will

(Refer Slide Time: 12:21) get some non trivial answer if c is infinity so now this c itself is kind of interpolating between

(Refer Slide Time: 12:26) how important is the margin which is by the length versus how important are you trying to tackle

(Refer Slide Time: 12:33) the outlay because we don't know a priori how many outlay are there in our you know data set

(Refer Slide Time: 12:38) the usual usually what we do is to do cross validation for the c and then figure out

(Refer Slide Time: 12:44) that the data figure out tell us that what is the right right c here okay so now this is our

(Refer Slide Time: 12:50) modified primal formulation so this is soft margin primal formulation it's called a soft margin

(Refer Slide Time: 12:57) again because we are you know we don't strictly ask for w transfer that say it's y8 to be greater

(Refer Slide Time: 13:03) than or equal to 1 we allow for the fact that some w's you know some points may not necessarily

(Refer Slide Time: 13:09) practice with condition it's a margin condition fire this bright so the bright I call this bright

(Refer Slide Time: 13:15) but then literature this is called a flat variables so this is the epsilon i's that we look

(Refer Slide Time: 13:21) into looking at here are typically for the flat variables okay so what we should do now is

(Refer Slide Time: 13:28) to follow right so now we have a modified formulation which can potentially take care of outlights

(Refer Slide Time: 13:35) but the earlier formulation that we had had a great benefit when we looked at the dual problem

(Refer Slide Time: 13:40) right so the dual was kernelizable the dual had simpler constraints alpha greater than or equal to

(Refer Slide Time: 13:45) but here we have completely modified the formulation we have added this extra term psi i and then

(Refer Slide Time: 13:50) we are searching over w's and psi i and now it's not at all clear immediately at least not obvious

(Refer Slide Time: 13:55) that you know how the dual problem is going to look like right so which means that we have to go

(Refer Slide Time: 14:00) through the process of converting this primal problem into a dual problem and then see if you

(Refer Slide Time: 14:05) have lost our ability to kernelize if you have lost our ability to you know have simpler constraints

(Refer Slide Time: 14:11) if we have then this is a bad formulation if we have not then this is a good formulation at

(Refer Slide Time: 14:17) this point we don't know so the only way we can know is if we actually write up the dual

(Refer Slide Time: 14:21) formulation and find out so let's go ahead and try and find that out
