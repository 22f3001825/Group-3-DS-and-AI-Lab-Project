# Week-11 - Lecture 5

### Timestamp: 00:00

 And the first way we will look at is what is called as the method of bagging, which is

### Timestamp: 00:24

 one technique to deal with this bias wave is straight off in a nice way.

### Timestamp: 00:30

 And the second method that we will do later is what is called as boosting.

### Timestamp: 00:33

 So what is bagging?

### Timestamp: 00:35

 So bagging stands for bootstrap aggregation and we will talk about what these two terms

### Timestamp: 00:41

 are in a bit in a bootstrap aggregation.

### Timestamp: 00:49

 So this is based on the idea that let us go back to our standard maximum likelihood estimation

### Timestamp: 00:57

 right.

### Timestamp: 00:58

 So just to draw an analogy.

### Timestamp: 00:59

 So if you had x1, x2 dot dot dot xn as n different samples all drawn from some Gaussian with

### Timestamp: 01:09

 some unknown mean and let us say variance 1 or variance can be anything let us say it is

### Timestamp: 01:14

 known variance.

### Timestamp: 01:16

 Now so I have to come up with an estimator for the unknown mean.

### Timestamp: 01:22

 So let us say mu hat 1 was just x1 or mu hat 2, the second estimator is x2 and mu hat

### Timestamp: 01:31

 n is xn.

### Timestamp: 01:34

 So what I am doing is I have a bunch of data points all real numbers all are drawn according

### Timestamp: 01:38

 to a Gaussian distribution with some unknown mean and variance.

### Timestamp: 01:43

 In a simple example maybe the unknown mean is you know 5.5 and if I draw points from

### Timestamp: 01:50

 this I might get you know 5, 7.3, 6.7 I do not know 8.2 and so on and so forth right.

### Timestamp: 02:00

 So I get a bunch of data points.

### Timestamp: 02:02

 Now I want to estimate this 5.5.

### Timestamp: 02:04

 I only have this data with me and I want to know what is the mean of the Gaussian that

### Timestamp: 02:08

 generated this data.

### Timestamp: 02:10

 Now one can come up with different estimators right.

### Timestamp: 02:13

 So now it is an estimation problem we are free to choose whatever estimator that we want.

### Timestamp: 02:17

 Let us say I estimate my mu hat 1 as just the first value 5 or I will estimate mu hat

### Timestamp: 02:23

 2 as just the second value which is 7.3 and so on.

### Timestamp: 02:27

 Mu hat n is let us say the last values 9, mu hat n is 9 right.

### Timestamp: 02:32

 So that is what I am saying is mu hat 1 is x1, mu hat 2 is x2 and mu hat n is xn.

### Timestamp: 02:37

 Now we all know that these are not the best way to estimate the mean of a Gaussian.

### Timestamp: 02:42

 What might be a best way to estimate mean of a Gaussian?

### Timestamp: 02:44

 Good time to pause and think it is just a recollection thing that we have seen this already.

### Timestamp: 02:49

 A good way would be to do something like a maximum likelihood estimator which would give

### Timestamp: 02:53

 me 1 by n sum over x i.

### Timestamp: 02:55

 It would just be the sample average right.

### Timestamp: 02:58

 Now one can argue that you know the why do we do the sampling?

### Timestamp: 03:08

 Why do we do this averaging right.

### Timestamp: 03:09

 So what is the benefit that we are getting from this averaging?

### Timestamp: 03:12

 So now if you were to measure how good our estimator is in predicting the truth then

### Timestamp: 03:19

 we can you know there are two ways to measure this right.

### Timestamp: 03:22

 So one way to say that you know you have an estimator and then you look at the expected

### Timestamp: 03:27

 value of this estimator.

### Timestamp: 03:28

 Let us call this estimator theta hat.

### Timestamp: 03:31

 You are trying to estimate parameter theta and then your estimator is theta hat and then

### Timestamp: 03:35

 you look at the expected value of this theta hat because your estimator is a random quantity

### Timestamp: 03:39

 because your data is random.

### Timestamp: 03:41

 Your estimator is a function of the random data.

### Timestamp: 03:43

 It is also a random quantity and you can ask what is the expected value of theta hat?

### Timestamp: 03:47

 Well if it is an unbiased estimator which means that your estimator on an average is

### Timestamp: 03:54

 going to behave like your truth right.

### Timestamp: 03:57

 So it means that it is actually you know measuring the truth in a good way.

### Timestamp: 04:01

 So your expected value of theta hat should be theta.

### Timestamp: 04:04

 In this particular case our theta is 5.5 which we do not know.

### Timestamp: 04:09

 We just have one sample and then we are which we can treat this as some random variables

### Timestamp: 04:14

 x1 to xn that we have and then our estimator is some function of this random variables.

### Timestamp: 04:20

 So what would this function be?

### Timestamp: 04:21

 This is a function which would given n random quantities would just pick the first random

### Timestamp: 04:26

 quantity.

### Timestamp: 04:27

 The mu hat 2 would be given n random variables.

### Timestamp: 04:30

 It will just pick the second random variable and output that as the answer and so on.

### Timestamp: 04:33

 Whereas mu hat ML would be given n random variables.

### Timestamp: 04:37

 It would average the random variables and now.

### Timestamp: 04:39

 Now if you look at this notion of you know this is unbiased estimators.

### Timestamp: 04:49

 Now if you think about which of these are all unbiased estimators.

### Timestamp: 04:53

 In other words if I ask the question what is the expected value of mu hat 1?

### Timestamp: 04:56

 What is the expected value of mu hat 2 1?

### Timestamp: 04:58

 So 1 till mu hat n and what is the expected value of mu hat ML.

### Timestamp: 05:02

 Then we will realize that all of these are unbiased estimators right.

### Timestamp: 05:05

 So the expected value of mu hat 1 what is this?

### Timestamp: 05:10

 Because mu hat 1 is just xn x1 but what is x1?

### Timestamp: 05:15

 x1 is a Gaussian with mean mu is a is a sample from a Gaussian with mean mu and some variance

### Timestamp: 05:20

 1.

### Timestamp: 05:21

 So what would be its expected value of a Gaussian with mean mu?

### Timestamp: 05:24

 Well it is mu right.

### Timestamp: 05:26

 So this is 5.5 in this case.

### Timestamp: 05:28

 So the same thing holds for all the n data points.

### Timestamp: 05:32

 So the expectation all of these are the same.

### Timestamp: 05:35

 It is correctly identifying the truth which means these are all unbiased estimators.

### Timestamp: 05:40

 On the other hand we still think that it is a good.

### Timestamp: 05:43

 So so is expected value of mu hat ML is also we can show it is mu right.

### Timestamp: 05:49

 So because expectation is a linear operator it will just be the average of the expected

### Timestamp: 05:52

 value of x size and each expected value of any x size mu.

### Timestamp: 05:59

 And so it is an average of mu which is mu.

### Timestamp: 06:01

 Now then we can just say that only looking at biasness is not a good idea to say whether

### Timestamp: 06:08

 estimator is good or not because in that case all these estimators are equally good.

### Timestamp: 06:13

 But we know that you know x1 is going to you know fluctuate a lot because if I draw

### Timestamp: 06:19

 another set of samples x1 to x1 dash to xn dash.

### Timestamp: 06:22

 Now my estimator is again mu hat 1 is just going to look at the first value and then predict

### Timestamp: 06:28

 that as the true mean.

### Timestamp: 06:30

 But then that is going to be a lot of fluctuation.

### Timestamp: 06:32

 But then when you do this averaging the fluctuation reduces significantly.

### Timestamp: 06:36

 The way we formalize fluctuation is by using the notion of variance right.

### Timestamp: 06:40

 So the reason why you do averaging here is to reduce variance.

### Timestamp: 06:44

 So the main idea here is averaging reduces variance.

### Timestamp: 06:58

 When these you know what are you averaging over right.

### Timestamp: 07:02

 So x1 to xn these are all IAD samples independently non samples.

### Timestamp: 07:06

 They are not correlated at all.

### Timestamp: 07:08

 When you have decorrelated set of random variables then when you do averaging it typically reduces

### Timestamp: 07:13

 variance.

### Timestamp: 07:14

 So what we are going to do is we are going to take inspiration from this idea and then

### Timestamp: 07:18

 see how it can be applied to classification problems.

### Timestamp: 07:21

 For that we are going to do the following right.

### Timestamp: 07:23

 So we are going to do bagging which is going to work as follows.

### Timestamp: 07:28

 Let us say we had access to datasets D1, D2 till some Dm where each Dm has you know

### Timestamp: 07:40

 HDI.

### Timestamp: 07:41

 Let me say HDI has N data points.

### Timestamp: 07:53

 Let us say somebody gave us you know different datasets where each dataset contains N points.

### Timestamp: 08:01

 What are these points?

### Timestamp: 08:02

 Well these are just feature common label pairs.

### Timestamp: 08:03

 It is a classification problem.

### Timestamp: 08:05

 For example you know your D1 could have you know x1, x2 dot dot dot xn.

### Timestamp: 08:11

 Let me put a one about indicate this D1 where each x1i is independently drawn according

### Timestamp: 08:21

 to some underlying distribution p and of course it is not just xn.

### Timestamp: 08:26

 So you also have y associated y with this which is where x1i is in RD let us say and y1i

### Timestamp: 08:36

 is in plus or minus 1.

### Timestamp: 08:38

 Basically you have a classification dataset.

### Timestamp: 08:40

 The standard features come on label pairs and you have N of them.

### Timestamp: 08:43

 Each dataset contains N of them.

### Timestamp: 08:45

 Each of this is independent of each other right.

### Timestamp: 08:47

 So that means that somebody drew N different data points from the underlying distribution

### Timestamp: 08:51

 and gave me D1 again drew N different data points gave D2 and so on till Dm.

### Timestamp: 08:56

 Now what you could do is you know you can run let us say your V-cloner which is let

### Timestamp: 09:04

 us say in this case you know let us say we are running a decision tree to complete depth

### Timestamp: 09:10

 which means we will over fit this let us say and then we get you know H1.

### Timestamp: 09:16

 Now you can again run another decision tree on D2 to get H2 dot dot dot Dm to get Hm.

### Timestamp: 09:25

 What is each H i?

### Timestamp: 09:27

 Well each H i is a mapping from RD2 plus or minus 1.

### Timestamp: 09:31

 It is a classifier right.

### Timestamp: 09:32

 So it is a decision tree.

### Timestamp: 09:34

 So which means that if I give a plugin and if I give a new test point x test H i of

### Timestamp: 09:39

 x test is going to tell me what is the prediction of the i th decision tree on the test data

### Timestamp: 09:43

 point.

### Timestamp: 09:44

 So now what is happening is that you can imagine as if each of these classifiers are independently

### Timestamp: 09:52

 trained on different datasets right.

### Timestamp: 09:56

 So now they might because they are trained till you know in this case we are making it

### Timestamp: 10:03

 to over fit they might have high variance they might suffer from high variance.

### Timestamp: 10:07

 If you change the dataset a little bit these predictions are going to go off a lot.

### Timestamp: 10:11

 Now one way to reduce this variance is by doing an averaging.

### Timestamp: 10:16

 That is what our statistical I mean methods that you have seen so far at least in the simpler

### Timestamp: 10:21

 sense simpler cases where we are drawing from random variables and so on suggestes.

### Timestamp: 10:27

 Why not use the same thing here right.

### Timestamp: 10:28

 So what you can then do now is that you can you know aggregate all these classifiers into

### Timestamp: 10:33

 a classifier H star where H star of x is just you know what you are going to do is you

### Timestamp: 10:41

 are going to look at H i of x each of these is a plus or minus 1 value.

### Timestamp: 10:48

 So this whole thing is going to be between minus 1 and plus 1 and then you can look at

### Timestamp: 10:52

 the sign of this right.

### Timestamp: 10:55

 So where sign in this case I am defining sign of x is plus 1 if sign of let us say z

### Timestamp: 11:01

 this plus 1 z is greater than or equal to 0 and minus 1 otherwise.

### Timestamp: 11:07

 So basically what you are taking doing is taking majority vote right.

### Timestamp: 11:10

 So when will the sign be plus 1 if majority of H 1 to H m say the actual label is plus

### Timestamp: 11:16

 1 then the average would be positive otherwise the average is going to be negative right.

### Timestamp: 11:21

 So basically what we are doing then is if we had access to yum independent training

### Timestamp: 11:29

 sets then what you could do is you can average the decision trees or the learners that you

### Timestamp: 11:36

 get from these each of these independent independent data sets to come up with an aggregate

### Timestamp: 11:42

 classifier.

### Timestamp: 11:44

 So now this aggregate classifier will have lesser variance than the original classifier.

### Timestamp: 11:50

 The original classifier had less bias because you know we started with classifiers which

### Timestamp: 11:56

 did not have too much bias because these were overfit classifiers.

### Timestamp: 11:59

 So now when you average them you ideally want a classifier with less bias and less

### Timestamp: 12:04

 variance because that is what your error that is when your error will be low.

### Timestamp: 12:07

 But you only have you know less bias high variance classifiers now the idea is to average

### Timestamp: 12:11

 them to get less bias low variance classifiers hopefully you would have a better classifier

### Timestamp: 12:16

 in that sense.

### Timestamp: 12:17

 The only problem with this approach is that you know nobody is going to give us yum different

### Timestamp: 12:22

 data sets right.

### Timestamp: 12:23

 So we are only given one single data set and not yum different data sets.

### Timestamp: 12:28

 So if we had access to yum different data sets then yes we can run separate classifiers

### Timestamp: 12:34

 on each of these and then we will be happy.

### Timestamp: 12:37

 But the problem is we do not right.

### Timestamp: 12:39

 So now we have to somehow create yum different data sets from a single data set that we have.

### Timestamp: 12:45

 So what we have in hand our input is just a single data set D right.

### Timestamp: 12:49

 So D which has x1 y1 dot dot dot xn yn where x i's are in R D yi's plus or minus 1.

### Timestamp: 13:01

 Now how can we create yum different data sets from this is the question.

### Timestamp: 13:06

 Now there are different ways to do this.

### Timestamp: 13:08

 The most straightforward immediate way that one can think of is well I can just take my

### Timestamp: 13:13

 n different data points cut it into yum pieces right.

### Timestamp: 13:16

 So each of these pieces independently independent of each other and things are fine.

### Timestamp: 13:21

 But the problem there is that you know you cannot create too many pieces because the more

### Timestamp: 13:25

 the pieces that you create the smaller these data sets are going to become.

### Timestamp: 13:29

 And so your trained classifier is going to work on a very very small set of data points

### Timestamp: 13:34

 and that is a bad idea because if you have too many pieces then you know you do not have

### Timestamp: 13:40

 enough information in each of these data sets that the you know the decision trees or the

### Timestamp: 13:44

 week learners that your training can take advantage of.

### Timestamp: 13:47

 So you have to come up with an alternate way where you cannot divide this into different

### Timestamp: 13:53

 pieces yet you want many many data sets that seems to be contradictory right.

### Timestamp: 13:59

 So how can we even do that?

### Timestamp: 14:01

 Well the only way you can do that is if you allow some data points to be repeated across

### Timestamp: 14:08

 these different data sets.

### Timestamp: 14:11

 And that way of creating data sets with repeated data points potentially repeated data points

### Timestamp: 14:18

 in each of these data sets is that procedure is called as I mean bootstrapping. So what

### Timestamp: 14:27

 is bootstrapping? Well bootstrapping is basically sampling with replacement.

### Timestamp: 14:39

 What does that mean? That means that maybe you have a data set you know x1, x2, x3, x4, x5.

### Timestamp: 14:51

 Now what I am going to do is I am going to create a bag it is called a bag and that is

### Timestamp: 14:58

 that comes from the term bagging. So which is just a data set D1 so this D now this bag is also

### Timestamp: 15:04

 going to contain five data points because the original data set contain five data points.

### Timestamp: 15:09

 And the way I am going to create this bag is I will first sample without replacement from x1 to

### Timestamp: 15:15

 x5 that is you know I put my hand inside the data set D close my eyes and then pick a data point

### Timestamp: 15:20

 right. So let us say that data point was x3. Now sorry sampling with three replacement I should

### Timestamp: 15:27

 not have said without replacement with three replacement. So next what I do is I put back this x3

### Timestamp: 15:32

 into my original data set and then again mix it uniformly and then put my hand and pick one

### Timestamp: 15:38

 data point. I might get x4 this time next time I might get x5 right. So if I do this again maybe

### Timestamp: 15:44

 I will get x3 again the next time I might get x5 again. Now this is a bag that I have created

### Timestamp: 15:51

 from my original data set where I have sampled you know with three placement each data point uniformly

### Timestamp: 15:58

 at random. Now I can create another bag like this which is a bag D2 right. So this might be a second

### Timestamp: 16:05

 bag bag 2 this is bag 1 this might have x1 maybe if I pull it again maybe I will get x1 again

### Timestamp: 16:12

 next time I might get x5 next time x4 maybe I will get x1 again right. So anything that happened

### Timestamp: 16:17

 because these are uniform draws. So what you do in bagging is you start with D and then create

### Timestamp: 16:23

 these you know uniform sampled with three placement bags D1, D2 till Dm and now once you have these

### Timestamp: 16:34

 bags each with n data points original had n points this also has n points and so on this has n points.

### Timestamp: 16:45

 Now you do whatever you want to do right. So you run this over a v-cloner it could be a decision

### Timestamp: 16:52

 tree it could be something else also this is a v-cloner and then you again aggregate these things

### Timestamp: 16:59

 well you get h1 here h2 here hm here and now your htr of x is just 1 over m well sin of

### Timestamp: 17:10

 1 over m sum over i h a of x. So this procedure which does two steps one is the first step which is

### Timestamp: 17:24

 this part which is the bootstrap part where you are bootstraping from your single dataset to create

### Timestamp: 17:32

 m different datasets and then this is the aggregation part where you are aggregating m different

### Timestamp: 17:40

 classifiers into a single classifier these two steps are involved in this way of doing you know

### Timestamp: 17:45

 ensembleing and so this is called as a bootstrap aggregate classifier or in other words called

### Timestamp: 17:51

 bagging class for bagging stands for bootstrap aggregation. Now one of the common ways so the okay of

### Timestamp: 18:03

 course the d1 to dm so one can now ask the question well there are points that are going to get

### Timestamp: 18:09

 repeated in each of d1 to dm so what can we say about the amount of repetition that happens in

### Timestamp: 18:14

 each of these bags right so if you think about that how am I creating d1 well I am creating the

### Timestamp: 18:21

 first point in d1 by you know picking one point from d uniformly at random now what is the chance

### Timestamp: 18:28

 that that point does not appear in dm well that chance is you know 1 minus 1 over m because with

### Timestamp: 18:34

 1 over n chance that point would have appeared in d1 why because it is uniformly at random if there

### Timestamp: 18:39

 are five points that is one by first chance that each point appears in my bag when I pull one

### Timestamp: 18:46

 data point the first time but now this if I am asking for the probability that a point does not

### Timestamp: 18:52

 appear in the bag well that is going to be 1 minus 1 over n now this happens so if a point does

### Timestamp: 18:58

 not appear in the bag at all this does not miss the first time I am picking it it misses it every

### Timestamp: 19:03

 time and then I am picking n such points and every time I miss a particular point well what is the

### Timestamp: 19:08

 probability that happens well that probability is 1 minus 1 by n into 1 minus 1 by n so many times

### Timestamp: 19:15

 n different times because these are independent rails n different times I am missing it every

### Timestamp: 19:19

 single time so this is the chance that a point does not appear in this bag so what is the

### Timestamp: 19:25

 chance that it actually appears in the bag well it actually appears in the bag would be 1 minus

### Timestamp: 19:30

 1 the chance that it does not appear so this is the probability that some x belongs to a bag d

### Timestamp: 19:39

 d i so x j belongs to d j is this so now this probability is something like 67 percent

### Timestamp: 19:47

 because for large n of n for large n this guy looks like something like 1 minus 1 by e where e is

### Timestamp: 19:59

 2.7 something right so on the 1 minus 1 by e now looks like 67 percent so what does that mean

### Timestamp: 20:05

 that means that you know 67 percent of the points kind of on an average appear in each dataset

### Timestamp: 20:12

 which means that there are going to be some 30 to 33 percent of repetition on an average in

### Timestamp: 20:16

 each of these data points now if I learn a weak learner which is kind of overfitting

### Timestamp: 20:21

 what does that overfitting means well the overfitting would fit the noise that is specific to this

### Timestamp: 20:30

 37 percent this you know this dataset which has a lot of repetition but then the points that

### Timestamp: 20:37

 get repeated in each of these datasets is completely different right so which means that you know

### Timestamp: 20:41

 you are fitting different noises in each of these weak learners which are you know overfit models

### Timestamp: 20:46

 let us say overfit decision trees and then when you actually average them what happens is that the

### Timestamp: 20:52

 noise hopefully gets averaged out and so you know you do not lose out so much on the bias but then

### Timestamp: 20:58

 your variance actually reduces right so you are still having a complicated classifier mind you

### Timestamp: 21:03

 right so because it is a it is a combination of multiple classifiers but then the hope is that

### Timestamp: 21:09

 the noise gets averaged out and we can see this in practice actually so if you plot the bias

### Timestamp: 21:15

 and variance of the classifier as you add more and more you know trees or weak learners what you

### Timestamp: 21:22

 will see is that the variance actually comes down but the bias stays afloat so which means that

### Timestamp: 21:28

 the main reason why somebody would want to do a bagging is to reduce variance right so the main

### Timestamp: 21:35

 message here is that you know bagging reduces variance

### Timestamp: 21:46

 of course if these weak learners are completely on I mean these weak learners are totally not

### Timestamp: 21:53

 correlated with each other then the reduction in variance will be large so now what people do is

### Timestamp: 21:59

 a lot of you know specific ways of making sure that you know these learners that you are learning

### Timestamp: 22:05

 are as less correlated from each other as possible so one way to do that is what is called as a very

### Timestamp: 22:13

 very popular technique is called as a random forest technique random forest which is one of the

### Timestamp: 22:22

 which is one of the very commonly used you know classification algorithm on sampling technique in

### Timestamp: 22:28

 practice what it does is well the first thing is it bags decision trees decision trees you know

### Timestamp: 22:40

 typically overfit trees what you do is you create these data sets and then D1 to Dm and then fit

### Timestamp: 22:52

 overfit tree for each of these that is you do not you know cross validate or anything you kind of

### Timestamp: 22:58

 go grow the tree so that it becomes as pure as possible that is you know you get to 0 training

### Timestamp: 23:06

 then what you do is you know in addition to this when you are actually fitting this tree you do

### Timestamp: 23:12

 some interesting things right so you do something called as feature bagging in addition to

### Timestamp: 23:22

 overfitting this tree you do something called as feature bagging what is feature bagging well

### Timestamp: 23:27

 the trees I mean you want overfit trees which are high bias but then sorry which are low bias but

### Timestamp: 23:34

 then you want the trees across these bags to be as decorrelated as possible one way to achieve

### Timestamp: 23:42

 that is using feature bagging in feature bagging what you do is when you are running this decision

### Timestamp: 23:49

 tree right so when you are building this decision tree remember how we built the decision tree

### Timestamp: 23:53

 well at every node to decide on which is the next node what you do is you look at all the features

### Timestamp: 24:00

 and all the splits and then see which feature comma threshold feature less than threshold question

### Timestamp: 24:08

 gives me the highest reduction in impurity and then using information gain in our genie index or

### Timestamp: 24:15

 different measures of impurity whichever your favorite measure of impurity is you look at which

### Timestamp: 24:20

 feature comma threshold value gives you the most decrease in impurity and then you pick that

### Timestamp: 24:26

 now this means that if I am building these multiple trees all the trees are going to use all

### Timestamp: 24:31

 features now feature bagging would tell us that you know pick a subset of features to consider

### Timestamp: 24:39

 splitting on for every node of your tree what does that mean that means that you know you have

### Timestamp: 24:47

 feature one feature two till let us say feature D these are your D features let us say height weight

### Timestamp: 24:54

 whatever right so you have let us say 1000 features now what you do is you want to ask the question

### Timestamp: 24:59

 well F i less than theta which is the best F i less than theta for my data set I have already

### Timestamp: 25:04

 created the data set now I need to build the tree now what I am doing is I am kind of doing

### Timestamp: 25:08

 feature bagging which is to say that to decide F i less than theta what I would do is I will not use

### Timestamp: 25:14

 all the features I will only sub sample a set of features so maybe if I sub sample set of features

### Timestamp: 25:21

 maybe I will get F 1 F 5 F 23 F 40 maybe I get 4 features and now only among these 4 features I

### Timestamp: 25:30

 asked the question which is the best feature to split off now maybe that will give me something

### Timestamp: 25:35

 maybe F 5 was the best feature in this case now here to decide which is the best feature now

### Timestamp: 25:41

 again I sub sample a bunch of features right so in this case maybe I will get F 1 F 10 F 40 F 20

### Timestamp: 25:49

 maybe something like that right so and then I asked among these features I pretend that this

### Timestamp: 25:53

 is my data set my data set has only this set of features and then I ask the question well how can

### Timestamp: 25:58

 I find the best feature come on split here right so if I do this at every split decide which is

### Timestamp: 26:05

 feature that I need to pick in a random manner then different set of features are being used by

### Timestamp: 26:11

 different trees and then hopefully they will get decorrelated a little bit more and so when

### Timestamp: 26:16

 you are averaging them the variance production will be larger and that is what is observed in practice

### Timestamp: 26:21

 as well so random forest is basically feature bagged decision trees right so you do bagging but then

### Timestamp: 26:28

 you also do this feature bagging if you do that then they are called as feature bagging and this is

### Timestamp: 26:33

 a very very popular technique that is you know commonly used in practice today.

### Timestamp: 26:41

 So again so there are several variants of random forests so you can do this for classification you

### Timestamp: 26:47

 can do this for regression where you replace your decision tree with a decision regression tree

### Timestamp: 26:53

 and so on and so forth we won't discuss everything in detail but it is good to know that you know

### Timestamp: 26:57

 random forest are very powerful techniques for variance reduction where your bias does not

### Timestamp: 27:04

 typically increase but then your variance goes down and so the error of the resulting class if I

### Timestamp: 27:08

 typically goes down good. So again so there are several more variants as I mentioned one variant

### Timestamp: 27:17

 would be to even look at you know the set of splits the threshold values that you want to use in

### Timestamp: 27:23

 every split right so you can kind of also randomly sample that and so on right so you can do a lot

### Timestamp: 27:30

 of you know ways to decorate these trees but then the usual standard practice is to just you know

### Timestamp: 27:37

 use decision trees as your weak learners you know overfit them and then overfit them but then at the

### Timestamp: 27:43

 same time do feature bagging as well. So one typical point that in practice what happens is that

### Timestamp: 27:50

 the number of features that you would use when you do this bagging is approximately square root of

### Timestamp: 27:56

 the right so if you start with D features at every round what you do is you only pick square root of D

### Timestamp: 28:03

 features to you know build your tree on to decide which is the best feature commatorship value

### Timestamp: 28:10

 and there are some theoretical reasoning as to why square root of D is a good idea in classification

### Timestamp: 28:17

 and regression problems I think the suggested value is something like B over 3 or B over 5

### Timestamp: 28:22

 something like that but order of B right so again so these are rules of thumb in typically in

### Timestamp: 28:29

 practice you can try out different values also and then pick one that works best right so depending

### Timestamp: 28:34

 on how much computational time that is available. So one of the biggest advantage of this approach

### Timestamp: 28:41

 of bagging is that you know this these weak learners right so can be run in parallel

### Timestamp: 28:50

 because we do not really need these weak learners until we come to the aggregate stage right so

### Timestamp: 28:58

 basically now because if you have a you know powerful CPU right so with a lot of course and so on

### Timestamp: 29:04

 right so you can kind of run these weak learners in parallel and then get these decision trees in

### Timestamp: 29:08

 parallel and then the aggregation of course during aggregation you need all the trees but then to

### Timestamp: 29:13

 before that step you do not need all these you do not need to wait for one weak learner to complete

### Timestamp: 29:19

 to start with the next decision right so and that is why this is also prepared a lot practice

### Timestamp: 29:24

 because you know you can run these algorithms very fast in parallel right so that is one point I

### Timestamp: 29:31

 also want to mention. So so there are two points which we want to you know consider here before

### Timestamp: 29:43

 we move on to our next algorithm one point is right so there are two steps basically there are

### Timestamp: 29:49

 two steps in bagging for first step is bootstrapping which is you know sampling with replacement

### Timestamp: 30:01

 well uniform sampling with replacement and the second is aggregation which is average

### Timestamp: 30:12

 now both of these are choices that we make to to kind of ensemble the class phase we decide to

### Timestamp: 30:23

 create these bags by uniformly sampling with replacement and we decided to kind of average with

### Timestamp: 30:29

 the understanding that you know averaging reduces variance one might ask the question are these

### Timestamp: 30:37

 the best things to do or are there other ways to you know do something else right so instead of

### Timestamp: 30:43

 doing uniform sampling can we do some other more principled way of sampling with replacement

### Timestamp: 30:49

 and instead of averaging can we do something more principled to kind of aggregate these classifiers.

### Timestamp: 30:56

 So the answer to both of these questions turns out to be yes and the algorithm which does these

### Timestamp: 31:03

 exactly these two steps but then it does these two steps in a slightly different way by thinking

### Timestamp: 31:09

 about what is the in some sense the best possible way to do each of these steps will lead us to a

### Timestamp: 31:13

 very very powerful algorithm called the boosting algorithm right so this will lead us to the boosting

### Timestamp: 31:22

 algorithm which is what we will start looking at next.

### Timestamp: 31:32

 so

### Timestamp: 31:38

 so