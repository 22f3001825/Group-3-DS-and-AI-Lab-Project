# Week-12 - Lecture 5

### Timestamp: 00:00

 So, now how would we train such a network? Well, one way to train such a network is you

### Timestamp: 00:21

 know to define what is the loss right. So, for regression problems our loss is the usual

### Timestamp: 00:28

 squared loss right. So, our regression problems loss will be you know a neural network of x,

### Timestamp: 00:36

 come on let me let me call it theta by which I mean when you pass the input x to a neural network

### Timestamp: 00:46

 whose weights are all parameterized by theta when I say theta it means in the previous example

### Timestamp: 00:52

 this is W 1 to W k and W out all of this put together I am calling as theta all the parameters

### Timestamp: 00:59

 of the neural network and now the entire neural network is you know fixed once I fix theta

### Timestamp: 01:06

 and then I give x right. So, now for this particular x let us say x i which is my first ith

### Timestamp: 01:12

 data point now this is what the neural network could predict now the loss would be this minus y i

### Timestamp: 01:20

 so, come on y i in general for regression problem this can be you know neural network of x i

### Timestamp: 01:27

 parameterized by theta minus y i squared and then I will sum it up over all data points as usual

### Timestamp: 01:34

 right. So, now the way we have to think about this is you know this is analogous to you know

### Timestamp: 01:39

 W transpose x i if you just had a single you know you only had one neuron in the hidden layer

### Timestamp: 01:46

 then there is only one W and this can be thought of as analogous to and then there is the activation

### Timestamp: 01:51

 function is an identity function then this is just W transpose x i somehow you are outputting

### Timestamp: 01:56

 something based on the input and that is what is your predicted value and this is the actual value

### Timestamp: 02:02

 and then as usual you are looking at the squared difference. Now of course, we need to find this theta

### Timestamp: 02:08

 now if your activation function is a differentiable function a continuous function and so on

### Timestamp: 02:17

 then you know what you can do is you can start with some parameter initialization and then you can

### Timestamp: 02:24

 do gradient descent with respect to theta right. So, learn theta star using gradient descent

### Timestamp: 02:38

 as usual right. So, because now your whole neural network is parameterized by theta and theta is

### Timestamp: 02:47

 some high dimensional object it includes W 1 to W k and W out and now as you change each entry

### Timestamp: 02:54

 of W's then that will affect my output in a certain way and that change is captured using the gradient

### Timestamp: 03:01

 and so I can take a step in the negative gradient direction and so on.

### Timestamp: 03:06

 So, now as the number of parameters that we have in our neural network increases

### Timestamp: 03:16

 this theta is going to become a very high dimensional object. Why would number of parameters in

### Timestamp: 03:20

 our neural network increase? Well here we had a very simplified neural network where we had one

### Timestamp: 03:26

 hidden layer but now we can think of a case where we have multiple hidden layers right. So,

### Timestamp: 03:34

 for instance you know all of these guys are voting based on my input data points somehow and now

### Timestamp: 03:43

 you are kind of combining these odds to create more odds right. So, this is layer 1 this is layer 2

### Timestamp: 03:54

 and so on and so forth right. So, each successive layer is kind of trying to operate at one level

### Timestamp: 04:02

 above the previous layer right. So, it is combining the odds of the previous layer. So, and it is

### Timestamp: 04:07

 voting on the combination and so on and so forth and you can add multiple layers here right. So,

### Timestamp: 04:13

 let us say I add L such layers and now finally, I will combine using an output layer right. So,

### Timestamp: 04:20

 this is output layer to produce my output this of course, input layer.

### Timestamp: 04:28

 Now, for this neural network you have many many more parameters right. So, every neuron corresponds

### Timestamp: 04:35

 to one w that we need to learn right. So, the w's might be in different dimensions based on which

### Timestamp: 04:41

 layer this neuron is in. So, for instance if it is in the first layer then the w will depend on

### Timestamp: 04:46

 the input layers dimension. So, these would be in d dimensional vectors. The second layer will

### Timestamp: 04:53

 depend on how many nodes that we had in the previous layer and that is a design choice right. So,

### Timestamp: 04:58

 we can try out different nodes typically all the layers from 2 all the layers from 1 to L will have

### Timestamp: 05:06

 the same number of nodes, but that is not a strict necessity you can try out with different things.

### Timestamp: 05:12

 But then depending on that you will your the parameters that you have to learn can blow right.

### Timestamp: 05:17

 So, it can become a very large number. So, now then question is how easy is it to compute the

### Timestamp: 05:24

 gradient of this complicated looking network right. So, for a given theta well it is a bit complicated,

### Timestamp: 05:34

 but then there is an efficient way to compute this gradient right. So, and that just uses you know

### Timestamp: 05:41

 the chain rule of differentiation right. So, the gradient computed taking advantage of

### Timestamp: 05:54

 stage of chain rule. Again we want to do this in detail again because this would be dealt with

### Timestamp: 06:03

 in deep learning course, but all I am trying to say is that this gradient with respect to some

### Timestamp: 06:10

 if you give me some parameter values w 1 till w k I mean all the parameter values if you give me theta

### Timestamp: 06:17

 then I can compute the gradient of this neural network at theta efficiently by taking advantage of

### Timestamp: 06:25

 the chain rule of differentiation and the algorithm that does this is actually called as the back

### Timestamp: 06:30

 propagation algorithm right. So, it is simply an algorithm that is trying to compute the gradient

### Timestamp: 06:42

 of this a neural network of a specified neural network at a given value of theta.

### Timestamp: 06:47

 Now, once you can compute the gradient then you will update your w's based on taking a negative

### Timestamp: 06:52

 step in this gradient as usual it is the standard gradient descent. But now the interesting thing is that

### Timestamp: 06:59

 because the output is not a convex function of these parameters the gradient descent

### Timestamp: 07:07

 is not going to converge to the theta of right. So, that value of the parameters which will

### Timestamp: 07:14

 minimize our training error right. So, the loss function right. So, it may not converge to

### Timestamp: 07:21

 you know the optimal the global optimal of this function because this is a non convex function

### Timestamp: 07:27

 right. So, it is called especially this is a very high dimensional function because there are too

### Timestamp: 07:31

 many parameters and and this is a very highly non convex function. So, you will converge to a local

### Timestamp: 07:39

 minima right. So, gradient descent converges to local minima local minima

### Timestamp: 07:48

 and now if you take a again a deep learning course you will understand you know when how to you

### Timestamp: 07:57

 know deal with this problem right. So, typically I mean first glance it appears that okay. So,

### Timestamp: 08:04

 we wanted to find the global minima which was easy in the case when the loss function was a

### Timestamp: 08:10

 convex function of the parameters. Here the loss function is a not a convex function of the

### Timestamp: 08:14

 parameters. So, we might end up with not necessarily a global minima we will only end up with local

### Timestamp: 08:20

 minima. So, it appears that this method may give us poor solutions. So, now how to deal with this

### Timestamp: 08:28

 and how it typically works very well in practice if you initialize your algorithm carefully and if you

### Timestamp: 08:37

 do some you know clever tricks to gradient descent to make it slightly different you just don't

### Timestamp: 08:42

 follow the direction of the gradient, but you do slightly select tricks with respect to the gradients

### Timestamp: 08:48

 is would be covered as part of a deep learning course right. So, so basically the ideas are similar

### Timestamp: 08:54

 right. So, you have you set up a loss function the loss function has some parameters,

### Timestamp: 08:58

 but then the function is not a convex function of the of the parameters of interest.

### Timestamp: 09:02

 So, you your gradient descent may not converge to a local minima still you can you know it converges

### Timestamp: 09:09

 to something that is very very reasonable practice. And the reason why that happens and how you can

### Timestamp: 09:14

 you know do these tricks and so on to get it working we part of a deep learning course,

### Timestamp: 09:20

 but in the standard classical artificial neural networks method it means your back propagation

### Timestamp: 09:26

 is a technique which simply computes the gradient. Now, this back propagation is common for both

### Timestamp: 09:34

 regression and classification right. So, so right now we have spoken about regression where we put

### Timestamp: 09:40

 down this loss function as the square to loss, but it need not be the square loss if you are working

### Timestamp: 09:46

 with a classification problem. So, let us say you have a classification problem then what would

### Timestamp: 09:53

 what would happen is that again you will have some input layers and some hidden layers let us say

### Timestamp: 09:59

 we have input layers x 1 2 x d and you have all these hidden layers.

### Timestamp: 10:13

 And then you kind of what you do is you know you can have multiple layers this is layer 1 layer 2

### Timestamp: 10:19

 and so on and so forth. If it is a binary classification problem then you have one output layer

### Timestamp: 10:24

 which will produce let us say sigmoid of W out transpose you know whatever is the input right.

### Timestamp: 10:35

 So, input to this right. So, which is just this is what I mean by input whatever this takes as input

### Timestamp: 10:42

 it will it will have a W corresponding to each way the corresponding to each of these edges and

### Timestamp: 10:47

 then it will do W out transpose input and it will do a sigmoid which means that basically we are

### Timestamp: 10:53

 predicting probability of Y given x right. So, this is a sigmoid function as usual.

### Timestamp: 11:02

 So, now there is an actual Y sitting here and now you can define an appropriate loss which depends

### Timestamp: 11:11

 on you know how well this probability of Y given x matches the actual Y right. So, this is

### Timestamp: 11:18

 let us say 0.1 then your loss will be less if Y is 0 and if it is 0.9 which means that you are

### Timestamp: 11:28

 more likely to say that Y is 1 but then the actual Y is 0 then the loss will be more right. So,

### Timestamp: 11:33

 basically you can use what is called as a cross entropy loss which kind of measures how close

### Timestamp: 11:46

 are these two things with respect to each other right. So, now the remaining thing is exactly the

### Timestamp: 11:52

 same right. So, because your neural interc is still is a function of all these parameters theta

### Timestamp: 12:00

 and the only thing that is going to change in the is in the final layer where instead of

### Timestamp: 12:05

 outputting a real number you are now going to do a sigmoid of a real number and predict the

### Timestamp: 12:10

 probabilities and then now you have to compare the probabilities with the actual the actual

### Timestamp: 12:18

 output Y and using the cross entropy loss and then again you will do the gradient with respect to

### Timestamp: 12:23

 this new loss function everything else is the same right. So, because we need to compute the

### Timestamp: 12:29

 gradient you want to do a gradient descent you want to compute the gradient of this loss function

### Timestamp: 12:33

 with respect to the underlying parameters you do the same thing you do a back propagation

### Timestamp: 12:39

 based algorithm which again takes advantage of the chain rule of differentiation because

### Timestamp: 12:45

 the chain rule is is an intuitive thing here why it should play use why it should be used here

### Timestamp: 12:51

 because you have multiple layers and then what does the gradient essentially tell you the gradient

### Timestamp: 12:55

 is telling you that if I change one weight how does it affect the output right. So, now this one

### Timestamp: 13:01

 weight will affect the weights on the next layer the next layer will affect the weights of the next

### Timestamp: 13:06

 layer and so on and so forth and so it has to output affect the output right. So, now because

### Timestamp: 13:11

 there is this layer by structure in our neural network we can use this structure to do this back

### Timestamp: 13:17

 propagation more efficiently right. So, and that is where you kind of gain in doing back propagation

### Timestamp: 13:23

 by taking advantage of the chain rule it is an efficient way to compute the gradients right. So,

### Timestamp: 13:27

 once that is done everything else is basically the same right. So, so basically the conclusion then

### Timestamp: 13:35

 is with with respect to neural network is that you know neural networks learns

### Timestamp: 13:45

 local minima of non-concave functions.

### Timestamp: 13:56

 Typically bugs very well in practice. Now, I will add that when I say practice especially for

### Timestamp: 14:20

 unstructured data like images or text or even speech and things like that where you know you

### Timestamp: 14:35

 know you are not given a tabular column of features, but then you are just given some unstructured

### Timestamp: 14:40

 pieces of information from which you need to learn these features. So, to say of course, depending

### Timestamp: 14:45

 on whether it is text or whether it is time series data or whether it is speech or whether it is

### Timestamp: 14:52

 you know images. Now, your neural network architectures have to be different for each of these

### Timestamp: 14:59

 different modalities. Now, again when you take a deep learning course you will understand that how

### Timestamp: 15:05

 today's state of the neural networks kind of use some information that we know about these

### Timestamp: 15:12

 modalities as part of the architecture. So, that it kind of learns you know these features

### Timestamp: 15:19

 feature mappings very well. So, why do I say this is feature mappings. So, one way to think about

### Timestamp: 15:24

 this is as follows right. So, you can you can think of what the neural network is doing for

### Timestamp: 15:31

 even for a regression problem it is taking as input and then it is producing an output right. So,

### Timestamp: 15:36

 it is producing some real value here. Now, you can think of the neural network itself as if

### Timestamp: 15:43

 it is mapping the input to a real number that is one way to think of it. The other way to think

### Timestamp: 15:47

 of it would be to think of the neural network as doing two different things. In the first level you

### Timestamp: 15:54

 can think of you know what it does till the last layer and then you can think of what it does in

### Timestamp: 16:00

 the last layer. Now, what you can one way to interpret the neural networks working is by saying

### Timestamp: 16:08

 that the neural network learns some feature mapping from layer one till layer L. So, basically this

### Timestamp: 16:20

 input input data which is an R D let us say is map to some R R M which is you know you have one

### Timestamp: 16:27

 to M nodes in the last layer. So, this is R L L has M nodes. So, you are mapping R D to R M using

### Timestamp: 16:38

 some non-linear map which is what this layer one till layer L is doing and now after you have learned

### Timestamp: 16:44

 this map what the output layer is doing is just doing a linear function on the last layer right.

### Timestamp: 16:50

 So, one the learned map. So, you learn a non-linear map and then you do a linear function in the

### Timestamp: 16:56

 non-linear space right. So, which is which should be reminiscent of what kernel machines typically do

### Timestamp: 17:02

 right. So, it is like implicitly you are trying to map your data to a higher dimension and then you

### Timestamp: 17:07

 are doing you are doing a you know a linear function you are learning a linear function in this

### Timestamp: 17:13

 high dimension. There in the kernel machines so, you specify the kernel which means to say that

### Timestamp: 17:20

 you specify the mapping from load I mentioned the high dimension. Let us say if it is a polynomial

### Timestamp: 17:24

 kernel we are saying that you take the original features and then you know you take height and

### Timestamp: 17:28

 weight as features you do height squared you do weight squared height into weight and so on and so

### Timestamp: 17:32

 forth. Whereas here you know neural network can be thought of as doing both feature learning

### Timestamp: 17:39

 and weight learning together. You can it because it is you are not really saying what are the

### Timestamp: 17:47

 features to use in the high dimension that is also being learnt in this particular neural network

### Timestamp: 17:52

 right. So, the first L layers learn this feature mapping together with the weights that should be

### Timestamp: 17:58

 learnt after you do the mapping to the high dimension which is what the output layer is doing right.

### Timestamp: 18:02

 So, it is do it is jointly learning both features and the parameters in some sense that is one way

### Timestamp: 18:07

 to think of it. Now, the moment you think of it like this now for images certain type of feature

### Timestamp: 18:13

 mappings might be more intuitive for a text certain other type of feature mapping might be more

### Timestamp: 18:19

 intuitive and so on and so forth. So, now you can design your neural networks play around with the

### Timestamp: 18:24

 design of your neural networks to suit the modality itself right. So, if it is images perhaps

### Timestamp: 18:30

 you know looking at edges looking at some properties some some specific things right. So,

### Timestamp: 18:39

 looking for edges corners and so on and so forth my looking for simple shapes might be relevant

### Timestamp: 18:45

 things that the neural networks should do. Now, you can you know set up the neural networks such that

### Timestamp: 18:51

 it kind of starts looking to for these things in some sense right. So, the way to design these things

### Timestamp: 18:56

 will be you know will be part of a deep learning course where you will understand how to come up with

### Timestamp: 19:01

 neural networks which two good feature mappings and also learns the mapped feature to the output

### Timestamp: 19:08

 that is always going to be straightforward. The last layer is always going to be a linear layer

### Timestamp: 19:12

 typically with a if it is a classification with a sigmoid and so on and so forth. But how do you

### Timestamp: 19:17

 what kind of architecture should the neural network have so that you kind of do this

### Timestamp: 19:22

 mapping for this unstructured data very well will will be part of a deep learning course.

### Timestamp: 19:27

 We will not talk about that much here but then if you take a deep learning course you will see that

### Timestamp: 19:32

 you know for unstructured data some variance of these neural networks called convolutional neural

### Timestamp: 19:38

 networks which are very very popular especially for image based data because convolution is a very

### Timestamp: 19:44

 useful image based operations for time series based data you will have something called as

### Timestamp: 19:51

 recurrent neural networks which works well for time series based data. There are something called

### Timestamp: 19:57

 as LSTM's which are which are again long short time memory based neural networks.

### Timestamp: 20:03

 There are something called as you know transformers and attention models and so on and so forth.

### Timestamp: 20:10

 These are all examples of how you know you can develop in some sense

### Timestamp: 20:18

 nice neural network architectures which are essentially nice way to map our input data to some

### Timestamp: 20:25

 useful feature space so that our problem of classification or regression becomes easier.

### Timestamp: 20:31

 So again these will all be covered as part of deep learning course I am not going to do that in

### Timestamp: 20:35

 this course. So kind of to summarize so summarize whatever we have seen so far in neural networks is

### Timestamp: 20:42

 that it is basically at the end of the day it is just a non-linear map from input to output

### Timestamp: 20:48

 but then it is just not arbitrary non-linear map you kind of you know specify this non-linear map

### Timestamp: 20:56

 using an architecture and the simplest architecture that we have seen is this one layer architecture

### Timestamp: 21:02

 but then there could be multiple layers and all sorts of architectures which map input to output

### Timestamp: 21:09

 and once you have specified the architecture the way to learn this the parameters of this architecture

### Timestamp: 21:14

 would be to do something called as back propagation which is nothing but gradient descent

### Timestamp: 21:19

 and algorithm to compute the gradient and then you do a gradient descent

### Timestamp: 21:23

 you will typically end up with a local minima of the loss function but that usually is very

### Timestamp: 21:30

 good in practice. In practice these are very powerful algorithms they beat state of the art

### Timestamp: 21:38

 classical machine learning algorithms that we have seen a lot in this course specifically for

### Timestamp: 21:43

 unstructured data for structured data still I would not say these are the best possible algorithms

### Timestamp: 21:49

 we will still we might have something like a boosting or a support vector machines are still

### Timestamp: 21:54

 very good algorithms when you have structured data when you have unstructured data because

### Timestamp: 21:59

 the modern day neural networks you know build these feature maps very carefully they perform

### Timestamp: 22:09

 they outperform classical methods like support vector machines or logistic regression where

### Timestamp: 22:13

 the kernels are not necessarily tuned to a particular modality right. So, the neural networks

### Timestamp: 22:21

 are very competitive in today's I mean they are the they give you state of the art performance for

### Timestamp: 22:26

 most unstructured data based problems whereas for structured data we will still use several

### Timestamp: 22:33

 algorithms learnt in this course right from you know support vector machines to logistic