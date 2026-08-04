# Week-11 - Lecture 6

### Timestamp: 00:00

 So, what we are going to see now is a very, very powerful ensemble technique called the

### Timestamp: 00:19

 method of boosting and it is a very general technique, but we look at a very specific

### Timestamp: 00:24

 algorithm which is called as the add a boost algorithm. So, this algorithm is due to

### Timestamp: 00:34

 front and shafi rei. I think back in the 90s and in fact, front and shafi rei won the

### Timestamp: 00:48

 Gordel price for coming up with this algorithm for their contributions to theoretical machine learning

### Timestamp: 00:55

 especially coming up with this technique of boosting. So, what is the idea of boosting?

### Timestamp: 01:01

 Boosting also tries to you know start with a weak learner and then convert it into a strong learner.

### Timestamp: 01:12

 In a very, very theoretically sound principle fashion, now these weak learners need not necessarily

### Timestamp: 01:20

 be overfit classifiers. These weak learners could be underfit classifiers also and that is one of

### Timestamp: 01:27

 the reasons why boosting is a very powerful technique because it is very easy to get quick

### Timestamp: 01:32

 underfit classifiers. For example, if you are running a decision tree algorithm and then you cut

### Timestamp: 01:38

 your stop your algorithm after you just run figure out one single question some feature less

### Timestamp: 01:46

 than threshold value. Now, that is a weak learner. So, because you are that is basically that is

### Timestamp: 01:53

 going to have a high bias with respect to the bias that we discussed earlier because it is

### Timestamp: 01:57

 going to be a very simple classifier. It is going to for instance if you are in a two dimensional

### Timestamp: 02:01

 plane, it is just going to cut your feature space into two parts and say that one side is positive,

### Timestamp: 02:06

 the other side is negative. So, it could be a vertical cut or a horizontal cut depends on which

### Timestamp: 02:11

 feature you are choosing, but then it is a very simple simplistic classifier. In higher dimension,

### Timestamp: 02:16

 it is even more simple. But then it is easy to obtain because you do not have to spend too much

### Timestamp: 02:21

 computational effort to obtain this such a classifier. So, a decision stump in this case,

### Timestamp: 02:26

 typically when we talk about boosting, we are talking about decision stump as our weak learners.

### Timestamp: 02:32

 What are decision stump? Decision stump are just no classifiers like this.

### Timestamp: 02:39

 So, a one level or two level classifiers. Sometimes you can even use two levels, which means that you

### Timestamp: 02:46

 are asking two different questions to decide plus one or minus one. The typical number of

### Timestamp: 02:51

 height of a decision tree in practice would be something like 10 to 15, but then if you are cutting

### Timestamp: 02:56

 it out at one or two, then it is typically going to that is going to be a significant drop in accuracy.

### Timestamp: 03:01

 Because you have not trained it enough, which means that you are looking at a very simple

### Timestamp: 03:05

 weak learner, very high bias low variance, but a high bias weak learner. Now, the question is

### Timestamp: 03:12

 can we somehow combine that let us say I have an access to a algorithm, which when given a data set

### Timestamp: 03:20

 is going to output a weak learner, which could be a decision stump for example, can I use this

### Timestamp: 03:25

 black box in an intelligent way such that I can convert this weak learner into a strong learner,

### Timestamp: 03:30

 which will give me let us say zero training error. So, if we start with a data set where I use a

### Timestamp: 03:36

 weak learner, which just ask one question to decide my classification, that is not going to get me

### Timestamp: 03:42

 100 percent training accuracy. So, whereas can we somehow use this weak learner as a black box

### Timestamp: 03:50

 to kind of massage what is being fed into the weak learner, so that we kind of get a different

### Timestamp: 03:57

 classified we will see how, which kind of gives you zero training error. If you get something

### Timestamp: 04:03

 like that, then that is what we are going to call as a strong learner in this case.

### Timestamp: 04:06

 The question is can we go from a weak learner to a strong learner, boosting says yes this is

### Timestamp: 04:11

 possible and it gives you an algorithmic way to achieve this. And we will let me put down the

### Timestamp: 04:16

 algorithm and then we will start discussing what this algorithm is. So, here is the algorithm.

### Timestamp: 04:23

 So, this is the add up boost algorithm, which stands for adapt to boosting,

### Timestamp: 04:33

 the add up stands for adapt to. And as usual the input to the algorithm is just a data set,

### Timestamp: 04:44

 let us call this data set s, which is x 1 y 1 dot dot x and y n, where our x i is in R d and y i

### Timestamp: 04:56

 is plus or minus 1. Now, the main idea is we are going to replace our two steps of bagging with

### Timestamp: 05:04

 more principle steps. If you remember from bagging the first step was create these bags.

### Timestamp: 05:10

 So, on each of the bags is created by uniformly sampling with replacement from the initial

### Timestamp: 05:16

 data set that you have. Here we are going to create bags in a slightly different way.

### Timestamp: 05:21

 We are not going to think of them as bags, but then let us say we are going to think of them as

### Timestamp: 05:26

 waves associated with each data point and we will see what is the connection with the bags in a minute.

### Timestamp: 05:31

 So, what we are going to do is we are going to initialize some waves or a distribution over

### Timestamp: 05:37

 these data points, which let me call them as d naught of i is 1 over n. What is d naught of i?

### Timestamp: 05:46

 This naught separates, indicates the iteration number. So, at initialization every data point i

### Timestamp: 05:53

 gets an uniform weight. So, which means that what I am going to do now is create a bag

### Timestamp: 06:02

 from the original data set based on these weights. You can imagine it that way, which means that

### Timestamp: 06:07

 if the weights are all the same, then the way I am going to create the bag data points in the bag

### Timestamp: 06:14

 is to sample from the original data set s according to this probabilities, which means every point

### Timestamp: 06:19

 gets a chance of 1 over n to be in the bag. To the for the next point I am again going to use

### Timestamp: 06:24

 the same distribution to sample a point, which means that essentially we are sampling uniformly sampling

### Timestamp: 06:30

 with replacement. Now, this is only for the initialization. The idea now in boosting is we are going

### Timestamp: 06:37

 to change this distribution at every round. So, this is an iterative algorithm, where at every

### Timestamp: 06:43

 round this distribution is not no longer going to be uniform, it is going to change and let us see

### Timestamp: 06:47

 how it changes. Let me put down the algorithm and then it will be clear how it changes.

### Timestamp: 06:52

 So, now what happens is for t equals 1 to capital T, so you have t different rounds and we will

### Timestamp: 06:59

 decide what t is in a bit. What you are going to do is we are going to input the current

### Timestamp: 07:08

 distribution d t and the data set s t to a v-cloner to get h t. So, let us say h t is this.

### Timestamp: 07:26

 What do I mean by this? Well, you have a v-cloner. When I say you are inputting s comma d t

### Timestamp: 07:33

 to this v-cloner, basically you can either think of the v-cloner getting as input the data points

### Timestamp: 07:40

 and some weights associated with this data points. If the v-cloner can handle data points along

### Timestamp: 07:46

 with weights, if we have an algorithm which can handle not just data points, but we are also

### Timestamp: 07:50

 saying some weights associated with this data points, then fine we can input both the data set

### Timestamp: 07:56

 and the weights associated with it to the learner. If the algorithms that we have seen so far,

### Timestamp: 08:01

 right, so typical algorithms like decision trees and so on, the vanilla version flavor of the

### Timestamp: 08:07

 algorithm, they do not handle specifically the weights associated with data points. In which case,

### Timestamp: 08:13

 what you can do is you can create a bag based on d t from s by which I mean that d t is

### Timestamp: 08:20

 telling me how important is each data point for this bag, right. So, it is giving me some

### Timestamp: 08:25

 probability. If a if a if a weight t t of i is 0.7, it means that if I sample from this distribution

### Timestamp: 08:32

 a data point 70 percent chance that this data point shows up, right. So, that is what 0.7 means.

### Timestamp: 08:37

 And then I kind of do this in different times and then I create a bag which I have created

### Timestamp: 08:42

 according to d t from s, right. So, I hope that is clear. And now if I pass it on to a v-cloner,

### Timestamp: 08:49

 I now run a decision tree on top of this and then I get out a classified which I am going to call

### Timestamp: 08:53

 as h t. So, that is the t-th classified that I am getting in round 1. So, which means that basically

### Timestamp: 08:59

 we are training a v-cloner on a bag which is generated according to some distribution d t and

### Timestamp: 09:05

 then we are calling the resulting class far as h t. Remember h t is r d 2 plus or minus 1, right.

### Timestamp: 09:12

 So, it is a it is a binary classification problem. So, it is a binary classification.

### Timestamp: 09:17

 So, now what we are going to do is this is the interesting part in boosting.

### Timestamp: 09:23

 Now we are going to change the distribution which we are going to use for the next round.

### Timestamp: 09:29

 So, we had some weights for each of these data points. Now what we are going to do is we are

### Timestamp: 09:33

 going to update these weights and the way we are going to update these weights is in an intuitive

### Timestamp: 09:39

 fashion, right. So, now what what are we trying to do is let us say initially we created a sample

### Timestamp: 09:47

 we created a bag by uniformly sampling from your original data set and then we ran a decision tree

### Timestamp: 09:53

 and then we got a decision tree out of it. A decision stump let us say. Now you had 1000 data points

### Timestamp: 10:00

 at the beginning let us say and now this decision stump is classifying 600 of these points

### Timestamp: 10:05

 correctly and 400 of these points incorrectly let us say, right. So, now in the next round you want

### Timestamp: 10:11

 a different decision tree to be locked. Now the question is I have the luxury now to change the

### Timestamp: 10:18

 weights of these data points. Now what should I do how the question is how should I update these weights?

### Timestamp: 10:27

 Now there are 600 points which this the first round decision tree has got correct and 400 points

### Timestamp: 10:32

 with the first round decision tree has incorrectly classified. Now in the second round should the

### Timestamp: 10:37

 weights of the 600 points go up or go down that is the question that we are asking. Now what do

### Timestamp: 10:45

 we intuitively want? Now the first decision tree has done well on 600 points. Now the second

### Timestamp: 10:52

 decision tree is also going to do better than random which means that if I increase the weight

### Timestamp: 10:58

 of the points where the previous decision tree has not done well has incorrectly classified.

### Timestamp: 11:06

 Now those points will become important for the next decision tree, right. So because they have

### Timestamp: 11:12

 higher weights now if it is a weak learner then you can argue weak learner basically if you are

### Timestamp: 11:19

 trying to sample according to you know weights where some points get higher weights now those

### Timestamp: 11:25

 points are going to get repeated more in your data set because they have high probability of

### Timestamp: 11:29

 getting chosen. So your decision tree will try to you know do well on those data points. It will

### Timestamp: 11:35

 try to find features which will do well for those data points, right. Now the way we are going to

### Timestamp: 11:42

 enforce that where we are going to enforce the next decision tree to do well on points where

### Timestamp: 11:48

 the previous decision tree fail to do is by updating the weights associated to the points

### Timestamp: 11:54

 in a specific fashion and what is the specific fashion? Well we are going to say the following.

### Timestamp: 11:59

 We are going to update the weight of the i th data point in the next round as follows.

### Timestamp: 12:05

 We are going to update it in a multiplicative fashion. We are going to say the weight let me first

### Timestamp: 12:11

 put it this way. We are going to say the weight multiplicatively increases by e power some alpha

### Timestamp: 12:19

 t and we will talk about alpha t in a minute which means we are increasing the weight if

### Timestamp: 12:26

 h t of x i equals y i, right. So which means that if the t th classifier

### Timestamp: 12:37

 well it is not equal to y which means that if the t th classifier did not get the point

### Timestamp: 12:43

 x i correctly classified then what we are going to do is we are going to bump up the weight of

### Timestamp: 12:50

 the i th data point by e power alpha t. On the other hand we are going to say d t we are going to

### Timestamp: 12:57

 reduce the weight by the same alpha t but then e power minus alpha t if h t of x i equals by

### Timestamp: 13:07

 a, right. So if it is correctly classified then I reduce the weight by a multiplicative factor

### Timestamp: 13:11

 if it is incorrectly classified then I increase it by a multiplicative factor.

### Timestamp: 13:15

 What this factor is we will talk about in a bit but this is the fact that this is how you

### Timestamp: 13:19

 increase the weight. But now what happens is there is a problem here, right. So the moment I

### Timestamp: 13:25

 increase by some factor and decrease by some factor now these weights are no longer going to sum

### Timestamp: 13:31

 up to 1 but then I want it to be a distribution because I am going to sample from this.

### Timestamp: 13:36

 So what I would do is typically I am going to you know think of this as d hat t which is like a

### Timestamp: 13:41

 middle in between term and then the actual updated weight is going to be you know d hat t plus

### Timestamp: 13:48

 1 i divided by you know sum over j d hat t plus 1 of j. Basically I am normalizing my weights

### Timestamp: 13:59

 so that they sum to 1, right. So you can think of this as maybe initially weight was 0.3,

### Timestamp: 14:04

 0.5, 0.2 for three different data points, right. So this was the this was

### Timestamp: 14:10

 d 1 of 1, 2, 3, right. So d of course d 0 is going to be 0.33, 0.33, 0.33.

### Timestamp: 14:24

 And now d 1 was like this let us say and now the h 1 classifier got these two points correctly.

### Timestamp: 14:32

 This is x 2, this is x 3, this is for x 1. Let us say the classifier that came out of this d 1

### Timestamp: 14:38

 was h 1 which correctly classified these two points and incorrectly classified this point.

### Timestamp: 14:44

 So now what would d 2 be? Well d 2 be will be 0.3 times e power alpha alpha 1 because h 1

### Timestamp: 14:53

 classified it can correctly. This would be 0.5 into e power minus alpha 1, 0.2 into e power

### Timestamp: 14:58

 minus alpha 1. But then now these two guys these three guys do not sum to 1. Here they sum to 1,

### Timestamp: 15:04

 here they sum to 1, but here they do not sum to 1. So what we do is we divide it by some z,

### Timestamp: 15:09

 so that they sum to 1, where z in this case would be 0.3 e power alpha 1 plus 0.5 power minus alpha 1

### Timestamp: 15:18

 plus 0.2 e power minus alpha 1. Basically you are normalizing it to sum to 1. So now this

### Timestamp: 15:24

 becomes a distribution, right. So now you can keep continuing this, right. So and you do this for

### Timestamp: 15:31

 T different rounds, right. So you do this for T different rounds and that is it, right. So now

### Timestamp: 15:40

 what you have done is you have kind of updated the weights so that you are correcting the mistakes

### Timestamp: 15:46

 of the previous classifiers and you are doing this for T different rounds. And now finally I need to

### Timestamp: 15:52

 tell you well at the end end of this procedure you have h 1 to h t, right. So you have h 1, h 2

### Timestamp: 16:00

 dot dot dot h t, T different classifiers, weak learners, which have been trained on different

### Timestamp: 16:06

 distributions with respect to the data. Now the question is how can I combine these T different

### Timestamp: 16:11

 learners to do something to come up with an aggregate classifier. Now boosting says that the way

### Timestamp: 16:18

 to combine this would be to do the following, right. So your final classifier which we are going

### Timestamp: 16:22

 to call as let us say h star of x is going to be very similar to bagging but then slightly

### Timestamp: 16:29

 different sum over T equals 1 to T, h t of x so far same but then you are not going to

### Timestamp: 16:37

 average these things but then you are going to do a weighted average of these things, right.

### Timestamp: 16:42

 So the weighted average is going to the weights are going to be given by the alphazes. The alphazes

### Timestamp: 16:49

 T's are exactly the bumping up factors for these weights, right. So one can argue that the right

### Timestamp: 16:55

 weights that you need to use here are in fact alphazes and of course you look at the sign of this

### Timestamp: 17:01

 classifier as usual, right. So basically what we have done is in boosting is we have changed

### Timestamp: 17:08

 both the assumptions that bagging does into something more principal. The first thing is that we

### Timestamp: 17:13

 have changed bootstrapping where all the bags were sampled uniformly at random. Now we are changing

### Timestamp: 17:19

 it to you know creating bags with respect to different distributions over the data points

### Timestamp: 17:24

 where the distributions are carefully chosen such that they kind of push the weights up for data

### Timestamp: 17:32

 points which had more errors with respect to the previous rounds classifier. So that is the

### Timestamp: 17:40

 bootstrapping part becomes slightly different right to a more principal way in boosting and the

### Timestamp: 17:45

 aggregation part also becomes slightly different in the sense that we are going to use a weighted

### Timestamp: 17:50

 average as opposed to just doing an average. So now what are these weights going to be? Well again

### Timestamp: 17:57

 if I had to derive goodness of the boosting algorithm one can argue that the right way to set these

### Timestamp: 18:04

 weights would be to do the following your alphazes has to be ln of square root of you know one

### Timestamp: 18:14

 minus error of ht divided by error of ht. Well this is this is this just comes from the analysis

### Timestamp: 18:26

 of the boosting algorithm basically what you are saying is that I gave a data set under distribution

### Timestamp: 18:34

 dt to a weak learner and I got an output ht which is a weak learner decision tree. Now that ht

### Timestamp: 18:40

 makes a certain error with respect to dt right so it makes some so some points are I have high

### Timestamp: 18:45

 weight some points have low weight. So now I look at the set of points where it makes mistakes and

### Timestamp: 18:50

 then just add up the weights of those points with respect to dt and that is the error ht.

### Timestamp: 18:56

 Now you set your alphate based on this error ht is what boosting says right so now the way you

### Timestamp: 19:02

 set it is you know there is a ln and you can see why the ln has to appear here is because this is

### Timestamp: 19:08

 an e power something it is somehow saying that basically you are increasing the weight by

### Timestamp: 19:13

 the square root of 1 minus error of ht by error of ht right so if the if the weighted error right so

### Timestamp: 19:21

 is low then that means that you are kind of increasing it by lot or if the weighted error is high

### Timestamp: 19:27

 then you are increasing it by low right so that is the that I mean that is the that is what comes out

### Timestamp: 19:32

 when if you set alphate in a very principled fashion it will be beyond the scope to discuss why

### Timestamp: 19:39

 we are setting alphate like this but then interested audience can look at a simple proof for you know

### Timestamp: 19:47

 the boosting algorithm where you can argue that as your number of round increases you can

### Timestamp: 19:53

 argue if you set alphate in this particular fashion then the training error of the final classifier

### Timestamp: 20:01

 so this is the final classifier this is ht right so after t rounds you get a classifier like this

### Timestamp: 20:07

 and then you can ask how much training error does this classifier make on the original data set yes

### Timestamp: 20:12

 because it is kind of aggregating a lot of weak learners weak learners are all going to make a lot

### Timestamp: 20:17

 of errors on my training data but then how does the training error of this aggregated class

### Timestamp: 20:21

 where look like on the original data set well one can argue that if we set alphate in this particular

### Timestamp: 20:27

 way then the training error decreases in some sense in a greedily fast rate right so we can in

### Timestamp: 20:33

 fact exactly argue that I will kind of make that statement if t is greater than a quantity which

### Timestamp: 20:47

 which is as follows and we will talk about this in a bit then

### Timestamp: 21:00

 training error equals 0 one can prove right so one this is this is why you boosting such a

### Timestamp: 21:08

 beautiful algorithm one can prove one can give a guarantee that if the number of rounds that you

### Timestamp: 21:13

 run this algorithm for is greater than a particular quantity then your training error goes to 0

### Timestamp: 21:20

 now what is this particular quantity well one quantity involves two things one is you know the number

### Timestamp: 21:26

 of data points the more the data data points that you have you know the more rounds that you would

### Timestamp: 21:31

 need to get to 0 training error which is a natural thing that you would expect but then here it is

### Timestamp: 21:35

 saying that well the number of rounds is only going to depend longer than a million the number of

### Timestamp: 21:40

 data points that you have which is a good thing to have but more importantly what it has is

### Timestamp: 21:47

 is a parameter gamma which determines how good our v-clerners are I did not define this formally

### Timestamp: 21:55

 again in this in this course but this parameter says how good is my v-clerner right so slightly

### Timestamp: 22:10

 more precisely what it means is that your v-clerner is better than random that is the assumption

### Timestamp: 22:17

 right so now how much more is it better than random is the question right so if it is accurate

### Timestamp: 22:24

 60 percent then it is 10 percent better than 50 percent accuracy which means that gamma is going

### Timestamp: 22:31

 to be 0.1 right so because 60 percent is 0.6 it is 0.1 more than 0.5 if it is 70 percent accurate then

### Timestamp: 22:37

 gamma is going to be 0.2 if it is 90 percent accurate gamma is going to be 0.4 and so on right so

### Timestamp: 22:43

 basically what what this is seeing is that if your v-clerner so the number of rounds that your

### Timestamp: 22:49

 algorithm is going to take to combine the v-clerners to get a strong learner which makes 0 error

### Timestamp: 22:55

 on my training data depends on how weak the v-clerner is if the v-clerner is 2 week it is just let us

### Timestamp: 23:01

 say 0.51 percent 51 percent accuracy is what it can guarantee then this gamma is going to be 0.01

### Timestamp: 23:09

 which means that it is a small value so the t is going to go up whereas your v-clerner is 0.75

### Timestamp: 23:14

 percent 75 percent accurate the gamma is going to be 0.25 in which case the number of rounds that you

### Timestamp: 23:19

 need to bring the training error down to 0 is going to be lower the stronger the weak learner is

### Timestamp: 23:23

 the lesser the number of rounds right so but then how we do not know a priori that is the beautiful

### Timestamp: 23:28

 part of boosting we do not know a priori how strong or weak the v-clerner is but then the

### Timestamp: 23:34

 guarantee is that the algorithm does not need to know how strong or weak the v-clerner is right so

### Timestamp: 23:40

 you can keep adding more and more v-clerners to your classifier and eventually the training error

### Timestamp: 23:45

 has to go to 0 that is what this theory would say the main reason why this is such a beautiful

### Timestamp: 23:50

 algorithm and such a principled algorithm is that you know the previous versions of boosting that

### Timestamp: 23:56

 came before this needed to know this gamma needed to know how weak the v-clerner is as part of

### Timestamp: 24:01

 the algorithm itself but here we do not use that at all and still we are able to you know get

### Timestamp: 24:07

 an algorithm which will drive the trainer to 0. So that is the power of boosting again we won't

### Timestamp: 24:13

 you know full-fledged derivation of why this is true and one can refer to standard textbooks

### Timestamp: 24:21

 on boosting for this but I would want to make one comment about boosting itself is that so what

### Timestamp: 24:29

 we are saying is if you run this algorithm for large in large enough number of iterations you

### Timestamp: 24:34

 have a lot of weak learners which you can combine such that the learner that results make zero

### Timestamp: 24:41

 training error but what we really care about is doing well on the test data so how does boosting

### Timestamp: 24:47

 perform on the test data is a question that one needs to think about one way to think about that

### Timestamp: 24:53

 is to you know plot this and see what happens as a function of t as I increase the number of

### Timestamp: 24:59

 v-clerners that I add to my booster classifier I can ask how does the error behave now the theory

### Timestamp: 25:08

 says of course that we can prove that the error the training error will go down to 0 and then

### Timestamp: 25:15

 we will continue to stay at 0 right so there will be some t t t t star after which the trainer will

### Timestamp: 25:22

 go to 0 right so this is trainer now we can imagine a situation where at after each rounds

### Timestamp: 25:33

 let us say 1 2 3 dot dot after each round I stop my boosting algorithm and I ask how much is the

### Timestamp: 25:39

 test error right so let us say there is a test set which I have not touched for my training I can

### Timestamp: 25:43

 ask how much error does my boosting algorithm make on the test set now if you measure that well the

### Timestamp: 25:49

 test error will kind of also decrease now one might think that the moment training error

### Timestamp: 26:02

 becomes 0 you have a classifier which gets all the data points correctly so now one can hope that

### Timestamp: 26:12

 or one can believe that after this if I still keep adding more classifiers well the training

### Timestamp: 26:18

 error is going to remain 0 but perhaps I am starting to fit the noise a little bit more and so

### Timestamp: 26:24

 I will start overfitting so one way to check if you are really overfitting is by looking at the test

### Timestamp: 26:31

 if the test error starts let us say increases like this the moment trainer will become 0

### Timestamp: 26:39

 then this part is actually overfitting because you are adding more and more

### Timestamp: 26:43

 weak learners into your aggregate classifier that it is starting to fit the noise

### Timestamp: 26:48

 but surprisingly what happens in practice for a lot of data sets is that even after your training

### Timestamp: 26:54

 error goes to 0 even if you keep adding more weak learners the trainer the test error still goes

### Timestamp: 27:01

 to it would not go to 0 of course right so you cannot because the training only provides so much

### Timestamp: 27:06

 information about the underlying distribution it will not go to 0 but it will it will it typically

### Timestamp: 27:13

 still goes to right so this is a very very non intuitive thing that typically happens because

### Timestamp: 27:21

 you would imagine that you are trying to overfit after training error 0 but then in practice that

### Timestamp: 27:27

 does not typically happen I keep saying typically because you can always create data sets where

### Timestamp: 27:33

 you know this phenomenon is not observed that it will start to the test error will start to increase

### Timestamp: 27:38

 that your algorithm will start to overset or overfit but in practice what people observe is that

### Timestamp: 27:46

 typically overfitting does not happen even after training error 0 so if you are running a boosting

### Timestamp: 27:50

 algorithm it might make sense not to stop your you know number of rounds the moment your training

### Timestamp: 27:56

 error becomes 0 but then still continue a little bit more so that to see if you are for instance

### Timestamp: 28:02

 you can look at your validation error and see if the validation error kind of goes down or it kind

### Timestamp: 28:07

 of starts reversing trend and you can take a call on the number of you know

### Timestamp: 28:12

 rounds that you need to run this algorithm based on your validation error so that is one point

### Timestamp: 28:17

 that I wanted to mention and and and of course people have given some kind of reasoning

### Timestamp: 28:23

 in some certain conditions you can actually argue and again this is beyond the scope of this

### Timestamp: 28:29

 discussion that after your training error become 0 the new classifier that kind of gets created

### Timestamp: 28:35

 right so with new weaklanders that get added ends up increasing the margin of the resulting

### Timestamp: 28:43

 and more the margin we know better is our ability to do well on the test data and so boosting

### Timestamp: 28:49

 kind of you know does better and better even after training error become 0 but to formally show

### Timestamp: 28:55

 this is beyond the scope of this discussion so but it is good to know that such a property

### Timestamp: 29:00

 exists for boosting typically in practice and it is good to look out for this when you

### Timestamp: 29:04

 if and when you are really implementing this in practice that is one point.

### Timestamp: 29:08

 So, in so to summarize you know we have a wonderful of the shelf classifier which was

### Timestamp: 29:16

 extremely well and even if you have a poor classifier it kind of boosts its accuracy really well

### Timestamp: 29:23

 the downside though is you cannot run it in parallel like how we did it in bagging right so

### Timestamp: 29:30

 this this is cannot run in parallel and if you think about it you should know why this is true

### Timestamp: 29:38

 because because of the nature of the algorithm itself right so you are running it in iterations

### Timestamp: 29:43

 and to create a weak learner you need to know where are the mistakes done by the previous weak

### Timestamp: 29:49

 learner. So, which means that to create this weak learner you have to wait for the previous

### Timestamp: 29:53

 weak learner so it has to run in a serial fashion whereas bagging creates bags uniform sampling

### Timestamp: 29:59

 with replacement uniformly and each bag is independent of other and I can kind of keep doing

### Timestamp: 30:05

 this in parallel. So, with respect to amount of time it takes to train the algorithm it is slightly

### Timestamp: 30:11

 more than what bagging would do but then typically boosting performs better in practice than by

### Timestamp: 30:18

 again typical statements. So, you can also compare it I mean some people have also done a

### Timestamp: 30:28

 comparative study of boosting versus support vector machines and so on and usually if you start

### Timestamp: 30:34

 with a very good learner right so very not a weak learner but a good learner then the improvement

### Timestamp: 30:40

 that you get you typically do not get any improvement in accuracy by just boosting it right so

### Timestamp: 30:46

 the improvement is felt more only when you have a weak learner a poor learner right so so typically

### Timestamp: 30:52

 you do not use you though theory would say that you can use an SPM as a weak learner potentially

### Timestamp: 30:59

 but in practice you would not do that you would use a quick and dirty algorithm like a decision

### Timestamp: 31:04

 stump and then you will try to boost that right. So, that is so but then if you compare

### Timestamp: 31:11

 boosting decision stump versus SPM of in practice they typically perform comparable right so we cannot

### Timestamp: 31:19

 really say that one is always better than that there are some datasets where one could be better

### Timestamp: 31:23

 than other and the other way around as well. So, this is the general discussion that I wanted to

### Timestamp: 31:29

 do about you know ensemble classification which is a very powerful technique I mean you do not

### Timestamp: 31:36

 really need to tune so many things here right so because both in bagging and boosting there is no

### Timestamp: 31:42

 tuning involved so we can quickly run these algorithms typically in practice of course,

### Timestamp: 31:49

 boosting is going to take more time because of the serial nature of it but then typically you

### Timestamp: 31:53

 do not need to tune any parameters per se and that is the power of this right. So, that is why these

### Timestamp: 31:58

 are called off the shelf classifiers and they were extremely well in practice and these are the

### Timestamp: 32:03

 these are what we will discuss in the scores about meta classifiers or ensemble classifiers.

### Timestamp: 32:09

 Next time we will look at you know we will try to unify all these algorithms that we have seen so

### Timestamp: 32:14

 far under a you know common theme called loss plus regularization and that will give us some

### Timestamp: 32:20

 perspective as to why there are so many algorithms for you know the problem of binary classification

### Timestamp: 32:25

 whereas, we just had one single algorithm for you know linear regression or regression problems

### Timestamp: 32:30

 whereas, we have host of algorithm for classification. So, so that we will see next time until then take care