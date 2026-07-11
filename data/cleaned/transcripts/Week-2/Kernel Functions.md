# **Machine Learning Techniques Professor Arun Raj Kumar Department of Computer Science & Engineering Indian Institute of Technology, Madras Kernel Functions**

(Refer Slide Time: 0:13)

So, this is. So, this is a major issue. So, what is the issue. The issue is the following. So, then<br>the issue is   in R D  may be too hard to compute. When you say hard it is perhaps not in<br>the hardness sense but then the number of features might be prohibitively large that you do<br>not necessarily want to compute  .<br>So, the question then is well unless I compute   it does not look like I am going to be able<br>to apply my PCA. So, I know of course I can apply my PCA when d is much much large by<br>looking at the matrix  but then even if you cannot compute  then does it mean<br>that everything is doomed or is there a way out.<br>Now, here let us notice the fact that the Eigen directions that we are going to compute in PCA<br>is only of that of   this is the matrix for which we will compute the Eigen<br>directions. So, essentially what you really need is  . So, meaning you need a matrix<br>

So, this is. So, this is a major issue. So, what is the issue. The issue is the following. So, then the issue is in R<sup>D</sup> may be too hard to compute. When you say hard it is perhaps not in the hardness sense but then the number of features might be prohibitively large that you do not necessarily want to compute . So, the question then is well unless I compute it does not look like I am going to be able to apply my PCA. So, I know of course I can apply my PCA when d is much much large by looking at the matrix but then even if you cannot compute then does it mean that everything is doomed or is there a way out.

Now, here let us notice the fact that the Eigen directions that we are going to compute in PCA is only of that of this is the matrix for which we will compute the Eigen directions. So, essentially what you really need is . So, meaning you need a matrix where you need the pairwise dot product between any two pair of items.

# (Refer Slide Time: 1:43)

So, if I give you an and . So, what you what is essentially happening is if I give you and some you are mapping to high dimensional space and you are mapping to a higher dimensional space and then both of these are given as input and then we are essentially computing . Now, this would be our and we will take the , Eigen vector vectors of k. So, which means we essentially need . So, the question is this is one way to go achieve this.

So, I this is the input and map it to , with which  I can compute this. Now, is there a direct way to go here meaning without going this way where I compute the first. So, I apply the explicitly compute , and then compute the dot product is there a way I can directly compute the dot product because that is what I need anyway. So, I need to know the dot product in the higher dimensional space.

So, is there a way I can compute this dot product without explicitly computing this . So, this becomes an important question to us because unless we answer this question we would not be able to really apply PCA to you know, non-linear relationships that matter. So, in the sense that if you really want to capture some high dimensional, some complicated p-th power relationship then you must be able to do this but how do we do this.

So, is this even possible this sounds like magic. So, without computing how do I compute is it even possible let us ponder about this for a minute. So, let us take

an example. So, here is an example let us say x is [ ] and is [ ] and now let us say consider this function.

(Refer Slide Time: 4:03)

I am just pulling this function out of the hat  but let us say we consider we want you to consider this function for the moment. So let us say this is the function that we want to care about. So now, what is this this is just this is the dot product. Now, that is that is + + 1+ 2 +2 + 2 .

So, so x is is and is this  complicated looking thing. Now, let us say I collect terms which are dependent on f separately and I look at them as a vector they look like I will tell you why the square root I am doing is a square root

here let us say this is 1 vector and now I am dotting this with another vector which is

.

# (Refer Slide Time: 5:53)

Now, you can see you can verify that this dot product is exactly the same as<br>wherever x is   and x prime is  . Now, interestingly what we have managed to do<br>is that these two vectors are of the same functional form. So, with respect to f and g in other<br>words. So, if I give a general  and  then you take the first component square it second<br>component square it then put a 1 then put a square root 2   and so on you get this<br>mapping.<br>If you do the same thing for   you get this mapping. So, basically I can think of this as<br>phi of x transpose phi of x prime where phi of x equals phi of basically x  is some<br>a,b some vector a,b is just the vector  [  of course if a and b are<br>and   I get this vector if a and b are   and   then I get this vector and then I dot that I get<br>what I want. So, basically what we are able to do. Now, is what we have been able to do is<br>the following.<br>

Now, you can see you can verify that this dot product is exactly the same as wherever x is and x prime is . Now, interestingly what we have managed to do is that these two vectors are of the same functional form. So, with respect to f and g in other words. So, if I give a general and then you take the first component square it second component square it then put a 1 then put a square root 2 and so on you get this mapping.

If you do the same thing for you get this mapping. So, basically I can think of this as phi of x transpose phi of x prime where phi of x equals phi of basically x is some a,b some vector a,b is just the vector [ of course if a and b are and I get this vector if a and b are and then I get this vector and then I dot that I get what I want. So, basically what we are able to do. Now, is what we have been able to do is the following.

(Refer Slide Time: 7:23)

So, this function that I have asked you to consider and this is the main insight. So, at least is an example nevertheless this gives us an insight of an examples give you most insights. So,

is an interesting function because these computes the dot product in a transformed space.

So, where [ ] get mapped to and similarly gets mapped [ . So, so basically, we have mapped x which is in R<sup>2</sup> to which is in R<sup>6</sup> and then we have managed to compute the dot product in the mapped space without explicitly computing these two guys. So, I never had to compute .

(Refer Slide Time: 8:50)

So, because given and I am just doing this calculation. This calculation is which is a two-dimensional vector plus 1 whole square. So now, that is a low dimensional calculation but then the number that results can be interpreted as if I did a high dimensional transformation of and to and respectively and then I to a dot product in the high dimensional space.

(Refer Slide Time: 9:16)

So essentially, we managed to compute without explicitly computing and that this was stressing. So, let me put that down. So, we managed to compute without explicitly computing . So, this should give us some hope that we can actually you know continue this technique and then try to see if we can solve the PCA problem when

you have non-linear linear relationships among features. So, we will do that but before that. So, this is just an example that we to.

So, where is just one example which tries to map a two-dimensional feature to a six-dimensional space but are there other examples. So, because we have a technique or a technique to solve once you have this power to compute dot products in a transformed space it makes sense to look for other examples where you know you can do this general.

So, of course mapping in from 2 to 6 dimension is not that useful I mean I might as well do the exact mapping and then compute the covariance matrix and do all sorts of things but what would be important is if this can be done for a general d dimensional feature where you need the p dimension p-th power. So, can you do that it is the next question we will ask and the answer to that interestingly is, yes and we look at some more examples.

Now, more examples here is another example. So, let us say we have the function some function k which takes and and then it can calculate the following x transpose . So, for some p greater than or equal to 1. Now, x can be in in general d dimension.

### Timestamp: 11:38

Now, the interesting thing is that and we would not really prove this but then this can be shown to be a valid map, valid function. what does it mean to say a function is valid for us. So, when will we say we are looking at valid functions well for us valid means the following. So, that means that there exists some .

So, and this typically, is from d dimension to some  D dimension such that you know if I just compute k(x, which is this quantity here with same as computing it is as if I went to this high dimension using and then did a dot product if such a exists for a k that I give you then well k is a valid function because otherwise if this does not happen I cannot rely on k to compute my K and then take its Eigen vectors and so, on for PCA.

So, this function here is in fact a valid function and it is a worthy exercise to argue this. So, I will give this as an exercise compute explicit of for p =3 and p= 4. How how does these pis look like and what happens to their dimension. So, I mean to convince yourself that this is indeed a valid , you need to comp be able to compute this . So, if you can I mean that is one way to convince yourself if you can exhibit a then that that that you have exhibited is a certificate of validity for this mapping.

So, that there is a transformation where this function is exactly computing the dot products remember not all functions are going to compute dot products in some high dimensional space. I mean I could have given you an arbitrary function but then if you want to convince yourself then one way to do that would be to actually exhibit this file exactly like how we did for p=2 when you had just two features. So, so please do this as an exercise very I mean this will reveal some insights about how the dimension increases as you increase d and p.

### Timestamp: 14:23

One more example and this is perhaps another famous mapping that people typically use in machine learning is the following. So, you your k(x, in this case for some

greater than 0. So, this should remind you of Gaussian pdf in fact sometimes this is also called the Gaussian map but the standard term is also called as the Radial Basis Function.

### Timestamp: 15:06

This is the Radial Basis Function two important points about this. So, the first thing is that<br>can be shown that this is also a valid function to be a valid map again. Valid in the sense that<br>you can exhibit a   where this this is exactly computing the dot products in the higher<br>dimensional space but what is this higher dimension that is actually even more interesting.<br>So, interestingly if you think about this, you might actually be able to kind of see why this<br>makes sense   in this case maps x to 1 infinite dimensional space.<br>So, the higher dimension that we are talking about here is actually infinite dimension. So,<br>infinite dimensional space. So, earlier we said that the dimension where it gets mapped to<br>increases, increases in certain fashion d to the p and so on in fact in this case you can think of<br>I mean you can argue that the   actually maps every data point on infinite dimensional space.<br>So, well whenever there is infinity involved there are a lot of technicalities but you know<br>technicalities aside we do not want to you know dig deeper right now into the technicalities<br>of what does it mean to say space is infinite dimension and so on. Technicalities aside what<br>

This is the Radial Basis Function two important points about this. So, the first thing is that can be shown that this is also a valid function to be a valid map again. Valid in the sense that you can exhibit a where this this is exactly computing the dot products in the higher dimensional space but what is this higher dimension that is actually even more interesting. So, interestingly if you think about this, you might actually be able to kind of see why this makes sense in this case maps x to 1 infinite dimensional space.

So, the higher dimension that we are talking about here is actually infinite dimension. So, infinite dimensional space. So, earlier we said that the dimension where it gets mapped to increases, increases in certain fashion d to the p and so on in fact in this case you can think of I mean you can argue that the actually maps every data point on infinite dimensional space.

So, well whenever there is infinity involved there are a lot of technicalities but you know technicalities aside we do not want to you know dig deeper right now into the technicalities of what does it mean to say space is infinite dimension and so on. Technicalities aside what you can do is you know can think this think of this as mapping a point a data point to a function and I will tell you what this means in a minute and dot products between functions become integrals.

So, sorry because this is an infinite dimensional space you can think of it as if it is a function. So, what is a function? A function is something where you give an input and then out comes

an output and the input can be any real number whereas it’s infinite of them and then in fact uncountably infinite of them and then the output is also a real number let us say. Now, you can think of the whole function itself as an infinite dimensional vector.

So,  if you kind of I mean loosely put all the inputs in a vector then all the outputs also become a huge infinite dimensional vector of course you cannot put down everything you cannot write down everything if it is uncountably infinite and that is why you should think of this mapping itself as mapping a point to a function but that is just technicality. Now, how do you do dot products after you map points to functions well because this is infinite dimensional your dot products is essentially a sum but instead of sum in the continuous case it becomes integrals.

### Timestamp: 18:39

So, that is what you do to exhibit that this is in fact I mean a valid map another way to think of why this should be a valid map is to see that your e power x itself can be written as a power series expansion where you have kind of all polynomial powers. So, of course with decreasing contributions nevertheless, you have all powers embedded into itself. So, in some sense you can think of it as you know mapping it to an infinite dimensional space where you have all powers contributing in different ways. So, that is one way to think about this as well.

So, what we have done. Now, is we have kind of given you multiple examples, the host family of examples, polynomial maps and then there is this radial basis map and so on but in

general can we give all these valid maps a name, yes sure we should give these valid maps a name because they will become useful and the name that is used is what is called as Kernels.

### Timestamp: 19:27

So, this is a Kernel Function. Kernel is a is a multiple , I mean it has multiple meanings in mathematics but for our purposes in machine learning we are going to think of Kernel functions as functions which are valid in the way that we described earlier that is they compute dot products in some high dimensional space.

So, we write this as follows any function again loosely writing these definitions given a function k which takes 2d dimensional input and then outputs a number any function such function which is a valid map. So, I am not defining valid again that is what we did earlier that means that there exists a such that this has this dot product interpretation is called a Kernel function.

So, so what is k ( x) if k(x, happens to be which is what we saw earlier. So, this is called as a polynomial curve with power p. So, if k(x, is

. Now, this is called as a radial basis or sometimes it is also called as a Gaussian Kernel. So now, these are specific examples but I think the more pertinent question is I mean it is not necessary that these are the only Kernels which are useful or relevant for our problem. So, maybe there are different non-linear nonlinear combinations which might help us.

#

### Timestamp: 21:45

So, in general we want to ask the question given a function. So, let us say I give you a<br>function k which takes in 2d dimensional vectors as input and then computes a number. Now,<br>how can we say it is a valid Kernel? So, if I give you a function and I ask you well hey is I<br>claim that this is a valid Kernel.<br>Now, how would you be convinced that this is in fact a valid Kernel well we have seen one<br>method already to convince ourselves that. So, that is method 1 which is the standard method<br>where you are going to say that hey you think this is a Kernel well which means there must<br>be some mapping file. So, if I can exhibit such a mapping exhibit a map  explicitly like how<br>we did for the Quadratic Kernel.<br>So, the power 2 Kernel we exhibited that  explicitly and said that   is actually a<br>dot product if you think of it as this map. So, in the mapped space. So, that is one way to, one<br>way to argue this. So, but sometimes this might be hard. So, might be hard sometimes to<br>come up with this explicit mapping might be harder or rather hard sometimes.<br>So, if this is not always possible is there an alternate way we can convince ourselves that a<br>function given function is Kernel because not all functions are Kernels. So, is there a<br>

So, in general we want to ask the question given a function. So, let us say I give you a function k which takes in 2d dimensional vectors as input and then computes a number. Now, how can we say it is a valid Kernel? So, if I give you a function and I ask you well hey is I claim that this is a valid Kernel.

Now, how would you be convinced that this is in fact a valid Kernel well we have seen one method already to convince ourselves that. So, that is method 1 which is the standard method where you are going to say that hey you think this is a Kernel well which means there must be some mapping file. So, if I can exhibit such a mapping exhibit a map explicitly like how we did for the Quadratic Kernel.

So, the power 2 Kernel we exhibited that explicitly and said that is actually a dot product if you think of it as this map. So, in the mapped space. So, that is one way to, one way to argue this. So, but sometimes this might be hard. So, might be hard sometimes to come up with this explicit mapping might be harder or rather hard sometimes.

So, if this is not always possible is there an alternate way we can convince ourselves that a function given function is Kernel because not all functions are Kernels. So, is there a different way to argue this, yes there is and this is given by what is called as the Mercer’s theorem we will not dwell deep into this theorem in this course but then I will at least give you a informal version of this theorem.

#

### Timestamp: 23:48

So, so that we get the essential understanding of this theorem I would not state it in full<br>rigorous mathematical detail but then we will give enough mathematics. So, that we know in<br>practice what it means k which is R d  x R d  to R. I have given a function k and then I am asked<br>if this is a valid Kernel Function is a valid Kernel, Mercer’s theorem says it is a valid Kernel<br>if and only if which is a very powerful theorem. So, that is why it is a powerful theorem<br>because it characterizes validity of a Kernel if and only if two things happen a k is symmetric<br>what does that mean that means that k(x,k(x,  should be same as k(k( , that is this.<br>Now, why should a Kernel be symmetric, well we know that the Kernel is going to compute<br>dot products in some high dimensional space which means  k(x,  has to be   for<br>some  . Now, because dot product is a symmetric operation. So, k(x,k(x,  should also be same<br>as   but then   equals k(k( , . So, it necessarily has to be symmetric.<br>So, if it is not symmetric if I give you a function which is not symmetric in other words if you<br>can find x and   where k(x,k(x,  is not same as k(k( ,  then you can immediately dismiss my<br>claim that k is a Kernel but let us say if it is a symmetric function then that does not<br>immediately mean it is a Kernel already you will have to check one more condition and that<br>

So, so that we get the essential understanding of this theorem I would not state it in full rigorous mathematical detail but then we will give enough mathematics. So, that we know in practice what it means k which is R<sup>d</sup> x R<sup>d</sup> to R. I have given a function k and then I am asked if this is a valid Kernel Function is a valid Kernel, Mercer’s theorem says it is a valid Kernel if and only if which is a very powerful theorem. So, that is why it is a powerful theorem because it characterizes validity of a Kernel if and only if two things happen a k is symmetric what does that mean that means that k(x,k(x, should be same as k(k( , that is this. Now, why should a Kernel be symmetric, well we know that the Kernel is going to compute dot products in some high dimensional space which means k(x, has to be for some . Now, because dot product is a symmetric operation. So, k(x,k(x, should also be same as but then equals k(k( , . So, it necessarily has to be symmetric.

So, if it is not symmetric if I give you a function which is not symmetric in other words if you can find x and where k(x,k(x, is not same as k(k( , then you can immediately dismiss my claim that k is a Kernel but let us say if it is a symmetric function then that does not immediately mean it is a Kernel already you will have to check one more condition and that condition is the following again I will write this in a machine learning way of looking at things but there is a formal way to state this as well which I am not doing .

So, for any data set let us say you consider some data set which has n points there is no restriction on what this data set should be because we could we could have gotten any data

set the matrix k which is an n x n matrix where you have . So, is the Kernel is evaluated at , . So, I give you a data set you are trying to claim if a k is valid Kernel or not.

Now, construct a K matrix where capital is the Kernel evaluated at , . So now, of course this is a symmetric matrix because k itself is a symmetric we have already let us say verified k is symmetric but can we say more about this matrix well the Mercer’s theorem says that this matrix is positive semi-definite well what does that mean, that means that all the Eigen values so, this just means that all Eigen values of k are non-negative. So, if I give you a data set I mean you can pick any data set construct the K matrix as equals the Kernel evaluated at , .

So, that would be a symmetric matrix because Kernel is a symmetric function and now, you compute the Eigen values of this matrix and the claim is that all the Eigen values have to be non-negative. So, well Mercer’s theorem says that these two conditions are not only necessary but they are also sufficient. It is slightly involved to argue the sufficiency side but at least the necessity side it is easier to argue and we will do that in a minute. For instance, we already argued why k should be symmetric it is necessary for k should be symmetric because dot product is a symmetric operation.

Now, can we argue the necessity for the Eigen values of K to be non-negative well we can do that because if I mean we need k to be of the form to be of the form So, which means K should be for some matrix or some phi. So, we do not know what the is but then there is a . Now, if you look at the Eigen values of this we know that they would be same at least the non-zero Eigen values of

.

So, the non-zero Eigen values of this is same as the non-zero Eigen values of

. But then this is just the covariance matrix or the scaled covariance matrix in the

higher dimensional space and we know that the scaled covariance matrix has the property that you know all Eigen values are non-negative. So, simply because they compute you know, the Eigen values equal to the variance in a corresponding Eigenvectors direction and variance is a positive quantity. So, and so the Eigen values of should also be non-negative which means that if k is a valid Kernel then

the K matrix should have necessarily non-zero Eigen non-negative Eigen values it could be zero but then it has to be non-negative.

Now, this this is a argument for necessity. So, both a and b are necessity condition necessary conditions for k to be a valid Kernel but Mercer’s theorem says that these are enough. So, these are also sufficient for k to be a valid Kernel. So, we would not prove Mercer’s theorem but then that is important to know.