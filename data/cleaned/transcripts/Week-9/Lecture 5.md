# Week-9 - Lecture 5

### Timestamp: 00:00

 So, what is how do you solve for this w? Well, this model let us go ahead and do the

### Timestamp: 00:23

 write down the model. So, this model is sometimes called as logistic regression. You want to

### Timestamp: 00:32

 be careful why is it with this name though it is it is called logistic regression it is

### Timestamp: 00:37

 still a classification model. The name logistic comes from the fact that of course, we are

### Timestamp: 00:44

 using the logistic function or the sigmoid function. It is called regression because you

### Timestamp: 00:48

 know these probabilities internally depend on a w transpose x s score which is a real number

### Timestamp: 00:52

 and so this is sometimes called as logistic regression. But the real use is that it is

### Timestamp: 00:57

 going to be used for a classification. So, of course, we have this right. So, probability

### Timestamp: 01:04

 of y equals 1 given x is now given by well the generator of the labels has some w which

### Timestamp: 01:12

 we do not know right. So, and with respect to that w the probability that y equals 1 is 1

### Timestamp: 01:17

 by 1 plus e to the minus w transpose x right. So, this this is what we were calling as z before

### Timestamp: 01:23

 but now there is some w such that this is the probability that y equals 1 given an x. Now,

### Timestamp: 01:29

 of course, we have a data set right. So, what we see is this data set which is x 1 y 1 dot

### Timestamp: 01:37

 dot x n y n. Now, question is how to find w right. So, we are we are assuming a model which depends

### Timestamp: 01:49

 on a parameter w we have a data. So, we can estimate w and what is how to find w well

### Timestamp: 01:56

 we know one powerful method to do this which is the method of maximum likelihood.

### Timestamp: 02:01

 So, let us try that right. So, which means if I have to do maximum likelihood by now we should

### Timestamp: 02:09

 know how to do maximum likelihood write down the function which means that I have to write down

### Timestamp: 02:14

 the likelihood function. The likelihood is a function of the parameter that I am trying to

### Timestamp: 02:18

 estimate in this case w and the data. So, what is this going to be we are going to assume that I

### Timestamp: 02:25

 somebody give the features and then the probability is only with respect to the labels and each label

### Timestamp: 02:32

 is generated independently of the other labels that is a usual assumption. So, which means that I

### Timestamp: 02:37

 can write this as a product of i equals 1 to n n data points that is why this is n.

### Timestamp: 02:43

 So, now let us just call this g of w transpose x so that it is easier to write g here.

### Timestamp: 02:52

 So, this is g so for the first data point it it if it is plus 1 it happened with the probability

### Timestamp: 03:05

 g of w transpose x i if it is minus 1 it happened with the probability g of 1 minus g of w transpose

### Timestamp: 03:11

 x i. If you remember the Bernoulli maximum likelihood function that we wrote down the like

### Timestamp: 03:15

 is exactly similar right. So, just that there it was just a p now that p has a functional form which

### Timestamp: 03:20

 is g of w transpose x. So, power y i into 1 minus g of w transpose x i power 1 minus y i.

### Timestamp: 03:30

 So, y i of course in this case we are assuming y i is 0 or 1 right.

### Timestamp: 03:39

 So, of course g has this functional form but before we plug in g's functional form let us take

### Timestamp: 03:44

 the logarithm of this we look at the log of the likelihood of w with respect to the data

### Timestamp: 03:50

 that is going to be sum over i is 1 to n y i log g of w transpose x i plus 1 minus y i

### Timestamp: 04:02

 log 1 minus g of w transpose x i which is simplified as now let me plug in g g is 1 plus 1 by 1

### Timestamp: 04:15

 minus w transpose x i plus 1 minus y i log well 1 minus this this is the probability of 0

### Timestamp: 04:25

 happening which is 1 minus 1 plus e power minus w transpose x i which is just going to be e power

### Timestamp: 04:31

 minus w transpose x i by 1 plus e power minus w transpose x i. Now, you can see that this functional

### Timestamp: 04:37

 form of using this e power things in the probabilities actually is helping because when you do the log

### Timestamp: 04:43

 likelihood the logs in the e sum few of those cancel out right. So, this can be written as i equals

### Timestamp: 04:49

 1 to n the way I am going to write this is so there is a 1 minus y i the log of e power minus

### Timestamp: 04:57

 w transpose x i will become 1 minus y i the log and the e in the numerator will cancel it will be

### Timestamp: 05:03

 minus w transpose x i there is a minus log 1 plus e power minus w transpose x i right. So,

### Timestamp: 05:17

 that comes from this 1 multiplying the log of the denominator so that is this term. So,

### Timestamp: 05:23

 the other term which remains is 1 multiplying the numerator which is which is which is what we

### Timestamp: 05:35

 took as this right. So, 1 minus y i into the numerator was this and 1 multiplying the denominator

### Timestamp: 05:40

 is the second term. So, now y i multiplying the denominator would just be y i log of 1 plus e

### Timestamp: 05:47

 power minus w transpose x i which will cancel the first term out right. So, so two terms get cancelled

### Timestamp: 05:53

 and the remaining is just this right. So, this is what we have now what we want to do then

### Timestamp: 06:00

 is maximize this with respect to w right. So, our goal is now to find an estimate for w is to

### Timestamp: 06:08

 do the following right. So, maximize with respect to w sum over i equals 1 to n 1 minus y i minus

### Timestamp: 06:18

 w transpose x i minus log 1 plus e to the minus w transpose x i which is exactly this I am not

### Timestamp: 06:27

 changed anything here. Now, because there is one of the terms is easy it is a linear in w the

### Timestamp: 06:36

 other term has this log of sum 1 plus e x which if you take the derivative and try to set it to 0

### Timestamp: 06:44

 with respect to w of course, take the gradient with respect to w set it to 0 you will not get

### Timestamp: 06:48

 a closed form expression in a nice closed form expression for this problem right. So,

### Timestamp: 06:53

 so we cannot solve this problem in closed form in an analytical form right. So, no closed form

### Timestamp: 06:59

 expression that is there is no formula for w no closed form expression, but that does not stop us

### Timestamp: 07:06

 from solving this problem because we can always solve this using the method of let us say gradient

### Timestamp: 07:12

 descent right. So, where if you are doing a maximization then it will be gradient ascent

### Timestamp: 07:17

 nevertheless we can do a gradient based algorithm to solve for w which means that you start at some

### Timestamp: 07:23

 point some guess for w and then iteratively improve the guess by moving along the direction

### Timestamp: 07:29

 of the negative gradient if you are doing a minimization and moving along the positive gradient

### Timestamp: 07:34

 if you are doing a maximization with some step size right. So, we know that that is how one one

### Timestamp: 07:39

 typically does gradient descent ok. So, because there is no closed form expression what we are going

### Timestamp: 07:45

 to do is we are going to go ahead and evaluate the gradient for this for this problem and see what

### Timestamp: 07:49

 happens right. So, can perform gradient descent or ascent if it is a maximization problem

### Timestamp: 08:04

 depending on whether we want write it as a max problem or a mean problem we will do gradient

### Timestamp: 08:07

 ascent or descent respectively. So, let us let us it is it is instructive to look at the gradient

### Timestamp: 08:14

 of this problem. So, that will give us some insights. So, let us do that. So, this is log

### Timestamp: 08:21

 likelihood of a w. So, I can look at the gradient of the log likelihood of w and see how that looks

### Timestamp: 08:28

 like well that is going to look like the following right. So, this is sum over i equals 1 to n

### Timestamp: 08:35

 1 minus w i into minus x i that would be the first terms gradient with respect to

### Timestamp: 08:44

 w minus well what is the log log of 1 plus e to the minus w transpose x i is gradient well

### Timestamp: 08:51

 that is going to be 1 by 1 plus e to the minus w transpose x i because log of anything we will get

### Timestamp: 08:56

 a 1 by this thing. And now I will have to take the gradient with respect to e to the minus w transpose

### Timestamp: 09:01

 x i that is the chain rule. So, that would be simply e to the minus w transpose x i and now again

### Timestamp: 09:08

 using the chain rule repeatedly I will have to do it for minus w transpose x i which will give me

### Timestamp: 09:13

 minus x i right. So, this is the gradient with respect to w. So, this is going to be sum over i

### Timestamp: 09:22

 equals 1 to n y i x i right. So, y i x i first I will write the minus x i plus y i x i plus

### Timestamp: 09:41

 this is x i e power minus w transpose x i by 1 plus e power minus w transpose x i right.

### Timestamp: 09:49

 So, this is what we have at this point which can further be written nicely as the following

### Timestamp: 09:56

 i equals 1 to n y i x i minus x i into. So, this this is going to be 1 minus this this term

### Timestamp: 10:09

 because that has x i common. So, if I take 1 minus this term will that is just going to be 1 divided by

### Timestamp: 10:18

 1 plus e power minus w transpose x i right. So, which is finally has a nice form which is just

### Timestamp: 10:26

 sum over i equals 1 to n x i into y i minus 1 by 1 plus e power minus w transpose x i right. So,

### Timestamp: 10:39

 this is the gradient with respect to some w of the original likelihood function and we would

### Timestamp: 10:45

 want to maximize this which means that the gradient ascent update rule would look like this w

### Timestamp: 10:52

 t plus 1 right. So, this is the gradient update rule w t plus 1 will be w t plus eta times the

### Timestamp: 11:06

 gradient of the log likelihood of w right. So, because it is a maximization problem if it was a

### Timestamp: 11:11

 minimization problem then it would be minus eta times the gradient right. So, here you are moving

### Timestamp: 11:15

 along the gradient direction using some step size eta eta t right. So, this is the step size step size

### Timestamp: 11:25

 typically one can use step size that goes down to 0 something like 1 over t right. So,

### Timestamp: 11:32

 would be a reasonable step size or some constant of 4 p that is that that can be a step size but

### Timestamp: 11:38

 what is this whole thing telling us now right. So, this is then w t. So, let me put this way plus

### Timestamp: 11:48

 eta t into the gradient term which we just computed as sum over i is 1 to n x i y i minus

### Timestamp: 11:58

 well what is this. So, this is 1 by 1 plus e power minus w transpose x i. So, this is my gradient

### Timestamp: 12:06

 update term rule. Now, if you look at this there is something interesting happening here right.

### Timestamp: 12:13

 So, this gradient is this is instructive to study this gradient. Now, this y i is just 0 or 1

### Timestamp: 12:22

 it is just a label in your dataset for this point 0 or 1. Now, this term one divided by 1 plus

### Timestamp: 12:30

 e power minus w transpose x i is what is that well that is the probability which is just g of

### Timestamp: 12:38

 w transpose x i right. So, this is just the what we think is the probability that this point is 1.

### Timestamp: 12:45

 Now, what is the gradient then telling us right. So, what is x i? x i is of course,

### Timestamp: 12:51

 the points in d dimension. What is the gradient telling us first thing to notice here is that

### Timestamp: 12:57

 the gradient is actually a linear combination of our data points because we are summing

### Timestamp: 13:02

 up over all data points x i times sum constant right. So, I can this is just a number right.

### Timestamp: 13:07

 So, y i minus 1 by 1 plus e power minus w transpose x i I can treat this as sum theta i right.

### Timestamp: 13:14

 So, this whole thing is summation over i equals 1 to n theta i x i where theta i is some number

### Timestamp: 13:19

 x i is a vector in r d. So, basically what I am doing is a linear combination of my data points.

### Timestamp: 13:25

 Now, that is the first observation. The second observation is that

### Timestamp: 13:30

 now the gradient how does each data point contribute to the gradient depends on how well my current

### Timestamp: 13:37

 guess for w approximates the probability for the label y a right. So, for example, if for a

### Timestamp: 13:44

 given point if the label is actually 1 right. So, let us say I observed a label as 1 and with respect

### Timestamp: 13:50

 to the current w the the probability that this point can be labeled 1 with respect to the current

### Timestamp: 13:57

 w right. So, because we are iteratively doing this at some w at some t at iteration w t right.

### Timestamp: 14:03

 So, in fact, I should put a t here just to be there has to be t here because it is the gradient

### Timestamp: 14:08

 at w t right. So, that is the that is what we are evaluating here. So, at our current w what is

### Timestamp: 14:16

 this telling me this is telling me what is the chance that this point will be labeled plus 1.

### Timestamp: 14:21

 If the chance is high and the point is actually labeled 1 then this difference is actually theta i

### Timestamp: 14:28

 corresponding to that point is going to be a small number right. So, it is going to be 1 minus

### Timestamp: 14:32

 let us say this chance was 0.99. So, that value is going to be 0.01 which means that that point

### Timestamp: 14:36

 is not going to really affect my gradient. Now, on the other hand if the label was 1 but then my

### Timestamp: 14:43

 chance that it is being labeled as 1 by the current w t is 0.1 right. So, which means that you

### Timestamp: 14:50

 know you are more likely thinking that with the respect to the current w this point should actually be

### Timestamp: 14:56

 negative label minus 1 with 90 percent chance only 10 percent chance you give it for plus 1.

### Timestamp: 15:01

 So, now that is a mismatch between the label and your current guess right. So, which means that the

### Timestamp: 15:05

 next w that you get will will be influenced more by the points where you are making mistakes right.

### Timestamp: 15:13

 So, because that is what is happening because that y i minus g of w t x i will be high when that is

### Timestamp: 15:20

 a mismatch and y i minus g of w t x i will be low when there is no mismatch which means w t

### Timestamp: 15:26

 correctly class wise my correct point current point right. It is of course, never going to be 0

### Timestamp: 15:30

 because this probabilities will never be 0 or 1 exactly, but then that does not matter right.

### Timestamp: 15:35

 So, as long as it is too small then that point does not matter to the next w. So, that you will kind

### Timestamp: 15:39

 of move in the direction. So, that you are concentrating more on points where the current w is

### Timestamp: 15:44

 making a mistake right. So, that is the gradient intuitive update rule for this gradient descent

### Timestamp: 15:52

 gradient descent in this case and this algorithm as we said is called as the logistic regression

### Timestamp: 15:56

 algorithm which is a very popular simple algorithm, but then a very popular algorithm because

### Timestamp: 16:01

 you can run it easily. Of course, there are other you know second order methods we just use a

### Timestamp: 16:07

 gradient descent or an ascent to solve this problem. There are more sophisticated methods also

### Timestamp: 16:12

 that you can use to solve this problem. Now, one of the methods again is using the IRLS technique

### Timestamp: 16:17

 which is an iterative re re re weighted least squares method where you kind of solve a

### Timestamp: 16:24

 successively a least squares problem to get to the original w. We are not going to see that,

### Timestamp: 16:29

 but just I mean be aware that there are more faster methods to solve this than the you know

### Timestamp: 16:35

 vanilla gradient descent or ascent type of methods. But for our purposes you know here is a nice

### Timestamp: 16:42

 model which will allow any dataset and you can get a w. So, what you do after you get the w well,

### Timestamp: 16:48

 you will use the w and do the prediction as sign of w transpose x i. So, for x test if I get

### Timestamp: 16:54

 an x test which is in R d now w hat is the solution that I that the gradient descent converges to,

### Timestamp: 17:01

 then I will just do w transpose x test and then I will predict the sign of this. So, this would be

### Timestamp: 17:07

 my y y y hat test as usual right. So, I will just predict reducing this, but now because this

### Timestamp: 17:15

 algorithm has probabilities implicitly embedded in it, you not only get a prediction, you also get

### Timestamp: 17:21

 a probability which can be thought of as a confidence with which you are actually making this

### Timestamp: 17:24

 prediction. That is one of the major advantage of this model because the probabilities are

### Timestamp: 17:29

 inbuilt in this model. So, the predictions can be made with certain confidence and so on right.

### Timestamp: 17:33

 So, this is this is the first thing that I wanted to say a couple of more points which I wanted to

### Timestamp: 17:40

 mention about this algorithm is that there is a kernel version for this algorithm that one can

### Timestamp: 17:44

 derive you know this again can argue that your w the optimal w should be a linear combination of

### Timestamp: 17:56

 your data points. And so, because of this fact now you can derive a kernel version for this

### Timestamp: 18:04

 problem right. So, if you substitute this form into the objective then you will you can write

### Timestamp: 18:09

 this in terms of x transpose x and and so that can be kernelized right. So, we will not do that,

### Timestamp: 18:15

 but it is good to be aware that you know this can be used to derive a kernel version of this algorithm.

### Timestamp: 18:22

 The fact that w has to be in this form you know the formal again this is just for your understanding

### Timestamp: 18:30

 for your knowledge. We are not going to well deep into this also, but then the formal theorem

### Timestamp: 18:36

 here is called that that guarantees that w will be in a as a linear combination of your

### Timestamp: 18:42

 data points w meaning w star right. So, that solves the logistic regression problem has to be

### Timestamp: 18:46

 of this form this is called as the represent of theorem right. So, for those who are curious you

### Timestamp: 18:52

 can look up represent of theorem right. So, now we can derive a kernel version for logistic

### Timestamp: 19:01

 regression which is another good thing. In practice what people also do is kind of look at

### Timestamp: 19:08

 like a Bayesian version of this which is a regularized version of logistic regression,

### Timestamp: 19:14

 regularized version which is also very popular in practice where you would do you know

### Timestamp: 19:21

 minimize over w. Now, you will write this as a minimization problem, some over i equals 1 to

### Timestamp: 19:26

 n now the maximization objective here will now get converted into a minimization objective which

### Timestamp: 19:33

 will become log of you know log of 1 plus e power minus w transpose x i which was the first term

### Timestamp: 19:47

 plus w transpose x i into 1 minus y.

### Timestamp: 19:57

 So, you can do this plus you do a regularization using our usual L2 norm regularization right.

### Timestamp: 20:06

 So, this is the regularization of course, you do not you can use a cross validation parameter

### Timestamp: 20:14

 that we have discussed earlier to right. So, to cross validate right. So, this is cross validation

### Timestamp: 20:21

 parameter hyper parameter. It is not hard to derive the gradient rule for this as well.

### Timestamp: 20:33

 It is it is very simple because it is the previous gradient plus just lambda times w right.

### Timestamp: 20:39

 So, it is you can still perform gradient descent very efficiently for this this regularized version

### Timestamp: 20:44

 as well ok. So, with this I want to summarize this new algorithm that we have seen which is the

### Timestamp: 20:51

 method of logistic regression which is the very popular algorithm in practice.

### Timestamp: 20:56

 One of the things that it does well with respect as against Perceptron is that you know this will

### Timestamp: 21:01

 allow this can model any dataset right. So, no matter if the dataset has you know outliers or not

### Timestamp: 21:09

 of course, if if the dataset has more structure more than linear then you can look at a

### Timestamp: 21:15

 kernelized version of this algorithm as well. So, in practice of course, Perceptron has the

### Timestamp: 21:23

 disadvantage that it works only for linearly separable dataset this algorithm does not.

### Timestamp: 21:27

 It will converge to reasonably very good w that you can then use for testing for new data points.

### Timestamp: 21:34

 But it does not try to I mean it has its own way to find out a w right. So, which maximizes

### Timestamp: 21:42

 the likelihood of observing the data under a certain model that we put out. But as I said earlier

### Timestamp: 21:49

 Perceptron gave us some mistake bound and that mistake bound merits a longer discussion because

### Timestamp: 21:57

 you know we can look at that mistake bound and then derive a more direct algorithm which depends on

### Timestamp: 22:06

 certain aspects that the mistake bound should tell us specifically about the margin right.

### Timestamp: 22:10

 So, the next time we see right. So, what we are going to see is that we have logistic regression

### Timestamp: 22:14

 which is a powerful algorithm on one side we will develop another algorithm which is a very

### Timestamp: 22:18

 very elegant algorithm which also is very powerful and works really well in practice especially

### Timestamp: 22:25

 for structured data and this algorithm is called as a support vector machine algorithm and that

### Timestamp: 22:30

 will derive inspiration from Perceptron's mistake bound to develop that algorithm that we will see

### Timestamp: 22:37

 starting next time. So, this time we will finish with logistic regression and I hope to see you

### Timestamp: 22:44

 again soon. Thank you.