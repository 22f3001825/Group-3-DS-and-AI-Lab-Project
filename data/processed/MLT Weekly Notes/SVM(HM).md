Support Vector Machine - Hard Margin 

✉ 23f1001171@ds.study.iitm.ac.in (Piush Das) 

## Perceptron and Margin 

Radius Margin Bound 




number of mistakes  ⩽ R 2<br>2<br>𝛾<br>




•  ‖ xi ‖2 ⩽ R2<br>* T<br>•  w xi yi ⩾ 𝛾 ; 𝛾 > 0<br>

Classifiers with a larger margin generalize better. That is, they perform better on test data-points compared to classifiers that have a small margin. 

2 The number of mistakes made by the pereceptron will depend upon the best possible w<sup>*</sup> margin, that is larger gamma ⟹ smaller proportion of mistakes. 

✉ 23f1001171@ds.study.iitm.ac.in (Piush Das) 



Given a linear classifier, let us make the notion of margin more precise. There are two kinds of margin. Consider a linearly separable dataset with a positive margin. Let w  be any valid classifier that perfectly separates the dataset. We can always find at least one point from the dataset that is closest to the decision boundary. Call this point x<sup>*</sup> , For convenience, let this point have y = 1 This point will lie on some line T parallel to the decision boundary, say w x = 𝛾 This  is termed the functional margin. 𝛾 

✉ 23f1001171@ds.study.iitm.ac.in (Piush Das) 

From our assumption, we have: 





T T The distance of between the lines w x = 0 and w x = 𝛾 is called the geometric margin and is given by 



Since both w and  can be scaled simultaneously without a𝛾 ffecting the setup, we will set 𝛾 = 1 





Therefore, for any linearly separable dataset with a positive margin, and a valid classifier w, we can set the functional margin 𝛾 = 1 and the geometric margin becomes 

Geometric Margin =<sup>1</sup> ‖w‖ 

✉ 23f1001171@ds.study.iitm.ac.in (Piush Das) 

## What is Width ? 




z<br>x<br>



2 width(w) = 2 ‖w‖ 

✉ 23f1001171@ds.study.iitm.ac.in (Piush Das) 



Equivalently, 



✉ 23f1001171@ds.study.iitm.ac.in (Piush Das) 

## Constraint Optimisation 





fix any w, 





If both function f and g are convex function, then we can swap min and max 





for multiple contraints, 









✉ 23f1001171@ds.study.iitm.ac.in (Piush Das) 

## Solving the Optimization Problem 

Since the objective function is convex and since the inequality constraints involve convex functions, the entire problem is a convex optimization problem. We can recast it in the standard form as 





### Objective Function 







fix some 𝛼 ⩾ 0 



Take gradient w.r.t w and set it to 0 



In Matrix Notation, 



✉ 23f1001171@ds.study.iitm.ac.in (Piush Das) 

Plugging XY𝛼 back into the dual objective, we get the following form 



The dual optimization problem therefore becomes: 




1<br>T T T T<br>max 𝛼 1 - 𝛼 Y X XY𝛼<br>𝛼⩾0 2<br>

- Dual variable dimension in R<sup>n</sup> while primal problem dimension is R<sup>d</sup> 

- Dual constraints are easier 

- T 

- • More Important, Dual depends on x x and so can be kernelised 

✉ 23f1001171@ds.study.iitm.ac.in (Piush Das) 



✉ 23f1001171@ds.study.iitm.ac.in (Piush Das) 

## Complimentary Slackness 



### Primal View 

- If wTxi yi > 1, we have 1 - w*<sup>T</sup> xi yi < 0, which forces 𝛼i* = 0. For a point which lies beyond the supporting hyperplanes, the value of 𝛼<sup>*</sup> is zero. 

- • If wTxi yi = 1, we have 1 - w*<sup>T</sup> xi yi = 0, which doesn't really forces 𝛼i<sup>*</sup> to be a particular value, So we just settle for 𝛼i* ⩾ 0. For a point which lies on the supporting hyperplanes, we can't comment on the value of 𝛼<sup>*</sup> but It can be any non-negative quantity. 



✉ 23f1001171@ds.study.iitm.ac.in (Piush Das) 

### Dual View 

- If 𝛼* = 0, we can't comment on the position of the point. It could either lie on the supporting hyperplane or beyond. 





✉ 23f1001171@ds.study.iitm.ac.in (Piush Das) 

### Some observations concerning support vectors 

- All support vectors lie on the supporting hyperplanes. 

- But note that every point on the supporting hyperplanes need not be a support vector. 

- The weight vector can now be seen as a sparse linear combination of the data-points. The sparsity comes from the fact that all nonsupport vectors have 𝛼* = 0 

- The support vectors are the most important training data-points as they lend their support in building the decision boundary. 

Once a SVM has been trained, it can be used to predict the label of a test point like any other linear classifier 



✉ 23f1001171@ds.study.iitm.ac.in (Piush Das) 

## Linear SVM vs Kernel SVM 



✉ 23f1001171@ds.study.iitm.ac.in (Piush Das) 

## Reference 

Arun Raj Kumar, Lecture Slides for Machine Learning Techniques Karthik Thiagarajan, Machine Learning Techniques Github Notes. Indian Institute of Technology Madras , CS2007 Course Website Stanford University, CS229 Machine Learning Notes 

# Thank You ! 

✉ 23f1001171@ds.study.iitm.ac.in (Piush Das)
