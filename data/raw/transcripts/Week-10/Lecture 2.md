# Week-10 - Lecture 2


(Refer Slide Time: 00:00) Ok goal, yeah to come up with the formulation

(Refer Slide Time: 00:28) that maximizes the margin ok. So, how can we do this right. So, what do I mean by this

(Refer Slide Time: 00:44) right. So, how can we mathematically make this statement precise we can do it as follows

(Refer Slide Time: 00:49) right. So, we want to maximize you know gamma you know you want to find a w that maximizes

(Refer Slide Time: 01:01) the margin as much as possible right. So, the parameters of our algorithm are w and gamma

(Refer Slide Time: 01:07) and we want to find a w and gamma such that gamma is as large as possible. But we cannot

(Refer Slide Time: 01:13) allow all possible w's we will only allow w's which linearly separate the dataset with gamma

(Refer Slide Time: 01:19) margin right. So, which means that we such that w transpose x i into y i is greater than or

(Refer Slide Time: 01:33) equal to gamma for all i right. So, what are we saying here right. So, we want to maximize

(Refer Slide Time: 01:42) the margin as much as possible that gamma value such that for your data the w that this algorithm

(Refer Slide Time: 01:52) this formulation outputs has to have the property that w transpose x i y i is greater than

(Refer Slide Time: 01:58) or equal to gamma that is all the points are on either side either of either on the right

(Refer Slide Time: 02:03) on or right side of the line given by the equation w transpose x equal to gamma or on

(Refer Slide Time: 02:10) on or left side of the line given by the equation w transpose x equal to minus gamma that is

(Refer Slide Time: 02:15) what this formulation is telling us. So, if you I think this is a good time to pass and

(Refer Slide Time: 02:21) think is this really specifying exactly what we want or are we missing something about

(Refer Slide Time: 02:27) this formulation. Now, let me tell you what we are missing about this formulation now and

(Refer Slide Time: 02:33) that will give us a slightly different way to think about this. Now, so what we are here

(Refer Slide Time: 02:40) saying is that you know let us say I have some w right. So, let us say this algorithm outputs

(Refer Slide Time: 02:47) a w and now why did this algorithm output a w that will that w had the largest gamma what

(Refer Slide Time: 02:54) does that mean that means that the w first of all satisfies w transpose x i y i is greater

(Refer Slide Time: 02:59) than or equal to gamma for all the data points which means that let us say gamma was some

(Refer Slide Time: 03:04) value 5. So, which means that this is the line set of all x such that w transpose x

(Refer Slide Time: 03:11) equals 5 and this is the lines the set of all x such that w transpose x equals minus

(Refer Slide Time: 03:17) 5. So, which means that this algorithm is now going to say well here is the w which

(Refer Slide Time: 03:21) is the answer to this problem and the gamma corresponding to this w is let us say 5 right.

(Refer Slide Time: 03:26) So, this is what the algorithm outputs let us say now this equation is w transpose x

(Refer Slide Time: 03:34) equals 5. The moment you tell me that here is the w and this is the corresponding gamma

(Refer Slide Time: 03:40) now what I can argue is that look at the corresponding w which is you know let us say 2 times w transpose

(Refer Slide Time: 03:50) x equals 2 times 5 if every x in the on the line satisfies w transpose x equals 5 then

(Refer Slide Time: 03:59) every x on the line also satisfies 2 times w transpose x equals 10 naturally right. So,

(Refer Slide Time: 04:05) it is just scaling both sides left and right by 2. So, this is also true now this means

(Refer Slide Time: 04:10) that now here is another w which is w dash transpose x equal to 10 where w dash has the property

(Refer Slide Time: 04:18) that it classifies it linearly separates the status set with margin 10 right. So, with gamma

(Refer Slide Time: 04:23) is 10. So, which means that if you had given me w and 5 as the answer and claim that that

(Refer Slide Time: 04:28) is the answer to this problem now I am I am saying that that cannot be the answer because

(Refer Slide Time: 04:33) you can scale w by 2 times and then the gamma also scales up right. So, which means that

(Refer Slide Time: 04:37) now you can keep scaling w infinitely such that the gamma can grow up to infinity. So,

(Refer Slide Time: 04:42) which means that if I solve only this problem it is not sufficient because the issue is that

(Refer Slide Time: 04:48) we can scale can scale w arbitrarily. So, this is not going to be a useful formulation

(Refer Slide Time: 04:56) so this is not going to be a useful formulation because w can grow arbitrarily.

(Refer Slide Time: 05:02) So, we have to you know ground w how can we do that well one simple way to do that would be to

(Refer Slide Time: 05:08) you know just say like how we did in the perceptron assumption that we are not going to allow all

(Refer Slide Time: 05:14) w's we are only going to allow w's which have length 1 which means that our modified formulation

(Refer Slide Time: 05:20) is going to be maximize over w and gamma gamma such that w transpose x i into y i is greater than

(Refer Slide Time: 05:29) or equal to gamma nothing changes so far. But then we are only going to allow w such that norm

(Refer Slide Time: 05:35) of w's 1 right. So, which means that I cannot scale w right so the moment I do w to 2 w then

(Refer Slide Time: 05:42) the length of w changes it the norm squared kind of becomes 4 times right. So, because I have

(Refer Slide Time: 05:50) scaling w by 2 the norm squared becomes multiplied by 2 squared which is 4. So, it is no longer going to be

(Refer Slide Time: 05:56) 1. So, which means that that 2 times w is not going to satisfy this condition so that we cannot

(Refer Slide Time: 06:01) just arbitrarily scale right. So, this is a possible solution to this problem right. So, we can try to

(Refer Slide Time: 06:06) solve this problem and then we will get some solution right. So, this is a reasonable formulation

(Refer Slide Time: 06:13) to solve this problem. But now I mean one can definitely solve this problem that and and using

(Refer Slide Time: 06:22) optimization techniques and you will get a w and gamma that is no doubting that.

(Refer Slide Time: 06:27) But one can ask if we really have to have these two variables in this formulation there are two

(Refer Slide Time: 06:34) variables that we are maximizing over w and gamma. Whereas, if you really see right so

(Refer Slide Time: 06:41) you are only searching for w's with length with unit length right. So, which means that in

(Refer Slide Time: 06:47) two dimension what this means is we are we are just looking for w's just yeah. So, we are just

(Refer Slide Time: 06:58) looking for w's with length you know 1 right. So, now if you have a data set let us take another

(Refer Slide Time: 07:08) data set simple data set let us say plus plus plus plus minus minus minus minus. Now,

(Refer Slide Time: 07:18) let us say we are only looking for w's in the unit circle on the unit circle maybe this is a w.

(Refer Slide Time: 07:24) Now, the moment I fix this w which means that I am fixing the direction the length is fixed in

(Refer Slide Time: 07:29) that direction. What happens is with respect to this data set the moment that the direction is fixed

(Refer Slide Time: 07:36) the length is fixed because we are only looking for length 1 the gamma corresponding to this is fixed.

(Refer Slide Time: 07:42) The data set will decide what the gamma is for this w let us call this w 1 the gamma is going to be

(Refer Slide Time: 07:49) you know what is the equation of this line right. So, set of all x such that w 1 transpose x equals

(Refer Slide Time: 07:55) maybe 5 right. So, if it is 5 then 5 is the gamma. So, similarly I can search for a w in this

(Refer Slide Time: 08:01) direction of length 1 which means that this would be my separator and again the data set will

(Refer Slide Time: 08:06) tell me what the gamma is the gamma is in this case is going to be this the equation of this line

(Refer Slide Time: 08:12) which is the set of all x such that maybe this is w 2 w 2 transpose x equals 3 right. So,

(Refer Slide Time: 08:18) maybe this is my this is my gamma. So, the gamma is in fact a function of your w the moment I

(Refer Slide Time: 08:24) fix w the gamma is fixed. Now, what we are doing in the previous formulation is that we are

(Refer Slide Time: 08:30) maximizing over both w and gamma, but then gamma is just a function of w. Now,

(Refer Slide Time: 08:36) what the way we got rid of the problem that w can be scaled arbitrarily is by grounding w length

(Refer Slide Time: 08:42) of w 2 b 1. The other way to solve the same problem is to say that well I am not going to only

(Refer Slide Time: 08:49) search for w's which have length 1 I am now I am going to throw that away right. So, I am going

(Refer Slide Time: 08:56) to say that I do not have the condition that norm of w square is equal to 1, but the moment I

(Refer Slide Time: 09:02) throw that condition away I can scale w arbitrarily right. So, which means to increase gamma,

(Refer Slide Time: 09:08) but now what I am going to say is that I am going to ground gamma I am going to say that well gamma

(Refer Slide Time: 09:15) is always going to be equal to some constant for example, constant is 1 right. So, what does that mean?

(Refer Slide Time: 09:21) That means that you know I am still going to search in each direction, but now the way it will

(Refer Slide Time: 09:29) look this picture will look is as follows right. So, this picture for the same data set is going

(Refer Slide Time: 09:34) to look like this. The data set is the same nothing has changed about the data set it is still

(Refer Slide Time: 09:39) the same data set. Now, if I look if I want w 1 in this direction now what I am saying is that

(Refer Slide Time: 09:49) so this w 1 has this line as let us say set of all x such that w 1 transpose x equals 5 this was

(Refer Slide Time: 09:59) our earlier w 1. Now, this w 1 I will not allow in my set of feasible w's I am only going to allow

(Refer Slide Time: 10:06) w 1 w such that the gamma is exactly 1. Now, I can always get a w such that gamma is exactly 1 right.

(Refer Slide Time: 10:18) So, if I find a direction which separates my data set positive from the negatives correctly,

(Refer Slide Time: 10:22) then I know that I can scale my w 1 to make sure that my gamma is always 1. For example, in this case,

(Refer Slide Time: 10:29) I can always set w 1 divided by 5 transpose x is equal to 1. This is also the equation of the

(Refer Slide Time: 10:35) line set of all x such that w 1 by 5 transpose x equals 1. Now, I can say that this is my w 1

(Refer Slide Time: 10:42) prime which satisfies w 1 prime transpose x equals 1 right. So, in other words, I now have to

(Refer Slide Time: 10:49) scale down this w to this point right. So, in this direction well this would be w 1 dash and now,

(Refer Slide Time: 10:56) with respect to this w 1 dash the same line will have gamma is 1 right. So, which means that the

(Refer Slide Time: 11:04) moment I find a direction which separates my positive from the negatives now I can scale the

(Refer Slide Time: 11:08) direction correspondingly such that these lines which I mean on which the data I can push my data,

(Refer Slide Time: 11:16) I mean I can push the lines parallel to this line passing through origin as much as possible such

(Refer Slide Time: 11:22) that it fits the data points on either side. I can always scale my w such that these lines

(Refer Slide Time: 11:29) satisfy the equation that w transpose x equals 1 and other side w transpose x equals minus 1.

(Refer Slide Time: 11:35) Now, because I can do this now I do not have to worry about gamma I can simply say that I will

(Refer Slide Time: 11:43) always set gamma to be 1 I will I am only going to be searching for w such that such a w will give me

(Refer Slide Time: 11:50) lines which are parallel to the line passing through origin but then with gamma equals 1.

(Refer Slide Time: 11:56) Now, if the moment I have grounded gamma now it becomes a question of what am I trying to maximize

(Refer Slide Time: 12:02) earlier I was trying to maximize gamma now because I am saying that I am only going to search for

(Refer Slide Time: 12:06) w such that gamma is 1 now what am I trying to maximize right. So, I now have to maximize this

(Refer Slide Time: 12:13) you know this width because that is what I am trying to you know make it as large as possible.

(Refer Slide Time: 12:19) Earlier we said we were saying that will that width when you fix w as 1 the length of w as 1 well

(Refer Slide Time: 12:25) that width was just gamma is what we were maximizing. Now, the gamma is 1 so this width somehow has

(Refer Slide Time: 12:31) to depend on the length we will see what that is in a minute but just to complete this argument

(Refer Slide Time: 12:35) right. So, the same thing with respect to w 2 right. So, we now let us say if we start with w 2 here

(Refer Slide Time: 12:43) that would give me the you know light blue separator you know this would become my separating

(Refer Slide Time: 12:50) these would become my separating lines. Now, this line if this had x such of set of all

(Refer Slide Time: 12:57) x such that w 2 transpose x equal to 3 now then I have to you know scale this by by a factor of

(Refer Slide Time: 13:04) 3 to get w 2 dash right. So, this would be w 2 divided by 3 transpose x equals 1 the same line

(Refer Slide Time: 13:12) but then the equation is different for a different w now as you can see right. So, if I have a

(Refer Slide Time: 13:18) smaller width then what I am essentially doing is I am kind of scaling it by lesser right. So,

(Refer Slide Time: 13:27) I started with w 1 and w 2 with length 1 and then I scaled it correspondingly to make sure that

(Refer Slide Time: 13:32) these parallel lines have length have gamma equals 1. Now, the amount I should scale will

(Refer Slide Time: 13:40) will depend on you know how wide is this separation essentially basically depends on gamma.

(Refer Slide Time: 13:48) So, so basically now this will give me a different width the blue line will give me a different width

(Refer Slide Time: 13:53) the red line will give me a different width. Now, what we can then say is that you know we can say

(Refer Slide Time: 13:59) our modified formulation as follows you know we can say that we want to maximize only over w you

(Refer Slide Time: 14:07) know the width that w gives with respect to my data set such that w transpose x i into y i is greater

(Refer Slide Time: 14:17) than or equal to 1 for all. This is an equivalent formulation is what I am trying to say right. So,

(Refer Slide Time: 14:25) now as you can notice there is no gamma the gamma is gone out of this this formulation

(Refer Slide Time: 14:31) because we are grounding gamma but you can also notice that I am not restricting the length of

(Refer Slide Time: 14:35) w what is the saying is that I am going to allow any w which linearly separates my data set

(Refer Slide Time: 14:43) with a margin exactly equal to 1 right. So, with this gamma equals 1

(Refer Slide Time: 14:49) but now what I am going to maximize is this width right. So, this this width is this length

(Refer Slide Time: 14:55) between these two parallel lines we have to find what that width is but then what I am saying is

(Refer Slide Time: 15:01) that once we have found find that width as a function of w then all we have to do is that you know

(Refer Slide Time: 15:07) we have to maximize this width right. So, this is an equivalent formulation just that we need to

(Refer Slide Time: 15:12) now say what is this you know what does this width of w mean. The moment we have pinned down what

(Refer Slide Time: 15:18) is the formula for the width of w then we have a you know clean formulation. So, let us let us go

(Refer Slide Time: 15:25) I go ahead and try to find out you know what is the width of w in this case now how can we find

(Refer Slide Time: 15:31) the width of w. So, what is width of w well what is the width of w well what are what are we trying

(Refer Slide Time: 15:45) to find out. So, we we have some w I give you some w and I say that well this w you know divides

(Refer Slide Time: 15:53) I mean it is classifies my data set such that this is the line where w transpose x equals 1

(Refer Slide Time: 16:00) and this is the line where w transpose x equals minus 1 and now I am asking what is this width

(Refer Slide Time: 16:08) this the length between these two parallel lines how can we find the length between these two

(Refer Slide Time: 16:12) parallel lines well you can simply take any point on one of these lines and then ask the question

(Refer Slide Time: 16:21) well what is the closest point on the other side right. So, for this point this would be the closest

(Refer Slide Time: 16:27) point and then the distance between these two closest points is in fact the length between

(Refer Slide Time: 16:32) these parallel lines and this should be independent of which point I take if I take this point the

(Refer Slide Time: 16:36) closest point on other line other line would be this point and the length would be the same because

(Refer Slide Time: 16:41) these are parallel lines. So, I can actually set up a problem as follows right. So, I will want to

(Refer Slide Time: 16:45) find out minimize over some z let us say the norm this the distance between x and z square

(Refer Slide Time: 16:56) side such that you know let us call this x this would be over z such that w transpose x equals

(Refer Slide Time: 17:07) minus 1 that is you start sorry w transpose z equals minus 1 you start with a z which has the

(Refer Slide Time: 17:16) property that sorry. So, you start with an x which has the property that w transpose x equal

(Refer Slide Time: 17:23) to minus 1 right. So, x satisfies w transpose x equal to minus 1 right. So, this is a this is a

(Refer Slide Time: 17:30) property of x you are looking for z such that the distance between x and z is as small as possible

(Refer Slide Time: 17:36) such that w transpose z equals plus 1 right. So, you you want to find a z on the line w transpose

(Refer Slide Time: 17:46) this line right. So, this line such that w transpose z equals plus 1 and the distance

(Refer Slide Time: 17:54) from x to z should be as small as possible, but what should x satisfy x should satisfy

(Refer Slide Time: 17:58) w transpose x equals minus 1 right. So, now this is an optimization problem in itself right. So,

(Refer Slide Time: 18:03) to find this width now we can try to solve this optimization problem I would not really go

(Refer Slide Time: 18:08) further solving this exactly, but you can again solve this using something called as the method

(Refer Slide Time: 18:14) of Lagrange multipliers if you are aware of it you can try it out we will not do that here in

(Refer Slide Time: 18:20) detail, but what what you will essentially get is that I mean I can neither solve this or I can

(Refer Slide Time: 18:25) do half of this that does not matter because whichever I mean you can either minimize the distance

(Refer Slide Time: 18:33) distance squared or half of the distance squared does not really matter the exact point is going

(Refer Slide Time: 18:37) to be the same. The solution to this problem though is will turn out to be the width of w will be

(Refer Slide Time: 18:46) 2 divided by norm w square when I say width of w I am considering this quantity right. So,

(Refer Slide Time: 18:55) the half of the distance squared between these two points right. So, that is what I am trying to

(Refer Slide Time: 19:00) minimize and that quantity happens to be 2 over norm w square. So, this is basically the solution

(Refer Slide Time: 19:06) to this problem. Now, as you can see as a sanity check the first thing that you observe is that

(Refer Slide Time: 19:10) this value depends only on w and it does not depend on the exact x point that I care about right.

(Refer Slide Time: 19:17) So, because these are just this is just a distance between two parallel lines right. So,

(Refer Slide Time: 19:21) the distance between parallel lines should only depend on you know what decides that parallel

(Refer Slide Time: 19:25) lines and the only thing that decides that parallel lines is w not this x right. So, no matter where

(Refer Slide Time: 19:31) took the x right. So, if I take an x here this would be my z if I if I take an x here this would

(Refer Slide Time: 19:37) be my z if my value between the distance between this x and z cannot naturally depend on x or z

(Refer Slide Time: 19:44) right. So, it only has to depend on w and and a sanity check we observe that this width is in

(Refer Slide Time: 19:50) fact 2 over norm w square. So, which is good because now we can actually write down the entire

(Refer Slide Time: 19:58) formulation that we want which can be written as follows right. So, what we want to do now is

(Refer Slide Time: 20:04) maximize over w width of w which is 2 over norm w square such that w transpose x i into y i is

(Refer Slide Time: 20:14) greater than or equal to 1. So, this is our modified formulation now and now this is basically

(Refer Slide Time: 20:25) telling us that then if you go back to our previous picture it is basically telling us that you know

(Refer Slide Time: 20:32) if you have a large separator right. So, separator is large then the corresponding w will have

(Refer Slide Time: 20:41) smaller length right. So, why why is that because you know the width is inversely proportional to

(Refer Slide Time: 20:47) the length square of w and that is in fact you know if you if you pause and think about this for

(Refer Slide Time: 20:53) a second you will realize why that has to be true right. So, because if I if I take a w if it

(Refer Slide Time: 20:59) so, turns out that you know a w that with respect to a dataset a w that gives me the equation of

(Refer Slide Time: 21:13) this line as w transpose x equal to 1 and this as w transpose x equal to minus 1 versus you know

(Refer Slide Time: 21:21) the same for the same dataset if I have a different w which which gave me a very very small

(Refer Slide Time: 21:27) you know width. Now, this guy is w 2 transpose x equals 1 set of all x for for a w 2 right.

(Refer Slide Time: 21:37) Now, because this this the difference is small right. So, what should happen right. So, now we

(Refer Slide Time: 21:45) can ask the question how should the length corresponding to the w that induced this should be

(Refer Slide Time: 21:52) right. Because this line has to have the equation the w 2 transpose x equals you know 1

(Refer Slide Time: 22:00) now what what essentially we are saying is that the length should be inversely proportional to

(Refer Slide Time: 22:05) the width which means that if this width is small well why is this width small because the length

(Refer Slide Time: 22:12) of the w that produced this is actually large. Why is the length of the w that produced it large

(Refer Slide Time: 22:21) well because we are grounding gamma to be 1 right. So, on both sides gamma for both this

(Refer Slide Time: 22:27) equation and this equation the gamma is now grounded to be 1. So, which means that you want

(Refer Slide Time: 22:35) you know set of all x such that w 2 transpose x equals 1 if the width is small if I

(Refer Slide Time: 22:42) told you that the width is small you know then the length of x you know should be so the set of

(Refer Slide Time: 22:49) all x that satisfies this are all here right. So, these guys the length of these guys are going to

(Refer Slide Time: 22:55) be smaller right. So, because they have to you know make this value as 1 right. So, which means

(Refer Slide Time: 23:00) that if the width width is small then the length of x's are smaller when compared to the x that you

(Refer Slide Time: 23:08) would get in the same direction for for the one which I with a larger width if the length of x is

(Refer Slide Time: 23:15) small but then the right hand side is 1 then the only way you can make the right hand side 1 is

(Refer Slide Time: 23:19) is if you make the length of w itself large right. So, here x in any fixed direction the length of

(Refer Slide Time: 23:26) x is small because the width is small and so to compensate for the smaller x your w should have

(Refer Slide Time: 23:33) longer length right. So, on so w 2 will have a longer length and w. So, basically then what we

(Refer Slide Time: 23:38) are essentially asking now is that if you want to maximize the width with respect to a particular

(Refer Slide Time: 23:43) direction which linearly separates the data then it is equivalent to minimizing the length or

(Refer Slide Time: 23:50) length squared of that particular w. So, and that is also true you can just look at this

(Refer Slide Time: 23:57) equation and argue why that is true because you want to maximize 2 divided by norm w squared which

(Refer Slide Time: 24:02) is equivalently equivalently you can say that you want to minimize over w half norm w squared

(Refer Slide Time: 24:16) such that w transpose x i into y i is greater than or equal to 1 right. So, you can either

(Refer Slide Time: 24:27) put post this is a maximization problem where you are trying to maximize the width or you

(Refer Slide Time: 24:32) can post this is a minimization problem where you are trying to minimize the length of w because

(Refer Slide Time: 24:37) the length of w is exactly you know if you will end to the when minimizing the length of w

(Refer Slide Time: 24:44) length squared of w is equal and to maximizing the width of that w gives you with respect to the

(Refer Slide Time: 24:49) dataset ok. So, basically what we have now done so far is the following just to summarize right.

(Refer Slide Time: 24:56) So, we wanted to find the w such that the w separates our datasets with as high a margin as

(Refer Slide Time: 25:04) possible. Now, what we are essentially saying is that well it is equivalent to finding a w with

(Refer Slide Time: 25:10) as small a length as possible such that w transpose x i y i is greater than or equal to 1 for all i

(Refer Slide Time: 25:18) right. So, for all i right. So, so this is our first formulation that we have right.

(Refer Slide Time: 25:26) Now, if you solve this problem so now the question is ok. So, we have set up the problem right. So,

(Refer Slide Time: 25:30) all this that we have discussed so far is to figure out you know what is the problem that we want

(Refer Slide Time: 25:35) to solve and we have arrived at the conclusion that this is the problem that we want to solve

(Refer Slide Time: 25:40) now the w that comes out of it will have the property that it will separate our dataset with

(Refer Slide Time: 25:45) you know as large a width as possible. Now, if such a w exists right. So, because if your dataset

(Refer Slide Time: 25:53) is not linearly separable then you know no w will satisfy the constraints that we have put down.

(Refer Slide Time: 25:59) So, this algorithm will just say that well there is no feasible solution. But if there is a

(Refer Slide Time: 26:04) feasible solution then you will in fact find such a w with with with the largest possible width right.

(Refer Slide Time: 26:11) So, so this is the problem that we want to solve right. So, now we can solve it in different ways

(Refer Slide Time: 26:18) for instance you can use gradient based approaches what are called as projected gradient

(Refer Slide Time: 26:23) descent based methods for instance to solve this problem and so on. We want really worry so

(Refer Slide Time: 26:28) much about you know the exact algorithm at this point to solve this problem. But what we would

(Refer Slide Time: 26:33) be interested in is to understand you know what are what what what what what insights can be derived

(Refer Slide Time: 26:41) from this problem right. So, right now we have a we have a clean optimization objective

(Refer Slide Time: 26:47) constraint optimization problem that we want to solve. Now, what we want to do is you know

(Refer Slide Time: 26:53) understand you know any other insights that we can draw from this optimization problem.

(Refer Slide Time: 27:00) And typically when you are solving an optimization problem one way to derive you know reasonably

(Refer Slide Time: 27:06) insights about the problem itself is to derive what is called as a dual problem to the original

(Refer Slide Time: 27:13) problem the primal problem that you would want to solve which is just another way of looking at

(Refer Slide Time: 27:19) the same optimization problem. But typically that if you look at it in a different way

(Refer Slide Time: 27:25) you might gain some more insights about the what is going on and that might lead us to you know

(Refer Slide Time: 27:29) more stronger algorithms. So, what we are going to do now is to say that well here is a problem

(Refer Slide Time: 27:35) here is an optimization problem which you can solve and then you will get a W which maximizes the

(Refer Slide Time: 27:39) width and we can be happy with that. But then you know this is only going to solve a problem

(Refer Slide Time: 27:47) which is linearly separable. So, it is not clear how to you know adopt this problem and the data

(Refer Slide Time: 27:54) is not linearly separable or if the data has you know maybe a quadratic decision boundary and

(Refer Slide Time: 28:00) things like that. So, what we are going to ask ourselves is that can we look at the same problem

(Refer Slide Time: 28:05) in a slightly different way and see if that is providing us some more context about this problem.

(Refer Slide Time: 28:10) And what we are going to do next is exactly that we are going to start with this problem.

(Refer Slide Time: 28:16) And then you know convert this into a different problem equivalent different problem which will

(Refer Slide Time: 28:23) provide us very strong insights about the algorithm or about the formulation itself right. So,

(Refer Slide Time: 28:29) on that will be called as the dual problem for this problem which is what we will start looking at next.
