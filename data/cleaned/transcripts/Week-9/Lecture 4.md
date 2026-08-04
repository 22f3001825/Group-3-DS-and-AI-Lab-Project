# Week-9 - Lecture 4

### Timestamp: 00:00

 Hello everyone, welcome back. So, far we have looked at the perceptron algorithm for binary

### Timestamp: 00:18

 classification and we have argued that the perceptron algorithm will in fact find linear

### Timestamp: 00:24

 classifier if the data that is given is linearly separable. We also argued that the perceptron

### Timestamp: 00:30

 algorithms number of mistakes, right. So, perceptron the number of mistakes that perceptron

### Timestamp: 00:36

 makes depends on is at most, right. So, let me put this this way perceptron mistakes

### Timestamp: 00:43

 is less than or equal to r square by gamma square where r is the radius of the data points

### Timestamp: 00:51

 and gamma is what we were calling as margin that is when the data set is linearly separable

### Timestamp: 00:56

 with gamma margin then what we are able to argue is that the perceptron number of mistakes

### Timestamp: 01:02

 is a finite quantity it is bounded by r square by gamma square. Now, this needs a very closer

### Timestamp: 01:08

 look what does it mean to say the margin is gamma and so on and that needs a longer

### Timestamp: 01:15

 discussion and the algorithms that will come out of it will have a will will need a longer

### Timestamp: 01:19

 discussion. So, what we are going to do is we are going to do this afresh in the coming

### Timestamp: 01:24

 week, but for now we will part the idea of perceptron that here is an algorithm and we

### Timestamp: 01:30

 know that that algorithm converges when the data is linearly separable and we know the

### Timestamp: 01:35

 number of mistakes that it makes is bounded by the radius square divided by the margin

### Timestamp: 01:40

 square. This this is the understanding that we have right now we will come back and revisit

### Timestamp: 01:44

 this idea of margin a little later perhaps in the next week where we will have a longer

### Timestamp: 01:49

 discussion about this and then see what kind of algorithms can that this discussion will

### Timestamp: 01:54

 inspire. But for today what we wanted to do is you know to see what is the assumption

### Timestamp: 02:01

 that perceptron makes and can be you know rethink this assumption in a slightly different

### Timestamp: 02:06

 way. So, if you remember the assumption that perceptron makes is a linear separability

### Timestamp: 02:11

 assumption right. So, but if you want to write that in a probabilistic way then one way

### Timestamp: 02:16

 to say that is that probability of y equals 1 given x this value is just 1 that is with

### Timestamp: 02:23

 certainty you will predict 1 if w transpose x is greater than or equal to 0 and this probability

### Timestamp: 02:29

 is 0 otherwise right. So, that is there is a probability, but then it is not really I

### Timestamp: 02:37

 mean non trivial probability right. So, which means that this is essentially we have argued

### Timestamp: 02:45

 that this is essentially saying that the data set is linearly separable with with the

### Timestamp: 02:49

 separator given by the plane perpendicular to w. Now, because of the strict assumption

### Timestamp: 02:56

 about this probabilities being just 1 or 0 perceptron is unable to model you know data

### Timestamp: 03:03

 sets like this right. So, if you have let us say plus plus plus plus plus plus plus minus

### Timestamp: 03:10

 minus minus minus minus let me put this in the black color. Now, if you have a minus here

### Timestamp: 03:19

 and if you have a plus here we know that this data set is not allowed under the perceptron

### Timestamp: 03:24

 model why because when I am trying to label this when there is a labeler who is giving

### Timestamp: 03:28

 me labels for this data points well that is going to depend on some w maybe the w is here

### Timestamp: 03:33

 and that w says that well everybody on one side is plus and the other side is minus.

### Timestamp: 03:39

 But then if the labeler had used this w then that labeler would have labeled this point

### Timestamp: 03:44

 as plus and this point as minus, but because we are seeing the other way in the data set

### Timestamp: 03:49

 this status set could not have generated could not have been generated according to the

### Timestamp: 03:54

 perceptron assumption which is this. And if you look closely at this assumption the

### Timestamp: 03:58

 main culprit is the fact that we are assuming that you know the probabilities are exactly

### Timestamp: 04:02

 1 and 0. So, can we somehow relax this assumption right. So, that is the question we are going

### Timestamp: 04:08

 to ask now and then we will see that what kind of algorithms that will lead us to.

### Timestamp: 04:12

 So, the question we are going to ask is can we model the probabilities differently what

### Timestamp: 04:25

 do I mean by differently well let us see what what does differently mean. There are

### Timestamp: 04:30

 several ways you can model it and here is one natural way that you might want to do this

### Timestamp: 04:34

 right. So, we can start with a simple model right. So, start with a simple model well

### Timestamp: 04:45

 what is a simple model a simple linear model simple models are typically linear what does

### Timestamp: 04:50

 that mean that means that you have some z. So, which which is like a score for a data

### Timestamp: 04:59

 point with respect to some w right. So, x is again your feature right. So, this is your

### Timestamp: 05:04

 feature vector x is in R D as usual and then there is some w. But now if I do w transpose

### Timestamp: 05:11

 x and if I am looking at that value now that value is like a score that w gives for this

### Timestamp: 05:17

 data point x right. So, in pictures it would mean something like this you have this two

### Timestamp: 05:23

 dimensional plane let us say this is our usual w that we typically take as an example.

### Timestamp: 05:29

 Now this line is just a set of all x such that w transpose x equal 0 that is the score

### Timestamp: 05:40

 that w gives to all the x on this line is just 0.

### Timestamp: 05:44

 Now, one might ask where is where are the set of points for which the score is 1 right.

### Timestamp: 05:49

 So, now if you think about that so that that is going to be somewhere here right. So,

### Timestamp: 05:53

 that is just going to be a line which is parallel one unit with respect to w. So, this is

### Timestamp: 05:58

 just the set of all x such that w transpose x equals 1. Now, similarly where are the set

### Timestamp: 06:03

 of points for which the score is minus 1 remember score is just a dot product the way

### Timestamp: 06:08

 we are thinking of it. So, the score could be minus 1 and that minus 1 could be somewhere

### Timestamp: 06:12

 here right. So, so this is set of all x such that w transpose x equal to minus 1.

### Timestamp: 06:18

 Well, if it is the score is negative then we are somehow saying that the data point is

### Timestamp: 06:23

 highly probable to be labeled minus 1 if the score is positive then the data point is

### Timestamp: 06:29

 probable to be labeled as positive. But now there is a difference that we want to you

### Timestamp: 06:36

 know in incorporate in our model between data points that are here and perhaps a data

### Timestamp: 06:42

 point which is may be somewhere here right. So, maybe this is a line which also has a data

### Timestamp: 06:50

 point. Now, this data point you know is the set of all x such that let say w transpose

### Timestamp: 06:58

 x is 100 right. So, if you move 100 units away in the parallel in the direction of you

### Timestamp: 07:05

 know the plane that separates I mean that is perpendicular to w. Now, if if I am generating

### Timestamp: 07:13

 these two I mean if I am generating labels for these two points let say somebody gave me

### Timestamp: 07:17

 these labels and now I have to give you sorry let say somebody gave me these points right.

### Timestamp: 07:21

 So, let us call this x 1 and this point as x 2 and now I have to give you labels for these

### Timestamp: 07:26

 points well I want to somehow associate a probability with these labels right. So, this

### Timestamp: 07:34

 label can be either 1 or minus 1 earlier we were saying that this probability that the

### Timestamp: 07:39

 label is 1 is 1 if it falls on one side of w which means that both these points will

### Timestamp: 07:44

 get label as 1 with probability 1 for this w right. So, whereas, the points whereas, there

### Timestamp: 07:49

 might be two other points on this side maybe x 3 and x 4 maybe x 3 is here and there is

### Timestamp: 07:56

 a corresponding maybe there is some x 4 on here which I am going to put here. So, this

### Timestamp: 08:02

 is the set of all x such that w transpose x equal to minus 150 let say right. So, this

### Timestamp: 08:09

 is parallel on this side 150 units. So, now I have to label x 1 x 2 x 3 and x 4 right.

### Timestamp: 08:16

 So, I have to give you labels earlier our assumption would say that I will just give you labels

### Timestamp: 08:21

 1 for x 1 and x 2 and minus 1 for x 3 and x 4 and that allowed only linearly separability

### Timestamp: 08:26

 as it is. Now, what I am going to say now is that I am going to allow for labels to be

### Timestamp: 08:31

 both plus 1 and minus 1 for all points, but what will decide this labels well there should

### Timestamp: 08:36

 be some probability for the label being plus 1 and there is some probability for the label

### Timestamp: 08:42

 being minus 1 for each of these points. Now, what will decide this probability that probability

### Timestamp: 08:46

 will be decide by how high or low the score associated with this point is which means

### Timestamp: 08:52

 that if I take a point like x 1 which is here versus x 2 which is here. Now, if you ask

### Timestamp: 08:58

 the question well which one should get a higher probability of being assigned to class

### Timestamp: 09:03

 1 well for this w this x 2 is much much far away from the separator right. So, which means

### Timestamp: 09:09

 that you are somehow more confident that this point has to be labeled plus 1 as opposed

### Timestamp: 09:14

 to x 1 which is close to the boundary which means that the probability that it should be

### Timestamp: 09:18

 labeled you know plus 1 should be lesser than the probability that x 2 is labeled plus 1 right.

### Timestamp: 09:25

 So, which means that as I move in this direction my probability that the point is labeled 1 should

### Timestamp: 09:32

 increase whereas as I move in this direction the probability that a point labeled minus 1 should

### Timestamp: 09:37

 increase right. So, still remember every point gets a non-zero probability of being plus 1 or

### Timestamp: 09:43

 minus 1, but then the chance that it becomes minus 1 somewhere here on the end of the I mean

### Timestamp: 09:51

 if you move for further away in this direction goes down right. So, somehow we need to capture

### Timestamp: 09:55

 this intuition using the score right. So, but remember the score itself is not a probability right.

### Timestamp: 10:00

 So, the score z is in minus infinity to infinity right. So, it is a real number. So, we have to

### Timestamp: 10:06

 convert the score somehow into a probability and the question is how can we do that right. So,

### Timestamp: 10:12

 so what do we want here we want the following larger the value of z larger the score

### Timestamp: 10:20

 which is z w transpose x more the probability of being 1 plus 1 right. So, because a large

### Timestamp: 10:34

 positive number should get a large positive probability of being plus 1 a large negative number

### Timestamp: 10:38

 should get a large probability of being minus 1 which means a small probability of getting plus

### Timestamp: 10:43

 1 right. So, we can just then decide the probability of being 1 using this score, but how to decide right.

### Timestamp: 10:48

 So, how can we convert this score into a probability well what do we want about this score right.

### Timestamp: 10:53

 The first question is what happens if we find a point which lies on this on this separate right.

### Timestamp: 11:01

 So, it is exactly lying on the separator which means that we are not really sure if this is going

### Timestamp: 11:06

 to be plus 1 or minus 1. So, we can give equal probabilities for them right. So, which means that

### Timestamp: 11:11

 every we want some function g such that which takes the score as input and outputs as probability,

### Timestamp: 11:20

 but this g of z should be 0.5 if z equal 0 right. So, whenever the score is 0 which means that

### Timestamp: 11:31

 the point lies exactly on the separator we want the probability of that being labeled plus 1 as 0.5

### Timestamp: 11:37

 and minus 1 also as point equal probability. Now, we want g of z the probability of the point being

### Timestamp: 11:44

 labeled 1 to to converge to 1 as z becomes larger and larger which means that as z becomes infinity.

### Timestamp: 11:53

 Similarly, we want g of z to converge to 0 as z becomes minus infinity the smaller and smaller

### Timestamp: 12:00

 the score is the chance that it being labeled as plus 1 should go to closer and closer to 0.

### Timestamp: 12:06

 So, any g that satisfies these 3 properties is a reasonable g to use right. So, this g is sometimes

### Timestamp: 12:14

 in literature is called as a link function because it links scores to real numbers to probabilities.

### Timestamp: 12:23

 There are several link functions that you might encounter in practice, but one of the most

### Timestamp: 12:27

 popular link function is one popular choice for link function is the following.

### Timestamp: 12:34

 So, g of z equals 1 divided by 1 plus e to the minus z right. So, this function is called

### Timestamp: 12:44

 sometimes as the sigmoid function or logistic function and I will plot this function and show you

### Timestamp: 12:53

 how this looks like right. So, this function would look like the following.

### Timestamp: 12:58

 So, this is going to take a value of 0.5 maybe I will draw this is just these are probability.

### Timestamp: 13:04

 So, they it is never going to take a negative value as you can see right. So, it is e power something

### Timestamp: 13:08

 so, it is always going to be positive and it is 1 divided by 1 plus e power something will

### Timestamp: 13:14

 always be a positive quantity right. So, it will take a value of 0.5 when z is 0. So, this is z

### Timestamp: 13:22

 this is g of z equals 1 by 1 plus e power minus z and here is 1 and let us put a virtual line here.

### Timestamp: 13:36

 Now, if you look at this, so if you plot this function it is going to look like this.

### Timestamp: 13:40

 So, it will get so, this should not touch here right. So, as z goes larger and larger

### Timestamp: 13:52

 it is 0 this is infinity this is minus infinity as z grows larger and larger the sigmoid

### Timestamp: 14:00

 functions probability that it give that z the point is labeled plus 1 goes closer and closer to 1

### Timestamp: 14:06

 and as z becomes to closer and closer to minus infinity the probability becomes closer and closer

### Timestamp: 14:11

 to 0. It is called the sigmoid because this looks like an s and s is stands for some and

### Timestamp: 14:17

 sigmoid the you know the Greek symbol for for some and so, it is called a sigmoid function.

### Timestamp: 14:26

 So, this is a reasonable choice and we will see why this is a reasonable choice later on

### Timestamp: 14:31

 because it makes certain math easier as we will see in a minute.

### Timestamp: 14:36

 But now this is all we are saying right now is that we have a model as to how the data could have

### Timestamp: 14:42

 been labeled. Now, let us ask the question well can I under this model do I allow a dataset like

### Timestamp: 14:50

 this right. So, this is what we were not allowing earlier. This was okay.

### Timestamp: 14:58

 This dataset is still okay even with perceptron but then this dataset was not okay right.

### Timestamp: 15:05

 So, so the moment I put up minus and plus on the opposite side of the 1 fixed w then it is not okay.

### Timestamp: 15:14

 Now is this dataset allowed according to according to the according to this model right. So,

### Timestamp: 15:20

 this model is sometimes called as a sigmoid model or the logistic model. Do we allow this dataset?

### Timestamp: 15:26

 Yes we allow this dataset because now there might be some w right. So, such that you know so these

### Timestamp: 15:35

 points I so for every point in my dataset before deciding the label this is what should have happened

### Timestamp: 15:44

 right. So, for example let us take this point why was this label plus 1 why is this label positive

### Timestamp: 15:50

 because this point falls with respect to this w on this line and this line is just the set of

### Timestamp: 15:56

 all x such that let us say w transpose x is 1 which means that I have actually tossed a coin whose

### Timestamp: 16:02

 probability of coming up heads is 1 by 1 plus e power minus 1 which is 1 by 1 plus 1 over e

### Timestamp: 16:10

 which is e by e plus 1 right. So, this is the chance with which this point gets labeled as plus

### Timestamp: 16:16

 1. So, which means that I have tossed a coin and that coin whose probability whose bias right.

### Timestamp: 16:22

 So, for probability of falling heads is e by e plus 1 and that coin actually fell heads and so

### Timestamp: 16:27

 this point was labeled as plus 1 that is the assumption we have made. Now, why was this point

### Timestamp: 16:31

 labeled minus 1 well now again you do the same process right. So, this point is in the set of all

### Timestamp: 16:38

 x such that w transpose x equal to you know maybe 10. Now, in this case well again there is a

### Timestamp: 16:46

 chance that this guy gets positive label and that chance is in fact greater than the chance that

### Timestamp: 16:51

 this guy gets a positive label in fact that will be 1 by 1 plus e power minus 10 right. So,

### Timestamp: 16:56

 it should be e power 10 by e power 10 plus 1 right. So, now I have tossed a coin with this

### Timestamp: 17:04

 probability and that coin fell tails right. So, and so I have labeled this point as minus 1.

### Timestamp: 17:12

 It is not a zero probability that it will show up as minus 1 right. So, though it is a minuscule

### Timestamp: 17:16

 probability in that if you do an experiment where you are assuming that the labels were generated

### Timestamp: 17:21

 according to this coin tosses where the coins bias depends on how far away from the separator

### Timestamp: 17:26

 this point is in the sense of the score that we have defined earlier. So, then every point could

### Timestamp: 17:32

 get some chance of being plus 1 or minus 1 right. So, now we are assuming that these points

### Timestamp: 17:37

 have been labeled because they fell heads or tails according to their labels right.

### Timestamp: 17:43

 Now, what may task the question well the moment I say that where every point could have been

### Timestamp: 17:49

 plus 1 or minus 1 depending on how far away it is from the separator that w that defines w.

### Timestamp: 17:56

 Now, one can say that well why only this w right. So, I could have had a completely different w maybe

### Timestamp: 18:02

 I am looking at a different w here right. So, now this is w dash this w dash separates like this.

### Timestamp: 18:10

 Now, I can still say right. So, even with this w dash this data set is still possible.

### Timestamp: 18:15

 Why because this data set now the same point here now would have a different line right.

### Timestamp: 18:23

 So, a different score with respect to this new w that I have defined here right. So,

### Timestamp: 18:27

 I mean I should draw the w carefully so that it looks perpendicular, but yeah right. So,

### Timestamp: 18:35

 this for with respect to this w again I get a probability that each point is plus 1 or minus 1.

### Timestamp: 18:40

 So, I would have tossed a coin and I have gotten this labels right. So, so basically then that means that

### Timestamp: 18:49

 you have seen a data set with certain labels. Now, every w has a probability of generating these

### Timestamp: 18:56

 labels right. So, now every w could be is a is a is a contender for being the w that actually

### Timestamp: 19:05

 generated the labels, which means then now our problem becomes as to you know because there are

### Timestamp: 19:13

 every w is a possible w I need to pick 1 w which I think would be the best w for this data set.

### Timestamp: 19:20

 So, now I can post this as a problem where I am trying to find that w which has the highest

### Timestamp: 19:26

 chance of having generated this data, which is simply a maximum likelihood estimation problem

### Timestamp: 19:32

 because for every w there is a probability that it generates the data that I see the labels that I

### Timestamp: 19:37

 see. So, which w has the highest probability of generating this data that is a typical estimation

### Timestamp: 19:42

 problem that we know how to solve right. So, let us let us go ahead and do that.