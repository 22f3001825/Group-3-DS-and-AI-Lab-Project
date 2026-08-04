# Week-10 - Lecture 3

(Refer Slide Time: 00:00) Hello, welcome back. So we are looking at supervised learning and specifically we are looking

(Refer Slide Time: 00:19) at final classification and we started looking at algorithm which tried to maximize the

(Refer Slide Time: 00:26) margin given a set of data points and find the linear classifier. So specifically we came

(Refer Slide Time: 00:33) up with the following formulation where given a set of data points we wanted to find a w in the dimension

(Refer Slide Time: 00:42) such that the length of w is as small as possible such that the w is actually classifying the set of data

(Refer Slide Time: 00:51) points with margin 1. Now we argued that the length being small is equivalent to being the

(Refer Slide Time: 00:58) quick produced by the parallel line that corresponds to margin equals 1 is large. It is also your

(Refer Slide Time: 01:03) naturally looking for classifiers or lines which have a smaller length. Now we said that well we

(Refer Slide Time: 01:12) can solve this problem using the different gradient based techniques and that might give us some

(Refer Slide Time: 01:17) solution. But what we want to do is to look at the same problem in a slightly different way so

(Refer Slide Time: 01:23) that we understand this in a different differently so that it will help us derive what is called as

(Refer Slide Time: 01:29) a dual problem for this problem from which we can derive more insights into the understanding of insights

(Refer Slide Time: 01:35) into the problem itself and further our understanding and probably try to improve the algorithm.

(Refer Slide Time: 01:43) So for this we are going to do a slight small detour to understand this concept in more

(Refer Slide Time: 01:51) generality and then we will talk about specifically what it applies to this problem. So let us call this problem A for the

(Refer Slide Time: 01:57) moment we will come back to this problem in a minute. But now what we are going to look at is you know you want to

(Refer Slide Time: 02:03) minimize some function f of w such that g of w is less than or equal to 0. Note that the problem that we

(Refer Slide Time: 02:12) have is of this form so here we have some function f of w. Now g of w is not less than or equal to 0 it is

(Refer Slide Time: 02:21) greater than or equal to 1 but then you know you can change it to a proper form such that it is less than or equal

(Refer Slide Time: 02:27) to 0. Now again note that in the problem that we have there are many constraints there are n constraints

(Refer Slide Time: 02:33) corresponding to n data points that we have whereas what we are going to first start looking at is just

(Refer Slide Time: 02:39) the case of one constraint and then we will see how the ideas also translate in the case where you have more

(Refer Slide Time: 02:44) constraints. So now what we are going to do is we want to solve this problem. So minimize type of w that

(Refer Slide Time: 02:52) is the value that is at g of w is less than or equal to 0. We are going to come up with a different way to

(Refer Slide Time: 02:59) solve this problem and we will see why that phase is useful especially in the case that we are looking at.

(Refer Slide Time: 03:04) So the way is to first define what is called as a function new function l which is called sometimes the

(Refer Slide Time: 03:10) Lagrangian function which is a function of two variables w and alpha and is defined as f of w plus alpha

(Refer Slide Time: 03:20) g of w where alpha is some real number. So it is basically what you are doing is that the objective

(Refer Slide Time: 03:28) function f of w is still intact. Now the constraint function becomes part of the objective itself. So it is f of w plus

(Refer Slide Time: 03:35) some alpha times f of w. Now why do we care about this function? How is this function even related to the

(Refer Slide Time: 03:41) original function? Well let us try to understand that. So now fix any w let us say I give you a w. So you fix this

(Refer Slide Time: 03:49) w and I ask you to consider the following quantity. So consider maximum over alpha greater than or equal to 0

(Refer Slide Time: 04:01) l of w comma alpha that is consider maximum over alpha greater than or equal to 0 f of w plus alpha g of w.

(Refer Slide Time: 04:14) Now I ask you the question what value can this function take? So remember I gave you a w maybe w equals 1 2 3 4

(Refer Slide Time: 04:27) so that is vector. Now I am asking you to maximize a different quantity with respect to alpha greater than or equal to 0.

(Refer Slide Time: 04:34) Now how will this quantity value look like? Well there are two cases to consider here. So now let us look at the first

(Refer Slide Time: 04:43) case where g of w is greater than 0. Let us say I gave you a w remember and that w has some

(Refer Slide Time: 04:53) above w value some g of w value. So it has some objective value it has some constraint value also which is which are

(Refer Slide Time: 05:00) evaluated at above w and g of w. Now let us say for the w that I gave you it so happens the g of w greater than 0 maybe

(Refer Slide Time: 05:07) g of w is 5 right so it is a positive quantity strictly positive quantity. Now how big can you make this function now?

(Refer Slide Time: 05:15) Let us say I gave you a w for which f of w and you are looking at f of w and g of w you realize f of w is

(Refer Slide Time: 05:24) maybe minus 100 and g of w is 5 for example right. So for the w that I gave you maybe the w is 1 2 3 4

(Refer Slide Time: 05:31) d is 4 dimensional this is the w that I gave you. Now what I am asking then is you know you want to maximize over

(Refer Slide Time: 05:38) alpha greater than 0 minus 100 plus alpha times but alpha is some positive quantity or a non-negative quantity.

(Refer Slide Time: 05:47) I can put any non-negative quantity here but then I want to push this value that the sum as high as possible.

(Refer Slide Time: 05:54) Now how high can I push this? Well if you look at this right so if I say alpha equals 1 then this value is you know for alpha 1 this is

(Refer Slide Time: 06:03) minus 95 for alpha equals 10 this is minus 100 plus 10 into 5 15 which is minus 50 if alpha equal to 100 then this is

(Refer Slide Time: 06:12) minus 100 plus 100 into 5 which is 400 500 minus 100 is 400 and so on. So as I increase alpha it looks like I can push this value as high as I want

(Refer Slide Time: 06:22) right. So on that is that is true because because I have fixed the w f of w some fixed number it can be as small as you want but then it is a fixed

(Refer Slide Time: 06:31) number it is not going to change as I change alpha. On the other hand this guy is going to change as I change alpha and because g of w is

(Refer Slide Time: 06:38) positive now and I am allowed to choose alpha which are greater than or equal to 0 I can make alpha arbitrarily large and the whole thing

(Refer Slide Time: 06:46) goes arbitrarily large positive quantity which means that I can push this whole quantity to be infinite which means if the w that I gave you had the property that g of w is greater than 0 then you can

(Refer Slide Time: 07:01) use this function evaluates to infinity. Now we will see why that is useful in a minute but now let us also look at the case where g of w is less than or equal to 0 right.

(Refer Slide Time: 07:12) So now here is another case where g of w is less than or equal to 0 let me put a box here.

(Refer Slide Time: 07:20) Now in this case maybe w is maybe you have a different w w is 3 4 5 6 now f of w here is minus let us say f of w is 100 and g of w is minus 5.

(Refer Slide Time: 07:39) Now what I am trying to maximize is earlier it was minus 100 plus 5 alpha now it is 100 minus 5 alpha. Now again I am only allowed to have non negative alpha right.

(Refer Slide Time: 07:51) So if I say alpha equals 1 this value is 100 minus 5 alpha is 95 if I say alpha equals 10 this value is 50 right.

(Refer Slide Time: 08:01) So the value actually goes down at the increase alpha right. So because of this negative sign of course I cannot set alpha is negative because I am only allowed to maximize alpha or greater than or equal to 0.

(Refer Slide Time: 08:10) So how how much can I increase this well I can always set alpha equals 0 to get 100 minus 0 which is 100 right.

(Refer Slide Time: 08:18) Any positive alpha is going to only reduce this one so the maximum value that I can get is actually 100 only which is f of w.

(Refer Slide Time: 08:28) So which means that if g of w is less than or equal to 0 then this function evaluates to because alpha is greater than or equal to 0.

(Refer Slide Time: 08:35) Well if g of w is strictly less than 0 I will just set alpha is 0 to make this value equal to f of w.

(Refer Slide Time: 08:42) If g of w is equal to 0 then does not matter what alpha is said this values for the second term is always going to be 0 the first term will be f of w.

(Refer Slide Time: 08:50) So in both the cases this term is going to be f of w if g of w is less than or equal to 0 right.

(Refer Slide Time: 08:56) So what then happen is that something interesting has actually happened right.

(Refer Slide Time: 09:01) So now here is a new function which if I give you a w if the w satisfy g of w less than or equal to 0 then this new function evaluates to f of w.

(Refer Slide Time: 09:13) If the w does not satisfy g of w less than or equal to 0 that is satisfy g of w greater than 0 then this function evaluates to infinity.

(Refer Slide Time: 09:21) Now in so to get a feel for this imagine this picture right.

(Refer Slide Time: 09:26) So maybe this is our space of w right. So this is w maybe w is a two dimensional vector w 1 and w 2 are two components.

(Refer Slide Time: 09:35) And now here is the space this is the set of all possible w's for which let's say g of w is less than or equal to 0 right.

(Refer Slide Time: 09:48) So let's let's consider this shaded region.

(Refer Slide Time: 09:55) Now what we are saying essentially is that now if if I give you a w here right to w equals w 1 w 2 here right.

(Refer Slide Time: 10:04) So w 1 this is w 2 if I give you this w then the function max of alpha greater than or equal to 0 f of w plus alpha g of w evaluates to g of w right.

(Refer Slide Time: 10:18) So at this point if I ask the functions value that value is going to be g of w at this point the functions value is sorry at this point the functions value is going to be f of w.

(Refer Slide Time: 10:31) Why because that's that's the argument that we may if g of w is less than or equal to 0 then the function evaluates to f of w.

(Refer Slide Time: 10:38) So let me also say what the shaded region is the shaded region is the set of all w such that g of w is less than or equal to 0.

(Refer Slide Time: 10:45) Inside this whenever I give you a point it will evaluate to the corresponding function f of w on the other hand if I give you a w outside this for which g of w is greater than 0 then it will evaluate to infinity right.

(Refer Slide Time: 11:01) So which means that there is a region where the function evaluates to some finite value which is f of w and outside the region it kind of goes to infinity.

(Refer Slide Time: 11:09) So that's the kind of function this guy right so as if you think of this as a function of w right so now how can we use this function of w well we can do the following now if I want to find the minimum value right so for every w I know what this function evaluates to either evaluates f of w or infinity.

(Refer Slide Time: 11:30) Now if I want to find that w where this function takes the smallest value right so I want to minimize over w maximize over alpha greater than 0 f of w plus alpha g of w this is what I care about then what does this mean this means that well here it's the black box right which is this function where if I give a w if evaluates to f of w if w satisfies g of w equal 0 now it is another w may be.

(Refer Slide Time: 11:59) W may be w 2 which will evaluate to infinity because g of w 2 was greater than 0 here g of w 1 was less than or equal to 0 now I am trying to give different values of w is input and t which one gives me the smallest value now there will be some w for which this value will be smallest and necessarily that w has to be somewhere here right so inside this shaded region that is w start.

(Refer Slide Time: 12:26) Why because outside this shaded region this function evaluates to infinity inside this shaded region it evaluates to f of w and so this w star has the property that among all w's which are in the shaded region it has the smallest value but what are the w's which are in the shaded region which are exactly the w's for which g of w is less than or equal to 0 which means that if I try to find the minimum over w maximum over alpha greater than or equal to 0 f of w plus alpha g of w this is e.

(Refer Slide Time: 12:56) So, we will find the value which minimizes f of w in the shaded region where g of w is less than or equal to 0 now this was the original problem that we wanted to solve what we are saying is that you can either solve the original problem or you can solve this min max problem both are equivalent right so this is these two are exactly the same this will give you the exactly the same answer that is what we have seen so far right so let me let me.

(Refer Slide Time: 13:26) Let me note that down right so let's let's call this you know the now this is a nice equivalent basically you have written a minimization problem a constraint minimization problem as a min max problem now the question arises is you know when you have a min max problem one one can ask the question you know can we swap min and max

(Refer Slide Time: 13:56) in this is the first question we will ask the so basically in other words I am asking if I look for the function I will of course you can always swap but the question is if you swap then does it affect the final answer right so can we swap and not affect the final answer is what we are actually that is instead of saying min over w max over alpha greater than or equal to 0 something can I look at max over alpha greater than or 0 min over w something the same thing

(Refer Slide Time: 14:25) it's a do do these things are these things the same thing so will they evaluate to the same value well in general they do not necessarily have evaluate to the same value in general the answer is no you cannot swap the min and max and I hope that they evaluate to the same value but if f and g are nice functions

(Refer Slide Time: 14:49) or nice functions well by nice I mean in our context convex functions then yes you can in fact swap these two things right so then this is a very fundamental result in convex optimization called convex duality result we won't prove this result but those were interested should look at a convex optimization course or convex optimization book where this result would be proved if f and g are convex

(Refer Slide Time: 15:18) convex then this is swapping is allowed right so which means that what that that essentially tells us that then it's that so I can either solve min over w max over alpha greater than 0 f of w plus alpha g of w either I can solve this problem or I can solve max over alpha greater than 0 min over w f of w plus alpha g of w

(Refer Slide Time: 15:48) I will get the same answer no matter I solve which one right which of either of right so but then this holds only for convex f and g we have already seen what convex functions are right so for our purposes the most important convex functions that we will encounter at least in this particular algorithm that we have been looking at or you know this includes quadratic function

(Refer Slide Time: 16:16) these includes mean a function these are all convex functions so you can very well assume that this statement that I made holds for quadratic function and linear function and that's all you need for our understanding for this point now again the original problem that we started looking at just had one constraint right so this was the original problem we just had one constraint but very similar ideas carry over for multiple constraints

(Refer Slide Time: 16:45) also let me make a note of that right so for multiple constraints the same kind of ideas fall through which is you know let's say you wanted to solve min over w f of w such that let's say there are g i of w less than or equal to 0 for all i so there are multiple constraints g 1 of w g 2 of w and so once until g k of w

(Refer Slide Time: 17:13) whatever k is my b that's we have k different constraints right so and you have this problem that you want to solve now this is equivalent to you know solving min over w now max over now because there are multiple constraints you will have to have an alpha corresponding to each of these constraints right so you will have alpha 1 dot dot alpha k if there are k constraints let me make that number 3 equals 1 to k so you have k different alpha

(Refer Slide Time: 17:42) and again the function itself is the same right so f of w but now because there are k different alpha this will be alpha 1 g 1 of w plus alpha 2 g 2 of w plus dot dot dot plus alpha k g k of w this would be our modified function this will be the min max problem that these guys will be equal to but then you will not allow all alpha you have to make sure that each of these alpha is created another way to solve this problem

(Refer Slide Time: 18:12) and then you will not be equal to 0 right so you are only searching in this phase of alpha greater than or equal to 0 you can do an exactly the same argument like how we did even if one of these constraints is not satisfied then you can make this quantity go up to infinity whereas if all the constraints are satisfied then this quantity will exactly evaluate f of w the same argument that we did earlier but then now it holds for multiple constraints so now again if f and all the g's are convex then this is also equivalent to the

(Refer Slide Time: 18:42) maximizing over you know alpha 1 greater than or equal to 0 dot dot alpha k greater than or equal to 0 minimizing over w f of w plus alpha the same thing if you know w plus dot dot alpha k g k f.

(Refer Slide Time: 19:07) So, this again is convex to a right so I just wanted to because our problem has multiple constraints we should also see the multiple constraints version of it right so now let's let's map this understanding to our problem and see if it helps it so at this point it doesn't really it's not clear why they should help us right so because we originally wanted to solve a minimization problem with some

(Refer Slide Time: 19:27) constraints we converted it into a min max and now we are saying that well you can either solve the min max or you can solve the max min that doesn't at least at least first glance it does not look like it has made our problem any easy to solve right so we need to argue why this might be a useful thing to even look at for our case so let's try to you know see what benefit do we get if we do this for our problem.