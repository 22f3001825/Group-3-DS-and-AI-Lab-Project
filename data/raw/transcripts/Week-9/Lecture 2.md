# Week-9 - Lecture 2


(Refer Slide Time: 00:00) So, the update rule of perceptron is as a very very simple update rule it just says

(Refer Slide Time: 00:19) that Wt plus 1 is Wt plus xy i if mistake. Now, there are two different ways you can make

(Refer Slide Time: 00:31) a mistake right. So, what are these two different ways your current Wt can go wrong on a data

(Refer Slide Time: 00:36) point. Well, pause and think about this it is nothing too hard to see I am going to say

(Refer Slide Time: 00:42) what these two types of mistakes mistake 1 is mistake type 1 is when the algorithm predicts

(Refer Slide Time: 00:51) the label as 1, but then the actual label is minus 1 right. So, which means that predicted

(Refer Slide Time: 00:58) let us say predicted is 1 actual is minus 1. What do I mean by predicted is 1 actual is

(Refer Slide Time: 01:06) minus 1 well this just means that you know sign of Wt transpose x i is greater than or

(Refer Slide Time: 01:13) equal to 0, but y i is minus 1 right. So, you have a current Wt you had a current Wt

(Refer Slide Time: 01:22) and you find an x i y i pair where it is making a mistake why is it making a mistake because

(Refer Slide Time: 01:27) with respect to Wt I am predicting 1 when will I predict 1 when I see that x i falls

(Refer Slide Time: 01:33) on one side of Wt right. So, the positive side of Wt or the non negative side of Wt which

(Refer Slide Time: 01:37) means the sign of Wt transpose x i is greater than or equal to 0, but because it is a mistake

(Refer Slide Time: 01:42) y i should have been minus 1 right. So, that is mistake type 1 of course, mistake type

(Refer Slide Time: 01:47) 2 is just a symmetric opposite of this yeah. So, here predicted is minus 1, but the actual

(Refer Slide Time: 01:55) is plus 1 right. So, y is the predicted minus 1 because sign of Wt transpose x i was

(Refer Slide Time: 02:02) less than 0, but actual y i is plus 1 right. So, the opposite condition happened both of

(Refer Slide Time: 02:08) these are mistakes right. So, but then the update rule is the same for both these mistakes.

(Refer Slide Time: 02:12) So, we need to justify why both these mistakes why the update rule makes sense in both these

(Refer Slide Time: 02:16) cases ok. So, let us analyze mistake 1 right. So, let us look at mistake type 1 type

(Refer Slide Time: 02:24) 1 mistake is when I am predicting the algorithm is predicting 1, but then the actual point

(Refer Slide Time: 02:30) label says minus 1 right. So, so you you had a Wt where this condition happened Wt transpose

(Refer Slide Time: 02:38) x i is positive well it should not say sign here right. So, it is just a sin s plus 1 or

(Refer Slide Time: 02:44) Wt transpose x i is greater than or equal to 0, but y is minus 1 right. So, now I updated

(Refer Slide Time: 02:52) Wt plus 1 to Wt plus x i y this is my new Wt right. So, I am believing that well the

(Refer Slide Time: 02:58) old W is no longer correct here is a new W which is correct. So, now I should ask the

(Refer Slide Time: 03:03) question well I have updated my W to a new W then how does this new W performed on the

(Refer Slide Time: 03:10) point where the old W was making a mistake that is the natural thing to ask. Now, what do

(Refer Slide Time: 03:14) I mean by how does it perform on the point how does it classify that point where the old

(Refer Slide Time: 03:18) W was making a mistake. Well how can I find that I need to look at the dot product of the

(Refer Slide Time: 03:23) new W with the same data point and see how that looks like right. So, which means that

(Refer Slide Time: 03:27) I should look at W my actually keep track of whether it is superscript or subscript.

(Refer Slide Time: 03:36) So, I should look at Wt plus 1 transpose x i, but by definition that is just Wt plus

(Refer Slide Time: 03:46) x i y i transpose x i which is just Wt transpose x i plus y i into x i transpose x i which

(Refer Slide Time: 03:55) is norm x i square right. Well this is what the new W dot product with the point where

(Refer Slide Time: 04:03) the old W made a mistake right. So, but now in mistake number 1 type 1 this value is greater

(Refer Slide Time: 04:10) than or equal to 0 norm of x i square is always a positive quantity right. So, this is going

(Refer Slide Time: 04:16) to be greater than or equal to 0 in fact, you can yes you can simply assume that the data

(Refer Slide Time: 04:21) points are all not all 0. So, this is going to be greater than 0, but because it is a mistake

(Refer Slide Time: 04:26) this guy was minus 1 right. So, which means that this whole thing is negative right. So,

(Refer Slide Time: 04:34) what does that mean that means that earlier I was making a mistake because the previous

(Refer Slide Time: 04:39) W dot product with x i was positive whereas, it should have been negative. Now, what I am

(Refer Slide Time: 04:45) saying is that the new W's dot product with x i is the previous W's dot product with

(Refer Slide Time: 04:50) x i minus something right. So, you are subtracting out something from the old W's dot product.

(Refer Slide Time: 04:56) Well the old W's was positive. So, you are subtracting out something that does not mean

(Refer Slide Time: 05:01) that the new W's dot product with x i immediately becomes you know negative we do not know

(Refer Slide Time: 05:07) that, but we know that it is moving in the right direction. Why because this is positive

(Refer Slide Time: 05:14) it should have been negative, but it is positive. So, you are subtracting out something. So,

(Refer Slide Time: 05:18) it is getting slower and lower right. So, at this point it is going in the correct direction

(Refer Slide Time: 05:23) that the dot product should be negative right. So, at this point we are not saying it is

(Refer Slide Time: 05:27) correcting the mistake, but the W is moving in such a way that the mistake I mean at least

(Refer Slide Time: 05:33) the dot product is going in the correct direction right. So, that is what is happening here

(Refer Slide Time: 05:38) in and very similar thing will happen here as well right. So, here also W the second mistake

(Refer Slide Time: 05:44) type also W t plus 1 transpose x i is W t transpose x i plus y i into norm of x i square,

(Refer Slide Time: 05:51) but now in this case well the first term is less than 0. Whereas, the second term is y

(Refer Slide Time: 05:58) i is plus 1 now and so the second term is greater than 0. So, now also the new W's dot product

(Refer Slide Time: 06:06) with x i you want it to be positive. The old W's dot product with x i was negative. What

(Refer Slide Time: 06:11) you are doing is you are adding a positive term to it right. So, if it is it was initially

(Refer Slide Time: 06:15) negative may be minus 10 now I am adding let us say plus 5. So, it becomes minus 5 it is

(Refer Slide Time: 06:21) no it is not at you know it is not at positive, but then it is getting closer and closer to

(Refer Slide Time: 06:29) being positive right. So, that is the idea. So, basically what is happening is you can

(Refer Slide Time: 06:34) say that you know the update rule is such that now this argument says that the update

(Refer Slide Time: 06:40) rule is a reasonable rule right. So, update rule pushes W in the right direction for x i.

(Refer Slide Time: 06:56) So, if the dot product is positive, but then it should have been negative then you are

(Refer Slide Time: 07:02) subtracting out something the dot product is negative, but it should have been positive

(Refer Slide Time: 07:06) you are adding something. So, the update rule is kind of moving our W's in the correct

(Refer Slide Time: 07:11) direction. It does not mean that it is fixing the problem, but it at least moving in the

(Refer Slide Time: 07:14) correct direction. Now, this is a local discussion right. So, what we are saying is that well

(Refer Slide Time: 07:23) I made a mistake in some point x i y i and I am asking the question how does the new

(Refer Slide Time: 07:30) update W work for this x i y. So, maybe you are lucky that the new x i y i it pushed in

(Refer Slide Time: 07:36) the right direction and it actually fix the mistake of x i y also right. So, maybe the

(Refer Slide Time: 07:42) old W was making a negative dot product whereas, it should have been making a positive

(Refer Slide Time: 07:46) dot product. So, you update the W and good good for you the new update W is making a positive

(Refer Slide Time: 07:52) dot product, which means that we have corrected the mistake for x i y i, but that does not

(Refer Slide Time: 07:57) mean that the mistake that I corrected here for this x i y i is not affecting some other

(Refer Slide Time: 08:07) data point in my data set, which was earlier correct, but then because I change made this

(Refer Slide Time: 08:12) change has now become incorrect right. So, another what I am saying is that this local

(Refer Slide Time: 08:18) update fixing it locally, it is not at all clear that fixing it locally will actually

(Refer Slide Time: 08:26) you know is a good thing the overall scheme of things because fixing it locally might

(Refer Slide Time: 08:29) break something else for some other data point that could potentially happen right.

(Refer Slide Time: 08:34) So, can that really happen well let us see an example to kind of understand this in

(Refer Slide Time: 08:39) action right. So, let us say here is our data set. So, this is a simple example where

(Refer Slide Time: 08:48) I am going to put some points here, there are some points like this and maybe there are

(Refer Slide Time: 09:01) some points like this and maybe there are some points like this. So, this is my label

(Refer Slide Time: 09:07) data set that I have in my hand and let us say currently I have a w like this, this is

(Refer Slide Time: 09:14) my let us say current w. Now, at some iteration I have this w, I have this label data set and

(Refer Slide Time: 09:23) I ask the question well this does this w make a mistake in my data set. Well how do

(Refer Slide Time: 09:28) I check that will I look at the line that this w corresponds to which is this line and

(Refer Slide Time: 09:36) now all the are all the green points on the positive set and all the red points on the

(Refer Slide Time: 09:40) negative set well almost except one guy right. So, except this point here everybody else

(Refer Slide Time: 09:47) is correct right. So, this is a point where I am making a mistake. So, which means that

(Refer Slide Time: 09:51) I need to update my w based on this point right. So, now how will I how will that update

(Refer Slide Time: 09:56) happen well greens are positive reds are negative right. So, that is let me make sure

(Refer Slide Time: 10:01) make sure we write that. So, this is plus 1 red is minus 1. So, which means that now what

(Refer Slide Time: 10:06) is what would be the new w where is going to be the new w well the new w is going to be well

(Refer Slide Time: 10:11) this is if this is x the corresponding label for this in my data set is green which is 1.

(Refer Slide Time: 10:17) So, I am going to when new w is going to w current w plus x into 1 I am multiplying 1 because

(Refer Slide Time: 10:24) the label is 1 right. So, this is let us say w let me say this is w old and now w new is just

(Refer Slide Time: 10:33) old plus x times 1 right. So, this 1 is just y right. So, it is just a green point. So,

(Refer Slide Time: 10:40) where is how what does that mean right. So, so this is my so let me plot the x point now

(Refer Slide Time: 10:49) which looks like this this is the direction of x which means that I am going to add that to my old

(Refer Slide Time: 10:57) w which if I am drawing it correctly which we will pull it we will put it somewhere here right.

(Refer Slide Time: 11:06) So, this is going to be my w new right. So, this is w new which is w old plus this x right. So,

(Refer Slide Time: 11:15) that is what it means to say I am adding x ok. So, now what has happened is my w has updated.

(Refer Slide Time: 11:22) So, let me look at the new w which is this is my new w which is w new and let us see how this

(Refer Slide Time: 11:30) w performs on my data set right. So, how would this w perform on my data set this would say

(Refer Slide Time: 11:35) anybody on this side is positive anybody on the below this orange line is negative.

(Refer Slide Time: 11:42) Well if you look at the point x now this new w saying x is positive which means that I have fixed

(Refer Slide Time: 11:50) the problem for x. But have I fixed the general problem well this has introduced new errors here

(Refer Slide Time: 12:00) right. So, these guys were earlier correct with respect to the blue line right. So, these were

(Refer Slide Time: 12:05) positive with respect to the blue line before for w old but now w old has become w new and so that

(Refer Slide Time: 12:11) the line has shifted and because the line has shifted these guys are all now mistakes right. So,

(Refer Slide Time: 12:17) I try to fix the mistake of x for w old and so I came to w new I fix the mistake of w old

(Refer Slide Time: 12:25) by for x. But then this w new is good for x but then it is bad for a lot of other guys right. So,

(Refer Slide Time: 12:31) which means that though the update rule is pushing correctly in the direction for the current point

(Refer Slide Time: 12:36) where you are making a mistake it might introduce mistakes for other data points. So, it is not at all

(Refer Slide Time: 12:41) clear if this update rule is actually a solid update rule right. So, and that is one of the reasons

(Refer Slide Time: 12:45) why this algorithm is surprising and surprisingly effective also. So, so let us let us talk about more

(Refer Slide Time: 12:52) about you know whether this this is a good algorithm in the sense that this update rule will it

(Refer Slide Time: 13:00) lead to a convergence or you know you might keep fixing local mistakes but then introducing some

(Refer Slide Time: 13:06) other mistakes somewhere else. Now, if I fix that mistake some other mistake will again get

(Refer Slide Time: 13:10) created and this will keep on going on forever that I will never converge right. So, one might

(Refer Slide Time: 13:15) argue that. So, if you if you are saying that algorithm converges then it means that we should say

(Refer Slide Time: 13:19) that this situation will never happen right. So, so that we need to kind of argue which is what we

(Refer Slide Time: 13:24) are going to do now right. So, but let me note down what is the problem that we saw here

(Refer Slide Time: 13:29) and then we will go ahead and try to fix this right. So, try to understand this better you know

(Refer Slide Time: 13:35) fixing W for 1x might affect decision for other data points.

(Refer Slide Time: 13:49) So, need more careful argument or for convergence this argument is when we have to be very careful

(Refer Slide Time: 14:14) when you are trying to argue convergence of the algorithm. So, let us let us look at another example

(Refer Slide Time: 14:21) which is another revealing example that will give us some insights into this working of the

(Refer Slide Time: 14:25) algorithm itself which will which is in some sense a border case right. So, it is like a corner case

(Refer Slide Time: 14:32) kind of an example, but it will give us something useful to understand. So, here is another example

(Refer Slide Time: 14:39) right. So, now let us say I have again a two dimensional data set, but this time the data set

(Refer Slide Time: 14:45) just has three points right. So, I am going to put two points here this is the point

(Refer Slide Time: 14:54) 0 comma 1 and it is labeled as plus 1 right. So, it is plus 1 and here is a point another point

(Refer Slide Time: 15:04) which is 0 comma minus 1 and I am going to label this as minus 1 and I have a third point let us

(Refer Slide Time: 15:13) say which is somewhere here which is minus 1 0.5 or half and now this is labeled as minus 1

(Refer Slide Time: 15:27) right. So, this is a negatively labeled point that is a positively labeled this this is my data set

(Refer Slide Time: 15:40) this is plus 1 sorry yeah. So, I just have three data points two data points are labeled plus

(Refer Slide Time: 15:50) 1 one data point is labeled minus 1 this is my data set right. So, first question that I would like

(Refer Slide Time: 15:55) to ask you is is this a linearly separable data set.

(Refer Slide Time: 16:11) So, what the so just I mean this is a good thing to pause and think about right. So,

(Refer Slide Time: 16:17) with respect to our definition of linear separability is this a linearly separable data set.

(Refer Slide Time: 16:23) In other words what I am asking is that is there a w such that for the points labeled plus 1

(Refer Slide Time: 16:28) w transpose x is greater than or equal to 0 and for points labeled minus 1 w transpose x is

(Refer Slide Time: 16:35) less than 0. If you can find such a w then this is a linearly separable data set. If you cannot

(Refer Slide Time: 16:40) find any w then this is a this is not a linearly separable data set. So, is this a linearly

(Refer Slide Time: 16:45) separable data set pause and think about it I will tell you the answer now right. So, just to make

(Refer Slide Time: 16:51) sure so this is our data set right. So, 0 comma 1 comma plus 1 0 minus 1 plus 1 minus 1 half

(Refer Slide Time: 16:59) which is minus 1 this is our data set. So, is there a w in r 2 this is a two dimensional w such

(Refer Slide Time: 17:11) that w transpose x is greater than or equal to 0 implies y is plus 1 and w transpose x is

(Refer Slide Time: 17:21) less than or equal to for all y i which is minus 1 right. So, is this is there a w like this

(Refer Slide Time: 17:28) well in fact the answer to this question is yes there is a w what is the w well that w is just

(Refer Slide Time: 17:38) you know any w that is pointing along the positive x axis. Now, if I take this w let say this is

(Refer Slide Time: 17:46) my w right. So, now with respect to this w my separator is just the y axis which means that for

(Refer Slide Time: 17:55) these two points which lie on the y axis w transpose x is 0 which satisfies w transpose x is

(Refer Slide Time: 18:02) greater than or equal to 0. So, the label has to be 1 which in fact is 1 in this case and for the

(Refer Slide Time: 18:07) point which is on the other side of the y axis w transpose x is negative and so the label is

(Refer Slide Time: 18:13) also minus 1. So, this is a linearly separable data set according to the definition that we put

(Refer Slide Time: 18:17) down. So, now what we want to ask is you know what does so let us say I give perceptron this

(Refer Slide Time: 18:23) dataset just three points and see what perceptrons algorithm does in the way that we have put down

(Refer Slide Time: 18:28) the algorithm right. So, let us let us it is a it is it is instructive to you know go through this

(Refer Slide Time: 18:33) example so that we understand what is happening with this algorithm right. So, let me draw this

(Refer Slide Time: 18:39) again you know. So, here is my data point which is plus 1 this is plus 1 this is minus 1 this is

(Refer Slide Time: 18:49) 0 1 0 minus 1 this is minus 1 half. So, what does perceptron do well perceptron

(Refer Slide Time: 19:03) how does perceptron work on this dataset it will go it is going to start with w naught which

(Refer Slide Time: 19:07) is just 0 0 right. So, this is 2 dimensional vector by our algorithm's initialization it is going

(Refer Slide Time: 19:14) to be 0 0. Now, what will it do well what does 0 0 mean well what is so let us call this points

(Refer Slide Time: 19:25) x 1 x 2 and x 3 so that we can keep referring to them easily. So, w naught transpose x 1 is 0

(Refer Slide Time: 19:33) w naught transpose x 2 is also 0 and w naught transpose x 3 is also 0 because w naught is 0 it is

(Refer Slide Time: 19:40) going to make a 0 dot product with everybody. So, which means that for the w naught my you know

(Refer Slide Time: 19:46) predicted y is y 1 is plus 1 predicted y had 2 is also plus 1 and predicted y had 3 is also plus

(Refer Slide Time: 19:55) 1 right. So, because the value is 0 if it is greater than or equal to 0 my sin function is going

(Refer Slide Time: 20:01) to say the label is plus 1 right. So, in this case all 3 would be predicted plus 1. So, which means

(Refer Slide Time: 20:07) I have I have gotten 2 points correctly out of 3 and the point where I make a mistake for this

(Refer Slide Time: 20:13) with respect to this w is x 3 which is this point right. So, which means my w 1 is just going to be

(Refer Slide Time: 20:20) w naught plus x 3 into y 3 because that is the point where I make the mistake in my dataset

(Refer Slide Time: 20:26) which is just 0 0 which is my w naught plus x 3 is minus 1 half and what is y 3 well y 3 is just

(Refer Slide Time: 20:35) y 3 in this case is the label of x 3 which is minus 1. So, that is minus 1. So, my new w is going

(Refer Slide Time: 20:41) to be 1 times half sorry 1 times minus half right. So, which is where is the new w well my new w

(Refer Slide Time: 20:49) is going to be pointing in this direction right. So, this is 1 minus half this is my w 1 right.

(Refer Slide Time: 21:00) So, which means that visually we can see that you know. So, everybody on the below this

(Refer Slide Time: 21:07) diagonal orange line is going to be labeled plus 1 and above is going to be labeled minus 1.

(Refer Slide Time: 21:13) So, now we ask the question is this w correctly classified all my data points?

(Refer Slide Time: 21:18) Well, almost except that it is incorrectly classified x 1 x 1 is a mistake it is correctly

(Refer Slide Time: 21:23) classified x 2 because it is on below the diagonal orange line it is correctly classified

(Refer Slide Time: 21:28) x 3 because it is above the diagonal orange line. But then x 1 is above but it is labeled plus 1

(Refer Slide Time: 21:33) which is a mistake right. So, which means that now I am going to update my w using x 1 right. So,

(Refer Slide Time: 21:39) which means my w 2 is going to be w 1 plus x 1 y 1 well what is w 1 1 minus half plus what is x 1

(Refer Slide Time: 21:48) x 1 is 0 1 times what is the label of x 1 which is 1. Now, what would this give me?

(Refer Slide Time: 21:55) Well, this is going to give me 1 plus 0 which is 1 minus half plus 1 which is half right. So,

(Refer Slide Time: 22:01) this is going to give me 1 half right. So, that is going to be my w 2 well where is w 2 well if

(Refer Slide Time: 22:08) you look at where w 2 is let me plot it using blue well it is going to be 1 half right. So,

(Refer Slide Time: 22:16) it will be somewhere here this is 1 half which is my w 2 which means that the corresponding

(Refer Slide Time: 22:26) line is going to be like this right. So, everybody on the right hand side of this diagonal blue line

(Refer Slide Time: 22:32) is positive on the other side is negative right. Again you see that you know it is classifying

(Refer Slide Time: 22:38) x 1 and x 3 correctly now but x 2 is incorrectly classified. So, which means that perceptron will

(Refer Slide Time: 22:43) make one more update and it will let us put that here and that update will get me w 3 as w 2 plus

(Refer Slide Time: 22:52) the mistake is with respect to x 2 which means that x 2 y 2 has to be added. What is w 2?

(Refer Slide Time: 22:59) w 2 is 1 half plus x 2 in this case is 0 minus 1 what is the label corresponding to x 2 which is 1.

(Refer Slide Time: 23:06) So, now the new updated thing would be 1 plus 0 1 half plus minus 1 which is minus half.

(Refer Slide Time: 23:14) Well w 3 is 1 minus half but we know this is also same as w 1 right. So, which was also 1 minus half.

(Refer Slide Time: 23:23) So, what is happening now is that well we were at w 0 which is 0 0 from which we got w 1

(Refer Slide Time: 23:30) and we went to w 2 and now again we are coming back to w 1. Now, we know that both w 1 and w 2 are not

(Refer Slide Time: 23:38) optimal for this dataset. So, that it makes one mistake each but then what will happen is you will

(Refer Slide Time: 23:43) keep switching between w 1 and w 2 and the algorithm will never converge. So, what does this tell us?

(Refer Slide Time: 23:50) This tells us that this tells us something interesting about the algorithm itself right. So,

(Refer Slide Time: 23:54) we started with the dataset which for which according to our definition is linearly separable

(Refer Slide Time: 24:01) and now we try to run our perceptron algorithm right. So, our goal was to see if perceptron

(Refer Slide Time: 24:08) algorithm will get us a w if the dataset is linearly converge. If the dataset is linearly

(Refer Slide Time: 24:15) separable will the algorithm give us a w which correctly classifies all our data points.

(Refer Slide Time: 24:20) But now it looks like that is not the case because we started with the dataset which is linearly

(Refer Slide Time: 24:24) separable though it had just 3 points nevertheless it is still a dataset and according to our definition

(Refer Slide Time: 24:30) it is linearly separable. But if I run the perceptron algorithm it is not going to get me a w which

(Refer Slide Time: 24:35) correctly classifies all my data points. In fact, what would happen is w perceptron algorithm will

(Refer Slide Time: 24:42) never converge it will keep jumping between w 1 and w 2 and it will never converge right. So,

(Refer Slide Time: 24:46) that is that means that you know we cannot say that if your dataset is linearly separable then

(Refer Slide Time: 24:55) perceptron algorithm will converge right. So, that is not good enough right. So, that is the

(Refer Slide Time: 25:00) problem that I am going to kind of say here. But that is you know so then one can ask why did

(Refer Slide Time: 25:08) this happen right. So, why are we you know though the dataset is linearly separable you know why

(Refer Slide Time: 25:15) did this algorithm fail to converge is it like you know there is something about special about

(Refer Slide Time: 25:20) this dataset which was carefully picked that made perceptron not converge or in general perceptron

(Refer Slide Time: 25:26) itself is a bad algorithm it will never converge right. So, we can ask that question

(Refer Slide Time: 25:31) and if you think about that right. So, one of the properties of this dataset is that

(Refer Slide Time: 25:35) we said that it is linearly separable but in some sense you know it is strictly linearly separable

(Refer Slide Time: 25:41) right. So, in well it is not strictly linearly separable I should say the reason I say that is that

(Refer Slide Time: 25:47) it is linearly separable but then we are using the fact that you know there are points on the boundary

(Refer Slide Time: 25:53) on the decision boundary and you know for which W transpose x is 0 and we arbitrarily decided to

(Refer Slide Time: 26:02) say that W transpose x a equals 0 means that the label is plus 1 that is because that is how we

(Refer Slide Time: 26:06) define the sign function right. So, but then if the points are on the decision boundary and

(Refer Slide Time: 26:13) it is it is a it is a corner case in some sense right. So, because it can either be labeled as

(Refer Slide Time: 26:19) plus 1 or minus 1 but then we chose to do it as plus 1 and because of this arbitraryness of

(Refer Slide Time: 26:25) labeling points on the decision boundary somehow that is affecting the convergence of perceptron

(Refer Slide Time: 26:30) algorithm. So, then we can ask the question well well if this is our definition of linear

(Refer Slide Time: 26:37) separability then perceptron is not going to give us convergence always. So, can I make a slightly

(Refer Slide Time: 26:44) more restriction on my dataset and ask well if I assume something more than just linear

(Refer Slide Time: 26:51) separability I will also assume that you know with respect to that optimal W that actually

(Refer Slide Time: 26:56) classifies my positives and the negatives no point should actually lie on the separator itself

(Refer Slide Time: 27:04) right. So, we can make such an assumption and then ask whether perceptron will converge or not

(Refer Slide Time: 27:09) right. So, what do I mean by that? So, let us make our assumption that we want perceptron I mean

(Refer Slide Time: 27:16) that we want to assume where perceptron will work well more precise right. So, let us make that

(Refer Slide Time: 27:23) assumption precise. So, here is the assumption. This assumption is a very fundamental assumption

(Refer Slide Time: 27:32) and it is called linear separability well we know we are saying that the dataset is going to be

(Refer Slide Time: 27:38) linearly separable. So, it is linear separability but then with a twist right. So, with gamma margin

(Refer Slide Time: 27:52) now this is the assumption that I am going to make right. So, what does it say mean to say

(Refer Slide Time: 27:55) linear separability with gamma margin well it means in pictures it means the following right.

(Refer Slide Time: 28:00) So, you have a dataset in two dimension again. Now, again I am labeling some points as

(Refer Slide Time: 28:07) positive some points as negative let us say things like this mean like this and now what

(Refer Slide Time: 28:24) is happening is you know I have this is a linearly separable dataset obviously, because I can draw

(Refer Slide Time: 28:32) w like this such that you know the line this line separates the positives from the negatives

(Refer Slide Time: 28:39) may be remove this. So, now it is not just linearly separable it is also linearly separable

(Refer Slide Time: 28:46) with gamma margin what does that mean that means that you know if I can draw these lines which are

(Refer Slide Time: 28:54) parallel to the separator this kind of adjust my point so that I can make the make my comment very clear.

(Refer Slide Time: 29:12) Maybe that is a point here right. So, now what we are saying is that you know you have a dataset

(Refer Slide Time: 29:20) now this is the w for which this line is w transpose x equal to 0 right. So, this is the set of all

(Refer Slide Time: 29:26) x such that w transpose x equal to 0. Now, what we are saying is that there are no points that will

(Refer Slide Time: 29:31) lie on this line in my dataset for the for there is a w which will separate my positives from

(Refer Slide Time: 29:36) the negative such that there are no points that lie on the line which is one more way of saying

(Refer Slide Time: 29:41) that is to say that well I can look at these two lines which are parallel to the line that

(Refer Slide Time: 29:46) passes through the origin. This is the set of all x such that w transpose x equal to some gamma

(Refer Slide Time: 29:51) may be gamma s 5 which is 5 units away parallel I have moved my you know separator on the positive

(Refer Slide Time: 29:58) side and this is the set of all x such that w transpose x equal to minus gamma. Now,

(Refer Slide Time: 30:06) what does this assumption essentially mean well it means that I I will not get any point

(Refer Slide Time: 30:15) in the space between these two parallel lines right. In other words I am saying that the dataset is

(Refer Slide Time: 30:23) such that there is a w such that this w classifies the positives from the negatives correctly

(Refer Slide Time: 30:29) and just not classifies it correctly it correctly it classifies it with some gap right. So,

(Refer Slide Time: 30:34) some margin. So, let us let me make this assumption in precise right. So, we are going to say a dataset

(Refer Slide Time: 30:41) which is just a bunch of x 1 y 1 till x and y n as usual is linearly separable

(Refer Slide Time: 30:54) with gamma margin. If there is some w star in R d such that w star transpose x i and the way I

(Refer Slide Time: 31:16) am going to write this is into y i is greater than or equal to gamma for all i for some gamma

(Refer Slide Time: 31:26) which is greater than 0 right. So, this is the this is the definition. So, it needs some parsing

(Refer Slide Time: 31:32) and we will do that now. So, basically what I am saying is that you are given a dataset.

(Refer Slide Time: 31:36) Now, there is some w star right. So, we are assuming that there exists a w star such that with

(Refer Slide Time: 31:42) respect to this w star if I try to find w star transpose x i and multiplied by y i then this

(Refer Slide Time: 31:51) product should be greater than or equal to some positive quantity gamma the gamma cannot be

(Refer Slide Time: 31:56) 0 right. So, the gamma is a positive quantity think of this is 0.1 still ok 5 is still

(Refer Slide Time: 32:02) ok 100 is still ok right. So, it cannot be 0 it has to be some positive quantity right. So,

(Refer Slide Time: 32:07) what I am saying is that there is a w star such that this w star has the property that w

(Refer Slide Time: 32:12) star transpose x i into y i is greater than or equal to some strictly positive quantity.

(Refer Slide Time: 32:18) Now, why am I doing this product w star transpose x i into y i well this is a compact way of saying

(Refer Slide Time: 32:24) that if y i is 1 then this is saying that for all the points which are labeled 1 w star transpose

(Refer Slide Time: 32:32) x i is greater than or equal to gamma which means that all the points which are labeled plus 1

(Refer Slide Time: 32:37) have the property that you know they are sorry over there they are on this side right.

(Refer Slide Time: 32:52) Now, this side when I say this side it includes this you know dotted line right. So,

(Refer Slide Time: 32:59) the dotted line and everybody on the other side right. So, this is the set where w star

(Refer Slide Time: 33:04) transpose x i is greater than or equal to gamma right. So, and now when I multiply it by y i

(Refer Slide Time: 33:10) right. So, which means that whenever y i is 1 it better be in this a low shaded region.

(Refer Slide Time: 33:16) And whenever y i is minus 1 which means w star transpose x i into minus 1 is greater than or

(Refer Slide Time: 33:21) equal to gamma equivalently w star transpose x i is less than or equal to minus gamma which means

(Refer Slide Time: 33:27) that it all the points which are labeled minus 1 in my data set must then have the property

(Refer Slide Time: 33:34) that you know they are on this side of the right. So, they are on this side of course,

(Refer Slide Time: 33:42) this also includes this line y w star transpose x equals minus gamma right. So, now this leaves

(Refer Slide Time: 33:51) this in between region right. So, this region there is no point in my data set in this region right.

(Refer Slide Time: 34:00) So, so this is the assumption that we are making which means that particular in particular there is

(Refer Slide Time: 34:05) no point on the line w star transpose x equal 0 that is no point in my data set satisfied w star

(Refer Slide Time: 34:13) transpose x equal to 0. Now, I am not assuming anything about how big or small this gamma is right.

(Refer Slide Time: 34:19) So, I am just assuming that there is some gamma which is positive gamma cannot be 0 which means that

(Refer Slide Time: 34:23) this gap could be as small as possible. But then we are saying that the gap cannot be 0 that means

(Refer Slide Time: 34:30) that no point can lie on the separating line itself right. So, this is what we will call as

(Refer Slide Time: 34:35) linear separability, but then with this extra small mild condition that there should be a gamma

(Refer Slide Time: 34:40) margin. Now, which means that if we are making this assumption on our data then well it means

(Refer Slide Time: 34:47) the previous you know bad data set that we had we just said three points is disallow right. So,

(Refer Slide Time: 34:53) we are saying that we will not see such a data set in our data right. So, this data set is

(Refer Slide Time: 34:58) not allowed under our model our model only assumes linear separability with gamma margin.

(Refer Slide Time: 35:02) However, small gamma can be it is going to have this assumption. So, this is assumption right.

(Refer Slide Time: 35:08) So, this is the main assumption and we are going to work with this assumption to see how this

(Refer Slide Time: 35:12) assumption can help us provide a proof of convergence for the perceptron algorithm right. So,

(Refer Slide Time: 35:17) this is one of the first algorithm which had a you know a proof for its convergence under this

(Refer Slide Time: 35:22) assumption and so it makes sense to you know go over this proof and understand you know what are

(Refer Slide Time: 35:28) the important elements of proving this and the reason why I want to do this proof in this course

(Refer Slide Time: 35:32) is because this proof will reveal something interesting about the dependence on the relevant

(Refer Slide Time: 35:37) quantities that make up a problem which will lead us to more stronger algorithms later than this

(Refer Slide Time: 35:43) course right. So, for that purpose I will go ahead and do this proof just for us to get a sense for

(Refer Slide Time: 35:49) how can we argue that perceptron actually converges when we put down this small mild extra

(Refer Slide Time: 35:54) condition that linear separability with gamma margin.
