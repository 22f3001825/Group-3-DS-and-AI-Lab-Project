aWeek-10Karthik Thiagarajan[1. Margin](#n0.14332213768754642) [2. Hard-Margin Support Vector Machines](#n0.24951535791960078) [3. Solving the Optimization Problem](#n0.07781655966076317) [3.1. Primal](#n0.10493881399988925) [3.2. Dual](#n0.3322105926663719) [3.3. Solution](#n0.9752934806455575) [3.4. Support Vectors](#n0.34912729981075774) [3.4.1. Primal View](#n0.8834810121127703) [3.4.2. Dual view](#n0.04663571720147508) [4. Prediction](#n0.6926874342041907) [5. Example](#n0.9488350989274434) [6. Kernel SVM](#n0.37969132706544695) 1. MarginClassifiers with a larger margin generalize better. That is, they perform better on test data-points compared to classifiers that have a small margin. Here is a visual intuition for to justify this: GRGRSmall marginLarge margin Given a linear classifier, let us make the notion of margin more precise. There are two kinds of margin. Consider a linearly separable dataset with a positive margin. Let w be any valid classifier that perfectly separates the dataset. We can always find at least one point from the dataset that is closest to the decision boundary. Call this point x\*. For convenience, let this point have y=1. This point will lie on some line parallel to the decision boundary, say wTx=𝛾. This 𝛾 is termed the functional margin. From our assumption, we have: (wTxi)yi⩾𝛾, 1⩽i⩽n Visually:wx\*wTx=𝛾wTx=0𝛾||w||The distance of between the lines wTx=0 and wTx=𝛾 is called the geometric margin and is given by: wTx\*||w||=𝛾||w|| Since both w and 𝛾 can be scaled simultaneously without affecting the setup, we will set 𝛾=1. The corresponding figure becomes:  wx\*wTx=1wTx=01||w||Therefore, for any linearly separable dataset with a positive margin, and a valid classifier w, we can set the functional margin 𝛾=1 and the geometric margin becomes:(geometric) margin = 1||w|| The margin is often used to denote both the distance as well as the hyperplanes wTx=±1. The context will determine what it means.  2. Hard-Margin Support Vector MachinesNow that the (geometric) margin is defined, we would like to find a classifier that has the maximum margin:

max

w 1||w|| But we also have constraints: wwTx=1wTx=0wTx=-1Green: 1Red: -1 Since the closest points to the classifier lie on the margin, all other points have to lie beyond the margin, giving us the following n constraints: (wTxi)yi⩾1, 1⩽i⩽n Putting these two together, we have:

max

w 1||w|| asubject to (wTxi)yi⩾1, 1⩽i⩽n A slight modification to the objective function results in:

min

w ||w||22 subject to (wTxi)yi⩾1, 1⩽i⩽n 3. Solving the Optimization Problem3.1. PrimalSince the objective function is convex and since the inequality constraints involve convex functions, the entire problem is a convex optimization problem. We can recast it in the standard form as:

min

w ||w||22 subject to 1-(wTxi)yi⩽0, 1⩽i⩽n We will call this the primal form. In the primal form, the variable we are optimizing over is w and the constraints are called the primal constraints. There are n constraints, one corresponding to each data-point. We now introduce the Lagrangian function with 𝛼i being the ith Lagrange multiplier: ||w||22+n∑i=1𝛼i[1-(wTxi)yi] We can equivalently express the original optimization problem as follows:

min

w

max

𝛼⩾0 ||w||22+n∑i=1𝛼i[1-(wTxi)yi] 3.2. DualThe dual problem can be expressed as:

max

𝛼⩾0

min

w ||w||22+n∑i=1𝛼i[1-(wTxi)yi] The dual objective is itself an unconstrained optimization problem which we will solve now:

min

w ||w||22+n∑i=1𝛼i[1-(wTxi)yi] Setting the gradient to zero, we get the weight vector to be a linear combination of the data-points: w=n∑i=1𝛼ixiyi In matrix notation: w=XY𝛼 Here X is the d×n data-matrix, Y is a n×n diagonal matrix whose diagonal elements are made up of the labels of the n data-points. 𝛼 is a n×1 vector that has the Lagrange multipliers. X=a

|  |  |  |
| --- | --- | --- |
| | |  | | |
| x1 | ⋯ | xn |
| | |  | | |

, Y=a

|  |  |  |
| --- | --- | --- |
| y1 |  |  |
|  | ⋱ |  |
|  |  | yn |

, 𝛼=a

|  |
| --- |
| 𝛼1 |
| ⋮ |
| 𝛼n |

 Plugging w=XY𝛼 back into the dual objective, we get the following form: n∑i=1𝛼i-12𝛼T(YTXTXY)𝛼The dual optimization problem therefore becomes:

max

𝛼⩾0 𝛼T1-12𝛼T(YTXTXY)𝛼

 Here, 1 represents a vector of n ones. The objective function is a quadratic function of 𝛼 and is concave. 3.3. SolutionFor a convex optimization problem, under certain conditions, the primal and dual have the same optimal value. Solving the dual problem is preferable for the following reasons: • The constraints are simpler.• The appearance of XTX points to kernels. We don't discuss the solution method here. It is enough to know that a solution exists. If the optimal dual variable is denoted by 𝛼\* and the optimal primal variable is denoted by w\*, the two are related as:

w\*=Xy𝛼\*

 The schematic diagram that summarizes the discussion so far. w\*=n∑i=1𝛼\*ixiyi(w\*)Tx=0w\*(w\*)Tx=1(w\*)Tx=-1 SVMSolvery=a

|  |  |  |
| --- | --- | --- |
| 1, |  | (w\*)Tx⩾0 |
| -1, |  | (w\*)Tx<0 |

𝛼\*=a

|  |
| --- |
| 𝛼\*1 |
| ⋮ |
| 𝛼\*n |

w\*Tx=0 is the decision boundary. w\*Tx=±1 are called the supporting hyperplanes. We will see why this name is used in the next section. 3.4. Support VectorsComplementary slackness conditions enforce the following equations: 𝛼\*i[1-(w\*Txi)yi]=0, 1⩽i⩽n 3.4.1. Primal View • If (w\*Txi)yi>1, we have 1-(w\*Txi)yi<0, which forces 𝛼\*i=0. For a point which lies beyond the supporting hyperplanes, the value of 𝛼\* is zero.•  • If (w\*Txi)yi=1, we have 1-(w\*Txi)yi=0, which doesn't really force 𝛼\*i to be a particular value. So we just settle for 𝛼\*i⩾0. For a point which lies on the supporting hyperplanes, we can't comment on the value of 𝛼\*. It can be any non-negative quantity. wwTx=1wTx=0(w\*Txi)yi>1(w\*Txi)yi=1w𝛼\*i=0𝛼\*i⩾0 3.4.2. Dual view• If 𝛼\*i=0, we can't comment on the position of the point. It could either lie on the supporting hyperplane or beyond.•  • If 𝛼\*i>0, we have 1-(w\*Txi)yi=0⟹(w\*Txi)yi=1. A point with 𝛼\*i>0 is going to lie on one of the supporting hyperplanes.•  wwTx=1wTx=0𝛼\*i=0(w\*Txi)yi=1w(w\*Txi)yi⩾1𝛼\*i>0wTx=1wTx=0

Support VectorsThe points for which 𝛼\*i>0 are called support vectors.

 Some observations concerning support vectors: • All support vectors lie on the supporting hyperplanes. • But note that every point on the supporting hyperplanes need not be a support vector. • The weight vector can now be seen as a sparse linear combination of the data-points. The sparsity comes from the fact that all non-support vectors have 𝛼\*i=0.• The support vectors are the most important training data-points as they lend their support in building the decision boundary. 4. PredictionOnce a SVM has been trained, it can be used to predict the label of a test point like any other linear classifier: y=a

|  |  |  |
| --- | --- | --- |
| 1, |  | (w\*)Txtest⩾0 |
| -1, |  | (w\*)Txtest<0 |

 Note that the constraint (w\*Txi)yi⩾1 is binding on only the training data-points. 5. ExampleConsider the following dataset:-4-3-2-112340-3-2-1123X=a

|  |  |  |  |  |  |
| --- | --- | --- | --- | --- | --- |
| 1 | 0 | 3 | -1 | 0 | -3 |
| 0 | -1 | 2 | 0 | 1 | -2 |

, y=a

|  |  |  |  |  |  |
| --- | --- | --- | --- | --- | --- |
| 1 | 1 | 1 | -1 | -1 | -1 |

TFeatureSpacex1x2 The optimization problem is:

min

w w21+w222subject to: a

|  |  |  |  |  |
| --- | --- | --- | --- | --- |
| w1 | ⩾1 |  |  | (1) |
| w2 | ⩽-1 |  |  | (2) |
| 3w1+2w2 | ⩾1 |  |  | (3) |
| w1 | ⩾1 |  |  | (4) |
| w2 | ⩽-1 |  |  | (5) |
| 3w1+2w2 | ⩾1 |  |  | (6) |

 On simplifying the constraints and plotting them along with the contours of the objective:-4-3-2-112340-3-2-1123w1210.5Feasible regionOptimumParameterSpacew2 We see that the primal solution is w\*=a

|  |
| --- |
| 1 |
| -1 |

. We can also solve for the dual. One possible solution is 𝛼\*=a

|  |
| --- |
| 0 |
| 1 |
| 0 |
| 0 |
| 2/3 |
| 1/3 |

.-4-3-2-112340-3-2-1123Feature SpaceExample-2w\*Tx=1w\*Tx=-1w\*a

|  |  |  |
| --- | --- | --- |
| w\* | a  |  | | --- | | =6∑i=1𝛼\*ixiyi | |
|  | =a  |  | | --- | | 1 | | -1 | |

02/30 1 𝛼\*=a

|  |
| --- |
| 0 |
| 1 |
| 0 |
| 0 |
| 2/3 |
| 1/3 |

01/3x1x2 This is an example of a linear hard-margin SVM problem. 6. Kernel SVMWe have the following correspondence between linear SVM and kernel SVM. 𝜙 is typically a function that cannot be explicitly computed.

|  |  |
| --- | --- |
| Linear SVM | Kernel SVM |
| xi | 𝜙(xi) |
| X | 𝜙(X) |
| XTX | K |
| max 𝛼⩾0 𝛼T1-1  2𝛼T(YTXTXY)𝛼 | max 𝛼⩾0 𝛼T1-1  2𝛼T(YTKY)𝛼 |
| w\*=XY𝛼\* | w\*=𝜙(X)Y𝛼\* |
| y=a  |  |  |  | | --- | --- | --- | | 1, |  | (w\*)Txtest⩾0 | | -1, |  | otherwise | | y=a  |  |  |  | | --- | --- | --- | | 1, |  | n∑i=1𝛼\*ik(xi,xtest)⩾0 | | -1, |  | otherwise | |

 An example of a dataset that is not linearly separable in the original feature space but can be separated after a non-linear transformation. A quadratic kernel has been used here. The decision boundary and the two supporting hyperplanes (when brought back to the original feature space) are also displayed: -5-4-3-2-11234560-4-3-2-11234x21+x22=8.5x21+x22=16x21+x22=1x1x2 Note that the decision boundary is not equidistant to the two supporting curves. This is because the actual optimization happens in the transformed space (R6 in this example) and we are visualizing the result in the original space. In the transformed space, the corresponding supporting hyperplanes will indeed be equidistant to the boundary.