aWeek-12Karthik Thiagarajan[1. Loss functions for Classification](#n0.14332213768754642) [1.1. 0-1 Loss](#n0.4912408814818401) [1.2. Convex Surrogates](#n0.054964895985824214) [1.2.1. Squared Loss](#n0.41137774006480243) [1.2.2. Hinge Loss](#n0.0006051100334039106) [1.2.3. Logistic Loss](#n0.6737521248325715) [1.2.4. Perceptron Loss](#n0.26534544060951815) [2. Neural Network](#n0.9302380268136794) [2.1. Network Architecture](#n0.9482947797121954) [2.2. Activation functions](#n0.24581266391579626) [2.2.1. ReLU: Rectified Linear Unit](#n0.7102328291073763) [2.2.2. Sigmoid](#n0.1560302854570368) [2.3. Computation at a neuron](#n0.3861118987730243) [2.4. Forward Pass](#n0.12931062743619437) [2.4.1. Regression](#n0.045554540390829734) [2.4.2. Binary Classification](#n0.13330812142788084) [2.5. Backward Pass](#n0.43466846914616464) [2.6. Flow of information](#n0.8703525281430815) 1. Loss functions for Classification 1.1. 0-1 LossGiven a classifier h:Rd→{-1,1}, the loss function used for determining the goodness of the classifier is: 1nn∑i=1I[h(xi)≠yi] This is the average number of points that are misclassified. The goal is to find a classifier that minimizes the 0-1 loss: 

min

h∈H 1nn∑i=1I[h(xi)≠yi] H is the class of functions that we will search in. Instead of looking at all possible functions, we can restrict the class of functions to linear functions: Hlinear={sign(wTx): w∈Rd} More elaborately, any linear classifier h∈Hlinear is given as: h(x)=sign(wTx)=a

|  |  |  |
| --- | --- | --- |
| 1, |  | wTx⩾0 |
| -1, |  | wTx<0 |

 The optimization problem now becomes:

min

h∈Hlinear 1nn∑i=1I[h(xi)≠yi] Even though the set Hlinear is simple enough, solving the above optimization problem is still (NP) hard. One way to mitigate the problems posed by the 0-1 loss is to look for alternative loss functions that approximate the behavior of the 0-1 loss but are easier to optimize. Convex functions fit this description. For a single training data-point (x,y), the 0-1 loss can be given as: I[(wTx)y<0] Visually: -5-4-3-2-1123450-112(wTx)y   1.2. Convex Surrogates We will look at various convex approximations to the 0-1 loss. Each such loss gives rise to a classification algorithm. For the rest of this document, we will only focus on linear classifiers. Since the quantity (wTx)y plays a major role, we will use the shorthand u=(wTx)y. Note that y∈{-1,1}.  1.2.1. Squared Loss a

|  |  |
| --- | --- |
| L(w,x,y) | =(wTx-y)2 |
|  | =(wTx)2+y2-2(wTx)y |
|  | =(wTx)y2+1-2(wTx)y |
|  | =[(wTx)y-1]2 |

 We can therefore express this as: (u-1)2 -4-3-2-11234560123 This loss is associated with a least squares classifier (inspired by regression). The loss is convex, but a poor approximation for the 0-1 loss. It heavily penalizes even points that are correctly classified. 1.2.2. Hinge Loss L(w,x,y)=

max

 (0,1-(wTx)y)This can be written as: 

max

 (0,1-u)Plotting it: -4-3-2-11234560123 The hinge loss is used in SVM. Notice that the loss penalizes points that are also correctly classified but violating the margin.  1.2.3. Logistic Loss In logistic regression, the negative log-likelihood is treated as a loss function, also called the binary cross entropy. -yln[𝜎(wTx)]-(1-y)ln[1-𝜎(wTx)] Here, the labels are in {0,1}.  a

|  |  |  |
| --- | --- | --- |
| -ln(1  1+e-wTx), |  | y=1 |
| -ln(1  1+ewTx), |  | y=0 |

 Since we are using {-1,1} as the label set, this loss becomes: L(w,x,y)=ln(1+e-(wTx)y) In terms of our notation: ln(1+e-u) -4-3-2-11234560123 This is the logistic loss and is associated with the logistic regression model.  1.2.4. Perceptron Loss The perceptron update rule is: w:=a

|  |  |  |
| --- | --- | --- |
| w+xy, |  | (wTx)y<0 |
| w, |  | (wTx)y>0 |

 This can be viewed as SGD with a step size of one and a batch-size of one with the following loss: L(w,x,y)=

max

 (0,-(wTx)y)which becomes: 

max

 (0,-u) -4-3-2-11234560123   2. Neural NetworkA neural network is a powerful model that learns highly non-linear relationships between inputs and outputs. They are capable of modeling almost any dataset and are particularly suitable for unstructured datasets such as images and text. The last decade of ML research has seen a resurgence of these models. Neural networks are now the state of the art in almost every conceivable sub-field of AI. 2.1. Network Architecture             InputlayerHiddenlayer-1Hiddenlayer-2OutputlayerThere are several layers in a network:• Input layer• Hidden layers• Output layer The computational components in each layer are called artificial neurons or just neurons. Neurons in successive layers are connected by edges. Each edge has a weight associated with it. All neurons other than the input layer neurons have a bias associated with them. The total learnable parameters in a network is the sum of the number weights and biases across layers. For example, consider the network given below:         #weights=3×4+4×2=20#biases=6#parameters=26 2.2. Activation functionsSome non-linear computation happens at each neuron in a network. This is achieved with the help of what is called an activation function. 2.2.1. ReLU: Rectified Linear Unit g(x)=

max

 (0,x)=a

|  |  |  |
| --- | --- | --- |
| x, |  | x⩾0 |
| 0, |  | x<0 |

-4-3-2-112345601232.2.2. Sigmoid g(x)=11+e-x -2-1.5-1-0.50.511.522.500.51  2.3. Computation at a neuron Consider a single neuron at some layer: x1x2x3w1w2w3  ⋮b The computation is composed of two steps:• Linear combination of inputs from the previous layer– These are often called the pre-activation values• Non-linear activation function over this linear combination– These are the activations (outputs at a neuron) For example: Step-1: Linear combination z=w1x1+w2x2+w3x3+bSince z is the input to the activation function, z is called the pre-activation. Step-2: Non-linear activation g(z)=g(w1x1+w2x2+w3x3+b) g(z) is called the activation. This is the output of the neuron and will be fed as input to neurons in the next layer. If g is ReLU, the entire computation can be summarized as: ReLU(w1x1+w2x2+w3x3+b)If g is sigmoid, the entire computation can be summarized as: 𝜎(w1x1+w2x2+w3x3+b) We often say that a neuron fires or is activated if it gives some non-zero output. For instance, in a ReLU neuron would fire if the pre-activations are positive. The bias expresses the propensity of a neuron to fire or activate, independent of the inputs received. That is, if all inputs to a ReLU neuron are zero, the bias gives an idea of what would happen. If the bias is positive, it has a propensity to fire, if the bias is negative, it has a propensity to remain dormant unless the inputs are powerful enough to activate it. 2.4. Forward PassThe forward pass in a network takes the input and produces an output. The network can be seen as a function. To keep things simple, consider a regression problem. Then, the network can be viewed as a non-linear function: h:Rd→R         x1x2x3y     The computations are propagated forward, from left to right, hence the term forward pass. Depending on the problem, the following things will change:• number of neurons in the output layer• choice of activation function at the output layer• loss function 2.4.1. Regression For a regression problem, the output layer will have one neuron and the activation function at the output neuron will be linear (identity) and the loss function will be the squared loss. If h is the neural network, we have: y=h(x) L(w)=(y-h(x))2  2.4.2. Binary Classification There is some variability here, but for this course, we will assume that the output layer has one neuron. The activation function at the output neuron will be sigmoid. In this case, the output value will be interpreted as a probability: h(x)=y=P(y=1 | x)  The loss function will be binary cross entropy loss. -ylny-(1-y)ln(1-y) 2.5. Backward PassGradient descent can be used to minimize the loss and update the weight vector. Combine all parameters of the network into one vector, say 𝜃. 𝜃(t+1):=𝜃(t)-𝜂∇L𝜃(t) Computing the gradient in a neural network is done using an algorithm called back-propagation (chain-rule applied from the last layer to the input layer). 2.6. Flow of informationThe flow of information in a neural network: • Forward pass– Left to right– Input to output• Loss function– True labels and output (predicted labels)• Backward pass– Compute the gradient of the loss with respect to the weights– Update the weights/biases using gradient descent Repeat this process for several iterations.