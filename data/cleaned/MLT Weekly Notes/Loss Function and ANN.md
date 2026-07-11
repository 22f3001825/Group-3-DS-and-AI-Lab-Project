# Week-12

Karthik Thiagarajan<br>

|Loss functions for Classifcation<br>1.|
|---|
|Loss<br>1.1.0-1|
|Convex Surrogates<br>1.2.|
|Squared Loss<br>1.2.1.|
|Hinge Loss<br>1.2.2.|
|Logistic Loss<br>1.2.3.|
|Perceptron Loss<br>1.2.4.|
|Neural Network<br>2.|
|Network Architecture<br>2.1.|
|Activation functions<br>2.2.|
|ReLU: Rectifed Linear Unit<br>2.2.1.|
|Sigmoid<br>2.2.2.|
|Computation at a neuron<br>2.3.|
|Forward Pass<br>2.4.|
|Regression<br>2.4.1.|
|Binary Classifcation<br>2.4.2.|
|Backward Pass<br>2.5.|
|Flow of information<br>2.6.|

## 1. Loss functions for Classification

### 1.1. 0 - 1 Loss

d - Given a classifier h : R → { 1, 1} goodness of the classifier is:

This is the average number of points that are misclassified. The goal is to find a classifier that minimizes the 0 - 1 loss:

H is the class of functions that we will search in. Instead of looking at all possible functions, we can restrict the class of functions to linear functions:

More elaborately, any linear classifier h ∈ Hlinear is given as:

The optimization problem now becomes:

Even though the set Hlinear is simple enough, solving the above optimization problem is still (NP) hard. One way to mitigate the problems posed by the 0 - 1 loss is to look for alternative loss functions that approximate the behavior of the 0 - 1 loss but are easier to optimize. Convex functions fit this description.

For a single training data-point (x, y), the 0 - 1 loss can be given as:

T<br>I w x y < 0<br>Visually:<br>2<br>1<br>-5 -4 -3 -2 -1 0 1 2 3 4 5<br>T<br>w x y<br>-1<br>

### 1.2. Convex Surrogates

We will look at various convex approximations to the 0 - 1 loss. Each such loss gives rise to a classification algorithm. For the rest of this document, we T fi w x will only focus on linear classi ers. Since the quantity y plays a major T role, we will use the shorthand u = w x y. Note that y ∈ {-1, 1}.

#### 1.2.1. Squared Loss

We can therefore express this as:

3<br>2<br>1<br>-4 -3 -2 -1 0 1 2 3 4 5 6<br>

This loss is associated with a least squares classifier (inspired by regression). The loss is convex, but a poor approximation for the 0 - 1 loss. It heavily penalizes even points that are correctly classified.

#### 1.2.2. Hinge Loss

This can be written as:

max - u (0, 1 )

#### Plotting it:

3<br>2<br>1<br>-4 -3 -2 -1 0 1 2 3 4 5 6<br>

The hinge loss is used in SVM. Notice that the loss penalizes points that are also correctly classified but violating the margin.

#### 1.2.3. Logistic Loss

In logistic regression, the negative log-likelihood is treated as a loss function, also called the binary cross entropy.

Here, the labels are in {0, 1}.

### - Since we are using { 1, 1} as the label set, this loss becomes:

### - wTx y L(w, x, y) = ln 1 + e

In terms of our notation:

### ln 1 + e-u

3<br>2<br>1<br>-4 -3 -2 -1 0 1 2 3 4 5 6<br>

This is the logistic loss and is associated with the logistic regression model.

#### 1.2.4. Perceptron Loss

The perceptron update rule is:

This can be viewed as SGD with a step size of one and a batch-size of one with the following loss:

### T L(w, x, y) = max 0, - w x y

#### which becomes:

### max -u (0, )

3<br>2<br>1<br>-4 -3 -2 -1 0 1 2 3 4 5 6<br>

## 2. Neural Network

between inputs and outputs. They are capable of modeling almost any dataset and are particularly suitable for unstructured datasets such as images and text. The last decade of ML research has seen a resurgence of these models. Neural networks are now the state of the art in almost every conceivable sub-field of AI.

### 2.1. Network Architecture

Output<br>Input<br>layer<br>layer<br>Hidden Hidden<br>layer-1 layer-2<br>

There are several layers in a network:

- Input layer

- Hidden layers

- Output layer

The computational components in each layer are called artificial neurons or just neurons. Neurons in successive layers are connected by edges. Each edge has a weight associated with it. All neurons other than the input layer neurons have a bias associated with them. The total learnable parameters in a network is the sum of the number weights and biases across layers. For example, consider the network given below:

#weights=3 × 4 + 4 × 2 = 20 #biases=6 #parameters=26

### 2.2. Activation functions

Some non-linear computation happens at each neuron in a network. This is achieved with the help of what is called an activation function.

#### 2.2.1. ReLU: Rectified Linear Unit

x, x ⩾ 0<br>x = max  x =<br>g( ) (0, )<br>0, x < 0<br>3<br>2<br>1<br>-4 -3 -2 -1 0 1 2 3 4 5 6<br>

#### 2.2.2. Sigmoid

1 g(x) = -x 1 + e

1<br>0.5<br>-2 -1.5 -1 -0.5 0 0.5 1 1.5 2 2.5<br>

### 2.3. Computation at a neuron

Consider a single neuron at some layer:

x1<br>w1<br>b<br>w2 ⋮<br>x2<br>w3<br>x3<br>

The computation is composed of two steps:

- Linear combination of inputs from the previous layer

   - These are often called the pre-activation values

- Non-linear activation function over this linear combination

   - These are the activations (outputs at a neuron)

For example:

#### - <u>Step 1: Linear combination</u>

z = w1x1 + w2x2 + w3x3 + b

z z Since  is the input to the activation function,  is called the pre-activation.

#### - - <u>Step 2: Non linear activation</u>

z g( ) is called the activation. This is the output of the neuron and will be fed as input to neurons in the next layer.

If  is ReLU, the entire computation can be summarized as:g

ReLU(w1x1 + w2x2 + w3x3 + b)

If  is sigmoid, the entire computation can be summarized as:g

𝜎(w1x1 + w2x2 + w3x3 + b)

We often say that a neuron fires or is activated if it gives some non-zero output. For instance, in a ReLU neuron would fire if the pre-activations are positive. The bias expresses the propensity of a neuron to fire or activate, independent of the inputs received. That is, if all inputs to a ReLU neuron are zero, the bias gives an idea of what would happen. If the bias is positive, it has a propensity to fire, if the bias is negative, it has a propensity to remain dormant unless the inputs are powerful enough to activate it.

### 2.4. Forward Pass

The forward pass in a network takes the input and produces an output. The network can be seen as a function. To keep things simple, consider a regression problem. Then, the network can be viewed as a non-linear function:

x3

The computations are propagated forward, from left to right, hence the term forward pass. Depending on the problem, the following things will change:

- number of neurons in the output layer

- choice of activation function at the output layer

- loss function

#### 2.4.1. Regression

For a regression problem, the output layer will have one neuron and the activation function at the output neuron will be linear (identity) and the loss function will be the squared loss. If  is the neural network, we have:h

y = h(x)

#### 2.4.2. Binary Classification

There is some variability here, but for this course, we will assume that the output layer has one neuron. The activation function at the output neuron will be sigmoid. In this case, the output value will be interpreted as a probability:

The loss function will be binary cross entropy loss.

### 2.5. Backward Pass

Gradient descent can be used to minimize the loss and update the weight vector. Combine all parameters of the network into one vector, say .𝜃

Computing the gradient in a neural network is done using an algorithm called back-propagation (chain-rule applied from the last layer to the input layer).

### 2.6. Flow of information

The flow of information in a neural network:

- Forward pass

   - Left to right

   - Input to output

- Loss function

   - True labels and output (predicted labels)

- Backward pass

   - Compute the gradient of the loss with respect to the weights

   - Update the weights/biases using gradient descent

Repeat this process for several iterations.