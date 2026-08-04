# Week-9 - Lecture 1

### Timestamp: 00:00

 Hello everyone, welcome back. So, for in this course we have looked at lot of algorithms

### Timestamp: 00:18

 for supervised learning, specifically the problem of binary classification and we said that

### Timestamp: 00:24

 last time we can look at two different ways of modeling binary classification problems. So,

### Timestamp: 00:29

 in under supervised learning we are looking at you know binary classification and under binary

### Timestamp: 00:42

 classification we said that there are two different broad models, broad ways of modeling

### Timestamp: 00:49

 binary classification problem. One is the generative model and the other is the discriminative model.

### Timestamp: 00:56

 And under the generative model we have looked at several examples, specifically we looked at

### Timestamp: 01:04

 the example last time of the naive base assumption which assumed a class conditional independence

### Timestamp: 01:12

 and then that gave us a naive base algorithm that use the simple binary features, but then we

### Timestamp: 01:18

 said that we can also look at a case where we can think of real features and that gave us a Gaussian

### Timestamp: 01:23

 naive base or sometimes also called as the Gaussian discriminant analysis. Both are just the same

### Timestamp: 01:33

 names for different names for the same algorithm. Whereas in the discriminative case we have looked

### Timestamp: 01:38

 at you know some basic algorithms like the K nearest neighbors and decision trees which are

### Timestamp: 01:47

 discriminative because we do not really model how the data itself is generated, but given the

### Timestamp: 01:53

 data point what we are modeling is how can we get an answer for it, how can we make a prediction

### Timestamp: 01:59

 for it based on the data right. So, in some sense you can think of this as there is a non-probably

### Timestamp: 02:03

 istic question of a discriminative model where we are just mapping, we are trying to learn mapping

### Timestamp: 02:08

 from input to output. So, that that is a discriminative model what we are going to do is we are going to

### Timestamp: 02:15

 study more discriminative models from here on and to motivate this when we looked at naive

### Timestamp: 02:21

 base algorithm for example, which was a generative model which modeled P of y and P of x given y,

### Timestamp: 02:30

 but then at the end of the day when we actually wanted to make a prediction we would use P of y given

### Timestamp: 02:34

 x and we use the base rule that is why the name naive base and the base rule would tell us a

### Timestamp: 02:41

 relation between P of y given x and P of x given y and P of y which we have already modeled,

### Timestamp: 02:47

 but what we saw interestingly in the naive base case was that P of y given x was actually

### Timestamp: 02:54

 can be I mean P of y given x greater equal to 0.5 right. So, that decision surface can actually

### Timestamp: 03:00

 be written as a linear function of the input. So, this is something that we saw in other words

### Timestamp: 03:05

 there is a line that separates the you know y equals 1 class from the y equals minus class in

### Timestamp: 03:10

 the best possible way. So, then we can ask the question well we made a generative assumption,

### Timestamp: 03:15

 but then what ended up being the best possible classifier is actually a line linear function,

### Timestamp: 03:21

 why can't we directly model the classifier as a linear function in a discriminative sense

### Timestamp: 03:28

 right. So, which is what we are going to do today what do I mean by that well what we are going to

### Timestamp: 03:32

 do is the first thing is we are going to look at discriminative models for classification.

### Timestamp: 03:41

 Discriminative models for classification where we are trying to understand discriminative

### Timestamp: 03:50

 model when you say discriminative model we want a model P of y given x right. So, we want to say

### Timestamp: 03:55

 how does the probability of y equals 1 given x looks like and of course that will determine the

### Timestamp: 04:00

 probability of y equals 0 given x which is just 1 minus probability of y equals 1 given x.

### Timestamp: 04:05

 So, the question we ask is how to model P of y given x right. So, that is you are given a

### Timestamp: 04:13

 feature now we want to be able to discriminate whether this feature is in class 1 or class 0.

### Timestamp: 04:19

 So, we want to make some assumptions about this discriminating power right. So, what is the

### Timestamp: 04:24

 functional form of this discriminator and the simplest assumption that we can make is that

### Timestamp: 04:28

 it is a linear function what does that mean that means the following. So, simplest assumption

### Timestamp: 04:38

 and yes this is an assumption that we are making on how the data is generated. So,

### Timestamp: 04:43

 this is where we are saying that the probability of y equals 1 given x right. So, this probability

### Timestamp: 04:50

 can only take two values it can either be 1 or 0 right. So, it is not really a probability that

### Timestamp: 04:56

 there is a deterministic thing that is happening here, but then trivially we can say that there

### Timestamp: 05:00

 is a probability of 1 or 0, but when will we say probability of y equals 1 given x is 1.

### Timestamp: 05:06

 Well if w transpose x is greater than or equal to 0 and otherwise 0 otherwise.

### Timestamp: 05:16

 Now, remember let us try to think about what this assumption actually means right. So,

### Timestamp: 05:20

 what are we saying we are saying that the probability that y equals 1 given x is either 1 or 0,

### Timestamp: 05:27

 which means that let us say somehow somebody gave a feature x we do not care about how the feature

### Timestamp: 05:34

 itself was generated because we are only modeling a discriminative model here. So, somebody

### Timestamp: 05:39

 gives us a feature x now we have to decide the label y equals 1 or y equals 0 right. So, to create

### Timestamp: 05:44

 let us say I am trying to create the training data. Remember in the generative process of the

### Timestamp: 05:49

 naive base we put down a generative story that created the training data. Here also there is a

### Timestamp: 05:55

 story, but this is a discriminative story in the sense that we do not care about how the x is

### Timestamp: 05:58

 generated we only care about how the y is generated given the x right. So, this is the discriminative

### Timestamp: 06:03

 story and what is the discriminative story here. Well if I am going to give you a data set this

### Timestamp: 06:08

 is how I would give you a data set I will give you some arbitrary x right. So, there is no

### Timestamp: 06:12

 probabilistic model that is generating x that we are assuming. So, I give you an x, but now when

### Timestamp: 06:17

 I have to decide what is the y corresponding to this x what I am going to do is I am going to toss

### Timestamp: 06:23

 a coin and this coin will have either both sides heads or both sides tails right. So, that is what

### Timestamp: 06:29

 it means to say that the coin has probability 1 or probability 0 right. So, when will this coin

### Timestamp: 06:36

 have both sides heads well when will this coin have probability of choosing 1 well when y equals

### Timestamp: 06:43

 for y equals 1 right. So, which means that if for the given x w transpose x is greater than or

### Timestamp: 06:50

 equal to 0 then I would simply say the label is 1. If for the given x w transpose x is less than 0

### Timestamp: 06:57

 then I am simply going to say the label is 0. Equalently I am and I can think of this as a

### Timestamp: 07:03

 probabilistic setup where the probability is just 1 if w of choosing y equals 1 if w transpose x

### Timestamp: 07:10

 is greater than or equal to 0 right. So, the probability should not really confuse you at the end

### Timestamp: 07:14

 of the day it is it is equivalent to saying that simply I am going to decide the label by checking

### Timestamp: 07:20

 whether x satisfies w transpose x greater than or equal to 0 or not in a deterministic fashion right.

### Timestamp: 07:27

 So, of course, you do not know what the w is I as a generator of this labels is going to give you

### Timestamp: 07:33

 the labels based on some w right. So, you as a learner you do not know what the w is, but you know

### Timestamp: 07:39

 there is some w based on which I am giving you the data which means what right. So,

### Timestamp: 07:44

 this means that what we are essentially assuming about the data is that the data is linearly

### Timestamp: 07:51

 separable or this is the linear separability assumption.

### Timestamp: 08:01

 So, let us make that very clear now right. So, what does this mean? This means that let say I have a

### Timestamp: 08:06

 dataset I see a dataset like this right where green corresponds to let say label as 1 and red

### Timestamp: 08:16

 corresponds to let say label as minus minus 1 of 0. Now, if I see this data right. So, where green

### Timestamp: 08:24

 is red is 0 label and green has label as 1 right. So, y equals 1 this has y equals 0 y equals 0.

### Timestamp: 08:37

 Now, can the I asked a question can this data be generated according to the model that I have assumed?

### Timestamp: 08:50

 Well, if you if you look at the stare at the data for a second you will realize that yes this data

### Timestamp: 08:55

 is linearly separable which means that I see this data now yes this data could have come from

### Timestamp: 09:02

 this model that I am assuming where there is some unknown w right. So, maybe there is there should

### Timestamp: 09:08

 be some w such that when the when the person who gave me the data label the data that person used

### Timestamp: 09:15

 some w I do not know what this w is but I am assuming that there is some w in this case yes there

### Timestamp: 09:20

 is some w right. So, maybe this is the w which says that everybody on one side of w the green ones

### Timestamp: 09:26

 are all on one side of w the red ones are all on other side of w right. So, for example, then

### Timestamp: 09:32

 I mean basically this example we say that this example is allowed under our model that is

### Timestamp: 09:41

 we are so we are putting down this model for the data's label generation process and well once

### Timestamp: 09:47

 you put down the model then you ask what type of data sets are allowed right. So, this is a

### Timestamp: 09:51

 dataset that is allowed under our model. Now, let us also think about a dataset which is not

### Timestamp: 09:56

 allowed under our model right. So, how could how would that dataset look like well you can now

### Timestamp: 10:01

 again create very very simple examples right. So, now here is a dataset where you have lots of greens

### Timestamp: 10:07

 here which corresponds to y equals 1 and let us say lots of reds here which corresponds to y

### Timestamp: 10:15

 equals 0 let us say there is a red here as well. Now, I asked the question well could I have seen

### Timestamp: 10:22

 this data under the model that I am assuming well if I have seen this data under the model that

### Timestamp: 10:29

 I am assuming then somebody has given me the labels according to some w. Now, if you look at this

### Timestamp: 10:36

 example there is no w such that all the points which have been labeled green are on one side of

### Timestamp: 10:44

 w and all the points which have been labeled red or on the other side of w right. So, there is no

### Timestamp: 10:48

 such w earlier we said that this there is this w right. So, this w but then this w will not

### Timestamp: 10:55

 label this point correctly right. So, if the labeler had used this w then the labeler would have

### Timestamp: 11:01

 actually labeled this point is green not as red, but then I am seeing this as red. So, this w could

### Timestamp: 11:06

 not have been the w that the labeler could have used. Now, it now it is not too hard to see that

### Timestamp: 11:12

 could be no such w that could have generated this data which means that we are saying under the

### Timestamp: 11:17

 situation that this data set is not allowed under our model that is to say that well

### Timestamp: 11:32

 I am assuming that I will never get such a data set because you know your model should be able to

### Timestamp: 11:38

 I mean you can only work with data sets which the model can generate and in this case we are

### Timestamp: 11:43

 saying that well this data set could not have been generated according to our model. So, our model

### Timestamp: 11:48

 can never explain this data set right. So, now this this means that there is no linear separator

### Timestamp: 11:55

 that separates the greens from the reds in this data set and so this model is not allowed in our

### Timestamp: 12:00

 data set. Now, one can ask the question well this looks like a very simple data set which we should

### Timestamp: 12:05

 be able to you know allow in a reasonable model I agree right. So, any reasonable model should

### Timestamp: 12:12

 should be able to you know generate be able to allow the possibility of generating data sets like

### Timestamp: 12:18

 this where you have these out layers also which is a disadvantage of this model that it only

### Timestamp: 12:26

 allows linearly separable data sets. But what we are going to do now is well we are going to

### Timestamp: 12:32

 acknowledge that there is this disadvantage at this point that we are only going to allow

### Timestamp: 12:36

 linearly separable data sets and then ask the question well if I allow only linearly separable

### Timestamp: 12:42

 data sets then how good can I do right. So, can I develop algorithms which which which can

### Timestamp: 12:49

 you know do the best if you cannot develop such an algorithm then you know even in a simple case

### Timestamp: 12:55

 right. So, you have made such a strong assumption about the data set about the model even in under

### Timestamp: 13:00

 this assumption if you cannot develop good algorithms then you know when these assumptions fail

### Timestamp: 13:05

 when you have all these out layers and so on then it is only going to be hard to develop algorithms

### Timestamp: 13:11

 right. So, so the hope is that will be make the strongest assumption and then ask the question

### Timestamp: 13:16

 can be you know develop good algorithms for this and let us see then later on once we have such

### Timestamp: 13:22

 algorithms how you can you know play around with the algorithm to make it work for this complicated

### Timestamp: 13:27

 slightly more complicated situations as well right. So, with that with that understanding so

### Timestamp: 13:32

 let us say we make this assumption of linear separability and now we are what is our goal right.

### Timestamp: 13:39

 So, our goal is to do the following right. So, I have a data set and I want if you remember

### Timestamp: 13:46

 that rates of from the beginning our discussion we want to find some H belonging to some you know

### Timestamp: 13:53

 set of classifiers which minimizes the 0 1 loss right. So, indicator of H of x i not equals y

### Timestamp: 14:05

 right. So, we said that this H even if this H is linear for a general data set this is an

### Timestamp: 14:13

 NP hard problem we did say this right. So, this is NP hard for a general data set

### Timestamp: 14:25

 even if H is just linear functions linear hypothesis right. So, which means that if I give you a

### Timestamp: 14:40

 general data set which which I am not assuming comes from any model if I give you a general data set

### Timestamp: 14:45

 of pairs of x, y and I ask you to find that line that best that makes the least number of mistakes

### Timestamp: 14:52

 then that is an NP hard problem even if you are just have to even if you have to just find a

### Timestamp: 14:56

 line it is still an NP hard problem it is a hard problem to solve right. So, what what do you mean by

### Timestamp: 15:01

 general data set well there is nothing no restriction on how the data set should be right. So,

### Timestamp: 15:06

 there could be outliers that could be all sorts of mixing and matching between great greens and

### Timestamp: 15:10

 rates that could happen right. So, in a general sense if you want to find the best possible line

### Timestamp: 15:14

 that is a hard problem. But now we are saying well I am not going to allow all possible data sets.

### Timestamp: 15:19

 It is not a general data set that I am going to deal with here is a data set which I am saying

### Timestamp: 15:24

 you know has a very strong restriction that the data set is linearly separable.

### Timestamp: 15:30

 That is an assumption that I am making but of course, I do not know which is the line that

### Timestamp: 15:34

 separates the data I am just seeing the data. But I know that there is some line that separates

### Timestamp: 15:38

 the data now the question is under the situation can I do can I minimize this 0 1 loss right.

### Timestamp: 15:45

 So, that is the question that we are going to ask now you know how about

### Timestamp: 15:52

 with extra you know linear separability assumption.

### Timestamp: 16:01

 What does that mean that means that we have a bunch of data points which we know is linearly

### Timestamp: 16:06

 separable right. So, that is there is some w such that you know sign of w transpose x matches

### Timestamp: 16:13

 the label y. Now, under that situation we know that you know the label is using some w to make

### Timestamp: 16:20

 these labels. Now, for that particular w what do you think is this value what is the minimum

### Timestamp: 16:27

 minimum 0 1 loss. Pause and think about this I will tell you the answer now right. So,

### Timestamp: 16:32

 because the label is using a w to you know label plus 1 or 0. Now, if you have the w access to

### Timestamp: 16:40

 that w then you will make 0 errors on the training set because that w is what was used to give the

### Timestamp: 16:45

 labels if I had access to that w I will make 0 training error right. So, so the training error can

### Timestamp: 16:51

 be as small as 0 in this case right. So, you can get a linear hypothesis which means a line which

### Timestamp: 16:58

 has 0 training error of course, I do not know which line this is right. So, that is that is hidden

### Timestamp: 17:03

 from me the label has used some line, but I do not know which line it is. Now, the question is

### Timestamp: 17:08

 is it still n p hard to find that line or are there algorithms which will help us find this line

### Timestamp: 17:14

 right. So, now given that we have put such a strong restriction on the data set now well we

### Timestamp: 17:21

 do not necessarily mean we at least hope now that the problem is not too hard now right. So,

### Timestamp: 17:26

 it is only you know that you are given a data set which has some line that separates the one

### Timestamp: 17:30

 from the zeros can you just find this line right. So, can you find a line that does this

### Timestamp: 17:34

 it turns out the answer to this problem is yes we can find such a line right. So,

### Timestamp: 17:41

 now what we are going to do is we are going to give a classic algorithm which actually

### Timestamp: 17:48

 tries to find such a line right. So, let me put down the algorithm and then we will talk about

### Timestamp: 17:53

 more about the algorithm, but before I do the put down the algorithm let me make this assumption

### Timestamp: 17:59

 very very precise right. So, what is the linear separability assumption in more formally stated

### Timestamp: 18:05

 so that you know there is no confusion about what we are talking about it just says the following

### Timestamp: 18:13

 right. So, it just says that we are just assuming that there is some w there exists some w in

### Timestamp: 18:18

 D dimension such that the sign of w transpose x i equals y i for all i in our data set right.

### Timestamp: 18:29

 So, this is the assumption that we are working with now we know that this our data set

### Timestamp: 18:34

 satisfies the assumption can be find such a w right. So, this is the question that we are asking

### Timestamp: 18:39

 ok. So, now let us go ahead and put down this simple algorithm which is a very classical algorithm.

### Timestamp: 18:45

 The algorithm that we are going to see is called as the perceptron algorithm

### Timestamp: 18:56

 and this was given by somebody called Rosenblatt in the 1920s.

### Timestamp: 19:05

 So, it is called perceptron because Rosenblatt at that point was trying to understand

### Timestamp: 19:10

 how to recognize objects right. So, the vision problem a computer vision problem and he realized

### Timestamp: 19:17

 that more and more that decision making the human brain makes decision based on these neurons

### Timestamp: 19:22

 and synapses and so on and he got inspired by how a neuron fires what makes a neuron fire

### Timestamp: 19:29

 and you know he got inspiration from that and then kind of build this algorithm that we are going

### Timestamp: 19:33

 to see now which is called as the perceptron algorithm. So, in fact Rosenblatt the history is

### Timestamp: 19:39

 that Rosenblatt went ahead and built a real purpose you know mechanical machine which

### Timestamp: 19:45

 implements exactly the algorithm that we are about to see right. So, and Rosenblatt believed that

### Timestamp: 19:51

 this algorithm can actually be is indeed can solve the problem of vision is can indeed you know

### Timestamp: 19:59

 can solve all reasonable decision making problems. With the power of hindsight we know that

### Timestamp: 20:06

 the power of this algorithm and the way that I have Rosenblatt put it down and the way that we

### Timestamp: 20:11

 are going to look at now is restricted in the sense that it will work when the dataset is linearly

### Timestamp: 20:17

 separable and it may not work when it is not linearly separable right. So, we are going to talk more

### Timestamp: 20:22

 about properties of this algorithm in a little later but before that let us understand what the

### Timestamp: 20:27

 algorithm is right. So, what did Rosenblatt put down and why is it that this algorithm is so

### Timestamp: 20:32

 important in understanding you know the basic ideas of classical machine learning.

### Timestamp: 20:37

 So, let us begin right. So, what is the what is the algorithm well the algorithm's input is

### Timestamp: 20:42

 as usual our dataset which has x 1 y 1 dot dot dot x n y n where x i's are all in r t and for

### Timestamp: 20:54

 the purpose of this algorithm we are going to assume y i is either plus 1 or minus 1 typically

### Timestamp: 21:00

 we assume 1 or 0 but for the analysis of this algorithm it is easier to assume 1 or 1 or minus 1

### Timestamp: 21:09

 we could state the algorithm completely even if you assume 1 or 0 just that you need to be careful

### Timestamp: 21:14

 carrying around certain terms and so on which we are trying to avoid here in the simplest possible

### Timestamp: 21:18

 way to explain this algorithm is just assume that the labels are 1 and minus 1 right. So, but that

### Timestamp: 21:23

 does not you know restrict anything here right. So, because it is just a label at the end of the day

### Timestamp: 21:27

 you can think of the features as corresponding to emails and the labels as spam and non spam here

### Timestamp: 21:33

 I am just saying that I am going to call the spam as 1 a non spam as minus 1 right. So, that is not

### Timestamp: 21:38

 that is just without loss of generality ok. So, what is the algorithm do the algorithm is trying

### Timestamp: 21:45

 to find a w that best that correctly classifies all the data points if such a w exists.

### Timestamp: 21:51

 So, what it is going to do is it is going to do a iterative it is an iterative algorithm.

### Timestamp: 21:57

 So, it is going to start with some w which is w naught and this naught here indicates iteration

### Timestamp: 22:03

 number right. So, this is which iteration of the algorithm we are in and initially w naught is

### Timestamp: 22:13

 just 0 this is just a 0 vector right. So, 0 0 0 this is just a 0 vector it is a very simple

### Timestamp: 22:21

 algorithm let me put down the algorithm and then we will talk about properties of this. So,

### Timestamp: 22:25

 the algorithm goes as follows until convergence the algorithm is going to do something what it is

### Timestamp: 22:34

 going to do is the following right. So, pick x i comma y i pair from the data set

### Timestamp: 22:44

 right. So, if sin of you know w t transpose x i is not equals y i well is equal to y i then do nothing

### Timestamp: 23:07

 and we will talk about what the step means else w t plus 1 equals w t plus x i to y i

### Timestamp: 23:19

 and that is it. This is the algorithm this is the what is called as an update rule and we

### Timestamp: 23:40

 will talk about this in beta. So, what is this algorithm well this algorithm begins with initialization

### Timestamp: 23:47

 of w naught equals 0 and now it is going to see you have one of data points it is going to find

### Timestamp: 23:56

 out if the current w naught is is enough right. So, if it classifies everybody correctly

### Timestamp: 24:03

 if it classifies everybody correctly then you are done we have found a w that classifies all

### Timestamp: 24:09

 points in your data set correctly. If not there is some point which your current w which whichever

### Timestamp: 24:15

 you are maintaining makes a mistake on right. So, which means that the sin of w t transpose x i

### Timestamp: 24:21

 does not match y i right. So, if there is such a point then you update your w based on that point

### Timestamp: 24:29

 right. So, using this update rule which is w t plus 1 is w t plus x i y i. Now remember x i is

### Timestamp: 24:37

 in r d y i is is plus or minus 1 depending on whether that point was labeled plus 1 or minus 1

### Timestamp: 24:44

 in my data set. So, all you are doing is you know you are maintaining a current w you are looking

### Timestamp: 24:50

 at all the points in your data set if you can find a point where the current w is going wrong

### Timestamp: 24:57

 then you make an update to the current w based on a point where you made a mistake that is you take

### Timestamp: 25:03

 the point x i y i where the current w w t makes a mistake and then just add x i into y i to your

### Timestamp: 25:10

 w t to get your new w. And now for this new w you go through all the data points see if it matches

### Timestamp: 25:15

 if it predicts correctly all data points. If it does then you are done you have found a w that

### Timestamp: 25:19

 works that has zero error otherwise you would have found a point where this w makes a mistake

### Timestamp: 25:25

 and you will add that point in multiplied by its label to the current point and you keep doing

### Timestamp: 25:29

 this. Now, what I am saying is that if you keep doing this then I am claiming that you know

### Timestamp: 25:35

 you do this until convergence. So, that is a statement that needs some you know clarification.

### Timestamp: 25:43

 So, what do I mean by convergence here well we will say that the algorithm has converged

### Timestamp: 25:49

 if you have found a w which correctly classifies all the data points. So, if not you are going to

### Timestamp: 25:56

 update this w based on the point where you make a mistake if at some point you find a w where

### Timestamp: 26:02

 all the data points are correctly classified then you are done right. So, it means that the

### Timestamp: 26:05

 algorithm has converged to that w you do not need to make any more updates and you would just end

### Timestamp: 26:10

 the algorithm. Now, the update rule is the only thing that is non-trivial happening here right.

### Timestamp: 26:17

 So, the only non-trivial step which is which is happening which is a very simple step in this

### Timestamp: 26:21

 algorithm is the update rule which says that if you make a mistake then add that point times its

### Timestamp: 26:27

 label to the current w and we do not know at this point if this algorithm is going to converge right.

### Timestamp: 26:34

 So, because though I say until convergence what is the guarantee that this algorithm is going to

### Timestamp: 26:40

 converge right. So, because I am kind of adding a lot of things to my w and keeping

### Timestamp: 26:45

 keeping on updating my w what is the guarantee that you know I will actually find a w that

### Timestamp: 26:51

 that eventually you know correctly classified all the data points not clear at all at this point.

### Timestamp: 26:58

 So, the moment I say until convergence that needs to be backed up with an argument.

### Timestamp: 27:03

 So, what we are going to do is we are going to understand whether this algorithm will actually

### Timestamp: 27:08

 converge or not and to understand that we first need to you know look closely into this update

### Timestamp: 27:13

 rule right. So, because that is the only non-trivial thing happening in this algorithm. So,

### Timestamp: 27:17

 we want to understand if the update rule is doing the most reasonable thing that we wanted to do

### Timestamp: 27:23

 right. So, that is the first thing that we are going to think about. So, let us start understanding

### Timestamp: 27:27

 the update rule of the perceptron algorithm to see what it is trying to do.