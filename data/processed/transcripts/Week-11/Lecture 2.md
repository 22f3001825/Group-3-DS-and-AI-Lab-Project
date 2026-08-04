# Week-11 - Lecture 2

(Refer Slide Time: 00:00) So, we are asking the question, what do the complementary slackness conditions

(Refer Slide Time: 00:29) say about the soft margin SVM? To understand this, so we will remember the complementary slackness

(Refer Slide Time: 00:50) is a condition that depends on your primal optimal solution and the dual optimal solution

(Refer Slide Time: 00:55) and it links both of these. So, in this case, let w star and epsilon star be the primal

(Refer Slide Time: 01:08) optimal solutions and let alpha star and beta star be the dual optimal solution.

(Refer Slide Time: 01:26) Well, I am going to retain both alpha star and beta star so that analysis becomes easier.

(Refer Slide Time: 01:34) Now, we will see why that is the case, but let me first write down what the complementary slackness

(Refer Slide Time: 01:39) conditions are. It says the following. So, C s conditions. So, the first set of conditions is

(Refer Slide Time: 01:48) with respect to w star and alpha star. It would say that at optimality for all data points i

(Refer Slide Time: 01:56) alpha star i into 1 minus w star transpose x i y i minus psi i star this is going to be 0 at

(Refer Slide Time: 02:09) optimality. So, this is going to depend on alpha star and the primal variables.

(Refer Slide Time: 02:14) Now, the second set of conditions would be with respect to beta star which would say that

(Refer Slide Time: 02:20) for all i beta i star into minus epsilon i star equals 0 which is equivalent to saying beta i

(Refer Slide Time: 02:30) star into epsilon i star equals 0. So, remember this these were the two things that we added to

(Refer Slide Time: 02:35) the Lagrangian and what we are saying is that the terms extra terms that we add to the Lagrangian

(Refer Slide Time: 02:40) will actually be 0 at optimality that is what essentially complementary slackness is saying.

(Refer Slide Time: 02:46) So, what are the implications because of this right. So,

(Refer Slide Time: 02:51) now the way we are going to think of this is that we are going to look at various cases.

(Refer Slide Time: 02:57) There are various cases which are possible in this particular setup.

(Refer Slide Time: 03:04) Like last time there were only two cases. There was only one set of complementary slackness

(Refer Slide Time: 03:10) conditions which was just this there was no beta there in the hard margin case and the cases

(Refer Slide Time: 03:17) that we cared about is whether alpha i alpha star i contributes to my w star or not and the way

(Refer Slide Time: 03:25) we looked at it was saying by was by looking at whether alpha star i was greater than 0 or was

(Refer Slide Time: 03:30) equal to 0. And then we said that if alpha star i is greater than 0 then that point cannot

(Refer Slide Time: 03:37) you know has to lie on the supporting hyper plane and so you know if an equivalently if a point

(Refer Slide Time: 03:45) does not lie on the supporting hyper plane then alpha star i has to be 0 which is which is what

(Refer Slide Time: 03:53) kind of told us that you know the solution will be sparse combination of our data points.

(Refer Slide Time: 03:58) But here remember alpha star i is bound to be between 0 and c.

(Refer Slide Time: 04:05) So, now because the c also makes an appearance the when alpha star i takes a value of c that

(Refer Slide Time: 04:12) becomes a special case. So, the cases that we are going to look at are three cases when first

(Refer Slide Time: 04:18) is when alpha star i equal 0 the second is when it is between 0 and c and the third is when

(Refer Slide Time: 04:25) it is actually c right. So, we are going to look at three different cases. So, the first case we

(Refer Slide Time: 04:30) are going to look at is if alpha star i equal 0 what does this mean this means that I solved the

(Refer Slide Time: 04:37) dual problem and I observed that for a particular data point alpha star i equal 0 and I tell you that

(Refer Slide Time: 04:43) information. Here is a point for which alpha star i equal 0 now the question is what what can you

(Refer Slide Time: 04:50) infer from this is the question. Now, what can you infer from this the moment I say alpha star i

(Refer Slide Time: 04:56) equal 0 now this implies beta star i has to be equal to c why is this because we know that at

(Refer Slide Time: 05:04) optimality alpha star i plus beta star i equals well not just optimality right. So, this is a

(Refer Slide Time: 05:11) feasible condition we are always looking for alpha and beta such that they add up to c that is

(Refer Slide Time: 05:16) that is how you know beta induced the upper bound on alpha right. So, any feasible solution has

(Refer Slide Time: 05:23) to have this property and so the optimal alpha star beta star combination will also have this

(Refer Slide Time: 05:27) property. Now, so now beta star i equal c implies what well. So, now this implies

(Refer Slide Time: 05:39) epsilon star i has to be equal to 0 why is that that is because we have the property that you know

(Refer Slide Time: 05:46) our c s 2 right. So, this comes from c s 2 the complementary slackness second set which says that

(Refer Slide Time: 05:52) beta star i into epsilon star i equal 0 and if for a point beta star i equal c it is a non-negative

(Refer Slide Time: 05:58) quantity we are assuming c is strictly positive. So, which means that epsilon star i has to be equal

(Refer Slide Time: 06:04) to 0 right. So, this has to be 0 now what does epsilon star i equal to 0 mean right. So,

(Refer Slide Time: 06:11) well we know that w star transpose x i y i plus epsilon star i is greater than or equal to 1.

(Refer Slide Time: 06:23) This is something that we already know but now we are saying that for this special point where alpha

(Refer Slide Time: 06:28) star i equal 0 epsilon star i has to be equal to 0 which implies w star transpose x i y i is greater

(Refer Slide Time: 06:36) than or equal to 1 right. So, we know this is true why because this is a primal feasibility condition

(Refer Slide Time: 06:44) and so the optimal point will also satisfy this condition and now because for the special point

(Refer Slide Time: 06:49) that alpha star i equal 0 epsilon star i equal 0 which means that w star i transpose x i y i is

(Refer Slide Time: 06:55) greater than or equal to 1 well if this is greater than or equal to 1 this implies what this implies

(Refer Slide Time: 07:00) that w star plusifies x i y i correctly that is the implication right. So, well what does this

(Refer Slide Time: 07:16) mean in pictures it means in pictures that you know if I have some w star here this is my w star

(Refer Slide Time: 07:24) transpose x i y i and all I am saying now is that my data point can be you know anywhere on this

(Refer Slide Time: 07:34) line or to the right hand side right. So, so if I told you alpha star i equal 0 it has to be

(Refer Slide Time: 07:42) in this region is what I am saying. Why because alpha star i equal 0 because of our argument here

(Refer Slide Time: 07:53) implies that w star transpose x i y is greater than or equal to 1 which means that it can either be

(Refer Slide Time: 07:58) on the supporting hyperplane or it can be away from the supporting hyperplane right. So, in both

(Refer Slide Time: 08:03) these cases it could be anywhere here right. So, we cannot say anything more this is something

(Refer Slide Time: 08:08) that we can conclude which is good right. So, which means that our w star classifies this point

(Refer Slide Time: 08:12) correctly that is the implication. So, in some sense this is kind of telling us that well alpha

(Refer Slide Time: 08:20) star i equal 0 means that this point is actually not useful for our w star right. So, and that point

(Refer Slide Time: 08:26) is very well classified. So, the points that are really useful are going to be you know for which

(Refer Slide Time: 08:32) alpha star i is not equal to 0 which is where which is where we have to see what happens with respect

(Refer Slide Time: 08:38) to the implications. So, let us try that right. So, now the second point that we want to look at is

(Refer Slide Time: 08:45) second case that we want to look at is alpha star i is now within 0 and alpha star i is

(Refer Slide Time: 08:56) in the interval 0 comma c that is 0 alpha star i is strictly greater than 0 and strictly less than

(Refer Slide Time: 09:02) c. Now, what what implications can be derived based on this right. So, now this implies what

(Refer Slide Time: 09:08) will be know again alpha star i plus beta star i equal c which means that if alpha star i

(Refer Slide Time: 09:14) is between 0 and c then that means that beta star i is also between 0 and c. Now, this implies

(Refer Slide Time: 09:19) that beta star i is also in the same interval 0 and c only then they will add up to 1 that is 0

(Refer Slide Time: 09:26) less than beta star i less than c. Well, this implies again epsilon star i equal 0 this is from

(Refer Slide Time: 09:36) c s 2 right. So, because beta star i into epsilon star i has to be equal to 0 but beta star i

(Refer Slide Time: 09:42) cannot be 0 and so epsilon star i is 0 this is one implication right. So, the other implication is

(Refer Slide Time: 09:48) that well this also implies now this is c s 2 but then what was c s 1 c s 1 is alpha star i into

(Refer Slide Time: 09:56) this term has to be 0. But now, because alpha star i is between 0 and c it is a positive quantity

(Refer Slide Time: 10:04) strictly positive quantity. So, which means that the second term has to be 0 well the second term

(Refer Slide Time: 10:08) being 0 implies 1 right. So, this implies 1 minus w star transpose x i y i minus epsilon star i

(Refer Slide Time: 10:16) has to be equal to 0 this is by complimentary slackness 1. Now, this implies well because

(Refer Slide Time: 10:23) we already have derived epsilon star i 0 this implies that 1 minus w star transpose x i y i

(Refer Slide Time: 10:31) equals 0 that is we are saying that w star transpose x i y i equals 1.

(Refer Slide Time: 10:40) What does this mean this means that well if I solve the dual and I find that for a particular

(Refer Slide Time: 10:46) point alpha star i is between 0 and c right then it means that that point lies on the supporting

(Refer Slide Time: 10:57) hyperplane right. So, it is strictly greater than 0 and strictly less than c then the only way

(Refer Slide Time: 11:02) that can happen is if this point is on the supporting hyperplane right. So, which means again in

(Refer Slide Time: 11:07) pictures right. So, this means that I have a w star here now like there may be points here

(Refer Slide Time: 11:19) right. So, these are points. So, these are points

(Refer Slide Time: 11:27) right. So, if if I find alpha star between 0 and c then it could be it has to be on this line right.

(Refer Slide Time: 11:35) So, now remember alpha star being between 0 and c means that it actually contributes to my w star

(Refer Slide Time: 11:42) right. So, which means that the points that are actually contributing with values less than c

(Refer Slide Time: 11:48) it is it is a positive value it contributes to my w star y because w star is a linear combination

(Refer Slide Time: 11:53) of our data points and these are points which contribute to my w star and it has to be on this line

(Refer Slide Time: 12:00) right. So, these have our support vectors because they are contributing to my w star

(Refer Slide Time: 12:08) and they are they you can find them on this line right. So, that is the first implication which

(Refer Slide Time: 12:13) is a which is an important implication. Now, there is one more case now which is the case where

(Refer Slide Time: 12:19) alpha star exactly equal c right. So, which means that you know the larger the value of alpha star

(Refer Slide Time: 12:26) the more it actually contributes to my w star in some sense right. So, when alpha star is 0 then

(Refer Slide Time: 12:31) we are saying that it is either on the supporting plane or it is away from the supporting plane that

(Refer Slide Time: 12:36) is the implication we derive. If alpha star equals is between 0 and c then it is exactly on the

(Refer Slide Time: 12:42) supporting plane. Now, what would happen if alpha star equal c that is where are the points where

(Refer Slide Time: 12:47) alpha star is the largest right. So, that is that is an interesting case too right. So,

(Refer Slide Time: 12:52) then let us case 3 alpha star equals c. So, now what what are the implications that we can derive

(Refer Slide Time: 13:00) if alpha star equals c well immediately this means that beta star alpha i star equals c

(Refer Slide Time: 13:08) the immediate implication is that beta star equals what is 0 because beta alpha star plus beta star

(Refer Slide Time: 13:13) has to be c. Now, this kind of implies that epsilon star i we cannot really say anything about

(Refer Slide Time: 13:20) epsilon star i now because the product has to be 0 and beta star is 0. So, we cannot really say

(Refer Slide Time: 13:26) anything but we know that you know by our constraint that epsilon star i the amount of bribe that

(Refer Slide Time: 13:32) i th data point base is greater than or equal to 0 that is still that is the only thing you can

(Refer Slide Time: 13:36) say you cannot really say anything more via this argument. On the other hand so, this is

(Refer Slide Time: 13:42) on the other hand we know via c is 1 that if this is a positive quantity then 1 minus

(Refer Slide Time: 13:50) w star transpose x i y i minus epsilon i star has to be 0 this has to be 0. Why because the product

(Refer Slide Time: 14:00) of these two things are at v 0 and alpha star is not 0. So, this guy is 0 right. So, now what does

(Refer Slide Time: 14:07) this tell us right. So, what what is the implication of this well the implication of this is that

(Refer Slide Time: 14:11) epsilon star i equals 1 minus w star transpose x i y i and this guy is greater than or equal to 0

(Refer Slide Time: 14:19) because epsilon star i you know is greater than or equal to 0. Now, this implies that w star

(Refer Slide Time: 14:26) transpose x i y i is less than or equal to 1 right. So, now, this is an interesting case.

(Refer Slide Time: 14:33) Now, what we are saying is that w star transpose x i has to be less than or equal to 1.

(Refer Slide Time: 14:40) What does that mean? Well that means something interesting is happening right. So, with respect to

(Refer Slide Time: 14:44) these data points where are these data points well again in pictures well if let us say this is

(Refer Slide Time: 14:51) w star this is w star transpose x i let us say we take a positive data point for the moment

(Refer Slide Time: 15:00) and see when would a positive data point satisfy this condition. Well this is saying if y i is

(Refer Slide Time: 15:06) positive then w star transpose x i is less than or equal to 1. Well where are those points? Well

(Refer Slide Time: 15:12) those points are here right. So, on this side it is here right. So, this is the set every

(Refer Slide Time: 15:25) point every point on the left side of this line which is w transpose x i equals 1.

(Refer Slide Time: 15:36) This is sorry about that. This is just the set of all x such that w star transpose x i equals 1.

(Refer Slide Time: 15:46) Now, this means that well for the w star I know that it is you will finally classify based on

(Refer Slide Time: 15:54) this line right. So, the dotted line here anybody to the right hand side of this is positive

(Refer Slide Time: 15:59) anybody to the left hand side is what you are going to say as negative.

(Refer Slide Time: 16:02) Now, if it so happens for this w star right. So, if there is a point that is here

(Refer Slide Time: 16:10) which is positively labeled in my training data. Now, for this w star it could so happen that

(Refer Slide Time: 16:19) this point is here. Now, what does mean this means that w star transpose x i is actually

(Refer Slide Time: 16:26) negative for this point because it is to the left of this line this is the line where w star

(Refer Slide Time: 16:31) transpose x is 0 right. So, this is the set where w star transpose x is 0 which means that if

(Refer Slide Time: 16:38) the point is on the negative half space then we are going to label this point as negative which

(Refer Slide Time: 16:42) means that w star might actually misclassify this point right. So, you solve the problem and then

(Refer Slide Time: 16:47) you observe that well for this w star this point is actually incorrectly classified that is one

(Refer Slide Time: 16:53) case or it can be correctly classified, but if it does it is in this region right. So, it is in

(Refer Slide Time: 17:01) this region in this region it will w star will classify this point maybe there is a point here

(Refer Slide Time: 17:07) right. So, for this point w star will actually classify this correctly, but it is not

(Refer Slide Time: 17:14) classifying it with enough margin. We want each data point to be classified with margin 1,

(Refer Slide Time: 17:20) but then here is a point where it is classified correctly, but not with margin 1 right or one or

(Refer Slide Time: 17:26) greater than one it is classified with margin less than or equal to 1 right. So, these so which means

(Refer Slide Time: 17:31) that the points where w star transpose x i y a less than or equal to 1 are exactly the points

(Refer Slide Time: 17:38) where either x i is incorrectly classified

(Refer Slide Time: 17:50) by w star or correctly classified, but with margin less than or equal to 1 right. So, what we

(Refer Slide Time: 18:14) really wanted was you know every point should be classified with enough margin with margin greater

(Refer Slide Time: 18:19) than or equal to 1, but it so happens that there are these points where the margin is less than

(Refer Slide Time: 18:25) or equal to 1 which means that it could be less than 0 in which case it is incorrectly classified

(Refer Slide Time: 18:30) or it is not classified with enough margin. Now, in some sense if you think about this these

(Refer Slide Time: 18:36) points where you are actually making a mistake are in fact the outliers in the original data set

(Refer Slide Time: 18:42) right. So, you can think of these as points where w star is getting being robust to our data set

(Refer Slide Time: 18:47) and then it is misclassifying these outliers in some sense right. So, but then that is okay right.

(Refer Slide Time: 18:53) So, because the outlier is on the wrong side of your w star and so it might get misclassified

(Refer Slide Time: 18:58) or it is too close to your w star in which case the margin it might not be classified with enough margin.

(Refer Slide Time: 19:04) Now, it so happens that now what we are saying is that these points are the ones that are the

(Refer Slide Time: 19:10) most important for our w star why because their alpha star is actually equal to c right.

(Refer Slide Time: 19:17) So, which means that if I solve the dual problem and I find that there is a point where alpha star

(Refer Slide Time: 19:22) equals c well which means that it is contributing the most to my w star. Now, where are those points

(Refer Slide Time: 19:28) those points are either incorrectly classified or classified with less margin margin less than or

(Refer Slide Time: 19:33) equal to 1 right. So, that so the important points are those which are you know which could be

(Refer Slide Time: 19:40) two things right. So, in this argument it is saying that well if the point has strictly between

(Refer Slide Time: 19:44) 0 and c then it is on the hyper plane those are support vectors on the supporting hyper planes

(Refer Slide Time: 19:51) but then those are not just the support vectors there are more support vectors in the soft margin

(Refer Slide Time: 19:56) which are points which are you know in this danger region in some sense right. So,

(Refer Slide Time: 20:02) it could be in this region I call this danger region because this is this is the region where

(Refer Slide Time: 20:07) you are not so confident about this w star and so your w star actually gets influenced by these

(Refer Slide Time: 20:12) points a lot and also the points which are incorrectly classified. These are all support vectors

(Refer Slide Time: 20:17) anything for which alpha star i is greater than 0 we are going to call it a support vector because

(Refer Slide Time: 20:22) those points actually are necessary for our final w star in the hard margin case they are they will

(Refer Slide Time: 20:29) necessarily lie on the supporting hyper plane in the soft margin case will they can either be on

(Refer Slide Time: 20:34) the supporting hyper plane or they can be to the left of the supporting hyper plane if it is a

(Refer Slide Time: 20:38) positive point and right of the supporting hyper plane if it is a negatively labeled point.

(Refer Slide Time: 20:42) In other words their points which are either on the supporting hyper plane or points which are

(Refer Slide Time: 20:47) labeled with in the danger zone with with have which have margin less than 1 less than or equal to

(Refer Slide Time: 20:54) 1 or points which are in fact actually classified incorrectly classified for which w star transpose

(Refer Slide Time: 21:00) x i y is less than 0. So, this is one way to think about this complementary slackness condition

(Refer Slide Time: 21:09) which is you solve that you imagine you are solving the dual problem and looking at alpha stars

(Refer Slide Time: 21:14) and then trying to argue where are these points.