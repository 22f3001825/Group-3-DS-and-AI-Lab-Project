# **Practice Questions from Week 1**

> **[Extracted Question]**
> Question 2 : 640653738030
> View Solutions (0)
> Total Mark .
> 4.00
> Typa
> McO
> Suppose
> dataset lies in R' and undergoes Principal Component Analysis (PCA) alter
> heing centered.
> The
> resulting first and second principal components are given by:
> #[
> Which of the
> following could be the third principal component?
> OPTIONS ;
> 7'
> E

## **Solution(2)**

we know, all pricipal components are orthogonal to each other i. e, wiTwj = 0  ∀i ≠ j

> **[Extracted Question]**
> W1
> 3
> W2
> 1
> 0
> V3
> V3l
> 1
> ~1

1 1
1 -1 1 0
w1 =    ; w2 =
0 1
3 3
-
1 1

> **[Extracted Question]**
> Wjwz
> 0
> wfb
> 1[1 -1 0 1]x-
> ;
> 3
> 3
> +0 + 0 | =
> 0
> V3l
> 1
> wZb =
> 1[1 0 1 -1]x
> 3
> +0 + 1
> +0/
> 2
> V3
> V3
> ;
> 3
> 3

T
w1 w2 = 0
1
w1Tb =  1 1 -1 0 1  × 1 11  =  13 - 13 + 0 + 0   = 0
3 3
0
1
w2Tb =   1 1 0 1 -1 × 1 1   = 1 + 0 +  + 0 = 1 2
1 3 3 3
3 3
0

similarly workout for option (a) , (c) , (d) T T T w1 w2 = w1 d = w2 d = 0

> **[Extracted Question]**
> Question 6 : 640653738031
> Total Mark : 0.00
> Type
> COMPREHENSION
> Based on the above data, answer the given subquestions:
> Standard PCA has been perforted 0n
> centered dataset in R"
> The first
> principal
> components are given below:
> W1 =
> "=7 [8]
> Consider the data point in the dataset: [2
> 1]"
> (a,6) is the representation of this
> point in the coordinate system formed by the two principal components given above:
> The first and second coordinates correspond to PC-L and PC-2 respectively:
> Discussions (0)
> Question 7
> 640653738032
> Vlew Parent ON
> Vlew Solutions (0)
> Total Mark
> 4.00
> Type
> What is the value of a? Enter your answer correctly to three decimal places:
> Answer (Numeric):
> Answer
> Discussions (0)
> Question 8 : 640653738033
> View Parent ON
> View Solutions (0)
> Tatal Mark ; 4.00
> Type
> What is the value of b? Enter your answer correctly to two decima
> places:
> Answer (Numeric):
> Answer
> tm"

## **Solution(7 and 8)**

> **[Extracted Question]**
> Given,
> 2
> W1
> 4
> W2
> -i
> X
> 2
> ==
> 4 =
> wfx
> =
> [v++-3]
> 1.15
> V3
> -1
> 2
> = b
> wIx
> =
> -1 0] x
> 1
> Vz
> + 0
> 0.70
> -1
> V2
> 1-[1 1 1] X
> 1 , (1

Given,
1 1 2
1 1
w1 =  1   ; w2 =  -1   ; x = 1
3 1 2 0 -1
2
1 2 1 1
⟹ a = w1Tx =  1 1 1 ×  1  =   + -  = 1.15
3 -1 3 3 3
2
1 2 1
⟹ b = w2Tx =  1 -1 0  ×  1  =  -  + 0  = 0.70
2 -1 2 2

> **[Extracted Question]**
> Question 2
> 640653827433
> View Solutions (0)
> Total Mark : 2.00
> Type
> McQ
> Let W1 and Wg be the
> two principal components of the covariance matrix
> of & centered dataset. Let
> x € Rd be
> a data-F
> Which of the following is the
> reconstruction error of the data-point after projecting it onto the
> two principal
> components?
> OPTIONS :
> Ilx - (x"w)w
> (x"
> Ilx - (x"w)wll?+Ilx
> we)well?
> (x"w)?+ (x"we)?
> Ilx - Wll? + Ilx
> Well?
> top
> point.
> top
> Wa)well?
> (

## **Solution(2)**

T projection of x into wi principal component = x wi wi

The reconstructed data point using the top two principal components is

> **[Extracted Question]**
> =3 X
> W1
> +
> W2
> XTws
> XTwz)

reconstruction error formulae

> **[Extracted Question]**
> =
> Ilx
> X

> **[Extracted Question]**
> =
> Ilx
> W1
> xTw2)wzll2
> XTws

> **[Extracted Question]**
> Question 4 : 640653827435
> View Solutions (0)
> Total Mark
> 3.00
> Type : MSQ
> Consider
> covariance matrix C for
> mean-centered dataset in R?.
> After performing
> standard PCA , the three principal components turn out to be
> Which of the following statements
> are tTUe?
> You can
> assume that C is not the zero
> matrix
> OPTIONS :
> OC is a diagonal matrix:
> OThe diagonal entries of €
> are
> nOn-negative:
> OThe diagonal entries of €
> are
> strictly greater than zero.
> OC has to be the identity matrix;
> OC is a matrix of the form kL. where k
> and
> is the identity matrix:

## **Solution(4)**

Option 1 : 𝐶 is a diagonal matrix

True, The eigenvectors are aligned with the coordinate axes, indicating 𝐶 is diagonal.

Option 2 : The diagonal entries of 𝐶 are non - negative

True, Covariance matrices are positive semi - definite, ensuring all eigenvalues (diagonal entries) are non - negative.

Option 3 : The diagonal entries of 𝐶 are strictly greater than zero False, While 𝐶 ≠ 0 , it is possible for some eigenvalues to be 0

Option 4 : 𝐶 has to be the identity matrix

False, 𝐶 being diagonal does not imply it must be I; the eigenvalues can vary.

Option 5 : 𝐶 is of the form kI, where 𝑘 > 0 False, The eigenvalues may not all be equal.

> **[Extracted Question]**
> Question 9 : 640653827440
> Total Mark
> 0.00 | Type
> COMPREHENSION
> Based on the above data, answer the given subquestions:
> Let C be the comriance matrix of
> mean-centered dataset:
> C=
> Standlard PCA is
> performed
> this dataset , Thc first (Wo
> PC;
> given bxelow:
> "=Xh ~#[4]
> Discussions
> Question 10
> 640653827441
> View Parent ON
> View Solutions (0)
> Total Marx
> 2.00
> Type
> Find the variance of the dataset along the first principal component:
> Answer (Numeric):
> Answer
> Discussions (0)
> Question 11 : 640653827442
> Vlow Paront QN
> Vlow Solutlons (0)
> Total Mark
> 1,00
> Type
> Find the variance of the dataset along the X-axis:
> Answrer (Numeric):
> Answ/0f

## **Solution (10)**

> **[Extracted Question]**
> We know , 11
> w]Cw1
> == ^1
> =
> Jlui 4434
> = 3

## **Solution (11)**

> **[Extracted Question]**
> The variance-covariance matrix has the following structure:
> var
> '(c)
> cov(€,y)
> cov(€,y)
> var
> (y)

⟹ C11 = 2

### **Q. Any alternative Way ?**

> **[Extracted Question]**
> X
> 0
> xTCx
> 2

**Q. What will be the variance of the dataset along y-axis?**

> **[Extracted Question]**
> y
> ==
> 12/
> = yTCy
> ==
> 2

> **[Extracted Question]**
> Question 12 : 640653827443
> View Parent QN
> View Solutions (0)
> Total Mark
> 2.00
> Type : MCQ
> Find the coordinates of the
> in the new   coordinate system
> formed by the principal components
> OPTIONS :
> point

## **Solution(12)**

> **[Extracted Question]**
> 2
> 1 st coordinate
> (xTw1)
> I[2
> 21Hil-v
> +
> 2V2
> V2
> V2
> 2 nd coordinate
> (xTwz)
> [[2
> 2]HiJ-
> 0

> **[Extracted Question]**
> Question 5 : 640653992016
> View Solutions (0)
> Total Mark
> 4.00
> Type
> MSQ
> Which of the following expressions is the reconstruction erTor for
> dataset ol
> with respect to
> line passing through the origin represented by the vector W.
> Note that
> Ulwll
> =1
> OPTIONS
> 'Zix
> (xf wJwll?
> "Elx -(x'wJwj"x - (x'wJw]
> o Z1x
> (xTw)?]
> o-'Zi'w?
> points;

## **Solution(5)**

> **[Extracted Question]**
> Error(line, dataset)
> error(line, xi)
> length?(x
> (xTw)w)
> =1
> Ilxi
> (x;Tw)w I2
> =1
> 2
> Ilx;
> x;Tw)w |12
> n
> 1
> 2
> Xi
> ~(xwJo) (w - (wwJwo)
> n
> 12
> xTx;
> (x;Tw)? _ (x;Tw)? + (x;Tw)? wTw

> **[Extracted Question]**
> 12 .fri
> (x;" w)
> nisl

> **[Extracted Question]**
> Question 7
> 640653992017
> Solutions (0)
> Total Mark
> 3.00
> Type
> SA
> The eigenvalues of the covariance matrix of
> centered   dataset in Ri
> are
> 30. 10.10,0,0. Standard PCA
> is performed on this dataset.
> What is the variance
> captured by the top two principal components expressed as
> percentage of total
> variance?
> Answer (Numeric):
> Answer
> View

## **Solution(7)**

> **[Extracted Question]**
> 11
> +
> + Ak
> 30 +
> 10
> 40
> S
> 0.8
> 11
> +
> + Ad
> 30 + 10 + 10 + 0 + 0
> 50
> 0.8 X 100
> 80

> **[Extracted Question]**
> Question 11
> 640653992013
> Total Mark
> 0,00
> Type
> COMPREHENSION
> Given the vector
> and the line pAssing through the origin represented
> by the Vector W
> Answer thc given sulqquestions
> Discussions (0)
> Question 12 : 640653992014
> Vlew Parent QON
> View Solutions (0)
> Total Mark
> 3,00
> Type
> Find the length of the projection of x
> Wl
> the line definerl by
> Enter rour ATSWeT correct t0 tWO
> decimal places.
> Answer (Numeric):
> nswver
> Discussions (0)
> Question 13
> 640653992015
> Wmen
> Parent QN
> View Solutions (0)
> Total Mark
> 4.00
> Type
> Calculate the magnitude(norm) of
> roConStructiOn
> error after projecting
> onto the line: defineel by
> oM
> CMAIt
> correct
> Mo
> decital places;
> Answer (Numeric):
> Answer
> Lutet

## **Solution(12)**

> **[Extracted Question]**
> formulae for projection
> Hv]
> Z
> t
> 7
> length of projection
> 2
> Iz} +()
> V12.25
> 12.25
> 4.95
> 7
> 2

**Solution(13)**

> **[Extracted Question]**
> Error vector
> [2] -H7]
> 1
> w
> W
>
> norm
> of error vector
> 2
> (2)
> +
> (2J
> Vo.25 + 0.25
> Vo.5
> 0.71
> 1
> 2
> XTw) w

-
1
T
- x w w 3 - 1 7 2
⟹ Error vector =  x   =   =
wTw 4 2 7 1
2
-
1
2 2
-
1 1
⟹ norm of error vector = ||  2  || =   + = 0.25 + 0.25 =  0.5 ≈ 0.71
1 2 2
2