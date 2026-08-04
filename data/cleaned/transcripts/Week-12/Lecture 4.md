# Week-12 - Lecture 4

### Timestamp: 00:00

 Hello everyone, welcome back. So, last time we looked at how various algorithms for supervised

### Timestamp: 00:20

 learning specifically binary classification can be viewed using the same lens of loss

### Timestamp: 00:26

 function plus regularization minimization. So, for instance we said that you know you can

### Timestamp: 00:32

 minimize with respect to some let us say parameter of interest may be w some loss function

### Timestamp: 00:39

 of how w transpose x predicts with respect to y plus some regularizer with respect to

### Timestamp: 00:46

 y. So, this is the regularizer and this is the loss with respect to at single data point

### Timestamp: 00:55

 but then we would sum up over all different data points because it is the same loss that

### Timestamp: 01:00

 applies to all different data points right. So, this is the loss. So, the first part depends

### Timestamp: 01:06

 on the data and the second part depends on the model and the regularizer is somehow trying

### Timestamp: 01:12

 to give us a model which has certain desirable properties for instance if you do half norm

### Timestamp: 01:18

 w squared as the regularizer then that means that we are desiring w's which have as many

### Timestamp: 01:24

 zeros or close to zero values as possible and so on and so forth. When we looked at loss of course,

### Timestamp: 01:31

 we wanted to minimize the zero one loss but then we argued that that is a NP hard problem it's a

### Timestamp: 01:36

 very hard problem in general for a general binary classification data set. So, we kind of you know

### Timestamp: 01:44

 we circumvented this idea by problem by saying that we will use some convex surrogates for the

### Timestamp: 01:52

 zero one loss and depending on which convex function we use as a surrogate loss for the zero one

### Timestamp: 01:57

 loss we would end up with different learning algorithms. For example, if the surrogate was a hinge

### Timestamp: 02:03

 loss we ended up with support vector machines if the surrogate was a logistic loss we ended up with

### Timestamp: 02:08

 logistic regression and so on and so forth. We also saw that the perceptron algorithm and even the

### Timestamp: 02:14

 boosting algorithm can be you know put in this framework for suitable losses perceptron uses the

### Timestamp: 02:19

 hinge loss of course, with certain specific type of hinge losses with certain you know parameter

### Timestamp: 02:27

 for the step size specific parameter for the step size and we did not do it in detail but then

### Timestamp: 02:33

 I said that even boosting can be viewed in the framework where the loss that we care about is what

### Timestamp: 02:38

 is called as the exponential loss. What we are going to do today is move away from this notion of

### Timestamp: 02:45

 convex optimization problems and one of the reasons why we did this convex optimization because

### Timestamp: 02:51

 you know convex optimization problems end up with unique global minima right. So, if you choose

### Timestamp: 02:58

 the regularizer carefully and the loss carefully then the w that you end up with is unique

### Timestamp: 03:05

 and that is a good property to have which means that our optimization algorithms will get us in

### Timestamp: 03:10

 fact the optimum of these problems. What we are going to see today is a slightly different way of

### Timestamp: 03:18

 coming up with an algorithm which not necessarily uses a convex loss function and this set of

### Timestamp: 03:26

 algorithms this class of algorithms that we are going to look at today are called as

### Timestamp: 03:30

 Neural Networks which are the second class of algorithms that are inspired by the basic perceptron

### Timestamp: 03:42

 algorithm. So, we are not going to do neural networks in too much detail in this course the reason

### Timestamp: 03:48

 I am not doing it in too much detail is because so, if you if you take a deep learning course which

### Timestamp: 03:56

 is typically taken after this introduction to machine learning kind of machine learning techniques

### Timestamp: 04:00

 course there you there you would start with neural networks right. So, because the whole of deep

### Timestamp: 04:05

 learning are different variants of the neural network idea. So, it will be covered in detail there

### Timestamp: 04:11

 because this is also a classical machine learning algorithm what I just wanted to do is to just

### Timestamp: 04:17

 introduce you to this algorithm and say that how it differs from the algorithms that we have seen

### Timestamp: 04:24

 and kind of leave it at that. So, what are neural networks? So, the way to understand neural

### Timestamp: 04:32

 networks is first to go back and understand what perceptron does which we have already seen before.

### Timestamp: 04:39

 So, you can view perceptron as follows right. So, you have some x which is a d dimensional vector

### Timestamp: 04:47

 and thus the the prediction that perceptron does for x is by maintaining a w and then you would

### Timestamp: 04:54

 just do sign of w transpose x as the prediction. Now, the same thing can be viewed pictorially

### Timestamp: 05:02

 as follows right. So, you have x which let us say in d dimension has variables x1 to x t remember x

### Timestamp: 05:10

 itself is x1 x2 till x t. So, that is what we mean by x1 x t. So, now these are you can think as

### Timestamp: 05:21

 if these are given as input right. So, that is the input the feature is the input and then we want

### Timestamp: 05:29

 to make a prediction for this. These could be features this this could be binary features real

### Timestamp: 05:34

 valued features does not really matter. So, these are features for us which are given to us.

### Timestamp: 05:38

 Now, what we do in perceptron is there is a w and we compute w transpose x which can be thought of

### Timestamp: 05:46

 as follows you know you have these edges and over this on sitting on top of these edges are these

### Timestamp: 05:54

 weights which let us call this w1 w2 till wd and now out comes w transpose x right. So, w transpose x

### Timestamp: 06:12

 now of course, then you look at the sign of this and and that is the prediction. So, one might ask

### Timestamp: 06:18

 what have we really gained by you know viewing this in this format. So, now what neural networks are

### Timestamp: 06:27

 are can be visually represented very easily as an extension of the simple idea of what perceptron

### Timestamp: 06:35

 is doing. So, the way we will think of this is as follows. So, in neural networks again you have

### Timestamp: 06:41

 you know something like this. So, you have an input which is x1 to x d. Now, you can think of this

### Timestamp: 06:47

 as you know some neuron that is why it is called neural network it is kind of trying to

### Timestamp: 06:55

 at least in at a very broad level trying to mimic what the neurons in the brain kind of mimic

### Timestamp: 07:04

 kind of try to do. Basically the neurons get activated if the signal is you know strong enough

### Timestamp: 07:11

 something like that is what we are trying to do here as well. So, basically you have x1 x2

### Timestamp: 07:17

 and then all of this is given as input to this neuron. Now, in the neural network case of course,

### Timestamp: 07:27

 there are weights associated with these edges right. So, the edges have directions. So,

### Timestamp: 07:38

 that is it always goes from left to right in this case. But in neural network we are not just

### Timestamp: 07:45

 learning a single w right. So, in perceptron of course, the goal is to learn this w that best you know

### Timestamp: 07:52

 best explains our wise. Now, here in neural network it is not a single w that we will learn. So,

### Timestamp: 07:59

 you will have multiple w's and each of these w's is represented using what is called as a hidden

### Timestamp: 08:07

 layer which has a bunch of what are called as neurons whenever I put a circle it is called a neuron

### Timestamp: 08:14

 and now you can think of as if you are providing the same input to all these hidden layers neurons

### Timestamp: 08:24

 right. So, it is the same input that goes into this hidden layers. But then the weights in these

### Timestamp: 08:29

 hidden layers could be different right. So, let us call this let me put a one here to indicate that

### Timestamp: 08:37

 though every weight that goes into the first hidden layer neuron is indicated using this one here

### Timestamp: 08:45

 everybody that goes to the second hidden layer neuron is indicated by the two here right. So,

### Timestamp: 08:50

 you have D of those and then you have let us say K hidden layers hidden layer neurons

### Timestamp: 08:58

 and you have you know D inputs to this neuron. Now, we will see why this might be a useful thing in

### Timestamp: 09:06

 a minute, but let me finish this argument. So, now what happens here is after so, what is the hidden

### Timestamp: 09:14

 layer essentially computing is it is computing the w transpose x corresponding to the

### Timestamp: 09:23

 the weights on the input that this layer receives right. So, for example, this guy would first compute

### Timestamp: 09:31

 w 1 transpose x right. So, it would compute that. So, that is a linear function of our input.

### Timestamp: 09:39

 Now, in addition to this in neural networks you can also what also happens is you know there is

### Timestamp: 09:46

 something called as an activation function which is which is a non-linear function applied to

### Timestamp: 09:52

 this w transpose x and we will talk about this activation function in a minute and what it means

### Timestamp: 09:57

 in a second. So, what it outputs is it takes a real number and then it outputs typically a number

### Timestamp: 10:05

 between 0 and 1 or it can also output a number real number depending on what kind of activation

### Timestamp: 10:10

 functions that we want in our neural networks. So, now what happens is so, each of these hidden layer

### Timestamp: 10:18

 neurons is going to output an activation value right. So, you get something like this from each of

### Timestamp: 10:25

 these it is the same activation typically. So, this would be w 2 transpose x and last one would be

### Timestamp: 10:35

 activation of w k transpose x if you have 1 2 till k neurons in the hidden layer.

### Timestamp: 10:46

 Now, what happens finally is you know you have a layer I mean it is the simplest representation

### Timestamp: 10:52

 of a neural network you have a final layer which is called as an output layer.

### Timestamp: 10:59

 The first layer is the input layer and in this simplified neural network you have one single

### Timestamp: 11:05

 hidden layer and then the hidden layer you know gives out activations of based on what weights

### Timestamp: 11:11

 that it takes as input and now the output layer also has weights associated right. So, let us call

### Timestamp: 11:19

 this w output 1 w output k right. So, this is the output layers weight and now what you might get

### Timestamp: 11:33

 as output is w out transpose this a of w 1 transpose x dot dot dot a of w d this k is w k right.

### Timestamp: 11:47

 So, because there are k layers here w k transpose x. Now, this is the real number.

### Timestamp: 11:55

 Now, let us say we are trying to solve a superwise learning problem I mean you can solve any super

### Timestamp: 12:01

 wise learning problem using neural networks. Let us say for simplicity for the moment let us say

### Timestamp: 12:05

 we are trying to solve a regression problem. Now, if regression problem the output is a is a real

### Timestamp: 12:12

 number and that real number is can be thought of as this number. Now, what does this mean right.

### Timestamp: 12:19

 So, what are we what are we trying to do here? We are trying to say here that for a given input x

### Timestamp: 12:28

 the algorithm is going to predict in the case of regression a real number and that real number

### Timestamp: 12:34

 is obtained by you know taking a pass in this neural network from left to right. So, how does

### Timestamp: 12:41

 that work? So, basically you give an input x to the neural network right. So, there are these w's

### Timestamp: 12:46

 which are part of the specification of the neural network the moment I fix some w's and neural

### Timestamp: 12:51

 network is specified. So, you have w 1 till w k and you do w 1 transpose x w 2 transpose x

### Timestamp: 12:58

 till w k transpose x and then there is this activation function which kind of takes w k

### Timestamp: 13:05

 w k transpose x and then maps it to some other real number. And all these real numbers are kind of

### Timestamp: 13:10

 again you know linearly combined using the vector w out which is again the specification of the

### Timestamp: 13:15

 neural network to output a value. So, the neural network in this simplified case the parameters of

### Timestamp: 13:21

 the neural network what would be the parameters the parameters which you know specify this neural

### Timestamp: 13:30

 network completely are the following right. So, w 1 till w k right. So, these are the first layer

### Timestamp: 13:40

 parameters where each w i is in r t because they they they you do a dot product with the input

### Timestamp: 13:46

 vector and then you have w out which is in r k where you take the dot product with the outputs

### Timestamp: 13:57

 of the hidden layer right. So, that so, once I specify w 1 till w k and w out then my neural

### Timestamp: 14:07

 network is completely specified at least in this simplified neural network is completely specified.

### Timestamp: 14:11

 I am kind of telling you how the regression problems output is generated as a function of these

### Timestamp: 14:17

 things how would that be well that would be your y hat for a given x would be w sum over i equals

### Timestamp: 14:27

 1 to k w out of i into a of w i transpose x right. So, so, this would be my of

### Timestamp: 14:47

 basically right I am going to do this correctly that is correct a of w i transpose x is.

### Timestamp: 14:56

 So, this would be my y hat right. So, now basically what we have specified in the neural network is

### Timestamp: 15:03

 so, this is part of the neural network specification these are part of the neural network specification

### Timestamp: 15:08

 of course, the activation functions activation functions how also have to be decided a

### Timestamp: 15:15

 priority once mean in the part of the specification of the neural network how many hidden layers number

### Timestamp: 15:22

 of hidden layer nodes have to be specified as part of the neural network specification.

### Timestamp: 15:28

 Once all of this is specified then basically what you have is a map from r d to r which is y r

### Timestamp: 15:36

 these you know w 1 to w k and w out. So, now so, what is the intuition here well the intuition is

### Timestamp: 15:46

 as can be thought of as follows. Now, in perceptron or in simplified linear models we assume that

### Timestamp: 15:54

 the output can be explained as a linear function of the input right. So, that is why you have a w

### Timestamp: 15:59

 and then you take w transpose x and that is a good enough explanation as if in good enough

### Timestamp: 16:06

 explanation for the y right. So, given x here we are assuming that a linear model is too simplistic

### Timestamp: 16:13

 it perhaps will not be able to explain y given x we need a non-linear model in the SVMs and other

### Timestamp: 16:19

 ways the way to we dealt with non-linearity even in logistic regression was by using the method

### Timestamp: 16:24

 of kernels here we are doing it in slightly different way what we are saying is that we are

### Timestamp: 16:29

 introducing non-linearity y are these activation functions. Now, one way to think of this is as follows

### Timestamp: 16:35

 now each of these hidden layers you can imagine as if they are saying whether some property

### Timestamp: 16:45

 holds for this input or not. Now, depending on the problem at hand these properties could mean

### Timestamp: 16:52

 different things for example, if the input was actually you know let us say an image and a pixel

### Timestamp: 17:00

 values of image. So, then one w transpose x right. So, let us say this w 1 transpose x might

### Timestamp: 17:06

 kind of say whether this image has a particular I mean edge or not right. So, does this image have an

### Timestamp: 17:15

 edge may be the second neural second node might say that whether this image has something else

### Timestamp: 17:21

 right. So, maybe a curve or something of that sort right. So, whatever that can be easily identified

### Timestamp: 17:26

 using a linear model let us say that is what each of these hidden layer is trying to learn.

### Timestamp: 17:31

 Now, what happens is now this activation function in the simplest form if you think of this as a

### Timestamp: 17:37

 you know a 0 1 value which indicates whether something is present or not then you can think of

### Timestamp: 17:45

 each of these hidden layer nodes as if they are voting whether a particular property is present in

### Timestamp: 17:51

 input domain or not in the input or not right. So, the input x that we are giving and now you can

### Timestamp: 17:57

 think of the second output layers job as to combine these votes right. So, you are taking a

### Timestamp: 18:03

 weighted vote and then you are presenting the answer based on that right. So, in the simplified

### Timestamp: 18:09

 case depending on your activation function you can you know you can view this hidden layers job

### Timestamp: 18:17

 as to produce in some sense of vote right. So, if it is a 0 1 that the activation layer is producing

### Timestamp: 18:23

 let us say it is thresholding w transpose x at 0 and then if it is positive I would say 1 if it

### Timestamp: 18:29

 is negative I am saying 0 then each of these w's is kind of learning a linear classifier and then

### Timestamp: 18:36

 my activation function is saying whether it is on left side of w or right side of w and each of

### Timestamp: 18:42

 these w's are I mean each of these hidden layer nodes are learning different w's. So,

### Timestamp: 18:47

 you are basically trying to you know pinpoint where in this d dimensional space my data point

### Timestamp: 18:53

 is present and based on the votes that each of these hidden layers are providing and then you

### Timestamp: 18:57

 are combining these votes to produce an output. So, because these activation functions in the way

### Timestamp: 19:03

 that I described is a 0 1 function there is a non-linearity that is being introduced here.

### Timestamp: 19:08

 But what might happen is you know now the question is how do I you know learn these w's right.

### Timestamp: 19:16

 So, nobody is giving me these w's what I am positing or hypothesis in here is that there are these

### Timestamp: 19:22

 w 1 till w k and w out which will best explain my output given the input. But I need to learn these

### Timestamp: 19:31

 w's of course, like how we learn w's in an SVM or a logistic regression or perceptron here you

### Timestamp: 19:36

 are not just learning 1 w, but then you are learning a lot of w's which means that you know we need

### Timestamp: 19:42

 to understand how to learn these w's given the data all we have is data from the data we need to

### Timestamp: 19:47

 learn these w's right. So, now what we have to have some procedure that learn these w's

### Timestamp: 19:54

 and that procedure will briefly talk about that procedure. But then let us say you have a procedure

### Timestamp: 20:00

 but then the procedure will work well depending on what this activation functions right.

### Timestamp: 20:07

 So, if this activation function is kind of you know discontinuous and so on like how it is a 0 1

### Timestamp: 20:14

 function if it is an indicator of whether w transpose x is greater than or equal to 0 it is like a 0

### Timestamp: 20:20

 1 function. And now we might end up you know it might be very hard to optimize this problem to find

### Timestamp: 20:26

 that w's. Instead in practice what people typically do is they use some kind of activations which

### Timestamp: 20:34

 look like this examples of activations activation functions that is the way we introduce non-linearities.

### Timestamp: 20:53

 Two popular examples let us call this activation function a a right. So, a of z is what something

### Timestamp: 21:04

 that we have already seen before right. So, which is like the sigmoid activation

### Timestamp: 21:11

 which is a differentiable function it is easy to handle and so on and so forth which does the

### Timestamp: 21:17

 following if you remember right. So, this guy looks like this where it is like a soft

### Timestamp: 21:26

 oat in some sense right. So, the larger the value of z is in the positive side it you can think

### Timestamp: 21:32

 of it as the what is the probability that you are voting positively right. So, it is going to go

### Timestamp: 21:37

 closer and closer to 1. So, this is 1 this is 0.5 this is 0 and the more negative this value is

### Timestamp: 21:45

 you know we are voting closer and closer to 0. So, that is one way to smoothen this 0 one thing

### Timestamp: 21:51

 that we have but remember it is no longer convex in this case right. So, the only thing 0 one

### Timestamp: 21:58

 problem is 0 one has a discontinuity and now we are trying to overcome this discontinuity by making

### Timestamp: 22:05

 it smooth but then it is no longer convex right. So, that is that is something to keep in mind.

### Timestamp: 22:10

 So, which means that you know the final function if you think of this as a function

### Timestamp: 22:17

 where a is some sigmoid it is no longer a convex function right. So, of input why is not a

### Timestamp: 22:23

 convex function of you know this input and these parameters of w basically. So, so that is why this

### Timestamp: 22:32

 is not a convex you know losses right. So, we will talk about the loss in a minute but this is not

### Timestamp: 22:37

 a convex loss because though this is a you know sufficiently smooth function it is not convex.

### Timestamp: 22:45

 Another example very popular example again you will learn a lot about this example you will

### Timestamp: 22:50

 encounter this when you look at deep learning courses I will just introduce this is called as the

### Timestamp: 22:55

 Relu function which is max of 0 comma z right. So, this is called as rectified linear

### Timestamp: 23:08

 unit right. So, again if you think of how this is going to look like so if z is positive this

### Timestamp: 23:19

 is going to be positive z is negative this is going to be 0 right. So, it is going to be max

### Timestamp: 23:24

 of these two things right. So, this is another function again it might be beyond this

### Timestamp: 23:31

 scope of this course to explain why somebody would want to use this function as opposed to a

### Timestamp: 23:37

 sigmoid function what are the advantages of this function and so on and so forth. So, all these

### Timestamp: 23:41

 will be covered when you talk in detail in a deep learning course, but I am just trying to put

### Timestamp: 23:45

 put put it out there that there are these different activation functions these are not just the

### Timestamp: 23:49

 two ones I mean there are several others there is a tan H activation function for example,

### Timestamp: 23:53

 and so on and so forth. So, basically some way to introduce non-linearity in the system because

### Timestamp: 23:58

 if you do not introduce non-linearity if a of z activation function happens to be a linear

### Timestamp: 24:03

 function well then this whole thing is a linear function and then this is just a linear combination

### Timestamp: 24:09

 of linear functions of w which will again be a linear function right. So, then that is not really

### Timestamp: 24:15

 that much of that that very useful then what a SVM or a perceptron is already doing right.

### Timestamp: 24:21

 So, because your output to input to output mapping will then become a linear function.

### Timestamp: 24:25

 You want to introduce non-linearity so that you can learn a richer class of

### Timestamp: 24:29

 mappings from input to output and that non-linearity is introduced using this activation functions in this case.