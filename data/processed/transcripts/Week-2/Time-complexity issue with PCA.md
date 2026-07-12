

# **Machine Learning Techniques Professor Arun Rajkumar Department of Computer Science and Engineering Indian Institute of Technology, Madras Time-complexity issue with PCA** 

(Refer Slide Time: 00:15) 



What is issue 1? It is a large d. In particular you can think of d is much much larger than n. So, d is the number of features and n is the number of data points. So, let us do some, I mean notational simplification. This will really help us, solving this issue. So, let us start by giving some, defining some matrices. The first matrix is the matrix of the data points. 

Let us say we have the data set which has , , ….. . So, let us say we stack these data points as vectors, d dimensional vectors in columns next to each other. So, that is my data set itself represented as a matrix which is a d x n matrix. Now, the covariance matrix, we know 

is . 



(Refer Slide Time: 01:33) 






Now, I want to write this covariance matrix in terms of this matrix that I have defined here<br>and that is possible, not too hard to see. So, if you look at  , now, which means that means<br>that you are taking a d x n matrix and then multiplying it with an n xd matrix which is the<br>transpose of the data points where the data points are all rows now.<br>Now, this is exactly  . So, this is perhaps you are already seen why this is the k’s,<br>if not try to show this. So, try to show this exercise. All I am saying is that your covariance<br>matrix which is  , this summation can actually be expressed succinctly in matrix<br>notation as   transpose. That just implies that our covariance matrix is just  .<br>So, say any d check,   is d x n,  is n xd,  is d x d which is also the dimension of our<br>covariance matrix. Of course, we are dividing it by n that is needed I mean standard<br>definition needs you to either divide by n or (n -1) does not really matter, we will stick to n at<br>least in this course. So, now, what does PCA do? PCA tries to find the Eigen vectors and<br>Eigen values of the covariance matrix or find the best-fit line which happen to be Eigen<br>vectors and Eigen values of the covariance matrix.<br>

Now, I want to write this covariance matrix in terms of this matrix that I have defined here and that is possible, not too hard to see. So, if you look at , now, which means that means that you are taking a d x n matrix and then multiplying it with an n xd matrix which is the transpose of the data points where the data points are all rows now. 

Now, this is exactly . So, this is perhaps you are already seen why this is the k’s, if not try to show this. So, try to show this exercise. All I am saying is that your covariance matrix which is , this summation can actually be expressed succinctly in matrix notation as transpose. That just implies that our covariance matrix is just . 

So, say any d check, is d x n, is n xd, is d x d which is also the dimension of our covariance matrix. Of course, we are dividing it by n that is needed I mean standard definition needs you to either divide by n or (n -1) does not really matter, we will stick to n at least in this course. So, now, what does PCA do? PCA tries to find the Eigen vectors and Eigen values of the covariance matrix or find the best-fit line which happen to be Eigen vectors and Eigen values of the covariance matrix. 

(Refer Slide Time: 03:24) 






So, let us say   be the Eigen vector corresponding to the k’th largest Eigen value of C and<br>let us call this Eigenvalue  . Now, you have a matrix C and then I am saying that you take<br>the Eigen values of this matrix, arrange them in decreasing order,  is the highest  is the<br>second highest and so on. And   corresponds to the Eigenvector associated with  .<br>Now, what is the equation that an Eigenvector satisfies and Eigenvector is a special direction<br>for a matrix where if the matrix acts on this vector it just scales this vector by some amount.<br>It does not change the direction. So, the direction is either scaling, it could reverse the<br>direction. So, scaling could be negative that is still okay but it does not change the direction.<br>So, which means in equations, it means that  . So, that is the definition of Eigen<br>vector and Eigen value. Now, what we want to understand is, we want to find these Eigen<br>directions which are   to  . Now, what can we say about these  ’s? Where do these<br>live? Where do these Eigen directions live?<br>Of course, they are all d dimensional vectors but can we say something more about where<br>these Eigenvectors live? That is what we are attempting to find now, Now, for that what we<br>

So, let us say be the Eigen vector corresponding to the k’th largest Eigen value of C and let us call this Eigenvalue . Now, you have a matrix C and then I am saying that you take the Eigen values of this matrix, arrange them in decreasing order, is the highest is the second highest and so on. And corresponds to the Eigenvector associated with . 

Now, what is the equation that an Eigenvector satisfies and Eigenvector is a special direction for a matrix where if the matrix acts on this vector it just scales this vector by some amount. It does not change the direction. So, the direction is either scaling, it could reverse the direction. So, scaling could be negative that is still okay but it does not change the direction. 

So, which means in equations, it means that . So, that is the definition of Eigen vector and Eigen value. Now, what we want to understand is, we want to find these Eigen directions which are to . Now, what can we say about these ’s? Where do these ’s live? Where do these Eigen directions live? 

Of course, they are all d dimensional vectors but can we say something more about where these Eigenvectors live? That is what we are attempting to find now, Now, for that what we will do is we will replace C with its definition which is . 



(Refer Slide Time: 05:50) 






Now, what I want to do is this is basically algebra, I will retain this   on the left-hand side,<br>bring the   to the other side and combine this   and   together. I can bring, essentially,<br>bringing that this   inside, it does not depend on i so, it can go inside. So, this whole thing<br>becomes  .<br>If you are not immediately seeing why these two equations mean the same thing, pause this<br>video, just work it out it is. I mean you should be able to convince yourself that these two<br>things are exactly the same. It is just one-step of algebra. Now, mean if you stare at this<br>equation for a while, something interesting becomes clear. So, this is kind of seeing.<br>Now, let me, actually, even I can put this in   inside. So, it does not really matter. So, I will<br>tell you why I do this, yeah. So, both are exactly the same. It is a constant. I mean  it does not<br>depend on I, you can pull it inside. Now, what is this saying? This is telling me that if I want<br>the k’th Eigen direction, so, Eigen direction corresponding to the k’th largest Eigenvalue.<br>Now, I can express that as a summation of some constant times   which means I take the<br>

Now, what I want to do is this is basically algebra, I will retain this on the left-hand side, bring the to the other side and combine this and together. I can bring, essentially, bringing that this inside, it does not depend on i so, it can go inside. So, this whole thing becomes . 

If you are not immediately seeing why these two equations mean the same thing, pause this video, just work it out it is. I mean you should be able to convince yourself that these two things are exactly the same. It is just one-step of algebra. Now, mean if you stare at this equation for a while, something interesting becomes clear. So, this is kind of seeing. 

Now, let me, actually, even I can put this in inside. So, it does not really matter. So, I will tell you why I do this, yeah. So, both are exactly the same. It is a constant. I mean  it does not depend on I, you can pull it inside. Now, what is this saying? This is telling me that if I want the k’th Eigen direction, so, Eigen direction corresponding to the k’th largest Eigenvalue. 

Now, I can express that as a summation of some constant times which means I take the data point multiplied with some number and then add up all these scaled versions of . In other words, this is essentially telling me that my is a linear combination of data points. So, we are going to assume is not 0 that. So, let us do that without loss of generality in this particular k’s. So, because otherwise this is going to not, I mean, this is going to be infinity and then that would not make sense. But for 0 this is true. 



Now, the interesting thing is that, is a linear combination of data points. Which means that somehow you need to combine your data points to get your Eigen directions. Now, for different Eigenvectors the way you combine these data points are going to be different. Now, what we care about in PCA is to get these Eigen directions which means now we can say that equivalently we can care about getting these combinations of these data points which give these Eigenvectors. 

Because once I have the Eigen vectors then I know how to get a compressed representation and all that, I can project each data point on to the Eigenvectors we know that. We know what to do once we have ’s. But now, to get these ’s itself what we are saying is that it suffices to find that combination of these data points that will give me the ’s. So, what does that mean? 

(Refer Slide Time: 09:16) 








That means that we can say our   equals our matrix  , which is remember the matrix of the<br>data point stacked in columns multiplied by some   for some   in R n . Now, what does this<br>mean? This simply means that remember, our data point is like this. So,   to, sorry, there<br>matrix   is like this   to  .<br>Now, I am saying there is some   which is in R n  which means that it gives some weight to<br>each of this data point. The k says that it corresponds, these weights corresponds to the<br>Eigenvector  . So,   to  . Now, if I multiply this, this is just  .<br>Of course, we know what this   is. So, this equation tells us that these weights are exactly<br>. But then to get these weights from this equation, it appears that you already need to<br>know  . So, this is  , you need to know  to find w. That is a chicken and egg<br>problem. We cannot use this equation to directly find these weights because this equation<br>needs what we are trying to find in the first place which is  .<br>So, let us leave this equation out. We are saying here that is there a different way that we can<br>somehow find this  ’s. We first recognize that there are these  ’s which exactly is this but<br>

That means that we can say our equals our matrix , which is remember the matrix of the data point stacked in columns multiplied by some for some in R<sup>n</sup> . Now, what does this mean? This simply means that remember, our data point is like this. So, to, sorry, there matrix is like this to . 

Now, I am saying there is some which is in R<sup>n</sup> which means that it gives some weight to each of this data point. The k says that it corresponds, these weights corresponds to the Eigenvector . So, to . Now, if I multiply this, this is just . 

Of course, we know what this is. So, this equation tells us that these weights are exactly . But then to get these weights from this equation, it appears that you already need to know . So, this is , you need to know to find w. That is a chicken and egg problem. We cannot use this equation to directly find these weights because this equation needs what we are trying to find in the first place which is . 

So, let us leave this equation out. We are saying here that is there a different way that we can somehow find this ’s. We first recognize that there are these ’s which exactly is this but then let us forget that it is this for the moment. But is there a different way you can somehow get these s. 

Because, if these weights, how should I weigh these data points to combine them to get my that is all I need. So, I to get my . So, somehow if I can get these s then I am done. 

And there is an for each k. So, remember that. Because for each there is a different set of weights. You have to combine the data points differently to get our ’s. 

Now, how can we get these ’s? That is the how to get ’s, this is the question. Once we have this, once if we can somehow efficiently get ’s which does not require order of d<sup>3</sup> computation then we are in business. Because the whole point was our Eigen vector solvers are going to take order of d<sup>3</sup> where d is the dimension, d is the dimension or the number of features. 

If we can somehow get without spending d<sup>3</sup> time then that is a good thing to do. So, how can we do that is the question. So, we will do some algebra here. It is more the algebra I will do it for completion sake but then what comes out of it is more important. But I would definitely suggest you to try and follow the algebra as we do it. 

(Refer Slide Time: 12:27) 



So, we have . We know that. We do not know what is but we know that there will exist some which is what we are trying to find. So, let this be right here. So, we know . That is by definition of the Eigenvector, is an Eigenvector. It has to satisfy this. We wrote C as this, .this is something that we wrote earlier. We also are saying . That is what we observed in just a minute ago. So, this is . 

(Refer Slide Time: 13:16) 






Let me bring the n to the other side and write this as  . Now, what I<br>would do is at this step is pre-multiply this equation by  . In other words, I am saying, I will<br>do   times whatever was there equals   time whatever was there. And what is there was<br> and we will see why this is useful in a minute,  .<br>Now, if I rearrange terms, this is I can do this, I mean I cannot, matrix multiplication is not<br>commutative always, so, I cannot swap terms but I can change the brackets. So, it is<br>associative. So, I can change the brackets however I wish. In other words, I can do it<br>. Basically, I am combining these two guys and these two guys into   equals<br>is a constant that can come outside. This   multiplies this  ,  .<br>

Let me bring the n to the other side and write this as . Now, what I would do is at this step is pre-multiply this equation by . In other words, I am saying, I will do times whatever was there equals time whatever was there. And what is there was and we will see why this is useful in a minute, . 

Now, if I rearrange terms, this is I can do this, I mean I cannot, matrix multiplication is not commutative always, so, I cannot swap terms but I can change the brackets. So, it is associative. So, I can change the brackets however I wish. In other words, I can do it . Basically, I am combining these two guys and these two guys into equals is a constant that can come outside. This multiplies this , . 

(Refer Slide Time: 14:39) 






Now, this is a matrix. Now, remember  was in R d x n. So,   is in, this is  n xd, x is d<br>x n, so, this is n x n. So, that is just to remember. Now, call   let us just give it a name, let<br>us call it K. Then this equation is  . So, we want the   somehow and we are<br>saying whichever   that is that you need to use to combine these data points to get   should<br>satisfy the equation  .<br>(Refer Slide Time: 15:37)<br>

Now, this is a matrix. Now, remember was in R d x n. So, is in, this is n xd, x is d x n, so, this is n x n. So, that is just to remember. Now, call let us just give it a name, let us call it K. Then this equation is . So, we want the somehow and we are saying whichever that is that you need to use to combine these data points to get should satisfy the equation . (Refer Slide Time: 15:37) 

In other words, if we can find that satisfies, there is a k on both sides, so, I am saying, if we can find an that satisfies then we can multiply by K on both sides and it 



would have satisfied the other equation as well. So, which means that all we need to find is an that satisfies . If we can do that then we are kind of done. 





Now, this looks like an Eigen equation. So, this looks like an Eigen equation. In fact, this is an Eigen equation. So, basically, we are saying that, if you take whatever this is, if I apply this K matrix to this , it has to scale this by . So, if I can find such an then I am done. So, this is an Eigen equation. Now, let us say, I give you an . So, I give you something and then claim that, that satisfies this equation. 

So, let us say I give you some vector u and then it satisfies this equation that , let us say. Now, is this u unique? No. So, now, what I can do is I can do will satisfy . Now, what does this tell us that every, I mean, I can scale this u by any number and then it will still satisfy this equation. 

So, which means that we need a specific way of combining these data points. So, specific alpha that will give us a . We know that the length of is 1. So, we were looking for directions with length 1. Now, which means that there should be something that we can say about the length of also or in general also. So, which means that you cannot arbitrarily scale this u that satisfies this equation and claim that all of these are ’s. So, now, what is that? What does that tell us is what we are trying to find out? 

(Refer Slide Time: 18:14) 





Let us try to find out how the length of gives us an indication of what is the length that we should look for, for . What do we know? So, we know . We saw that. So, we know that is some combination of this which means which is the length is . Now, this is . We know that we are looking for ’s with the length 1 which means the left-hand side is 1. On the right-hand side, this shows up which is what we are calling as K. Which means this is . 

So, now, we are saying that we need an that satisfies this equation but it can not be any , such an should also satisfy . If you find an that satisfies this equation and if that satisfies then that is the that corresponds to which has length 1. 

So, all this is algebra. All that we are saying is that we wanted , we are saying we we can equivalently solve for . And solving for looks like solving for an Eigen equation in K. But then the Eigenvectors length is unspecified. So, we need to normalize the length and then the fact that ’s of length 1 implies that . So, we should look for ’s Eigen equations but then you should also have this property. So, this is first point. 

(Refer Slide Time: 20:42) 





So, which means, so, now, we need one more important theorem from linear algebra which will actually be very very useful in understanding, in solving, in completing this problem. And that fact, I mean this is a linear algebra fact or actually a theorem but I will state it as a fact for now. And we will see why this fact is useful. 

So, essentially before I state this fact, so, let me say why we need this fact. Essentially, we wanted the Eigenvectors of but now we are saying we can solve the Eigen equation of K, where K is just . Now, somehow this also involves . We need to know which is the Eigen value of . But then we are only solving the Eigen equation for . 





So, now, is there a relation between the Eigen values of and ? So, because if we solve the Eigen equation for K that will give you a set of Eigen vectors and Eigen values, how are these Eigen values related to the Eigen values that you would have gotten had you solved the Eigen equation for . That is the question we are asking. 




how are these Eigen values related to the Eigen values that you would have gotten had you<br>solved the Eigen equation for  . That is the question we are asking.<br>And the answer is this linear algebra fact. The non-zero Eigenvalues of   and   are<br>exactly the same. So, now, to make it precise, so,   e is a vector, it is a matrix in d xd,<br>is a matrix in n xn. But because both of these come from the underlying x which is d x n their<br>Eigen values are related.<br>In fact, if you are aware of the singular value decomposition of matrices then you can simply<br>use that to prove this in two steps. I would not do that. Feel free to try this. But what I am<br>saying is that the non-zero Eigenvalues, there might be 0 Eigen values because this is d x d,<br>this is n x n, so, the maximum number of non-zero Eigen values of these matrices will be the<br>minimum of d and n. That is again a linear algebra fact.<br>So, there is going to be a lot of zero Eigen values if d is large. But which there would not be<br>corresponding Eigen values in n. So, if n is smaller than d then and if your matrix has full<br>length, so, then your number of non-zero Eigen values will be n and they will match with the<br>top n Eigen values of   which is a d x d matrix. So, what does this essentially tell us? So,<br>what is all of this telling us now? It is telling us the following. And this is the most important<br>thing.<br>

And the answer is this linear algebra fact. The non-zero Eigenvalues of and are exactly the same. So, now, to make it precise, so, e is a vector, it is a matrix in d xd, is a matrix in n xn. But because both of these come from the underlying x which is d x n their Eigen values are related. 

In fact, if you are aware of the singular value decomposition of matrices then you can simply use that to prove this in two steps. I would not do that. Feel free to try this. But what I am saying is that the non-zero Eigenvalues, there might be 0 Eigen values because this is d x d, this is n x n, so, the maximum number of non-zero Eigen values of these matrices will be the minimum of d and n. That is again a linear algebra fact. 

So, there is going to be a lot of zero Eigen values if d is large. But which there would not be corresponding Eigen values in n. So, if n is smaller than d then and if your matrix has full length, so, then your number of non-zero Eigen values will be n and they will match with the top n Eigen values of which is a d x d matrix. So, what does this essentially tell us? So, what is all of this telling us now? It is telling us the following. And this is the most important thing. 

# (Refer Slide Time: 23:44) 



We will now try to put everything together and see all of these together. So, we initially had C which was whose Eigen vectors and Eigen values we wanted. So, let us say the Eigenvectors of C where to , some which we want. So, now, for all k in from 1 to l we know w k is 1, the length is 1. 

Now, the Eigen values corresponding to this are , in fact, they are in decreasing order, > >…… . So, this is what we wanted to get. Now, X, let us look at , is just nC. Now, what will be the Eigen vectors of length 1 for . 

They can they will exactly be again to . It is just X, the matrix is just scaled. So, the Eigen values will scale accordingly but the Eigenvectors of length 1 will stay the same. The Eigen values will n > n >…… n . So, we need this to somehow. 

(Refer Slide Time: 25:17) 





Now, what are we saying? We are saying we need to solve an Eigen equation of . This is the matrix which we care about. Now, let us say the Eigenvectors of happen to be some vectors to , some Eigenvectors. Now, what we know? We know that all the Eigenvectors length is 1. All of these guys are of length 1 and let us say, now, what are the corresponding Eigen values. 

Now, the fact, linear algebra fact that I stated before says that and have exactly the same non-zero Eigenvalues. Which means the Eigen values of will also be n > n >…… n . So, this we have. So, now, what does this mean? This means that this is K. 



So, which means that . So, we have found an Eigen vector which satisfies . Now, question is what we wanted. We wanted some ’s which satisfies . 



Now, here is something which satisfies, we found a which satisfies . But, is = ? Can we solve the Eigen equation like this and say is same as ? Well we saw that there is a length constraint also on this ’s. It is not just the fact that it has to satisfy this equation, it also has to satisfy . 

(Refer Slide Time: 27:30) 



So, which means, now, let us check with . So, now, what is , what is this value? If was then this has to be 1. But what is this? By the virtue of the fact that is an Eigen vector of K, so, is . So, this is . 





But we know beta k is of length 1. So, this is just . So, 



is actually . But then we wanted, if we said is then it is not going to work because then no longer . So, there is a scaling of that is happening. 





So, which means we can set as . If you do this, now, if once I set this for all k, now, and . Why? Because is simply . But we know the numerator is that is what we argued here, divided by . This is just 1. 

So, now, this is kind of telling us, how to convert your Eigen solutions for this matrix k into the that we really needed. We will talk about why this is a useful thing to do. So, we are kind of going in circles and trying to find but then I will tell you why this is a good thing to do in a minute. 

(Refer Slide Time: 29:40) 



So, now, here is what is the algorithm that we are proposing. So, our input is just the data set d which is { ,….. } , where all 's are in R<sup>d</sup> and the assumption is that d is much much larger than n. So, this is the setup that we are in if we have too many features. That is where the time complexity is a problem. Now, what are we saying? 

We are saying that step 1, earlier, we would have computed the covariance matrix and then we would have computed the Eigenvectors and Eigenvalues. We no longer want to do that because it is expensive. So, what is the step 1? Step 1 compute . So, K is in R<sup>n</sup> x n. Step 2. Compute Eigen decomposition of K. 

Now, this is still an Eigen decomposition. Well we wanted to avoid a costly Eigen decomposition but then we are saying in step 2, we are doing an Eigen decomposition of K. But note that K is an n x n matrix. Which means the Eigen decomposition of K is only going to take order of n<sup>3</sup> . 

And if d is much much larger than n, essentially, what you are saying is that instead of doing a d<sup>3</sup> Eigen decomposition you can do an n<sup>3</sup> d Eigen decomposition. So, which might be much 

cheaper, in general. So, we do Eigen decomposition of K and we get Eigen vectors to with corresponding Eigen values. These are Eigen vectors, n …… n . 



(Refer Slide Time: 31:44) 




Once you have done this, so, this is an order of n 3  computation. So, once this is done this then<br>we are almost done. So, step 3. We know that these ’s are not exactly  ’s but then you<br>have the Eigen values also with. So, what you can do is set   for all k equals 1 to l.<br>That is it.<br>So, once you have this then you can get back your w's if you want. So,  . So,<br>essentially, what we have done is we have gone in a different row root to find our<br>Instead of directly solving the Eigen decomposition, we are solving a different matrix, a<br>related matrix, the Eigen decomposition of which is cheaper.<br>And then we are getting the Eigenvectors and then converting that into the weights that you<br>need to combine the data points to get the Eigen directions of the covariance matrix. Now,<br>this is pretty much solving problem number 1, issue number 1. Because we are not working<br>

Once you have done this, so, this is an order of n<sup>3</sup> computation. So, once this is done this then we are almost done. So, step 3. We know that these ’s are not exactly ’s but then you have the Eigen values also with. So, what you can do is set for all k equals 1 to l. That is it. 

So, once you have this then you can get back your w's if you want. So, . So, essentially, what we have done is we have gone in a different row root to find our ’s. Instead of directly solving the Eigen decomposition, we are solving a different matrix, a related matrix, the Eigen decomposition of which is cheaper. 

And then we are getting the Eigenvectors and then converting that into the weights that you need to combine the data points to get the Eigen directions of the covariance matrix. Now, this is pretty much solving problem number 1, issue number 1. Because we are not working with a huge d x d matrix but then we are working with smaller n x n matrix. 

Of course, this is helpful only if d is much much larger than n. If n is larger than d, you might as do the covariance matrix decomposition. But then we are in that setup where we are assuming that d is much much larger than n and then we are trying to do this. So, this solves issue 1, the time complexity issue. 

Now, note that you cannot, I mean you cannot get away with the Eigen decomposition completely. So, you have to do it. But then because there are only two important parameters in this matrix, one is d, one is n. We are just trying to make it as simpler as possible by picking the smaller one of, smaller of these. So, that is all issue 1. 

Now, we want to talk about issue 2 in the next video. But before going there, I would want to make one observation which I will again make in the next video but then I want to hint it at this point and then we will come back and connect it to the next video. Now, what are we saying here, we are given this data set, the first step was to compute Kas . So, what is in that case? 




this point and then we will come back and connect it to the next video. Now, what are we<br>saying here, we are given this data set, the first step was to compute Kas  . So, what is<br>in that case?<br>is  . You can verify that this is what  j would be, so, for all i ,j. In some sense, this is<br>capturing the similarity between   and  , in the dot product sense. More importantly, this<br>also tells us that to solve the PCA problem, you only need these pairwise dot products<br>between the data points. If you have that you have all the information that you need to<br>compute the PCA things.<br>So, whatever you want in PCA. We will make this more precise next time and then we will<br>see that this important observation of the fact that you only need this kind of a similarity<br>between these data points and not necessarily the data points themselves always plays a very<br>important role in trying to use the solution of issue 1 to actually solve for issue 2 which is a<br>totally different question. It says that what if the data points are not linearly related. It needs<br>some creative thought to take this solution and then solve issue 2 and that is, in fact, one of<br>the very important ideas in classical machine learning and we will talk about that in the next<br>video.<br>For now, I would want to summarize saying that all we have seen today is this set of videos is<br>to see how we have identified some issues with PCA and then how you can solve the issue of<br>time complexity by converting your original problem into a simpler problem in a<br>

is . You can verify that this is what j would be, so, for all i ,j. In some sense, this is capturing the similarity between and , in the dot product sense. More importantly, this also tells us that to solve the PCA problem, you only need these pairwise dot products between the data points. If you have that you have all the information that you need to compute the PCA things. 

So, whatever you want in PCA. We will make this more precise next time and then we will see that this important observation of the fact that you only need this kind of a similarity between these data points and not necessarily the data points themselves always plays a very important role in trying to use the solution of issue 1 to actually solve for issue 2 which is a totally different question. It says that what if the data points are not linearly related. It needs some creative thought to take this solution and then solve issue 2 and that is, in fact, one of the very important ideas in classical machine learning and we will talk about that in the next video. 

For now, I would want to summarize saying that all we have seen today is this set of videos is to see how we have identified some issues with PCA and then how you can solve the issue of time complexity by converting your original problem into a simpler problem in a computational sense and solving the simpler problem will help you solve the original problem. We will talk more about issue 2 in the next video. Thank you.
