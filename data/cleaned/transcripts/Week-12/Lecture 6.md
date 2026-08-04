# Week-12 - Lecture 6

### Timestamp: 00:00

 So, that brings us to the end of the classification discussion right. So, and typically to and also

### Timestamp: 00:21

 to the end of this course. So, I kind of want to you know leave you with the final summary

### Timestamp: 00:28

 of all that we have seen in this course so far. So, we started with the problem of unsupervised

### Timestamp: 00:36

 learning and we said that you know there are D if 3 different major types of unsupervised

### Timestamp: 00:41

 learning. One was representation learning for which we saw PCA and kernel PCA. Then we looked

### Timestamp: 00:49

 at clustering for which we saw the k mean sulgur them and of course, I said that you can

### Timestamp: 00:55

 also extend k means to kernel version which is called as spectral flustering algorithm.

### Timestamp: 01:00

 And then we looked at estimation as part of unsupervised learning where we looked at maximum

### Timestamp: 01:07

 likelihood Bayesian methods and mixture models specifically focusing on the EM algorithm.

### Timestamp: 01:13

 And then we moved on to supervised learning we started with regression we put down the ordinary

### Timestamp: 01:19

 least squares based regression algorithm. Then we looked at you know ridge regression lasso

### Timestamp: 01:25

 and then we moved on to classification and we have seen a host of algorithms right from K

### Timestamp: 01:29

 nearest neighbors decision trees logistic regression per sub-tron support vector machines

### Timestamp: 01:35

 bagging boosting and now at a high level neural networks as well. So, with this I hope that we have

### Timestamp: 01:43

 a very solid foundational material covered for machine learning and now you should be able to

### Timestamp: 01:52

 smoothly transition to you know easily implementing these algorithms in practice either I mean

### Timestamp: 01:58

 you learn more if you are taking a machine learning practice course and also you will be able to

### Timestamp: 02:04

 smoothly transition to a deep learning course where you will be able to appreciate the algorithms

### Timestamp: 02:08

 much better than perhaps taking that before such a course before looking at the machine learning

### Timestamp: 02:13

 course. Let me also briefly comment that you know what is what are things that we did not look at

### Timestamp: 02:23

 it in look at in this course which are some things that interested audience can also look up.

### Timestamp: 02:30

 We did not cover couple of things. So, one thing we did not cover is semi-supervised learning we

### Timestamp: 02:37

 looked at supervised learning and unsupervised learning but then there is something in between called

### Timestamp: 02:40

 as semi-supervised learning where you have supervision for some data points but then you also have

### Timestamp: 02:45

 some unsupervised data points we did not cover that again with the understanding of whatever we

### Timestamp: 02:51

 have covered in this course you should be able to pick up those things if need be. We did not look

### Timestamp: 02:56

 at self-supervised learning which is another variant of you know especially in a deep learning

### Timestamp: 03:02

 context when the data is scarce you can kind of create new data from existing data using self-supervision

### Timestamp: 03:11

 techniques that is something that we did not cover with with respect to paradigms.

### Timestamp: 03:18

 We also did not cover sequential decision making which is perhaps hopefully at some point will be

### Timestamp: 03:23

 a separate course itself where the problem is very similar just that you know here we are we

### Timestamp: 03:30

 always start with the assumption that I have x1 y1 till x and yn right so you are given a bunch

### Timestamp: 03:35

 of data and then you need to do something with this data whereas in a sequential decision making

### Timestamp: 03:39

 problem your data comes one at a time and then you have to make a decision for the point that you

### Timestamp: 03:45

 are right now looking at and you will be given feedback whether it was correct or not and then

### Timestamp: 03:50

 over time you have to learn good you have to learn good strategies to predict well and so on and

### Timestamp: 03:56

 so forth. So there is an entire course that can be taught on sequential decision making hopefully

### Timestamp: 04:02

 at some point we will do that course also as part of this online BSE program. So that is something

### Timestamp: 04:09

 that we have not seen in this course and certain other things which are as follow-ups might be

### Timestamp: 04:15

 interesting for people who want to look at something more advanced especially right now instead of

### Timestamp: 04:22

 that machine learning conference is focuses on a couple of interesting things which are what I call

### Timestamp: 04:29

 as techniques for deployable machine learning deployable AI slash ML. So what we have learned in

### Timestamp: 04:38

 this course is one piece of an entire pipeline in a in a practical setup right so we have seen the

### Timestamp: 04:47

 most important part which is the algorithmic part. Now when you take this algorithm and try to

### Timestamp: 04:54

 deploy it on the field several issues might crop up. Let me point out a few issues I am not going

### Timestamp: 05:01

 to talk about the solutions to these issues now but then at least just to make you more curious

### Timestamp: 05:08

 about these topics let me give you some point out some issues one issue might be the issue of

### Timestamp: 05:16

 fairness right. So for example let us say this so one common example that is often given is

### Timestamp: 05:28

 a machine learning based system which was trying to predict some risk score for you know criminals

### Timestamp: 05:36

 of course in the US this was used at some point this was a system an ML system which would

### Timestamp: 05:42

 predict a risk score for a criminal for recommitting a crime and then coming back to the to the

### Timestamp: 05:50

 prison what is the chance that this person would recommit a crime right. So it used a lot of features

### Timestamp: 05:57

 of this person their previous crime records and so on and so forth and then it would predict a

### Timestamp: 06:03

 predict a score for that. Now it so happened that such a system

### Timestamp: 06:08

 started learning to predict scores which were not which were favorable to one ethnicity of

### Timestamp: 06:21

 criminals whereas it was not favorable to a different ethnicity of criminals.

### Timestamp: 06:27

 But then we know that you know a risk score should not be associated to ethnicity it should be

### Timestamp: 06:33

 associated to the nature of crimes committed in the past and so on and so forth. But the problem

### Timestamp: 06:38

 here is the the algorithm started picking up ethnicity as a feature which can be used to make such

### Timestamp: 06:46

 bad predictions. Now why did this happen well there is nothing in the algorithm like a logistic

### Timestamp: 06:53

 regression on SVM which is biased to one group of population than others. The problem though here

### Timestamp: 06:59

 comes because the bias is actually in the data right. So if your data or the previous judges who

### Timestamp: 07:08

 had given judgment were biased towards one ethnicity than other and then they had you know given higher

### Timestamp: 07:17

 risk scores for one ethnicity than other or higher prison time for one ethnicity than others

### Timestamp: 07:25

 then any algorithm that learns based on biased data is also going to produce biased outputs.

### Timestamp: 07:30

 So the question it's a big question today right. So if you deploy AI in a real world scenario you

### Timestamp: 07:36

 should really ask the question is the AI that I am deploying really responsible really doing the

### Timestamp: 07:43

 right thing is it fair right. So now question of fairness is a meta question it's not necessarily

### Timestamp: 07:49

 the algorithm that is unfair it is the data that could be unfair right. So so algorithm so can we

### Timestamp: 07:55

 make fair algorithms this is one important question that that that is still being discussed and we

### Timestamp: 08:02

 have some solutions at this point and still a research area. Second point right so is as we saw

### Timestamp: 08:09

 today it's a neural networks are slightly much more complicated you know beast than a linear

### Timestamp: 08:18

 regression right. So for example because of a lot of non-linearity involved and so on and so forth

### Timestamp: 08:22

 well while these algorithms might give you very good accuracy now the question that

### Timestamp: 08:27

 one should answer is can we use this in mission critical applications let's say you are a

### Timestamp: 08:33

 health care professional let's say you are a doctor and then you are trying to prescribe a

### Timestamp: 08:38

 particular medication to a patient and then you are taking help of a neural network to make

### Timestamp: 08:44

 you give you suggestions right. So and let's say the neural network says hey this patient should be

### Timestamp: 08:51

 prescribed a particular medicine right. So I am just making a this example but then let's say such

### Timestamp: 08:57

 a situation arises now as a doctor you should know why did the algorithm make this decision right.

### Timestamp: 09:05

 So if it is a simple decision tree based algorithm then the algorithm can say it not only gives you

### Timestamp: 09:14

 the actual output as to whether a particular medication should be taken or not it also tells you

### Timestamp: 09:19

 why it arrived at such a decision because a particular feature was less than certain threshold

### Timestamp: 09:24

 particular feature was greater than certain threshold and so on and so forth you can

### Timestamp: 09:27

 trace down the decision tree to its leaf and then that's just a set of you know if then else

### Timestamp: 09:32

 conditions. Now that is a very explainable way to make predictions. On the other hand a very

### Timestamp: 09:39

 complicated 100 layer hidden layer neural network if you ask why did you make this prediction now

### Timestamp: 09:45

 that is there is no simple way to make this explanation right. So because the model itself is

### Timestamp: 09:51

 inherently very very complicated. So now how can as a doctor I can be very confident about using

### Timestamp: 10:00

 the prediction that a neural network does or let's say we are using neural networks to or

### Timestamp: 10:06

 some complicated algorithm to design self-driving cars right. So now the car some passenger walks

### Timestamp: 10:15

 in front of the car the car is supposed to apply brakes but it does not and then the car jams into

### Timestamp: 10:20

 the passenger let's say unfortunately the passenger dies. Now we have to ask the question why was

### Timestamp: 10:27

 the brake not applied right. So it is a decision problem that the algorithm has solved and then it

### Timestamp: 10:32

 has decided not to apply brakes right. So but then how do who should be held accountable first of all.

### Timestamp: 10:39

 So how can we make the model explain its decision right. So if the model cannot explain the decision

### Timestamp: 10:44

 in a simple way in a human understandable way then how can we decide who should be blamed for

### Timestamp: 10:49

 this model. This is the person who wrote the algorithm or is it because certain type of training

### Timestamp: 10:55

 method was used and what should be I mean who should be held accountable. It's not at all clear

### Timestamp: 11:01

 right. So these are questions which needs more thinking about and people are

### Timestamp: 11:04

 doubling with these questions as we speak. So this is a very important area of machine learning that

### Timestamp: 11:10

 people are looking at called the explainable AI explainable machine learning. So fairness is one

### Timestamp: 11:16

 explainability is one and of course people want another important thing in

### Timestamp: 11:23

 deployable machine learning is privacy. For example I have a very good algorithm but then you know if

### Timestamp: 11:28

 the algorithm is kind of leaking information about the data points maybe it's these are confidential

### Timestamp: 11:34

 information maybe this is my salary information or maybe it is my health records based on which

### Timestamp: 11:40

 the algorithm is trying to you know predict something in general learn a model. Now if maybe as

### Timestamp: 11:46

 a patient I may not be happy to you know provide information to a machine learning algorithm if the

### Timestamp: 11:53

 algorithm potentially my leak information about my health status. I do not want the algorithm to

### Timestamp: 11:59

 do that right. So which means that can we develop machine learning algorithms which are private.

### Timestamp: 12:04

 So if so what is the definition of privacy how can we define privacy and so on and so forth before

### Timestamp: 12:10

 you deploy certain algorithms right. So privacy is another big question that people talk about all

### Timestamp: 12:16

 the time. The other point which is also of interest is as neural networks become larger and larger

### Timestamp: 12:24

 and we make more and more complicated models question of you know if you want to bring these

### Timestamp: 12:30

 models to a phone right. So which is in your pocket which has limited memory mind you no matter

### Timestamp: 12:37

 how fast it is right. So the memory might still be limited especially when you think of neural

### Timestamp: 12:42

 network billions of parameters right. So how can we put such a complicated model into

### Timestamp: 12:49

 into low memory resources right. So can we kind of truncate the precision of neural networks

### Timestamp: 12:59

 can be subsample can we do something right. So how can we make you know small neural networks

### Timestamp: 13:05

 which kind of mimic the large neural networks. These are questions that people researchers have been

### Timestamp: 13:11

 asking which I can call as A for edge right. So that is one interesting direction of that people

### Timestamp: 13:19

 are looking at as well. The other thing which is which is always important is because once you

### Timestamp: 13:26

 deploy your models on the field now it is all you have learnt is from training data but then

### Timestamp: 13:33

 your test data might gradually change over time right. So maybe you are you have a model which is

### Timestamp: 13:42

 which is to predict which team in an IPL match will win based on previous you know scores and

### Timestamp: 13:50

 players statistics that you have you built a model and now you are using that to make predictions

### Timestamp: 13:56

 but what might happen is over time people skills might change teams might change also the things might

### Timestamp: 14:01

 happen and so the distribution and so the way people play against each other might be completely

### Timestamp: 14:08

 different from what the data that your model has learned from. So how can we continuously make the

### Timestamp: 14:13

 model make changes right. So now you cannot retrain your model from scratch every time a new data

### Timestamp: 14:18

 point comes in how can you kind of do this learning seamlessly after you have done your deployment

### Timestamp: 14:26

 or also questions of interest right. So to summarize you have several you know post deployment

### Timestamp: 14:33

 questions to take care of including fairness, explainability, privacy, you know distributed learning

### Timestamp: 14:42

 which I did not talk about too much but that is also another interesting thing. A for edge

### Timestamp: 14:48

 and transfer learning which is how to transfer the knowledge from one domain to another domain

### Timestamp: 14:54

 or continuous learning how do you learn keep on learning after you have deployed the model.

### Timestamp: 14:59

 So these are all several interesting directions that as a learner I would suggest all of you to

### Timestamp: 15:04

 you know think about and read about these are all you know state of the art techniques that people

### Timestamp: 15:11

 are you know developing as we speak. So I hope there are so many things that you can do after

### Timestamp: 15:20

 finishing this course. As I said this is an introductory course the goal of this course is to give

### Timestamp: 15:25

 you a solid foundation so that you are prepared to take up all these slightly advanced courses

### Timestamp: 15:32

 courses which deal with state of the art algorithms like the deep learning course for unstructured data

### Timestamp: 15:37

 or you can look at research works going on that in several areas that I just listed in

### Timestamp: 15:44

 deployable A. So with this I would like to conclude my talk today and we will finish this course here.

### Timestamp: 15:53

 I sincerely hope all of you had a good time listening to these lectures and hopefully you learn

### Timestamp: 15:59

 something useful from this course. So all the best and until we see in a different course

### Timestamp: 16:08

 thank you thank you very much for your attention and see you soon bye.