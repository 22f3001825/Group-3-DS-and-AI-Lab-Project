aWeek-7Karthik Thiagarajan[1. Zero-One Error](#n0.15818483882423062) [2. Linear Classifier](#n0.31640271738594117) [3. KNN](#n0.894470240485761) [4. Decision Trees](#n0.2808147332065756) [4.1. Binary tree](#n0.7390399908708527) [4.2. Entropy: Node impurity](#n0.5092079283121982) [4.3. Decision Stump](#n0.2890987339098041) [4.4. Growing a Tree](#n0.8302596907465722) [5. References](#n0.0550756651777502) 1. Zero-One Error If f:Rd→{1,0}: L(D,f)=1nn∑i=1I[yi≠f(xi)] This is the average number of errors in prediction by the classifier. 2. Linear Classifier f:Rd→{1,-1} f(x)=sign(wTx)=a

|  |  |  |
| --- | --- | --- |
| 1, |  | wTx⩾0 |
| -1, |  | wTx<0 |

  wx1x2{x | wTx⩾0}{x | wTx<0}halfplanes  The optimization problem given below is NP hard. 

min

w 1nn∑i=1I[yi≠sign(wTxi)] Using the SSE for classification is not a good idea. The SSE is sensitive to outliers.

min

w 1nn∑i=1(wTxi-yi)2  wx1x2 Besides, modeling classification as a regression problem has another issue. There is no natural ordering among the labels in a classification problem. For example, if the labels are "cat", "dog", "mouse", all permutations of the labels {1,2,3} are equally valid. A regression based approach would however take into account the ordering between {1,2,3}. There is a definite sense in which 3>2>1 and 3-2=2-1=1. However, no such order exists among the labels "cat", "dog" and "mouse". 3. KNNPrediction for a given test-point:• Find d(xtest,xi) for all i• Sort distances in ascending order• Find the labels of the first k points• Return the most frequently occurring label Usually an odd number is chosen for k to avoid ties.Hyperparameters: • k• distance metric– L2– L1k=3 Dataset 



Figure 1:Source: Pg 36, ISLP

  Effect of k on decision boundary As k increases, the model becomes less flexible. 



Figure 2:Source: Pg 39, ISLP

   



Figure 3:Source: Pg 39, ISLP

 Advantages• Very easy to implement• Interpretable– Increases trust in the model– Easy to explain to non-experts Disadvantages• Computationally expensive– n points in training data– n distances have to be computed for each prediction– n distances have to then be sorted• No model is learnt• Training data has to be stored even during prediction• Curse of dimensionality Curse of Dimensionality As dimensions increase, neighborhood information becomes less reliable. RR2R3 4. Decision Trees4.1. Binary tree • Qi:feature<value• Depth = 3• Nodes– Root node: Q1– Internal nodes: Q2,Q3,Q4– Leaves: L1,L2,L3,L4,L5 The tree is the model. Once the tree has been grown from data, the data can be thrown away.

Depth: The number of edges on the longest path from the root to a leaf.

 Q1Q2Q3L1L2L3YNYNNYQ4L4L5NY 4.2. Entropy: Node impurity • nP→ number of positive data-points• nN→ number of negative data-points n=nP+nN p → proportion of positive (negative) data-points in a node p=nPn The entropy of a node is a measure if the node's impurity: H(p)=-plog2p-(1-p)log2(1-p) 0.250.50.75100.250.50.751pImpurity 4.3. Decision Stump PLRYN• D: dataset at the parent• xf<s: question• DL and DR: partitions• pP,pL,pR: proportions at P,L,R• 𝛾: proportions of points in L• EP: entropy of P• EL: entropy of L• ER: entropy of R • IG: information gain n=nL+nR 𝛾=nLn E=-plog2p-(1-p)log2(1-p) IG=EP-[𝛾EL+(1-𝛾)ER] 4.4. Growing a Tree Growing a tree is a recursive and greedy algorithm: • At each node, choose the (feature, value) pair that gives the greatest reduction in entropy or the maximum gain in information.• Choice of values for a given feature– Sort all the values for this feature in the training dataset\* Use this set of values (OR)\* Use the mid-point between consecutive feature values in this set.• Stop growing the tree when the stopping criterion is met– Default stopping criterion is when a node is completely pure– Other stopping criteria are discussed in the end.• Assign labels to leaf nodes– Label is most frequently occurring label Sample dataset 1234567812345678 Treex2<5.5x1<5.5x1<5.5YN0110YNNY Decision boundary1234567812345678 Decision Regions • 4 regions• 4 leaves In general, boundaries of the regions are parallel to the axes: RR2R3Rdhyper-rectangles  Prediction Traverse the tree. When a leaf node is reached, output the label of the leaf node. Overfitting Deep trees have high variance.x1<3.5x2<5.5x2<2.50x1<2.51x1<5.501x2<5.501• 7 regions• 7 leaves  Mitigation• Minimum samples at leaf node• Maximum depth• Minimum decrease in impurity Advantages • Shallow trees are interpretable• Easy to implement Disadvantages • Simple model with low predictive power• Deep trees have high variance– small changes to the training data result in big changes in the resulting tree 5. References• ISLP: Introduction to Statistical Learning using Python