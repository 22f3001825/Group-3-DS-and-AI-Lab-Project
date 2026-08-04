# Week-9 - Lecture 3

(Refer Slide Time: 00:00) So, so to prove this you know we want to make two other small you know very innocuous

(Refer Slide Time: 00:21) assumptions. So, this is assumption number 1 which is linear separability with gamma

(Refer Slide Time: 00:25) margin. We are going to make two more assumptions, but as you will see these are not really assumptions

(Refer Slide Time: 00:29) they are they are just simplifications. So, to say the second one is what is called

(Refer Slide Time: 00:35) as the the radius assumption. So, we can work without the second and the third assumption

(Refer Slide Time: 00:43) that I am going to put down and still prove convergence, but it might make things easier

(Refer Slide Time: 00:48) and easier to you know work with if you make these assumptions right. So, the math becomes

(Refer Slide Time: 00:54) slightly easier to analyze. I mean the other ways you just have to carry on a few extra

(Refer Slide Time: 00:58) terms which we are trying to avoid. So, what is the radius assumption? The radius assumption

(Refer Slide Time: 01:02) says that for every point in my dataset the length of my the Euclidean norm is at most some

(Refer Slide Time: 01:11) or radius r right. So, for some r greater than 0. Well all this is saying is that you

(Refer Slide Time: 01:22) know you have a finite dataset and all the data points fall within a ball of some radius

(Refer Slide Time: 01:27) r. This is obviously true because if you have 100 data points there is one data point which

(Refer Slide Time: 01:32) is going to have the highest length and now if I put a ball Euclidean ball of radius

(Refer Slide Time: 01:37) equal to the length of that data point then all the data points will fall within that ball

(Refer Slide Time: 01:42) right. So, for example if I had a dataset like this you know maybe I have a bunch of points

(Refer Slide Time: 01:47) here here here here maybe there are some red points here. Now, I can look at the length

(Refer Slide Time: 01:53) of each point and then I will realize that in this particular example I have taken this

(Refer Slide Time: 01:58) guy has the longest length. So, which means that if I put a Euclidean ball of radius

(Refer Slide Time: 02:03) equal to this guy's length of course I have not drawn the ball carefully but yeah. So,

(Refer Slide Time: 02:07) if this is r then it means that all the points the length of every point will be less than

(Refer Slide Time: 02:12) or equal to r right. So, by definition because I have taken the largest point so I can I

(Refer Slide Time: 02:17) am just assuming that there is this r right. So, for any finite dataset this is going

(Refer Slide Time: 02:21) to be true right. So, this is what is called as a radius assumption just that there is

(Refer Slide Time: 02:28) a big ball of radius r within which all my data points are right. So, this is assumption

(Refer Slide Time: 02:35) number 2 well more than assumption it is a simplification. The third one is also a simplification

(Refer Slide Time: 02:40) but it needs a slightly careful understanding you know without loss of generality we can

(Refer Slide Time: 02:51) assume norm of W star is 1. Well what is W star? Well W star is this guy which separates

(Refer Slide Time: 03:01) my dataset with margin gamma. Now, I am saying that W star's norm is actually 1. Now, what

(Refer Slide Time: 03:07) does this even mean right. So, it means the following. So, again we have this dataset where

(Refer Slide Time: 03:14) let us say we have this positive points and then there are these negative points here.

(Refer Slide Time: 03:20) And let us say we have a W which is like this which separates the positives from the negatives

(Refer Slide Time: 03:29) using some gamma margin which means that no. Now, this may be I will put a positive point

(Refer Slide Time: 03:36) here. Now, this is this is a W and this is the set of all x such that W transpose x

(Refer Slide Time: 03:46) equals gamma of course, this is the set of all x such that W transpose x equal to minus

(Refer Slide Time: 03:52) gamma and all my data points are on both sides. But now, I observe that this W's length

(Refer Slide Time: 03:57) is not 1 right. So, maybe let us call this W star right. So, this W star's length is not

(Refer Slide Time: 04:03) 1 because the set of all W's whose length is 1 is let us say somewhere here right. So,

(Refer Slide Time: 04:11) maybe this is the set of all W's with length 1. Now, what I am saying is that well if you

(Refer Slide Time: 04:20) give me a W star such that it separates my dataset linearly with some margin gamma.

(Refer Slide Time: 04:26) Now, I can find another W star whose length is 1 which also separates my dataset linearly

(Refer Slide Time: 04:32) with some other gamma which is still not negative not 0 right. So, where is that gamma? Well,

(Refer Slide Time: 04:39) I can pick that gamma that W star in this the same direction, but then if I just normalize

(Refer Slide Time: 04:47) it to have length 1. Now, think of this as my new W star let us call this W star hat not

(Refer Slide Time: 04:55) maybe not hat I will just call this W star dash. Now, what is W star dash? Well, with respect

(Refer Slide Time: 05:01) to this W star dash well the original with respect to the original W star this lines equation

(Refer Slide Time: 05:07) was W star transpose x equal to gamma. Now, if I do W star transpose x divided by norm

(Refer Slide Time: 05:13) W star on both sides well norm W star is a positive quantity. So, I can that will not affect

(Refer Slide Time: 05:19) the equation the equation still stays the same. Now, but then what I can now do is it is

(Refer Slide Time: 05:24) the same line, but now I can write this as W star by norm W star transpose x equal to

(Refer Slide Time: 05:33) gamma dash where gamma dash is gamma by norm W star. So, basically the gamma is we scaled

(Refer Slide Time: 05:42) I got a new gamma gamma dash and now with respect to now if I rename this W star by norm

(Refer Slide Time: 05:48) W star as W star dash now this transpose x equal to gamma dash. Remember it is the same

(Refer Slide Time: 05:54) line I am not changing the line I am changing the equation of the line by scaling on both

(Refer Slide Time: 05:58) sides. It is like saying that if y equals m x plus c is my original line then so is 2

(Refer Slide Time: 06:05) y equals 2 m x plus 2 c right. So, I can multiply 2 on both sides that does not change my line

(Refer Slide Time: 06:11) it is still the same y equals m x plus c line right. But now what I am saying is that in

(Refer Slide Time: 06:16) this particular case because I have divided by norm W star on both sides the line is the

(Refer Slide Time: 06:21) same, but now with respect to this renaming I can write the same line as the set of all

(Refer Slide Time: 06:30) x such that W star dash transpose x equal to gamma dash. It is a new W star it is called

(Refer Slide Time: 06:37) W star dash and the gamma has changed to gamma dash it is the same line gamma dash is

(Refer Slide Time: 06:44) still a positive quantity because originally gamma was positive I divided it by a positive

(Refer Slide Time: 06:48) quantity still a positive quantity, but the advantage of doing this is that this new

(Refer Slide Time: 06:54) guy that I have now has norm 1 which means that you know if you give me a W star which

(Refer Slide Time: 07:01) separates my dataset with some gamma let us say gamma is 10. Now I can create another W star

(Refer Slide Time: 07:06) by rescaling your W star to make sure it has length 1 and the gamma will rescale accordingly

(Refer Slide Time: 07:12) so but still I can I now have a W star whose length is 1 which also linearly separates

(Refer Slide Time: 07:19) this dataset with a different gamma, but because we did not make our assumption 1 just said

(Refer Slide Time: 07:24) that there is some W star with some gamma greater than 0 it did not tell me that gamma has

(Refer Slide Time: 07:29) to be at least this much or anything of that sort right. So we allowed for any gamma greater

(Refer Slide Time: 07:33) than 0 now we are still satisfying this assumption right. So which means that without loss of

(Refer Slide Time: 07:38) generality I can assume that W star the length of my W is actually 1 right. So because for every

(Refer Slide Time: 07:45) W star that linearly separates my dataset with some gamma there is an equivalent W star dash

(Refer Slide Time: 07:50) whose length is 1 which separates my dataset linearly with some other gamma gamma dash right.

(Refer Slide Time: 07:56) So I can assume that the W star that is given to me is as well of length 1 itself right.

(Refer Slide Time: 08:02) So this is without loss of generality. So now these with these three assumptions linear

(Refer Slide Time: 08:08) separability with gamma margin which is the most important assumption the radius assumption

(Refer Slide Time: 08:13) and the length assumption we can now go ahead and try to analyze the proof of the perceptron

(Refer Slide Time: 08:19) algorithm which we will do next. So let us analyze the perceptron algorithm with our assumptions

(Refer Slide Time: 08:30) that we have put down right. So analysis. So what we are going to analyze is we are going

(Refer Slide Time: 08:38) to look at how many mistakes this algorithm makes right. So the way we are going to prove

(Refer Slide Time: 08:53) that this algorithm actually converges is using the following method. We are going to say

(Refer Slide Time: 08:58) that perceptron algorithm cannot make more than a certain number of mistakes maybe that

(Refer Slide Time: 09:09) number is 10,000 right. So we are saying that the algorithm cannot make more than 10,000

(Refer Slide Time: 09:13) mistakes which means that after it makes 10,000 mistakes right. So it cannot make any more

(Refer Slide Time: 09:20) mistakes what does it mean to say it does not make any more mistakes it correctly class

(Refer Slide Time: 09:24) anyways all my points in my dataset and so the algorithm would have converged which means

(Refer Slide Time: 09:29) that if I can get a bound a finite number as a bound for the number of mistakes the algorithm

(Refer Slide Time: 09:34) makes then that implies that the algorithm has actually converged right. So which is what

(Refer Slide Time: 09:38) we are going to try and do now right. So can we analyze the mistakes of this algorithm how

(Refer Slide Time: 09:42) many mistakes will this algorithm make right. So why do we care about mistakes because the

(Refer Slide Time: 09:48) algorithm only makes an update when a mistake happens right. So now observe that an update

(Refer Slide Time: 09:57) in the perceptron algorithm happens only when a mistake happens. So now let us say we are

(Refer Slide Time: 10:17) at some point in the running the perceptron algorithm we are given some dataset we are running

(Refer Slide Time: 10:21) the perceptron algorithm and let us say at some point WL may be we will put the L about WL is

(Refer Slide Time: 10:30) the current guess and a mistake happens. So with respect to some data point x comma

(Refer Slide Time: 10:47) over right. So I found a point where WL is incorrectly classifying. So the moment I find a

(Refer Slide Time: 10:53) point where it incorrectly classifies I will update WL to WL plus 1 as WL plus x into y.

(Refer Slide Time: 10:58) This is my update rule I know this right. Now if you observe what is happening is I am adding a

(Refer Slide Time: 11:06) new point to my current old WL right. So now what we are going to look at is we are going to ask

(Refer Slide Time: 11:14) how much is the length of my WL plus 1 growing right. So I am updating my W by adding some point

(Refer Slide Time: 11:22) right. So x times y of course there is a label also which is 1 or minus 1 nevertheless I'm

(Refer Slide Time: 11:27) adding something to my old data point. So how much is my length of my WL plus 1 growing right.

(Refer Slide Time: 11:34) So I can try to understand that quantity right. So let us say I want to understand that quantity

(Refer Slide Time: 11:38) and we will see why that is a good quantity to understand. So we want to understand what is the

(Refer Slide Time: 11:43) length square let us say of WL plus 1. This is of course the length square of WL plus x times y

(Refer Slide Time: 11:51) square. But what is the length square? This is the norm square of a vector which we know can be

(Refer Slide Time: 11:57) written as WL plus x into y transpose WL plus x into y which is on expansion you will get four

(Refer Slide Time: 12:07) terms which is WL norm square plus you know two of the terms will be the same which is two times

(Refer Slide Time: 12:16) WL transpose x into y plus x transpose x which is norm x square into y square. This would be the

(Refer Slide Time: 12:27) expansion well what is y square? Well y square y is plus or minus 1 so y square is always plus 1.

(Refer Slide Time: 12:36) So this whole thing is going to be just norm x square. But now how much how big can norm x square

(Refer Slide Time: 12:44) be right. So x is any data point in my data set and now I am trying to understand what is the

(Refer Slide Time: 12:50) norm squared of x. But we made a assumption about the algorithm I mean one of the assumptions that

(Refer Slide Time: 12:57) we made before we started proving was the radius assumption which said that the length of any

(Refer Slide Time: 13:02) data point is at most r. It is within a ball of radius r which means the length squared of my data

(Refer Slide Time: 13:07) point is going to be less than or equal to r square. So the third term is at most r square because

(Refer Slide Time: 13:13) norm of x is less than or equal to r by our assumption. Now what about the second term?

(Refer Slide Time: 13:19) Well it is two times WL transpose x into y. Now what can we say about this term?

(Refer Slide Time: 13:26) Pause and think about this. This is a very interesting question to think about what can you say

(Refer Slide Time: 13:30) about WL transpose x into y? Well what happened with respect to WL for the point x y? Well WL

(Refer Slide Time: 13:40) made a mistake for x y that is why we are updating it to WL plus 1. So which means that WL

(Refer Slide Time: 13:46) is making a mistake for x, y means what? Well the sign of WL transpose x and the sign of y

(Refer Slide Time: 13:54) which is plus 1 or minus 1 they do not match. Either WL transpose x is positive and y is minus

(Refer Slide Time: 14:00) 1 or WL transpose x is negative and y is plus 1 which means if I multiply these two quantity.

(Refer Slide Time: 14:07) So then it necessarily has to be the case that because WL makes a mistake on x y their product

(Refer Slide Time: 14:13) cannot be positive. The product has to be less than or equal to 0. So this guy has to be less than

(Refer Slide Time: 14:20) or equal to 0 because mistake. The update happens only when there is a mistake so this guy has to

(Refer Slide Time: 14:29) be less than or equal to 0. So then we can say we can upper bound the whole thing by the norm of

(Refer Slide Time: 14:35) WL plus 1 squared by norm WL squared plus R squared because this is less than or equal to 0.

(Refer Slide Time: 14:44) I can throw away the term and just say that this is less than or equal to just the first term

(Refer Slide Time: 14:48) plus the third term which we know is less than or equal to R squared. So now what is this

(Refer Slide Time: 14:53) telling us? This is telling us that I have a WL, I make a mistake, I change my WL to WL plus 1

(Refer Slide Time: 15:00) and now this new WL plus 1's length squared can grow by at most the previous length squared plus R

(Refer Slide Time: 15:10) squared. So it cannot grow more than that that is what this is saying. So it can grow at most by R

(Refer Slide Time: 15:16) squared. But now interestingly well how did I get WL in the first place? I got WL because there

(Refer Slide Time: 15:24) was some WL minus 1 and now I made a mistake with respect to some data point and so I updated it

(Refer Slide Time: 15:31) to WL which means the same argument should also apply to WL. So which means that I can say this

(Refer Slide Time: 15:37) is less than or equal to WL minus 1 plus R squared this term of course plus R squared. So WL plus 1

(Refer Slide Time: 15:47) squared is at most WL minus 1's length squared plus R squared plus R squared. So because WL came

(Refer Slide Time: 15:55) from WL minus 1 and it's length grew by at most R squared. Now WL minus 1 came from WL minus 2

(Refer Slide Time: 16:01) and then I can inductively keep going behind till I get to W0. But if you remember perceptrons W0

(Refer Slide Time: 16:08) the initialization was just the all 0 spectre. So which means that this can keep going and then I

(Refer Slide Time: 16:14) can say that this is less than or equal to W0 squared plus L times R squared which is less than

(Refer Slide Time: 16:22) or equal to WL plus 1's length squares. But W0 squared is just 0 because our initialization of W0

(Refer Slide Time: 16:29) was just 0. So this just tells us that which implies what we are saying is that after you make

(Refer Slide Time: 16:36) Lth mistake. So in some round you make some Lth mistake you are the length of after making L

(Refer Slide Time: 16:45) mistakes the new W that you end up is at most L times R squared. So this is one observation

(Refer Slide Time: 16:54) one. So we are saying the length cannot grow by too much it can grow only by L times R squared

(Refer Slide Time: 17:00) of WL right of the W that we are maintaining. So now remember this L you know makes an appearance

(Refer Slide Time: 17:08) here that's the interesting part here L is remember L is the number of mistakes that we have made

(Refer Slide Time: 17:12) so far right. So you have made L different updates for our our W and so that is the number of

(Refer Slide Time: 17:18) mistakes that has happened right. So this is mistakes. So somehow we are we are converting our length

(Refer Slide Time: 17:26) of W into a bound on the number of mistakes that we have. Of course this is not enough to say

(Refer Slide Time: 17:32) the number of mistakes of perceptron is bounded because we are only bounding the length from one

(Refer Slide Time: 17:36) side. We need to bound it from the other side also which is what we will try and do next.

(Refer Slide Time: 17:51) From the other side to understand the same quantity from the other side

(Refer Slide Time: 17:54) we want to use the fact that there is some W star which linearly separates our data set with

(Refer Slide Time: 18:01) gamma merge that's the assumption on the data set that we have. We have not used that assumption

(Refer Slide Time: 18:06) at in this argument right. So the way we are going to think of that is that I have W L plus 1

(Refer Slide Time: 18:12) which is my new W after WL makes a mistake on X comma Y and now I want to understand how does

(Refer Slide Time: 18:18) this WL's dot product with the W star look like. Remember W star is something that I don't know

(Refer Slide Time: 18:25) because I mean that's that's an assumption that I am making about the underlying data set

(Refer Slide Time: 18:30) that there is a W star which separates this data with gamma merge. I don't know what this W

(Refer Slide Time: 18:34) stars but I know that there is some W star. So I can still reason about such W star. What I am

(Refer Slide Time: 18:39) trying to reason about is as my data set I mean as I make mistakes in perceptron I keep changing

(Refer Slide Time: 18:44) my W and I am asking how does my dot product with the W star change. We know that this is W L

(Refer Slide Time: 18:52) plus X times Y because W L made a mistake on X Y transpose W star which is this W L transpose

(Refer Slide Time: 18:59) W star plus W star transpose X into Y. Now what can I say about W star transpose X into Y?

(Refer Slide Time: 19:09) Well what is this quantity? Well W star transpose X is the dot product the W star the optimal W

(Refer Slide Time: 19:15) makes with respect to my X and then I am multiplying it with the label. Now what is the property

(Refer Slide Time: 19:21) of the optimal W? The optimal W in fact separates my data set with gamma margin which means by definition

(Refer Slide Time: 19:28) W star transpose X into Y should be at least gamma. So this guy is greater than or equal to gamma

(Refer Slide Time: 19:35) where gamma is some positive quality. This is an assumption that we have already made. So that's

(Refer Slide Time: 19:39) that's the property of W star. So now basically what is this saying this is then saying that

(Refer Slide Time: 19:45) W L plus 1 transpose W star is greater than or equal to W L transpose W star plus gamma.

(Refer Slide Time: 19:54) This is kind of telling us that you know the previous dot product with the optimal W star

(Refer Slide Time: 19:59) has to grow by at least gamma once you make a mistake and update W L to W L plus 1.

(Refer Slide Time: 20:06) So W L plus 1's dot product W star should be at least gamma more than W L's dot product with W

(Refer Slide Time: 20:13) star. So which means that I can do the same argument now for W L because W L again came from

(Refer Slide Time: 20:19) W L minus 1 the previous mistake happened and so I updated W L minus 1 to W L and so that should

(Refer Slide Time: 20:25) have given me an extra gamma boost to my dot product with respect to W L minus 1 which means

(Refer Slide Time: 20:30) this is greater than or equal to W L minus 1 transpose W star plus gamma plus this gamma.

(Refer Slide Time: 20:37) This is this gamma this guy is greater than or equal to this same argument.

(Refer Slide Time: 20:44) And now we can keep going and then say that W L plus 1 transpose W star is greater than or

(Refer Slide Time: 20:50) equal to W naught transpose W star plus L times gamma. But W naught we know is just the 0 all 0

(Refer Slide Time: 20:58) vector right. So this dot product with any W star is going to be 0 so this is just the 0 this

(Refer Slide Time: 21:03) quantity 0 which means what we have is W L plus 1 transpose W star is greater than or equal to

(Refer Slide Time: 21:10) L times gamma. This is true. What it is saying is that as I make mistakes my dot product with W

(Refer Slide Time: 21:18) star keeps increasing right. So and I know already from previous argument as I make mistakes my length

(Refer Slide Time: 21:25) of W L plus 1 cannot grow by too much somehow we need to relate these two things right. So on one

(Refer Slide Time: 21:32) side we have a upper bound on the length squared of W L plus 1 on the other side we have a lower bound

(Refer Slide Time: 21:38) on the dot product with W star right. So how can I combine these two things well we can combine

(Refer Slide Time: 21:44) this if we can get a bound on the dot product with W star as a function of the length of W L

(Refer Slide Time: 21:51) itself. But that is not too hard to right. So for any x comma y let me put this in a different color

(Refer Slide Time: 22:00) so this is something that we should know for any x comma y right. So let us say we are in some

(Refer Slide Time: 22:08) direction y and then we have an x here. Now if you remember from our PCI discussion earlier right.

(Refer Slide Time: 22:17) So if I take the projection of x on to this direction of y if this is a perpendicular vector

(Refer Slide Time: 22:24) this makes a 90 degree in two dimension. So now this point which is like a proxy of x on the

(Refer Slide Time: 22:30) direction of y we know is just x transpose y divided by norm of y into y right. So this is some

(Refer Slide Time: 22:40) constant times y and that constant is just x transpose y divided by y transpose y normal square

(Refer Slide Time: 22:46) actually normal y square. So now this point is this vector right. So now we know by Pythagoras

(Refer Slide Time: 22:54) that this length is less than or equal to this length. Why? Because you know Pythagoras says that

(Refer Slide Time: 23:01) the length of the hypotenuse length square of the hypotenuse is the sum of the length square of the

(Refer Slide Time: 23:06) other two sides right. So which means that this length squared right. So the length square of

(Refer Slide Time: 23:13) this guy this length squared is less than or equal to the length square of x itself.

(Refer Slide Time: 23:20) This is Pythagoras. Of course Pythagoras would say that this is plus the length squared of this guy

(Refer Slide Time: 23:28) but then we can ignore that and say that this is less than or equal to this. But what is this

(Refer Slide Time: 23:33) if I unravel this this is just x transpose y is a constant squared length y squared divided by

(Refer Slide Time: 23:40) length y squared which is length y power 4 is less than or equal to norm x squared which implies

(Refer Slide Time: 23:46) that x transpose y squared is less than or equal to norm x squared into norm y squared.

(Refer Slide Time: 23:54) So basically for any x and y what this is saying is that the dot product square is at most the

(Refer Slide Time: 24:00) length squared times the length of the x squared times length of y squared right. So this is I mean

(Refer Slide Time: 24:07) people might have seen this as a version of Cauchy Schwarz inequality.

(Refer Slide Time: 24:15) So this is true for any x and y right. So but now x and y that we care about is w l plus 1

(Refer Slide Time: 24:21) and w star right. So we know already right. So from 2 we know that l gamma right is less than or

(Refer Slide Time: 24:31) equal to w l plus 1 transpose w star. I have just written it the other way right. So this is

(Refer Slide Time: 24:38) w l plus 1 transpose w star is greater than or equal to l gamma. Equalently l gamma is less than

(Refer Slide Time: 24:43) or equal to w l plus 1 transpose w star which means that you know l squared gamma squared is less

(Refer Slide Time: 24:52) than or equal to w l plus 1 transpose w star squared. Now think of this as some x and think of

(Refer Slide Time: 25:01) this as y. Now this is x transpose y squared which by Cauchy Schwarz would our previous argument

(Refer Slide Time: 25:08) has to be less than or w l plus 1 squared times w star squared right. So this is from Cauchy's

(Refer Slide Time: 25:17) Schwarz. Now we use our assumption that you know we could have always picked my w star which

(Refer Slide Time: 25:26) has a gamma margin such that w stars length is 1 right. So this length is just one without loss

(Refer Slide Time: 25:33) of generality. So I can forget that and then this just then says that norm w l plus 1 squared

(Refer Slide Time: 25:41) is greater than or equal to l squared gamma squared. This is my 3 third point right. So on the

(Refer Slide Time: 25:52) one hand we have from argument 1 that norm l plus 1 squared is less than or equal to l times

(Refer Slide Time: 25:58) r squared whereas from the other side we have norm w l plus 1 squared is greater than or equal

(Refer Slide Time: 26:03) to l squared gamma squared right. So which means that you know this guy is actually sandwich

(Refer Slide Time: 26:08) between two terms right. So this is greater than or equal to l squared gamma squared.

(Refer Slide Time: 26:15) This is from 3 and this is less than or equal to l r squared. This is from 1.

(Refer Slide Time: 26:24) Now this implies l square gamma square has to be at most l r square because this quantity is

(Refer Slide Time: 26:31) kind of sitting in between these two terms right. So which means this has to happen which now

(Refer Slide Time: 26:35) implies l is at most no r square by gamma square. Now this means what right. So this is kind

(Refer Slide Time: 26:48) of telling us what is l. l is the number of mistakes that we make in our algorithm and now we are

(Refer Slide Time: 26:54) saying that this mistakes is bounded by a term which is r square by gamma square where r is the

(Refer Slide Time: 27:00) radius assumption the radius of our data and gamma is the margin of the optimal separator right.

(Refer Slide Time: 27:05) So this bound is what is called as the radius margin bound right. So what is this telling us right.

(Refer Slide Time: 27:21) So why do we why do we care about this bound. This is telling us that the number of mistakes

(Refer Slide Time: 27:27) that Persephone makes is at most r square by gamma square where r is the radius of our data set

(Refer Slide Time: 27:35) and gamma is the margin with respect to the optimal W star right. So this means that you know

(Refer Slide Time: 27:42) the number of mistakes is bounded because well why is this because gamma is positive.

(Refer Slide Time: 27:56) And so r square by gamma square is a finite number if gamma was 0 which means that if

(Refer Slide Time: 28:02) if we assume linear separability with 0 allowing gamma is 0 which means that we allowed points to lie

(Refer Slide Time: 28:07) on the hyperplane that separates the pluses from the minuses then we are saying this this argument

(Refer Slide Time: 28:15) would just say that l is less than or equal to r square by 0 which means l is less than or equal

(Refer Slide Time: 28:19) to infinity which means the number of mistakes is less than or equal to infinity is a useless statement.

(Refer Slide Time: 28:24) But the moment we say that we do not allow gamma to be 0 that there is some W star such that gamma

(Refer Slide Time: 28:30) is strictly greater than 0 then we get a finite value as an upper bound and so the number of

(Refer Slide Time: 28:37) mistakes that the algorithm makes is finite and so the algorithm necessarily has to converge right.

(Refer Slide Time: 28:43) So this implies Persephone converges.

(Refer Slide Time: 28:47) So just to summarize what we have essentially saying is that we have an algorithm now which is

(Refer Slide Time: 29:03) based on a very very simple update rule when you find a mistake just add x times y to your current

(Refer Slide Time: 29:09) W and keep going on so this is the algorithm and now this algorithm will run until convergence.

(Refer Slide Time: 29:14) But what does convergence mean convergence means that you run the algorithm until you find a W

(Refer Slide Time: 29:19) that correctly class phase all over data points. Now we are saying now that it will indeed converge

(Refer Slide Time: 29:25) because the number of mistakes that this algorithm can make is bounded by a function of the radius

(Refer Slide Time: 29:31) and the margin and if radius is of course of something that you can calculate from your data set

(Refer Slide Time: 29:37) which is a finite number and if you assume that the data set has a W star with a positive margin

(Refer Slide Time: 29:44) then the number of mistakes is bounded and so the algorithm necessarily cannot make more than

(Refer Slide Time: 29:50) a bounded number of mistakes which means that eventually the algorithm has to converge right.

(Refer Slide Time: 29:55) So if our data set satisfies linear separability with gamma margin then Persephone converges

(Refer Slide Time: 30:02) in a finite number of steps. So this is good news because now we have an algorithm which is

(Refer Slide Time: 30:08) super simple algorithm and we know that it converges. It is useful to understand this radius,

(Refer Slide Time: 30:16) margin bound and its implication carefully and that is what we want to do next because that will

(Refer Slide Time: 30:21) lead us to several other sophisticated algorithms a little later on this course.

(Refer Slide Time: 30:27) But you know the good news is Persephone converges but then what does it mean to say with respect to

(Refer Slide Time: 30:34) the quality of solution that we get and what does it mean to say that converges with mistakes

(Refer Slide Time: 30:40) less than or equal to r square by gamma square right. So what is the role of this gamma?

(Refer Slide Time: 30:44) How can we understand the role of this gamma more carefully right. So the role of the margin.

(Refer Slide Time: 30:48) So these are things that we need to think a little bit more carefully about this Persephone algorithm

(Refer Slide Time: 30:53) and that will provide us more insights into developing new algorithms which we will see later in

(Refer Slide Time: 30:57) the course right. So at this point I would want to stop by saying that we have put down an algorithm

(Refer Slide Time: 31:02) which is a very solid algorithm simple solid algorithm which has guaranteed convergence.

(Refer Slide Time: 31:08) In fact this is one of the first algorithms in machine learning with probable convergence

(Refer Slide Time: 31:12) guarantees and inspired by these algorithms you know there are two major branches of

(Refer Slide Time: 31:21) thought which led us led to two different types of algorithmic development whose base was

(Refer Slide Time: 31:27) Perseptron. We will see both of these in this course one is called the neural network one is

(Refer Slide Time: 31:33) called the support vector machine both of which have inspiration from Perseptron and its analysis

(Refer Slide Time: 31:38) and so this becomes a very very interesting and important algorithm to understand in a classical

(Refer Slide Time: 31:43) machine learning setup. So with this we will stop here and then next time when we come again

(Refer Slide Time: 31:49) we will look at you know what are the implications of the radius margin bound and how that will

(Refer Slide Time: 31:54) inspire us to develop more algorithms. Thank you.