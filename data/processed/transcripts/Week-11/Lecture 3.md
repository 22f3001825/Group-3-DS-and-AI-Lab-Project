# Week-11 - Lecture 3

(Refer Slide Time: 00:00) The other way to look at this the same question would be to start from the primal problem

(Refer Slide Time: 00:20) and see what we can what we can argue we will do that as well. And I will tell you why

(Refer Slide Time: 00:24) we are doing this two different things. When when we summarize everything together you

(Refer Slide Time: 00:29) will be able to appreciate that better. So, what we are going to do this is that let us

(Refer Slide Time: 00:35) see this from the you know primal point of view. So, what do I mean by primal point of

(Refer Slide Time: 00:49) view let us say I solve the primal problem and then I observed again there are three

(Refer Slide Time: 00:53) different cases I observed that for the point I solved primal I got a w star and I observed

(Refer Slide Time: 00:59) that w star transpose let us say x i y i is strictly less than 1 which means that the

(Refer Slide Time: 01:06) point is strictly classified with margin less than 1 or which also implies that this could

(Refer Slide Time: 01:13) be a point which is misclassified. Now, what can we say about this right. So, the moment

(Refer Slide Time: 01:19) I observe that this happens what can I say well I know that from my feasibility w star

(Refer Slide Time: 01:26) transpose x i plus psi i star is greater than or equal to 1. Now, this means that w star

(Refer Slide Time: 01:34) transpose x i y i is or rather let me put it the other way psi i star is greater than

(Refer Slide Time: 01:41) or equal to 1 minus w star transpose x i y i. Now, this implies that we are assuming that

(Refer Slide Time: 01:48) the point satisfies w star transpose x i y is strictly less than 1 that is the case we

(Refer Slide Time: 01:52) are in. Now, this means that epsilon i star is strictly greater than 0 because this guy

(Refer Slide Time: 01:58) is strictly less than 1 the whole thing has to be strictly greater than 0. Well, if epsilon

(Refer Slide Time: 02:03) i star is strictly greater than 0 now by complementary slackness 2 we know that beta star i will

(Refer Slide Time: 02:10) be equal to 0 because the product has to be the product has to be equal to 0. Now, beta

(Refer Slide Time: 02:16) i star equal to 0 implies alpha star i equal c right. So, now, what is this saying this

(Refer Slide Time: 02:23) is saying that if I solve the primal and I find that a point has strictly less than 1

(Refer Slide Time: 02:31) margin then it means that that point necessarily has alpha star i equal c. It is I am not saying

(Refer Slide Time: 02:40) the point is lying on the hyper plane the point is strictly away from the hyper plane

(Refer Slide Time: 02:45) but on the wrong side then that point is very very important because alpha star i equal

(Refer Slide Time: 02:50) c for that point that is the implication that we that we derive here.

(Refer Slide Time: 02:55) The other case is case 2 is when w star transpose x i y i equal 0 now if I solve sorry equals

(Refer Slide Time: 03:03) 1 now if I solve the primal problem and I observe that a point actually lies on the supporting

(Refer Slide Time: 03:09) hyper plane can I say anything well I know that epsilon star i is greater than or equal

(Refer Slide Time: 03:14) to 1 minus w star i transpose x i y i by feasibility. But now this guy is 1 which means that epsilon

(Refer Slide Time: 03:22) star i is greater than or equal to 0 I cannot really say anything more from this argument

(Refer Slide Time: 03:29) well this just implies that alpha star i belongs to well I cannot say anything about beta

(Refer Slide Time: 03:36) if epsilon star i is greater than or equal to 0 beta can be greater than or equal to 0

(Refer Slide Time: 03:40) if beta is greater than or equal to 0 then alpha has to be between 0 and c. So, I cannot

(Refer Slide Time: 03:45) really take away any specific values for this alpha which means that if the point is on

(Refer Slide Time: 03:51) the supporting hyper plane right. So, then alpha star could be anywhere between 0 and c it

(Refer Slide Time: 03:56) could be 0 it could be c it could be anywhere between 0 and c.

(Refer Slide Time: 04:00) From the previous argument we said that if it is between 0 and c if alpha star i is between

(Refer Slide Time: 04:05) 0 and c then I know that it has to be on the supporting hyper plane. But then if I find

(Refer Slide Time: 04:09) a point on the supporting hyper plane well it does not imply that alpha star i is between

(Refer Slide Time: 04:14) 0 and c that is not a if and only if that is what I am trying to say. If you solve the

(Refer Slide Time: 04:19) primal and you observe that a point is on the supporting hyper plane then it you can only

(Refer Slide Time: 04:23) conclude that alpha star i can be between 0 and c that is the second case.

(Refer Slide Time: 04:28) The third case is the good points where w star transpose x i y i is greater than 1 which

(Refer Slide Time: 04:36) means the points for which you know you are classifying this with margin greater than

(Refer Slide Time: 04:40) 1 which are like well away from your supporting hyper plane.

(Refer Slide Time: 04:45) Now this implies what well this implies 1 minus you know w star transpose x i y i minus

(Refer Slide Time: 04:54) epsilon star i what can we say about this well if this is greater than 0 well we can conclude

(Refer Slide Time: 05:01) that well this guy is less than 0 but because epsilon star i is greater than or equal to

(Refer Slide Time: 05:07) 0 well we can say that this is a negative quantity now this can be 0 or negative and so

(Refer Slide Time: 05:13) this whole thing is strictly less than 0. Well if this whole thing is strictly less than

(Refer Slide Time: 05:17) 0 now by complementary slackness 1 we can conclude that alpha star i has to be 0.

(Refer Slide Time: 05:24) Well what does this tell us this tells us that those points which are classified with margin

(Refer Slide Time: 05:33) strictly greater than 1 do not matter they do not really you know are part of this

(Refer Slide Time: 05:41) or part of this w star they do not contribute to w star so that is the conclusion that

(Refer Slide Time: 05:46) we are able to derive right. So this is from the primal point of view now let us just

(Refer Slide Time: 05:53) summarize all of this to see everything together so that it becomes much clearer the summary

(Refer Slide Time: 05:58) is the following right. So if I start looking at it from the dual point of view there are

(Refer Slide Time: 06:04) three cases alpha star equal 0 0 and alpha star is between 0 and c and alpha star i equal

(Refer Slide Time: 06:15) c. So if I look at it from the dual point of view I have w star transpose sorry primal

(Refer Slide Time: 06:21) point of view I have w star transpose x i y i is less than 1 w star transpose x i y i

(Refer Slide Time: 06:27) equals 1 and w star transpose x i y i is greater than 1.

(Refer Slide Time: 06:33) Now this is what we saw is that if alpha star i is equal to 0 this this implies w star

(Refer Slide Time: 06:40) transpose x i y i is greater than or equal to 1 it is classified with margin at least

(Refer Slide Time: 06:45) one. If you find alpha star is between 0 and c then it is exactly on the hyperplane and

(Refer Slide Time: 06:53) if you find alpha star i equal c then it is classified with margin less than or equal

(Refer Slide Time: 06:59) to 1. On the other hand if you find a point which is which has strictly less than 1 margin

(Refer Slide Time: 07:06) then that implies alpha star i equal c if a point is on the hyperplane then you cannot really

(Refer Slide Time: 07:13) conclude anything about alpha star i and if a point is away from the hyperplane in the

(Refer Slide Time: 07:20) right way then alpha star i does not contribute anything right. So it does not contribute anything

(Refer Slide Time: 07:26) to our final data final conclusion w star. So this is the summary so just to give a

(Refer Slide Time: 07:34) feel for in pictures right. So let us say we have a data set like this.

(Refer Slide Time: 07:41) So let us say this was our w star now if I told you that this is my w star well this

(Refer Slide Time: 07:52) is these are the supporting hyperplanes let us say this was my data set.

(Refer Slide Time: 07:59) A bunch of points on this side I am just point on the line maybe that is a point here.

(Refer Slide Time: 08:17) Let us say this was our this was my data set. Now if you are asked the question if this

(Refer Slide Time: 08:22) is the scenario and let us say I solve the problem and I observed the w star is like this.

(Refer Slide Time: 08:28) Now if I ask the question well what can I comment about the which are the important points

(Refer Slide Time: 08:33) which are the support vectors well what can I say right. So I can go over each of the

(Refer Slide Time: 08:40) points and see you know what equation does it satisfy with respect to w star. Now this

(Refer Slide Time: 08:46) is w star transpose x i y x i equals 1 this is w star transpose x i equals minus 1.

(Refer Slide Time: 08:54) Now if you look at this these points right so which are labeled with margin greater than

(Refer Slide Time: 09:00) 1 or these points which are also labeled with margin greater than 1 right. So these are

(Refer Slide Time: 09:09) on I mean these are not on the supporting hyperplane away from the supporting hyperplane

(Refer Slide Time: 09:15) and is classified correctly also these points right. So any point like this does not contribute

(Refer Slide Time: 09:22) to my w star at all right. So alpha star is 0. Now if I look at these points right. So this

(Refer Slide Time: 09:32) plus and this minus now maybe I should add a point here that is not maybe I will add

(Refer Slide Time: 09:37) a point here as a plus point. Now let us look at these 3 points maybe right. So I can

(Refer Slide Time: 09:45) improve this point as well in the in the discussion or maybe there can be minus here also right.

(Refer Slide Time: 09:53) So these 4 points now what can I say about these 4 points well for these 4 points w star

(Refer Slide Time: 10:01) transpose x i y i is strictly less than 1 right. So in fact for the points where I am pointing

(Refer Slide Time: 10:09) with the arrow w star transpose x i y i is actually less than 0 because they are incorrectly

(Refer Slide Time: 10:14) classified by w star whereas the points which are where I am pointing with dotted arrows

(Refer Slide Time: 10:21) these are correctly classified by w star because w star is eventually going to classify using

(Refer Slide Time: 10:26) this line right. So the dotted light blue arrow points are correctly classified by w star

(Refer Slide Time: 10:32) but then they are not classified with enough margin. So it does not matter if it is correctly

(Refer Slide Time: 10:37) classified or not as long as it is not classified correctly classified with enough margin all

(Refer Slide Time: 10:42) these points are contribute you know similarly and then in fact they are the most important

(Refer Slide Time: 10:47) points for these points alpha star equals c. Now there are some more points which I am going

(Refer Slide Time: 10:55) to you know highlight using orange circles. So these points what can I say about these points

(Refer Slide Time: 11:02) well they are on the supporting hyperplane right. So if they are on the supporting hyperplane

(Refer Slide Time: 11:09) I cannot really conclude what is their alpha star going to be right. So their alpha star can

(Refer Slide Time: 11:16) be anywhere between 0 and c. What I can conclude is that if I know that for a point alpha star

(Refer Slide Time: 11:24) is between 0 and c then I know that it has to be on the hyperplane but it should it could

(Refer Slide Time: 11:31) so happen that this guy has alpha 0 this guy has maybe 1 this guy has c let us say c is greater

(Refer Slide Time: 11:38) than 1 this guy has you know 0 this guy has 1 this guy has c all sorts of things are possible

(Refer Slide Time: 11:45) here right. So on the line it could be either 0 it could be c it could be 1 right. So but the

(Refer Slide Time: 11:54) moment I say that for this point so one the value is 1 which is between 0 and c then I know

(Refer Slide Time: 12:01) for sure that this point is on this line right. So these two points are on this line but if I

(Refer Slide Time: 12:06) just say that you know the point has value 0 or c then I cannot really conclude it is exactly

(Refer Slide Time: 12:12) on the line right. So on the line can take any value on one side of the line you get exactly 0

(Refer Slide Time: 12:17) values on the other side of the line you get you get exactly c values on the line it can be

(Refer Slide Time: 12:22) anywhere between 0 and c that is the conclusion that we draw here. Now the final point that I want

(Refer Slide Time: 12:28) to make about this is that still if you look at this picture everybody so let me let me point

(Refer Slide Time: 12:35) this right. So this this points can alpha star I can belong to 0 and c I do not know right.

(Refer Slide Time: 12:41) So it can be anywhere. So the final point that I want to say is that still if you look at the

(Refer Slide Time: 12:47) number of points which are actually going to contribute to my w star they are they are going to

(Refer Slide Time: 12:51) be only a handful because all the points with blue circles dark blue circles I have kind of

(Refer Slide Time: 12:57) I know for sure that they are their alpha star is 0. So they do not contribute to my w star

(Refer Slide Time: 13:03) the only ones that contribute to my w star are either on the hyper plane supporting hyper plane

(Refer Slide Time: 13:08) or on the wrong side of the supporting hyper plane. This the hope is that this set of points

(Refer Slide Time: 13:13) is still going to be a small set as compared to the billions of data points that we might have right.

(Refer Slide Time: 13:17) So because if your data set is indeed linearly separable with some outliers with respect to you

(Refer Slide Time: 13:24) know whatever kernel that you are using then it is you are still going to get a good w star

(Refer Slide Time: 13:29) where you the points which are not which are either on the supporting hyper plane or on the

(Refer Slide Time: 13:35) wrong side of it are going to be much smaller in number compared to the total number of data points.

(Refer Slide Time: 13:39) So you still are going to get a sparse solution which means that the conclusion is that even with

(Refer Slide Time: 13:45) respect to sparsity the soft margins of auto-veitermission does not lose out anything that is the

(Refer Slide Time: 13:50) final conclusion that I want to draw. So to summarize our discussion about soft margins of auto-veitermission

(Refer Slide Time: 13:56) by looking at the dual we are saying that it can be kernelized point number one the constraints

(Refer Slide Time: 14:01) for alphas are very simple these are box constraints between 0 and c which are easy to handle even

(Refer Slide Time: 14:07) if you are doing like a projected gradient descent kind of algorithm. And the final point is that

(Refer Slide Time: 14:12) you know the solution is still going to be sparse that is the number of points for which alphas

(Refer Slide Time: 14:17) star i is not is going to be non-zero is still going to be a handful of points when compared to the

(Refer Slide Time: 14:23) total number of points that you have. So all these make the soft margins of auto-veitermission

(Refer Slide Time: 14:30) as super powerful elegant formulation and and that is why you know it is not just the theoretical

(Refer Slide Time: 14:39) that is why if you look at several practical applications this algorithm performs really well in

(Refer Slide Time: 14:44) practice. So with this what we have kind of what we can conclude is that you know what we have

(Refer Slide Time: 14:51) seen so far is a very powerful algorithm in classical machine learning called the support vector

(Refer Slide Time: 14:57) machine we have looked at in quite some detail. And this has you know been successfully applied

(Refer Slide Time: 15:07) in several applications specifically in structured data that is data where you have features in a

(Refer Slide Time: 15:14) structured format this algorithm has been I mean really found to be very useful in practice.

(Refer Slide Time: 15:22) Now the actual implementation of this algorithm people have worked on a lot of you know advanced

(Refer Slide Time: 15:28) techniques optimization techniques to make this implementation really fast. In fact you can

(Refer Slide Time: 15:33) run this algorithm today using the fastest solver which runs in linear time in terms of the parameters

(Refer Slide Time: 15:38) of the problem. So even with respect to the running the algorithm you know we have very solid

(Refer Slide Time: 15:44) optimization techniques which we are not going to look at in this course but it is good to be aware

(Refer Slide Time: 15:48) that you know because it is a quadratic optimization problem natural question is how much time will

(Refer Slide Time: 15:53) it take to solve this problem it does it won't take too much time typically. So with all these

(Refer Slide Time: 15:59) advantages we want to conclude this part of the course by saying that we have put down a solid

(Refer Slide Time: 16:06) algorithm which is a soft margin support vector machine algorithm which can deal with non-structural

(Refer Slide Time: 16:11) relationships in classification boundaries decision boundaries can deal with outliers it is

(Refer Slide Time: 16:18) kernelizable so it is a very powerful algorithm. So what we will so I mean one small point that I

(Refer Slide Time: 16:26) wanted to make in contrast this with logistic regression which is also you know it can deal

(Refer Slide Time: 16:31) with outliers it there is also a kernel version of it. So these two algorithms typically you know

(Refer Slide Time: 16:39) are comparable usually in practice right. So both these algorithms are you know well motivated

(Refer Slide Time: 16:45) algorithms so to say and there is subtle difference in terms of what they are trying to optimize

(Refer Slide Time: 16:52) but other than that both these algorithms are usually competitive in practice. So people use

(Refer Slide Time: 16:59) I mean typically the idea is if you have a data set you can try out both these algorithms and see

(Refer Slide Time: 17:05) which one works well with respect to your validation set and then choose that algorithm for your test set.

(Refer Slide Time: 17:12) So with that we conclude the discussion about support vector machines and what we will see next time

(Refer Slide Time: 17:18) is a broader or a more meta type of approach to classification we have seen several algorithms

(Refer Slide Time: 17:27) now right from naive base you know decision trees can be as neighbors logistic regression support

(Refer Slide Time: 17:33) vector machine perceptron so on and so forth. So now we will look at a more broader view point

(Refer Slide Time: 17:39) we will take a meta view point and the next thing that we will start looking at or what are called

(Refer Slide Time: 17:45) ensemble classifiers and that will lead us to two interesting type of approaches for classification

(Refer Slide Time: 17:52) called bagging and boosting which is what we will start looking at next in this course.

(Refer Slide Time: 17:57) But now we conclude the discussion about support vector machine and hope you enjoyed it. Thank you.