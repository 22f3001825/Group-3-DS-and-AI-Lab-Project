# Week-11 - Lecture 4

### Timestamp: 00:00

 Hello and welcome back to this lecture. So, for we have seen several algorithms for

### Timestamp: 00:20

 supervised learning, what I am going to do now is just summarize at a high level what

### Timestamp: 00:24

 are these algorithms. And now we will start looking at a slightly different way of thinking

### Timestamp: 00:28

 about you know learning algorithms which is called as ensemble learning which is what

### Timestamp: 00:33

 we will do today. So, so far this is this is the picture that we have seen so far. We have

### Timestamp: 00:39

 looked at two different types of you know approaches to algorithms one is the generative model

### Timestamp: 00:47

 and the other is the discriminative model. And we have seen several examples of algorithms

### Timestamp: 00:56

 in both these cases. In the generative case for example, we looked at the naive base algorithm.

### Timestamp: 01:03

 We looked at the Gaussian discriminant analysis or Gaussian naive base and here what the idea was

### Timestamp: 01:11

 you assume a probability of x, y somehow and then you try to estimate the parameters.

### Timestamp: 01:17

 Whereas, in the discriminative world we looked at you know multitudinal algorithms starting from

### Timestamp: 01:22

 you know simple K nearest neighbors decision trees logistic regression per subtrom

### Timestamp: 01:41

 and support vector machines.

### Timestamp: 01:43

 So, these are all different classification algorithms and what we will see a bit later is how to

### Timestamp: 01:56

 you know kind of view several of these algorithms under the same framework which is called as

### Timestamp: 02:00

 the loss plus regularization framework. We look at it a little later but for now I just wanted to

### Timestamp: 02:06

 you know recall that we have looked at several algorithms and the goal of today is going to be

### Timestamp: 02:13

 look at what are called as you know meta classifiers or sometimes also called as ensemble classification.

### Timestamp: 02:25

 So, what are meta classifiers or ensemble classifiers? So, these are also I mean some kind of a

### Timestamp: 02:43

 learning algorithm but they are going to work on the idea that if you start with what are called as

### Timestamp: 02:51

 weak learners and we will talk about what weak learners are you somehow want to convert this into

### Timestamp: 03:00

 what are called as strong learners. So, weak learners are just classification algorithms

### Timestamp: 03:12

 which are weak in a certain sense that I mean without defining it formally here for this course

### Timestamp: 03:19

 let me say that weak learners are those which you know will give you you know better than random

### Timestamp: 03:25

 performance on any test data right. So, these are kind of better than random.

### Timestamp: 03:34

 What do I mean by better than random? Well, you can you have a data set which you are assuming is

### Timestamp: 03:39

 coming from some underlying distribution you are training your classifier on this and then if

### Timestamp: 03:44

 you are trying to do a testing on the test data well if it is a binary classification I can just

### Timestamp: 03:49

 simply toss a coin and then decide on the label and that is going to be a random classifier right.

### Timestamp: 03:53

 So, a classifier which is I mean simply going to get 50 percent error rate let us say.

### Timestamp: 03:57

 Now, this classifiers which are which we are calling as weak learners might get you know 60 percent

### Timestamp: 04:03

 accuracy or 55 percent accuracy things like that right. So, slightly better than random. So,

### Timestamp: 04:09

 we have a weak learner like this and now the goal is to somehow convert this weak learner into a

### Timestamp: 04:15

 strong learner. The question is why should we start with weak learners why cannot we I mean

### Timestamp: 04:22

 directly try to get a good learning algorithm. So, there are several reasons why one would want to

### Timestamp: 04:27

 do this we will look at two different types of reasoning for this. The first is to understand

### Timestamp: 04:34

 weak learners which do something called as you know overfitting and the second is we look at

### Timestamp: 04:40

 weak learners which do something called as underfitting. So, for this we need to understand that the

### Timestamp: 04:45

 terms overfitting and underfitting at a broad level. So, overfitting and underfitting are two

### Timestamp: 04:56

 terms which we will try to understand first and then we will look at what weak learning means in

### Timestamp: 05:02

 this context. So, overfitting happens when for example, you have a decision tree that you train

### Timestamp: 05:11

 you know to to arbitrary height such that you know if your training error becomes 0 that is

### Timestamp: 05:17

 what happens is you can always keep adding depth to your decision tree that is you can keep

### Timestamp: 05:24

 splitting your decision tree if you recall decision tree it would ask a question and then based

### Timestamp: 05:28

 on that it would split the data under two parts such that the impurity reduces. Now, you can keep

### Timestamp: 05:34

 splitting your decision tree to arbitrary depth such that at some point you know it becomes

### Timestamp: 05:39

 completely pure. We saw that that is a bad idea to do because doing that would lead to

### Timestamp: 05:46

 fitting noise as well right. So, your data set is not exactly

### Timestamp: 05:51

 subscribing to the structure that you are believing it to have because there is some noise associated

### Timestamp: 05:56

 with it. So, it is always structure plus noise that determines the labels. So, now if you somehow

### Timestamp: 06:01

 if your learner is trying to you know so fit noise thinking that it is structure part of the

### Timestamp: 06:14

 structure then this is what we will end up with we will end up with the overfit model.

### Timestamp: 06:20

 On the other hand underfitting happens when the opposite happens right. So, your your actual

### Timestamp: 06:26

 prediction actual relationship between input and output depends on some structure let us say a

### Timestamp: 06:32

 linear structure or a decision tree based structure plus some noise added to it. Now,

### Timestamp: 06:37

 what might happen when you are doing underfitting is that you are thinking you know you are

### Timestamp: 06:41

 missing out on the structure thinking that it is noise it means that you are being too conservative

### Timestamp: 06:47

 right. So, missing out on structure thinking it is noise.

### Timestamp: 07:02

 So, to give an example let me motivate this with an example on a regression problem where it

### Timestamp: 07:08

 might be easier to look at the case that we are looking at similar ideas of way to classification

### Timestamp: 07:14

 as well. Let us say we are we have an input variable which is x and then we want to predict an

### Timestamp: 07:18

 output which is y and our actual structure that relates x to y let us say is something like a

### Timestamp: 07:27

 let us say sinusoidal curves of sorts.

### Timestamp: 07:33

 Let us say this is the true structure which is a sine curve but then the data points that we get

### Timestamp: 07:38

 for x comma y is let us say we we kind of get these x values and then the corresponding y which

### Timestamp: 07:45

 is our data points are looking not exactly on the structure but then there is some noise

### Timestamp: 07:53

 there is some noise associated with the structure something like this right. So, this is the data

### Timestamp: 08:02

 set that we actually look at. Now, a model which is trying to understand the structure right. So,

### Timestamp: 08:10

 now we do not know what the real structure is that relates the input to the output. So, as

### Timestamp: 08:15

 designers of algorithms we are trying to pick some structure which we believe relates the input

### Timestamp: 08:19

 to the output. Now, under fitting happens when we look at a very very conservative structure

### Timestamp: 08:25

 very simplistic structure whereas, over fitting happens when we look at a very very complicated

### Timestamp: 08:30

 structure. So, what would be a very simple structure for this data well if I just draw plot the

### Timestamp: 08:35

 data points now without plotting the structure relevant structure here. So, your data point looks

### Timestamp: 08:41

 like this right the data point looks like this and a simplistic structure for this could be

### Timestamp: 08:50

 you know a linear structure which means that I might learn a linear classifier linear regressor

### Timestamp: 08:55

 for this for this data which might say that well maybe this is the best possible line right.

### Timestamp: 09:02

 Now, here what has happened is the actual structure is more complicated than a linear structure

### Timestamp: 09:10

 whereas, we are imagining that linear the input to the output mapping is indeed linear and we are

### Timestamp: 09:15

 trying to find the best possible regressor in this case. So, we are missing out so, we are

### Timestamp: 09:20

 imagining that what is actually structure is we are thinking of that as noise because in this

### Timestamp: 09:24

 case the moment I say it is a linear it is a linear structure which means that I am thinking of

### Timestamp: 09:30

 all these bits as noise bits right. So, this pieces are all noise for me, but then they are not really

### Timestamp: 09:36

 noise there is some structure in this noise as well which we are kind of missing out in this case.

### Timestamp: 09:41

 So, when we do this this is a case where under fitting happens. Similarly, for a classification

### Timestamp: 09:48

 problem if you are trying to imagine a classification problem with a linear model whereas, the actual

### Timestamp: 09:54

 you know why the label why decide is decided based on let us say quadratic or a cubic model

### Timestamp: 09:59

 then under fitting happens. Whereas, on the other hand I can imagine for the same data set

### Timestamp: 10:05

 a very very complicated looking classifier sorry regressor in this case I keep saying it as classifier,

### Timestamp: 10:12

 but what I mean is in this example it is a regression problem right. So, now what I can do is that I

### Timestamp: 10:21

 can fit a very very complicated polynomial for this let us say I am trying to fit a yeah. So,

### Timestamp: 10:29

 in this case 6, 7, 8 to degree polynomial or something like that which might fit my data like this.

### Timestamp: 10:38

 So, this is a overfit model because now it is making my training error 0 whereas, in the

### Timestamp: 10:53

 underfit model the training error was not 0 and the overfit model the training error is 0.

### Timestamp: 10:58

 The reason training error 0 is because your classifier your regressor in this case is too

### Timestamp: 11:03

 complicated that it can make the training error 0, but both of these are not going to do so well

### Timestamp: 11:09

 on our test data right. So, what is going to be our test data maybe we have a test point which is

### Timestamp: 11:16

 somewhere here maybe I will put a point here for which the test value is here right. So,

### Timestamp: 11:22

 now if you look at the same point here my weak learner which is an underfit model is going to say

### Timestamp: 11:30

 something wrong similarly my overfit model is also going to predict something wrong whereas,

### Timestamp: 11:36

 the actual answer is somewhere here right the actual answer is here. So, this is the error of the

### Timestamp: 11:42

 overfit model this is the error of the underfit model both are performing incorrectly in this case right.

### Timestamp: 11:47

 So, and both are not good ideas right. So, in one case you are missing out structure for noise

### Timestamp: 11:54

 you are thinking of structure as noise in the other case you are thinking of noise structure

### Timestamp: 11:58

 both are bad ideas. Now, what so if the way we handled this for instance in decision trees

### Timestamp: 12:07

 or even in K nearest neighbors where you had K as the parameter as you increased K if K was

### Timestamp: 12:15

 K was small then you had a very complicated classifier if K was large as K becomes larger and

### Timestamp: 12:21

 larger the classifier decision boundary smoothens out it becomes simpler and simpler and when K is in

### Timestamp: 12:26

 fact n then it just becomes you know one value for the entire space. Similarly, for decision trees as

### Timestamp: 12:32

 you increase the depth right. So, I mean if depth is one then it means that it is a very simply

### Timestamp: 12:38

 simple classifier where you are only looking at one feature and value pair to make a decision

### Timestamp: 12:44

 which is not going to give you so I mean great test accuracy. Similarly, if you train a decision

### Timestamp: 12:50

 tree to to the end that it is as pure as possible then you would actually be fitting noise as well.

### Timestamp: 12:56

 So, in both these cases you are going to get a weak learner which is not going to perform so well

### Timestamp: 13:02

 in the test data. Now, how can we how do we you know deal with this situation right. So, now

### Timestamp: 13:15

 one way or we are going to look at two different ways to deal with weak learners.

### Timestamp: 13:19

 The first way we look at cases where you have potentially an overfit model and then try to somehow

### Timestamp: 13:26

 reduce I mean somehow kind of come up with a better learner that starts with the overfit model but

### Timestamp: 13:34

 then somehow avoids overfit. So, the problem with overfit model is that if I slightly change let's

### Timestamp: 13:44

 look at the overfit model first and then we will talk about the underfitting in a bit. So,

### Timestamp: 13:47

 if I slightly change the data the overfit model is going to change a lot. For example, in the same

### Timestamp: 13:54

 case right. So, let's focus on this picture where we have fit an 8 degree polynomial that is the

### Timestamp: 13:58

 bag of class bag of for aggressors from which I am picking one. Now, and it is this complicated

### Timestamp: 14:04

 the 8 degree polynomial that I am getting. Now, if I change my model sorry if I change my data set

### Timestamp: 14:11

 a little bit right. So, maybe my data set change is a little bit which means which is very

### Timestamp: 14:20

 possible if you for instance again draw a bunch of x's and y's from the same distribution right.

### Timestamp: 14:25

 So, because there is some inherent noise and that noise might change because that noise is a

### Timestamp: 14:30

 random quantity and so your data set might change a bit if you draw the same distribution again

### Timestamp: 14:35

 from the same distribution again. Now, what might happen is if I fit an again 8 degree polynomial

### Timestamp: 14:41

 here I might you know again will fit the training data exactly I mean I am just these are not exact

### Timestamp: 14:51

 polynomials, but then I am giving you an illustration here. Now, what would happen is for the same

### Timestamp: 14:57

 test point right. So, basically I drew another set of data points same set say 8 data points and then

### Timestamp: 15:03

 I am fitting an 8 degree polynomial I get training error 0, but then for the same data point for

### Timestamp: 15:08

 the same test point right. So, this is the x test right. So, this is y hat this is my predicted this

### Timestamp: 15:15

 is my actual y. Now, the actual y is somewhere here that I am plotting that in green. So, let me

### Timestamp: 15:22

 put that in green this is y. Now, my predicted y is somewhere here right. So, now if I again and

### Timestamp: 15:28

 again sample different data points different data sets and then try to fit the same 8th means

### Timestamp: 15:34

 from the same class of 8 degree polynomials. I am going to get different polynomials because

### Timestamp: 15:39

 each one will fit the noise differently and so if I just look at you know for different polynomials

### Timestamp: 15:46

 how I am how is my output differing right. So, how how does my output with respect to the truth

### Timestamp: 15:52

 differs my output might be completely off right. So, one point might be here the other next data

### Timestamp: 15:57

 set it might be here next data set it might be here here and here right. So, now which means that

### Timestamp: 16:02

 the the the model is too sensitive to the data which means the one way to capture this is used by

### Timestamp: 16:10

 saying that the model has you know high variance. So, which means that if the data change is a

### Timestamp: 16:20

 little bit your models prediction is going to change a lot. So, there is going to be a lot of

### Timestamp: 16:24

 variation in prediction right. So, these are high variance models whereas, in this case in the

### Timestamp: 16:30

 underfit case even if the data change is a little bit the best linear line right. So, it is not

### Timestamp: 16:36

 going to change too much right. So, maybe it will change from here to somewhere here

### Timestamp: 16:43

 we will use a different color maybe it will change a little bit here right. So, if I change the data

### Timestamp: 16:49

 again redraw the samples and now now you can think of it as you know the predictions was here.

### Timestamp: 16:55

 Now, it is here the next time it will be here here here and then it will only vary within a small

### Timestamp: 17:01

 region the variance is slow right. So, but then we are still going to you know make mistakes with

### Timestamp: 17:07

 respect to the test data because we have missed out on the structure. So, less complicated

### Timestamp: 17:12

 classifiers are not going to vary too much but then because it has missed out on the structure

### Timestamp: 17:18

 your test date your test performance is going to be bad. The largely I mean high complicated

### Timestamp: 17:24

 classifiers are going to vary too much and so you are going to miss out on performance in the test

### Timestamp: 17:29

 data right. So, these are the classifiers which suffer from what is called as high

### Timestamp: 17:38

 or other yeah high bias right. So, bias is kind of telling you how good is your assumed structure

### Timestamp: 17:52

 actually representing the truth. If the truth in this case is a sinusoidal wave but then my assumed

### Timestamp: 17:57

 structure is a line then there is a lot of bias between the truth and my assumed structure.

### Timestamp: 18:03

 So, these are classifiers which high bias. On the other hand how good can an eighth degree

### Timestamp: 18:08

 polynomial kind of simulate a sign curve well in that case we can say that your bias is low

### Timestamp: 18:17

 but then because you want to do well on the test data your variance is high.

### Timestamp: 18:22

 In one case you suffer from high bias in the other case you suffer from high variance right. So,

### Timestamp: 18:26

 your error will always again without defining it formally your error will always be

### Timestamp: 18:32

 a mix of bias and variance. Now, as you start with low small I mean very very less complicated

### Timestamp: 18:41

 classifiers you will suffer an error larger due to high bias. As you increase the complexity of

### Timestamp: 18:47

 your classifiers you know your bias will go down but then your variance will increase. So, there is

### Timestamp: 18:52

 always a trade of between bias and variance. Now, all the parameters that we cross validated

### Timestamp: 18:57

 let us say K in K nearest neighbors or depth in decision tree and so on or even your lambda in

### Timestamp: 19:03

 your regularized logistic regression or your support vector machines can be somehow thought of as

### Timestamp: 19:10

 balancing this bias variance trade off right. So, how am I allowing long larger I mean searching

### Timestamp: 19:16

 from a larger set of classifiers larger class of models or are I am I searching in a very

### Timestamp: 19:22

 less complicated class of models. So, now what we are going to see is two different ways to deal

### Timestamp: 19:30

 with this bias variance trade off by kind of ensembleing classifiers.