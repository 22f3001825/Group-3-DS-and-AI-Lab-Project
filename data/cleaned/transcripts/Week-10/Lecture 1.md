# Week-10 - Lecture 1

### Timestamp: 00:00

 Hello and welcome back. So, far we have looked at several supervised learning algorithms,

### Timestamp: 00:18

 including Perceptron and the Logistic Regression Algorithm. And now what we are going to do today

### Timestamp: 00:24

 is Revisit Perceptron and see some of the properties of Perceptron that we spoke about

### Timestamp: 00:29

 earlier and see how that leads to a more principled and elegant formulation for coming up with

### Timestamp: 00:36

 a new supervised learning algorithm. So, let us start by recalling that for the Perceptron

### Timestamp: 00:42

 algorithm, the number of mistakes that Perceptron makes are dependent on quantity which we called

### Timestamp: 00:50

 as the radius margin bounds which was as follows. The number of mistakes was at most r squared

### Timestamp: 00:58

 by gamma squared where r squared r is just the radius of the data points. So, where what was r

### Timestamp: 01:06

 squared? Well, if you had a data set such that all of norm of x i squared is less than or equal to r

### Timestamp: 01:11

 squared, then it is basically saying that there is a big ball of radius r and all the data points

### Timestamp: 01:17

 are within this ball. More importantly gamma is the assumption that we made about the

### Timestamp: 01:23

 data set that the data set is linearly separable L s with margin gamma. What does that mean?

### Timestamp: 01:35

 That means that for there exists some w, right. So, whatever we call it as w star such that w

### Timestamp: 01:41

 star transpose x i into y i was greater than or equal to gamma for all the data points i,

### Timestamp: 01:49

 where gamma is some value greater than 0. In pictures, this meant the following, right. So,

### Timestamp: 01:54

 that if you had a data set like this, well you if you had a w star like this, then it means

### Timestamp: 02:02

 that well maybe this is some line such that the set of all x such that w star transpose x equals

### Timestamp: 02:12

 gamma and this is the line such that the set of all x such that w star transpose x equal

### Timestamp: 02:17

 to minus gamma, then what we are saying is that all the positive points are lying either on the

### Timestamp: 02:24

 line or on to the right of this line and all the negative points are lying either on the line

### Timestamp: 02:30

 or to the left of this line, right. So, this condition that w star transpose x i y i is greater

### Timestamp: 02:36

 than or equal to gamma just means that you know there is this separation between the positive

### Timestamp: 02:42

 class and the negative class, I mean which is and which is given by this non-zero gamma.

### Timestamp: 02:47

 And that was crucial because we also saw an example where if the separation was not there,

### Timestamp: 02:52

 then perceptron may not converge. Now, if the separation is there, we proved that perceptron

### Timestamp: 02:56

 indeed converges and it converges with a finite number of mistakes. Of course, finite number of

### Timestamp: 03:02

 mistakes implies convergence and we have bound on the number of mistakes perceptron makes which is

### Timestamp: 03:07

 r square by gamma square. Now, there are couple of important points that we need to talk about here

### Timestamp: 03:15

 with respect to you know what does this mean that you converge with number of mistakes at most

### Timestamp: 03:21

 r square by gamma square, right. So, the first point that I would like to talk about is the following,

### Timestamp: 03:27

 right. So, quality of final solution, quality within codes, what do I mean by this?

### Timestamp: 03:43

 Well, let us take an example to illustrate this point. Let us say we had positive points which

### Timestamp: 03:50

 were all let us say here something like this and negative points were all let us say here

### Timestamp: 04:12

 something like this, right. So, let us say this was our data set. Now, maybe I will add a few more

### Timestamp: 04:19

 points here just to illustrate this better. Let us say this was our data set. Now,

### Timestamp: 04:28

 now this is a linearly separable data set with some gamma margin. Now, let us take

### Timestamp: 04:34

 a w which is pointing in this direction, right. So, let us call this w star. Now, this w star

### Timestamp: 04:43

 implies that the line that separates the positive from the negatives is going to be this line.

### Timestamp: 04:49

 So, it does separate the positive from the negatives, right. So, the data set is linearly separable.

### Timestamp: 04:58

 Not only that it is in fact linearly separable with some gamma margin.

### Timestamp: 05:02

 And that gamma margin is comes from the fact that you know you have this line which is parallel to

### Timestamp: 05:08

 this w star on one side and this line which is parallel to the w star on other line, other side.

### Timestamp: 05:14

 So, this is just a set of all x such that w star transpose x equals let us say some gamma and

### Timestamp: 05:20

 this is the set of all x such that w star transpose x equals minus gamma. Let us say this is our

### Timestamp: 05:25

 data set. So, this data set is linearly separable with gamma margin. Now, it is not necessary that

### Timestamp: 05:33

 this is the only w star that separates this data set with some margin. Well, for example,

### Timestamp: 05:41

 I am going to show you another w star another direction which also separates this data set with some

### Timestamp: 05:45

 margin. Now, can you already think of a w w w w 2 star w star 2 right. So, different direction

### Timestamp: 05:53

 which also separates this data set with some other margin. Pause and think about this I will tell

### Timestamp: 05:59

 you one example. So, here is one example right. So, just look at the direction which is the x axis

### Timestamp: 06:06

 direction let us call this w star 2 right. So, this is another w star which also separates our

### Timestamp: 06:13

 data set because you know this would be in fact, the y axis would now be the separating line

### Timestamp: 06:19

 and all the green points are on one side of the y axis and all the red points are on the other

### Timestamp: 06:23

 side of the y axis. So, that the x axis direction is also a valid direction it also separates our

### Timestamp: 06:29

 data set with some margin. Now, one can ask the same question what would be the margin for this

### Timestamp: 06:36

 particular w star 2 right. So, now if you look at it you know it is going to be like this right.

### Timestamp: 06:42

 So, this would be the margin for w star 2 here it would be for this right. So, this would be the

### Timestamp: 06:56

 margin for w star 2 sorry about that yeah w star 2 right. So, basically what has happened is that

### Timestamp: 07:06

 you know you have two different w stars right. So, one with you know separation given by the blue

### Timestamp: 07:15

 shaded blue region because the first red point is here with respect to the blue you know with

### Timestamp: 07:25

 respect to the blue separators right. So, that is the margin that is the amount that w 2 star has

### Timestamp: 07:30

 whereas, if you look at w 1 star it it separates sorry actually it is a different color it separates the

### Timestamp: 07:38

 same data set with a larger margin right. So, now one might ask the question among these two

### Timestamp: 07:51

 w's w's w star and w 2 star which one would you prefer if you were given this data set a priori.

### Timestamp: 07:57

 Well somehow intuitively it feels that w star is a better separator for this data set than

### Timestamp: 08:05

 w star 2 because it separates the data set that direction separates the data set with a larger

### Timestamp: 08:10

 you know so to say margin right. Now, let us go back and ask what is the mistake bound of

### Timestamp: 08:18

 perceptron telling us in this regard. It is telling us that the number of mistakes is at most

### Timestamp: 08:24

 r square by gamma square. Well now when I when we argued this gamma square right. So, we just

### Timestamp: 08:32

 assumed that there is some w star which separates the data with some gamma. We did not say anything

### Timestamp: 08:38

 else about this w star right. So, we just assumed that there is some w star which means that in this

### Timestamp: 08:43

 data set yes there are two different w star with two different gamma 1 and gamma 2 perhaps.

### Timestamp: 08:50

 But you know because we do not make any other assumptions about the true w star well the number

### Timestamp: 08:55

 of mistakes will depend upon the best possible w star's margin right. So, which means that

### Timestamp: 09:03

 then the observation is the following right. So, the number of mistakes

### Timestamp: 09:10

 mistakes depends on the best possible w star's margin.

### Timestamp: 09:26

 Remember for the perceptron algorithm we assume that w star had norm 1 right. So, here both these

### Timestamp: 09:32

 w star and w 2 star are on the unit circle we can make that assumption. But then one has a

### Timestamp: 09:38

 smaller margin let us say this gamma gamma was just maybe this gamma was 10 whereas, this gamma

### Timestamp: 09:44

 was just 1. Now, what we are saying is that well though w 2 star classifies it with only margin 1

### Timestamp: 09:52

 the number of mistakes is going to depend on the one that has the largest margin right.

### Timestamp: 09:58

 Because we did not make any assumptions about the specific w star it could be any w star here is a

### Timestamp: 10:03

 w star with the large margin gamma equals 10 and so, the number of mistakes are going to be

### Timestamp: 10:08

 bounded by r square by 10 squared in this case right. So, which means that if you are if there is

### Timestamp: 10:15

 some w star which separates your data set with a large margin then the number of mistakes that

### Timestamp: 10:22

 perceptron is going to make is going to depend on this large margin large number and it is going

### Timestamp: 10:27

 to be inversely proportional which means that larger gamma squared is smaller is going to be the

### Timestamp: 10:33

 number of mistakes right. So, because this is an upper bound right so, which means that it has

### Timestamp: 10:39

 to hold for any w star with with with its corresponding margin and we want to and and and so,

### Timestamp: 10:45

 this the w star with the largest margin which will have will imply the tightest upper bound right.

### Timestamp: 10:52

 So, what we are essentially saying is that the number of mistakes of perceptron depends on the

### Timestamp: 10:58

 best possible w star's margin right. So, in this case it is going to depend on the orange line.

### Timestamp: 11:03

 This is observation 1. Observation 2 though is very important in the sense that

### Timestamp: 11:11

 though the number of mistakes is going to depend on the w star which has the largest separation

### Timestamp: 11:17

 margin the w that perceptron is going to output at the end need not necessarily be that w star

### Timestamp: 11:27

 which separates the data with the largest margin right. So, why is that because there is nothing

### Timestamp: 11:34

 in the algorithm that is really driving it towards finding a w star or w that the perceptron

### Timestamp: 11:40

 outputs right. So, let us call that you know w perceptron P or C right. So, this is what perceptron

### Timestamp: 11:47

 outputs now this w perceptron need not necessarily be w star which has the largest margin.

### Timestamp: 11:56

 Why because you know perceptron has nothing inbuilt in the algorithm in the update rule that

### Timestamp: 12:01

 says that you want to find a w where the margin is as high as possible.

### Timestamp: 12:06

 What we just argued is that well the update rule that perceptron uses is enough to argue that

### Timestamp: 12:12

 if there is some w star with a large margin then the number of mistakes that perceptron will

### Timestamp: 12:18

 make is small. However, the output w perceptron that perceptron finally gives you need not necessarily

### Timestamp: 12:25

 be in this case the orange line it could be the blue line also right. So, w perceptron need not

### Timestamp: 12:31

 necessarily be w star it could be w star 2 also the blue line right. So, why because the

### Timestamp: 12:51

 moment perceptron finds w star 2 right. So, as a trans algorithm it is immediately going to see

### Timestamp: 12:58

 that hey for w star 2 it is not no longer making any mistakes with respect to the data set it is

### Timestamp: 13:02

 just going to stop the algorithm there and say that it is converged right. Now, then is that

### Timestamp: 13:11

 a contradiction it is not right. So, why is it not a contradiction because what we are essentially

### Timestamp: 13:16

 saying is that the if there is a w star with a large margin then it means that the problem is

### Timestamp: 13:23

 inherently simpler because the class of plus 1 and minus 1 are separated well separated and so

### Timestamp: 13:29

 perceptron makes fewer mistakes to figure out some line that separates the plus from the minus 1.

### Timestamp: 13:36

 It does not mean just because the problem is simpler perceptron is going to find that

### Timestamp: 13:41

 separator which separates it with the largest margin no that is not necessarily 2 because there

### Timestamp: 13:46

 is nowhere in the algorithm where we have specifically said that you want to find a w that

### Timestamp: 13:51

 separates the data with the largest margin right. So, this is this is these are two important

### Timestamp: 13:58

 points that we want to make about perceptron. Now, what is this kind of telling us is that though

### Timestamp: 14:04

 intuitively it feels that we want to find a separator which kind of separates our positive

### Timestamp: 14:10

 from negatives with as much width as possible your perceptron may not necessarily find it.

### Timestamp: 14:16

 Though perceptron is a super simple update rule it does not have the power to find a w star that

### Timestamp: 14:23

 separates the data with the largest margin. So, then we ask the question well here is the question

### Timestamp: 14:29

 that we are going to ask now now given that we prefer separators with large margin right.

### Timestamp: 14:42

 So, classifiers or separators with large margin you know can we directly find them.

### Timestamp: 15:03

 So, what we want to really do now is that well we want to let go of perceptron and then

### Timestamp: 15:08

 directly focus on the problem that well given a data set where there which is linearly separable

### Timestamp: 15:14

 can we directly find the w star which separates this data set with as large a margin as possible right.

### Timestamp: 15:20

 So, maybe that is the question that we would directly want to ask instead of saying that we will

### Timestamp: 15:25

 find some separator let us find a separator which is actually good. Now, intuitively we understand

### Timestamp: 15:30

 that this is important this seems like the orange line is a better line than the

### Timestamp: 15:36

 than the blue line. But so when I say orange line I mean this separator of course right.

### Timestamp: 15:44

 Yeah so this has a larger margin. Now, why is that true right. So, why would we want to

### Timestamp: 15:51

 prefer the orange than the blue separator well one way to think about this is the following right.

### Timestamp: 15:58

 So, now again for this data set the blue line has a very thin margin whereas, the orange one has

### Timestamp: 16:05

 a large margin, broader margin. Now, what is the implication of that well the implication of that

### Timestamp: 16:12

 is that you know if you kind of perturb your data set a little bit right. So, maybe add some

### Timestamp: 16:20

 noise to this data set right. So, which means that you know imagine that there is some noisy

### Timestamp: 16:26

 version of this data set that you might see in the test data. Now, if you have a broader margin

### Timestamp: 16:32

 then you are going to be tolerant to this noisy version of the train data because even if you add

### Timestamp: 16:39

 noise you are still going to be in the on the right side of the of the separator. So, what do I

### Timestamp: 16:44

 mean by this right. So, let us take an example maybe there was a point which was you know somewhere

### Timestamp: 16:49

 here and now I add some noise that this point moves here right. So, this negative point after

### Timestamp: 16:57

 adding noise move to this point the new point that I have circled in red. Now, if this was my

### Timestamp: 17:05

 test point now the blue separator would say that well how am I going to make a prediction I am

### Timestamp: 17:11

 going to make a prediction either going to use using this line or using this line depending

### Timestamp: 17:15

 on which W I use. Now, if I use the blue line then the circled red point is going to be predicted

### Timestamp: 17:20

 as you know positive because it is on the right side of the blue line whereas, it is still on

### Timestamp: 17:25

 the left side of the orange line of the orange of this line right. So, in other words even if

### Timestamp: 17:30

 the test is a noisy version of the train right. So, you still have some leeway which this margin

### Timestamp: 17:37

 provides you which takes care of you know the generalization ability of our algorithm loosely speaking

### Timestamp: 17:45

 right. So, in some sense the larger the width that or the margin that we can ensure for our W

### Timestamp: 17:52

 you know the more robust that line is right. So, it is I mean if you have points close to the margin

### Timestamp: 17:57

 then close to the separator right. So, then small change might not affect the label so much right.

### Timestamp: 18:04

 So, that is the goal that is the reason why we prefer lines with a larger width.

### Timestamp: 18:09

 But how can we formalize this right. So, this is the informal way to write this question that

### Timestamp: 18:13

 given that we prefer classifiers with large margin can be directly find them. So, what we are going

### Timestamp: 18:18

 to do today is to you know our goal is to come up with a principled way to find you know a W

### Timestamp: 18:26

 which classifies our data points with as large a margin as possible right. So, let us let us start

### Timestamp: 18:31

 with that goal right. So, this is going to be our goal number.