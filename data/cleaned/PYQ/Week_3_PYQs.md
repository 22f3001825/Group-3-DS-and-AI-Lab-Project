**Practice Questions from Week 3**

> **[Extracted Question]**
> Question 9 : 640653738038
> Total Mark
> 0.00
> Type
> COMPREHENSION
> Consider the data points shown in the following image: Based on the above data, answer the given subquestions:
> Discussions (0)
> Question 10
> 640653738039
> View Parent QN
> View Solutions (0)
> Total Mark
> 4,00
> MCQ
> Perform K-means clustering with K = 2 and initial cluster centers at (0,0) and (6,0). What are the final means of clusters after convergence?
> OPTIONS :
> (2, 0) and (8,0)
> (2, 0) and (8.5, 0)
> O)and (8,01
> O) and (8.5
> None of these
> Type

## **Solution**

Given,

> **[Extracted Question]**
> pi
> (0,0) and pz
> (6,0)

t = 1

|**x**
‖ x - 𝜇 ‖
0
1
2
2||‖ x - 𝜇 ‖
0
2
2
2|zi|
|---|---|---|---|
|(-2 , 2)
=-2-0 + 2-0
(
)<sup>2</sup>
(
)<sup>2</sup>
= 4 + 4 = 8|<|=-2-6 + 2-0
(
)<sup>2</sup>
(
)<sup>2</sup>
= 64 + 4 = 68|c1|
|(-2 , -2)
8|<|68|c1|
|(2 , -2)
8|<|20|c1|
|(2 , 2)
8|<|20|c1|
|(0 , 0)
0|<|36|c1|
|(8 , 2)
68|>|8|c2|
|(9 , 1)
82|>|10|c2|
|(9 , -1)
82|>|10|c2|
|(8 , -2)
68|>|8|c2|
|
1
-2 +-2 + 2 + 2 + 0
(
)
2 +-
(|2 +
)
(|0  0
-2 + 2 + 0
)

||
|∴ 𝜇
=
,
1
5|5|=  ,
(
)||
|𝜇=
,
1
2
8 + 9 + 9 + 8
4
2 + 1 +-1 +
4
(
)|
 -2
(
)|=
,
= 8.5 , 0
34
4
0
4
(
)||

t = 2

|**x**
‖ x - 𝜇 ‖
1
1
2
2||‖ x - 𝜇 ‖
1
2
2
2|zi|
|---|---|---|---|
|(-2 , 2)
=-2-0 + 2-0
(
)<sup>2</sup>
(
)<sup>2</sup>
= 4 + 4 = 8|<|=-2-8.5 + 2-0
(
)<sup>2</sup>
(
)<sup>2</sup>
= 110.25 + 4 = 114.25|c1|
|(-2 , -2)
8|<|114.25|c1|
|(2 , -2)
8|<|46.25|c1|
|(2 , 2)
8|<|46.25|c1|
|(0 , 0)
0|<|72.25|c1|
|(8 , 2)
68|>|4.25|c2|
|(9 , 1)
82|>|1.25|c2|
|(9 , -1)
82|>|1.25|c2|
|(8 , -2)
68|>|4.25|c2|
|
2
-2 +-2 + 2 + 2 + 0
(
)
2 +
(|-2 +
)|0  0
 -2 + 2 + 0
(
)

||
|∴ 𝜇
=
,
1
5
 𝜇=
,
2
2
8 + 9 + 9 + 8
4
2 + 1 +-1
4
(
)|+-2
(
)|=  ,
5
(
)
=
,
= 8.5 , 0

34
4
0
4
(
)||

∵ At t = 1 and t = 2,  the value of 𝜇1t and 𝜇2t are same. we can conlude that the algorithm has converged.

> **[Extracted Question]**
> Question 11 : 640653738040
> 8 View Parent QN
> View Solutions (0)
> Total Mark
> 4.00
> Type
> After introducing
> new data point (7, 0)
> the cluster centers were updated: Enter the sum of the updated X-coordinates for both cluster centers
> accurately; rounding your answer to two decimal places:
> Answer (Numeric):
> Answer

## **Solution**

x = 7, 0 ( ) is added in the datatset

- 2 d((7, 0), (0, 0 =)) ‖ x 𝜇1 ‖2 = 49 - 2 d((7, 0), (8.5, 0 =)) ‖ x 𝜇2 ‖2 = 2.25

∴ the datapoint will be assigned to cluster 2 No changes will be done in 𝜇1

> **[Extracted Question]**
> 8 + 9 + 9 + 8 + 7
> 2 +1 + (-1) + (-2) + 0
> The updated Hz
> be
> 5
> 5
> 5 ,0)
> =
> (8.2 , 0)
> will

Sum of x - coordinates of the final cluster centers are : 0 + 8.20 = 8.20

> **[Extracted Question]**
> Question 15 : 640653738037
> View Solutions (0)
> Total Mark
> 5.00
> Type
> MSQ
> Consider
> Lloyd's algorithm used for k-means clustering and choose the correct statements:
> OPTIONS ;
> K-means algorithm may
> stuck at local minima
> It guarantees finding the optimal clustering (global minimum) in every run:
> practice; k should be as large as possible:
> 0 If the resources are limited and the data set is huge, it will be
> to prefer K-means over K-means++.
> get =
> good

## **Solution**

a) True – K-means can get stuck in local minima due to poor initial centroid selection.

b) False – K-means does not guarantee finding the global minimum in every run.

b) False – A very large k can lead to overfitting and unnecessary computation. d) True – K-means is preferable over K-means++ when resources are limited, as K-means++ has higher initial computation costs.

> **[Extracted Question]**
> Question 8 : 640653827438
> View Solutions (O)
> Total Mark : 4.00
> Type
> Consider the k-means + + algorithm with k = 2 for a dataset that has
> {T1,
> Ti}. The data-point T- has been chosen as the first mean; that iS;
> 041 =I7.
> The Euclidean distance of the remaining points from this mean is given below:
> Point
> 3
> What is the probability of choosing Tg as the second mean given that Iv has bcen chosen
> as the
> mnean?
> Answer (Numeric):
> Answer
> points:
> d(T_
> fitsl

|**Solution**|||
|---|---|---|
|**Point**|d x,𝜇
( i
1<sup>)</sup>|d x,𝜇
( i
1<sup>)2</sup>|
|x1|1|1|
|x2|2|4|
|x3|2|2|
|x4|3|3|
|x5|5|5|
|x6|1|1|
|
|

d x
,𝜇
( 2
1<sup>)2</sup>
4|025|
|p x
( 2)|=
=

d x,𝜇
∑<sup>n</sup>
i= 1 <sup>( i</sup>
1<sup>)2</sup>
16|= .|

> **[Extracted Question]**
> Question 13 : 640653827444
> Total Mark -
> 0.00
> ypC
> COMPREHENSION
> Based on the above data, answer the given subquestions;
> Consider the following dataset of six points in R%:
> K-mcans
> clustering
> 15 Tun
> this dataset with k = 2
> Tn this Version;
> the means are initialized first
> The MCAH 0f the firsl cluster
> initialized
> and the MeAn of the second cluster is initialized to (6.6).
> Discussions (O)
> Question 14
> 640653827445
> View Parent ON
> View Solutions (0)
> Total Mark
> 2.00
> Type
> If (xl,YI)is the mean of the first cluster after convergence; find the value of xI+y1
> Answer (Numeric):
> Answver
> Check Answer
> Dlscusslons (0)
> Question 15
> 640653827446
> Vlew Parent ON
> Vlew Solutlons (OL
> Total Mark
> 2.00
> Type
> If (x2, yZ) is the mean of the second cluster after convergence, find the value of x2 +y2.
> Answer (Numeric):
> Answver
> Check Answer
> (-1

## **Solution**

Given, 𝜇10 = (-4 , -4 ) and 𝜇20 = 6, 6( ) t = 1

|**x**
‖ x - 𝜇 ‖
0
1
2
2|‖ x - 𝜇 ‖
0
2
2
2|zi|
|---|---|---|
|(-1 , -4)
9
<|149|c1|
|(5 , 6)
181
>|1|c2|
|(-2 , -2)
8
<|128|c1|
|(4 , 5)
145
>|5|c2|
|(-3 , -3)
2
<|162|c1|
|(3 , 4)
113
>|13|c2|
|𝜇=
,
=
1
1
-1 +-2 +-3
3
(
)
(
)
-4 +-2 +-3
3
(
)
(
)|-2 ,-3
(
)||
|𝜇
=
,
= 4 , 5
1
2
5 + 4 + 3
3
6 + 5 + 4
3
(
)|||

# t = 2

|**x**|‖ x - 𝜇 ‖
1
1
2
2|‖ x - 𝜇 ‖
1
2
2
2|zi|
|---|---|---|---|
|(-1 , -4)|2
<|106|c1|
|(5 , 6)|130
>|2|c2|
|(-2 , -2)|1
<|85|c1|
|(4 , 5)|100
>|0|c2|
|(-3 , -3)|1
<|113|c1|
|(3 , 4)|74
>|2|c2|
|
2
-1 +|
 -2 +-3
(
)
(
)
-4 +-2 +-3
(
)
(
)|23

||
|𝜇
=
1|,
=
3
3|-,-
(
)||

> **[Extracted Question]**
> 5 + 4 + 3
> 6 + 5 + 4
> p2
> = (4, 5)
> 3

∵ At t = 1 and t = 2,  the value of 𝜇1t and 𝜇2t are same.

- we can conlude that the algorithm has converged.

- - -

- x1 + y1 = 2 + ( 3 = ) 5 x2 + y2 = 4 + 5 = 9

> **[Extracted Question]**
> Question 8
> 640653992024
> View Solutions (0)
> Total Mark
> 5.00
> Type
> SA
> Consider the
> following data points for k-means clustering:
> (-1,0). (-1,1). (-1,-1). (2.0) . (3.1), (3,-1), (4,0)
> In the initialization step of k-means with k = 2, suppose /8 = (-1.0) and /! = (2,0).
> Distances of datapoints
> initial cluster means is tabulated below:
> Uti
> PYI6
> It;
> E
> (-1,0)
> 3
> (1,D)
> 70
> CL-
> T0
> (2,0)
> 8D
> 77
> 2
> As per these cluster centers, the data points
> are
> then assigned to either cluster
> OT
> cluster 2
> After this assignment, what will be the value of the objective function?
> Note: Objective function is given by
> F(21.22..Zn) =
> Zlri
> V_Il?
> 1=1
> Answer (Numeric):
> Answer
> from

## **Solution**

Given 𝜇10 = (-1 , 0 ) and 𝜇20 = 2 , 0( ) t = 1

|**x**|‖ x - 𝜇 ‖
0
1
2
2|‖ x - 𝜇 ‖
0
2
2
2||zi|
|---|---|---|---|---|
|(-1 , 0)|0|3|1||
|(-1 , 1)|1|10|1||
|(-1 , -1)|1|10|1||
|(2 , 0)|3|0|2||
|(3 , 1)|17|2|2||
|(3 , -1)|17|2|2||
|(4 , 0)|25|2|2||

∴ 𝜇11 = (-1 , 0 ) and 𝜇21 = 3 , 0( )

# t = 2

|**x**|‖ x - 𝜇 ‖
1
1
2
2|‖ x - 𝜇 ‖
1
2
2
2||zi|
|---|---|---|---|---|
|(-1 , 0)|0|16|1||
|(-1 , 1)|1|17|1||
|(-1 , -1)|1|17|1||
|(2 , 0)|9|1|2||
|(3 , 1)|17|1|2||
|(3 , -1)|17|1|2||
|(4 , 0)|25|1|2||

- ∴ 𝜇12 = (-1 , 0 ) and 𝜇22 = 3 , 0( )

- t t

- ∵ At t = 1 and t = 2,  the value of 𝜇1 and 𝜇2 are same.

we can conlude that the algorithm has converged.

- ∴ F(Z) = 1 + 1 + 1 + 1 + 1 + 1 = 6

> **[Extracted Question]**
> Question 14 : 640653992021
> Total Mark
> 0.00
> Type
> COMPREHENSION
> Based on the above data, answer the given subquestions:
> A k-means++
> algorithm with k = 3 is
> OH
> the
> following 2D points:
> (0.1) . (1.0) . (1.2), (2,1). (2,3). (2.4). (3.2)
> First cluster
> mean
> 149 is chosen
> 4s
> (2 1).
> Suppose the
> with the highest score is chosen as the 2nd cluster mean /9
> Discussions (0)
> Question 15
> 640653992022
> 0 View Parent QN
> View Solutions (0)
> Total Mark
> 3.00
> Type
> MCQ
> What is /9? Use squared distance to
> calculate the scores.
> OPTIONS
> (0,1)
> (2,3)
> (3,2)
> (2,4)
> applied
> point

**Solution**

> **[Extracted Question]**
> Given, ui
> (2,1)

metric to select 0 is data with the score 𝜇2 point highest

formulae to calculate score = ‖ x - 𝜇1 ‖22

> **[Extracted Question]**
> (0,1) : (0 _ 2)2 + (1 _ 1)2 = 4+0 = 4
> (1,0) : (1 _ 2)2 + (0 _ 1)2 = 1+1 = 2
> (1,2) : (1 _ 2)2 + (2 - 1)2 = 1+1 = 2
> (2,1) : (2 _ 2)2 + (1 _ 1)2 = 0 + 0 = 0
> (2,3) : (2 _ 2)2 + (3 _ 1)2 = 0+4 = 4
> (2,4) : (2 _ 2)2 + (4 - 1)2 = 0+ 9 = 9
> (3,2) : (3 _ 2)2 + (2 _ 1)2 = 1+1 = 2

Highest squared distance is 9, corresponding to the point 2, 4( ) 0 ∴ 𝜇2 = 2, 4( )

> **[Extracted Question]**
> Question 16
> 640653992023
> 6
> View Parent QN
> View Solutions (0)
> Total Mark
> 4.00
> Type
> MCQ
> Which point has the lowest probability of being chosen as the 3rd cluster mean? Use squared distance
> to calculate the scores
> OPTIONS
> (1,0)
> (2,3)
> (3,2)
> (1,2)

## **Solution**

Given, 𝜇10 = 2, 1 ( ) and 𝜇20 = 2, 4( )

|**x**|‖ x - 𝜇 ‖
1
2
2|‖ x - 𝜇 ‖
2
2
2|min d x,𝜇
,d x,𝜇
(
1<sup>)2</sup>
(
2<sup>)2</sup>|P x
( )|
|---|---|---|---|---|
|(0 , 1)|4|13|4|=<sup>4</sup>
11|
|(1 , 0)|2|17|2|=<sup>2</sup>
11|
|(1 , 2)|2|5|2|=<sup>2</sup>
11|
|(2 , 1)|0|9|0|= 0|
|(2 , 3)|4|1|1|=<sup>1</sup>
11|
|(2 , 4)|9|0|0|=   0|
|(3 , 2)|2|5|2|=<sup>2</sup>
11|

- ∵ p(x5) is lowest

∴ It has lowest chance selected as the next cluster mean. of getting