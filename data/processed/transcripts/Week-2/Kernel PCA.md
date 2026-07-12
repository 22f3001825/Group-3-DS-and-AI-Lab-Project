

# **Machine Learning Techniques Professor Arun Raj Kumar Department of Computer Science & Engineering Indian Institute of Technology, Madras Kernel PCA** 

(Refer Slide Time: 0:14) 



So, now putting all these things together, let us actually try to come up with the main algorithm that we wanted to do. We wanted to do PCA, but then where we have these nonlinear relationship between features, and we have discussed kernels as a trick or method to achieve that. So, let us put down this algorithm so that we see everything else in place. 

(Refer Slide Time: 0:36) 








And that will make things clearer. So, this algorithm is what we are going to call as kernel<br>PCA. So, what is the input, the input to this algorithm is as usual the data set { …. } where<br>all  ’s are in R d . Now in addition to this, we also have a kernel function given to you some<br>kernel K, which is which takes any two d dimensional data points and then maps it to a real<br>number. So, that is, we know that it is a valid kernel.<br>Let us say, we have tested Mercer’s theorem and then argued that it’s a valid kernel. So, that<br>is given to us as input. Now, what is the step one? Well, step one, you will do the following.<br>So, compute K. So, K in n x n, where Kij equals your kernel evaluated at the point   , , so<br>ij. So, once we compute the kernel, then what is the next step? Well, we compute the Eigen<br>vectors and Eigen values of this kernel matrix.<br>So, compute, L=let us call them   to  ,   or   does not matter. And nn  to nn  as Eigen<br>vectors and Eigen values of k. Once you have that, now, you can also normalize because we<br>saw this last time, you need a normalization factor for  s because the length of  s is not same<br>as one, which is what the length of   is. So, you need a normalization, you can normalize to<br>get   is  .<br>

And that will make things clearer. So, this algorithm is what we are going to call as kernel PCA. So, what is the input, the input to this algorithm is as usual the data set { …. } where all ’s are in R<sup>d</sup> . Now in addition to this, we also have a kernel function given to you some kernel K, which is which takes any two d dimensional data points and then maps it to a real number. So, that is, we know that it is a valid kernel. 

Let us say, we have tested Mercer’s theorem and then argued that it’s a valid kernel. So, that is given to us as input. Now, what is the step one? Well, step one, you will do the following. So, compute K. So, K in n x n, where Kij equals your kernel evaluated at the point , , so ij. So, once we compute the kernel, then what is the next step? Well, we compute the Eigen vectors and Eigen values of this kernel matrix. 

So, compute, L=let us call them to , or does not matter. And nn to nn as Eigen vectors and Eigen values of k. Once you have that, now, you can also normalize because we saw this last time, you need a normalization factor for s because the length of s is not same as one, which is what the length of is. So, you need a normalization, you can normalize to get is . 



So, you do that, so you have got an is for all k. Maybe I will put this as ,. So, that just confused with other k that we have just an index. So, with how many of our Eigen vectors you want, so that that many alphas you get? So, what would be the step three? 

(Refer Slide Time: 3:11) 







Well, in the original, when we are solving issue one, we said that step 3 now, is you get you got that as 



here, it is going to be . But there is a problem here. So, what is this telling us? Well, if you want then you have to combine your data points in the higher dimensional space using the coefficients that you get from the Eigen computation of your kernel matrix. 

But, the whole point of going through the kernel matrix was to avoid the computation of in the first place, we know cannot be computed. In some sense, if is maps into an infinite dimensional space then you cannot even compute it let alone computational issues. It is simply impossible. So, now, doing this now, this defeats the purpose, so this is a bad idea, because it needs which is what we are trying to avoid in the first place. 



So, this looks like a bad idea, we should not compute . So, what does that tell us? Well, this tells us the following. So, we cannot reconstruct the Eigen vectors of the covariance matrix, why because you need and needs , which we are not, let us say allowed to compute. So, that seems like an issue. 

But, the good thing is that but we can still compute the compressed representation. So, compute or obtain the compressed representation. What do I mean by this? What I mean is that what you may not be able to do is to compute the Eigen vectors of the covariance matrix, but you can still compute the dot product of a or map data points on the Eigen vectors of the covariance matrix. What does that mean? 

Well, how would we actually do the compression? So, if you go back to where we started, we said that we will find these directions and then project our data points along this direction to get these dot products. So, which means that after a in case, if I had the power to compute , I would compute that and then I would do , which is the data point transpose . 



This is the number that I would like to store as the kth most important number corresponding to this data point xi. But I cannot compute . But do I have to is the question, so let us see, 




to this data point xi. But I cannot compute  . But do I have to is the question, so let us see,<br>this is just  we know is just some combination of the data points<br>appropriately weighed by alpha k. So, alpha kj this whole thing then is just<br>, I am just bringing the   inside.<br>Now, this just becomes  . Essentially, this is k of kij. Well, that we already know<br>because now, the dot product of the map data points on to the Eigen direction depends only<br>on the dot products among the data points themselves, which I know already how to compute<br>using my kernel function, I can compute this, this is a good. So, because we cannot of course,<br>reconstruct the Eigen vector explicitly.<br>But we can compute the dot products or the projections onto this Eigen vectors in the high<br>dimensional space. So, now, typically, the reason why you do kind PCA in general is that,<br>you get these projections and then you map you throw away the original data points and only<br>retain these projections along each of these data points.<br>That is where the dimensionality reduction happens. Original data point was 100 dimension<br>but then you only care about the top 5. So, you only you map the 100 dimensional data into a<br>5 dimensional projection onto these 5 most important directions. So, that becomes a 5<br>dimensional representation of your 100 dimensional data.<br>

this is just we know is just some combination of the data points appropriately weighed by alpha k. So, alpha kj this whole thing then is just , I am just bringing the inside. 

Now, this just becomes . Essentially, this is k of kij. Well, that we already know because now, the dot product of the map data points on to the Eigen direction depends only on the dot products among the data points themselves, which I know already how to compute using my kernel function, I can compute this, this is a good. So, because we cannot of course, reconstruct the Eigen vector explicitly. 

But we can compute the dot products or the projections onto this Eigen vectors in the high dimensional space. So, now, typically, the reason why you do kind PCA in general is that, you get these projections and then you map you throw away the original data points and only retain these projections along each of these data points. 

That is where the dimensionality reduction happens. Original data point was 100 dimension but then you only care about the top 5. So, you only you map the 100 dimensional data into a 5 dimensional projection onto these 5 most important directions. So, that becomes a 5 dimensional representation of your 100 dimensional data. 

Now, that you can do even here, so though you cannot compute on what it is being projected on, you can compute the value of this projection. That is what we are essentially saying here. So, the reason why this is that, so let me make a note here for downstream tasks. So, if you want to do this as a pre processing step, for some other, so once you learn that a presentation in a low dimensional space, as just the projections onto these Eigen directions. 

You can use these projection values as, I mean, you can imagine that this is your data point. And then work with this for a downstream task, supervised learning task, which we will see later. So, this is for downstream tasks, this is usually good enough. So, you do not necessarily need to compute the Eigen vectors. 

So, you would need the Eigen vectors only if you want to reconstruct the proxy. So, how would you reconstruct the proxy if I give you the projections? Well, you will multiply the projection with the corresponding Eigen vector and then add them up. So, for that, you need the Eigen vector. And if you need the Eigen vector, then you need , we have to let go of that. So, we would not be able to reconstruct the proxy in the high dimensional space. 

But still, we will be able to store these projections and these predictions are typically good enough for downstream tasks. So, typically, what you do then is just, do not do step 3. So, you cannot do step 3. Instead, your step 3 would just be the following. 

(Refer Slide Time: 9:42) 







So, modified step 3, well, your modified step 3 would be to compute for all k, so 

these are your numbers. So, basically you have your x, which is, f which is an R<sup>d</sup> . Now, what you are doing is you are mapping it to the following. So, you are mapping it to , 





…………. whatever top l that you want. So, this is what xi, let us say, where xi 

data point becomes this, basically. 

So, of course, this K ij is just the ith row of your kernel matrix, what you are doing is you are taking the ith row of your kernel matrix, which kind of tells you how similar is the ith data point to each of the other data points with respect to this kernel, and then you are weightinh the similarities in different fashions given by these alphas, and then storing them as the most important, information corresponding to this data point. 

So, from d dimension, you can reduce it to l dimension, where l is, I mean, you can either reduce or increase does not matter because you are going to a nonlinear higher dimensional space and then reducing the dimension. So, you might go from 2 to 100 dimensional space, and then reduce it to 10 dimensional space. 

So, it might seem like you are actually increased from 2 to 10. But then this increase is necessary to capture the nonlinear structure of your data, it is a low dimensional representation of the maps data points, but which means it might actually increase the original dimension to a higher dimension, nevertheless, it is it might allow you to capture more complicated relationships. 

So, this is the general idea of kernel PCA, there is one small important detail that we kind of missed out on that detail, comes somewhere here. In the original PCA, we assumed that we are given a data set and then you center this data set and then compute the covariance or the kernel matrix and then compute the Eigen vectors. 

Now, here what we are seeing is that we are given a kernel, if the origin of the data is set to centered fine, we apply the kernel which means it is mapping it to a higher dimensional space using some mapping . But now, if you think of this data set , 




using some mapping  . But now, if you think of this data set  ,<br> till   that may or may not be centered. So, that depends on your mapping kernel<br>mapping.<br>It is a valid kernel, which means there is a  , but then there is nothing that we are seeing that<br>is that will make sure that the   that we have which result in a map data, which is also<br>centered, but then we need the center data only then our directions really make sense. So, we<br>need to center the kernel. So, there is an extra step that is needed here, which is center we<br>need to center the kernel.<br>So, which means we only have kernel cannot compute  . So, is there a way to compute<br>slightly different kernel, which will do the same mapping  , but then after mapping<br>it will also center the data. So, is there a function that we can create which will so I give you<br>a kernel, now that kernel will correspond to a   map.<br>So, you want to apply that   map, so you use the kernel, but then you also want to do the<br>centering after you apply the phi map which means, can we mimic these two steps of going to<br>a higher dimension and then doing the centering using just a single function kernel function,<br>which is called as centering the kernel, so that that becomes important.<br>

till that may or may not be centered. So, that depends on your mapping kernel mapping. 

It is a valid kernel, which means there is a , but then there is nothing that we are seeing that is that will make sure that the that we have which result in a map data, which is also centered, but then we need the center data only then our directions really make sense. So, we need to center the kernel. So, there is an extra step that is needed here, which is center we need to center the kernel. 

So, which means we only have kernel cannot compute . So, is there a way to compute slightly different kernel, which will do the same mapping , but then after mapping , it will also center the data. So, is there a function that we can create which will so I give you a kernel, now that kernel will correspond to a map. 

So, you want to apply that map, so you use the kernel, but then you also want to do the centering after you apply the phi map which means, can we mimic these two steps of going to a higher dimension and then doing the centering using just a single function kernel function, which is called as centering the kernel, so that that becomes important. 

(Refer Slide Time: 14:04) 






So, I will just give the details but then these are just details. But, I mean, for the sake of<br>completeness, I am going to give this that you can indeed center the kernels. So, these are<br>details, so how to centering the kernel? The good news is that you can center a kernel without<br>explicitly computing  . So, that is the most important news perhaps.<br>So, given kernel matrix K, which is an n x n, so give you a kernel function from which you<br>create a kernel matrix K for the data set that you have. So, you have n points in your data set.<br>So, kernel matrix is an n x n matrix, where kij is just your kernel evaluated at xi and xj for all<br>ij. Now create a new kernel.<br>So, you want to create a new kernel let us call this Kc, c for centered where Kcij is some<br>function of K but then it does not use the explicit mapping  . It can be done, we would not<br>do the algebra here, but it’s just for sake of completeness, I am saying this that this can be<br>done. And it is good to know how this looks like, though it’s not so important.<br>You take Kij, and then you do the following. I will write it down and then make a<br>

So, I will just give the details but then these are just details. But, I mean, for the sake of completeness, I am going to give this that you can indeed center the kernels. So, these are details, so how to centering the kernel? The good news is that you can center a kernel without explicitly computing . So, that is the most important news perhaps. 

So, given kernel matrix K, which is an n x n, so give you a kernel function from which you create a kernel matrix K for the data set that you have. So, you have n points in your data set. So, kernel matrix is an n x n matrix, where kij is just your kernel evaluated at xi and xj for all ij. Now create a new kernel. 

So, you want to create a new kernel let us call this Kc, c for centered where Kcij is some function of K but then it does not use the explicit mapping . It can be done, we would not 

do the algebra here, but it’s just for sake of completeness, I am saying this that this can be done. And it is good to know how this looks like, though it’s not so important. 

You take Kij, and then you do the following. I will write it down and then make a comment . So, basically, you take the original kernel value Kij and then subtract with something, I mean, you need to do some subtraction. So, there is a mean subtraction happening in the higher dimensional space. And then we are trying to mimic what would happen if you do the mean subtraction and then do the dot product. 

That is essentially what we are saying. So, on that dot product can be achieved by doing some manipulation of the original kernel itself. And that manipulation is, you multiply it with some value , , which is just the average row sum corresponding to the ith data point. And then you do some manipulation, I mean, this 1i, 1j just refers to a vector, which just has one in the jth position and zero everywhere else. 

And then that is an n dimensional vector. So, you basically, well, one can algebraically argue that this is exactly same as doing, mapping the following, so you have { …. }, you apply your kernel, which will map it to { …. }. And then what you do is in the transform space, you do { - …. - }, where is . Now, this is your new data point. 

Now, if you take the dot product of any two data point here, well, that is going to look like . So, that would be +μ^2. So, there are four terms and those four terms correspond to these four guys, essentially, that is what it is. So, this Kij corresponds to this, we already know is Kij. Now, I mean, it is just a matter of algebra to verify that if I set and as this, so then you will be able to get the other three terms as well. It is easy, I mean, it is just algebra, it is nothing, interesting going on here other than just saying that you can do this. So, that kind of completes the most important ideas for this algorithm. 

(Refer Slide Time: 18:37) 








And again, just to summarize, what we are doing now is that kernel PCA would be like this,<br>you are given a kernel, compute the kernel and then you center the kernel, then get the Eigen<br>vectors and Eigen values corresponding to the centered kernel, normalize it, get the  s and<br>once you have the  s, do not construct the Eigen vectors instead, map it to these projections<br>onto these Eigen vectors for each of the data points.<br>So, for every data point at the end, you have the top K projections and that projections, the set<br>of projections is the representation for these data points as per kernel PCA. So, this is a very<br>interesting technique. So, we have kind of used a lot of linear algebra here. But end of the<br>day, all of this works out and we have been able to solve two important issues that we<br>thought about for PCA, one is high dimensionality and the second is non linearity.<br>Surprisingly, the trick that solves both of them is the kernel matrix. You can map to higher<br>dimension and then you can achieve nonlinear relationships as well. So, this kind of matrix is<br>nothing specific to PCA you will encounter this object again and again, in this course,<br>especially unsupervised learning as well, where the idea would be typically solve the problem<br>for linear, when the data is linear has a linear relationship, which is easier problem solve. And<br>

And again, just to summarize, what we are doing now is that kernel PCA would be like this, you are given a kernel, compute the kernel and then you center the kernel, then get the Eigen vectors and Eigen values corresponding to the centered kernel, normalize it, get the s and once you have the s, do not construct the Eigen vectors instead, map it to these projections onto these Eigen vectors for each of the data points. 

So, for every data point at the end, you have the top K projections and that projections, the set of projections is the representation for these data points as per kernel PCA. So, this is a very interesting technique. So, we have kind of used a lot of linear algebra here. But end of the day, all of this works out and we have been able to solve two important issues that we thought about for PCA, one is high dimensionality and the second is non linearity. 

Surprisingly, the trick that solves both of them is the kernel matrix. You can map to higher dimension and then you can achieve nonlinear relationships as well. So, this kind of matrix is nothing specific to PCA you will encounter this object again and again, in this course, especially unsupervised learning as well, where the idea would be typically solve the problem for linear, when the data is linear has a linear relationship, which is easier problem solve. And now use the kernel trick to map it to a nonlinear problem. 

So, here the kernel trick works because our whole algorithm is dependent only on pairwise products and not the exact data points themselves, if we know only the pairwise dot products, I can run this algorithm, which is essentially what the kernel matrix is doing in a high dimensional space. So, as we develop algorithms, we will also see if the algorithm depends only on the pairwise dot products. 

If they do, then it is it suffices to kernelize this algorithm. Here in PCA, we observed that you can run PCA by only considering pairwise dot products and so we kernelized it and that resulted in kernel PCA. Similarly, we will kernelize slightly different other algorithms that we will encounter in this course. 

But that is for later. For now, to summarize, we have a powerful unsupervised learning algorithm for representation learning and that is PCA and its kernel version, which is kernel PCA. Next time we will look at other types of unsupervised learning algorithms, including clustering and some kinds of estimation techniques. Thank you. 




PCA. Next time we will look at other types of unsupervised learning algorithms, including<br>clustering and some kinds of estimation techniques. Thank you.<br>
