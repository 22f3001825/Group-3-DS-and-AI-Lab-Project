

# **Machine Learning Techniques Professor Arun RajKumar Department of Computer Science and Engineering Indian Institute of Technology, Madras Feature Transformation** 

Welcome back, we have been looking at the principal component analysis algorithm. And we were trying to understand some of the issues related with this algorithm, we identified two different issues. One issue was when the number of features is much, much larger than n. That resulted in a computational issue where you had to spend order of d<sup>3</sup> for computing the eigenvectors and Eigen values in general, where d is the dimension of your data. 

And we try to solve that issue by saying that instead of computing the Eigen vectors for the covariance matrix, you could compute the Eigen vectors for an associated matrix, which is the matrix, where is the  data set, a matrix and you can use the Eigen vectors of the to convert it into the Eigen vectors of the covariance matrix. So, that kind of solved issue one. 

(Refer Slide Time: 01:14) 



Now, we will look at issue two, which we also mentioned in a previous video. So, the issue two, that we are going to talk about today is the issue of nonlinear relationships among features. So, we know that PCA is very good at identifying the linear relationships among features. But what, if we just had a nonlinear relationship? To motivate this, let us take a simple example, where we have again, a two-dimensional data, where, let us say the data points were like this. That is the 

data points all lie on the circle, on the, on the circumference of a circle, let us say centered at a and b. 

Now, let us ask the question, what would PCA give? So, if I run the standard PCA algorithm on this data set. What should I expect to see? In other words, what are the most interesting or important directions with respect to, the variance maximization or error minimization that PCA will uncover? What will be the most important direction? So, if you are already seeing it fine. Otherwise, I encourage you to pause and think about this question. I will answer this question now. 




important directions with respect to, the variance maximization or error minimization that PCA<br>will uncover? What will be the most important direction? So, if you are already seeing it fine.<br>Otherwise, I encourage you to pause and think about this question. I will answer this question<br>now.<br>So, what would PCA do? PCA would first center this data set, which means that the center will<br>move from a,b to 0, 0, so the origin will be 0, 0. And then what it would do is it would try to find<br>that direction where if you project this data points, the length of the errors is as small as possible,<br>or the variance is as high as possible. Now, because the points are all around the circle, no<br>direction is more important than other direction.<br>So, I can project my data along this direction, or this direction, or this direction, or this direction.<br>And they would result in more or less the same variance, I say more or less, because depending<br>on the exact data points and how they are spread around the circle, one direction might be<br>slightly better than the other.<br>But in general, all directions are equally important. So, which means the PCA is going to pick<br>one direction that would be based on how exactly these points are around the circle. But let us<br>say PCA picked this direction as  , the most important direction. Now, what would be<br>Well,   we know has to be perpendicular to this  . Well, it would be this direction, let us say,<br>of course, I am assuming a instead of a,b, this is origin centered here.<br>So, now, if we had to do a dimensionality reduction for this problem, using PCA, then what<br>would happen is the following. So, we would compute the Eigen values, which is simply the<br>

So, what would PCA do? PCA would first center this data set, which means that the center will move from a,b to 0, 0, so the origin will be 0, 0. And then what it would do is it would try to find that direction where if you project this data points, the length of the errors is as small as possible, or the variance is as high as possible. Now, because the points are all around the circle, no direction is more important than other direction. 

So, I can project my data along this direction, or this direction, or this direction, or this direction. And they would result in more or less the same variance, I say more or less, because depending on the exact data points and how they are spread around the circle, one direction might be slightly better than the other. 

But in general, all directions are equally important. So, which means the PCA is going to pick one direction that would be based on how exactly these points are around the circle. But let us say PCA picked this direction as , the most important direction. Now, what would be ? Well, we know has to be perpendicular to this . Well, it would be this direction, let us say, of course, I am assuming a instead of a,b, this is origin centered here. 

So, now, if we had to do a dimensionality reduction for this problem, using PCA, then what would happen is the following. So, we would compute the Eigen values, which is simply the variance along each direction that PCA finds and then try to see, how many directions do we need to capture 95 percent of the variance. 

Now, in this particular example, what would happen is your will have, let us say the most variance. But then because all directions are almost similar to each other ’s variance or the 



variance of the data set along would be similar to the variance of the data set along which means that maybe slightly more than 50 percent of the variance would be captured with and slightly less than 50 percent would be captured by . 

Now, this would tell us then that if I use the thumb rule of 95 percent to pick the top k directions, PCA would say in the standard way that you need both directions. Both the directions are important. So, that is what PCA would give. So, it would give and . And both important, it will think both are important actions. 

But the real question is, do we really need two directions here? In other words, do we really need two numbers here. I mean, is the relationship such that you need necessarily to, to capture two directions? Or is there a different way to capture this relationship? So, let us think about that. So, what is the real basic fundamental relationship among the, among these data points, by the virtue of the fact that they lie around a circle, the following is true. The relation between features is the following. So now, any data point I can take in this data set, and it has to satisfy , where we say, when I say f1, this is feature 1, the axis y axis is feature 2. 

(Refer Slide Time: 06:15) 



Why because this is the equation of a circle centered at a and b with radius some radius r. So, which means that every data point is on the circle, and so it satisfies this equation. Now, let us 

expand this equation and see what we get this implies, we get . So, this is the basic relationship that that all the data points satisfy. And as we can see, this is not a linear relationship. Why? Because this has f1 squared term, f2 squared term and so on. So, this is not a linear relationship. That is that is obvious from the picture, but also from the equations. 

(Refer Slide Time: 07:04) 



So, now let us do let us try to do the following. Let us take the feature f1, f2, this is just some data point. I mean, maybe f1 is 5, f2 is 10, some numbers, so two numbers. And now what I am going to do is for each point in my data set, I am going to map it to some other data points. So f1, f2, if f1, f2 was my data point in my data set, I am going to map it to a different point. 

And that different point looks like this. So, the first coordinate of this map vector is 1, the second coordinate is , the third is , fourth is , fifth is just , sixth is just (. So, this is a two-dimensional vector that you give me. And then I map it to a 6-dimensional vector, now. 

So now, what is the use of doing this? Why am I doing this mapping? So, for this, let us say you consider this vector u in sixth dimension, let us say you have a 6-dimensional vector, and that vector is the following. So that vector is, and I will tell you why we are choosing this vector [ 1 1 0 -2a -2b] . 

So, this is a sixth dimensional vector that I am choosing, which has nothing to do with the data points. So, well, so it is it is a common vector that I am choosing. It has something to do with the data points, we will see what it is, but it does not use the data points. So, to define this vector, I have not used any of the f1 or f2 of the data points. 

So, now what to be observed from this, so I have given a data point, I have mapped it to a 6- dimensional vector. And then I have also exhibited a 6-dimensional vector, which I am seeing special with respect to this dataset. So, what is so special about that? Well, we know that each of the data points satisfies this equation here, so the star equation here, so because it satisfies the star equation, now you can see that each data point satisfies, =0, where is the mapping that maps this 2-dimensional data point to a 6-dimensional data point. 

Now, once I have mapped f1, f2, which is my specific two-dimensional data point, we put any number here you get a data point on the circle. Well, our data set has if we put any point from the data set, as f1 and f2 then that is the point on the circle. Now, I have mapped that to 6- dimensional feature using . 



So, is a map that is that is defined on all of our, but then for those points that are there in my data set, if I use the map to map it from a two-dimensional space to a 6-dimensional space, then I immediately noticed that all the points in the data set satisfy the equation =0. So, 



that is this implies that the data points are all orthogonal to this vector u in the 6-dimensional space after they have been mapped using this map. So, that is the data points lie in linear 



subspace of R<sup>6</sup> . So, that is the interesting point here. So, so, what we have done is, we have mapped our data points to a high dimensional space. Now, you can verify that the dot product of this is exactly this equation here. So, which means that =0 is same as equivalent to start. So, this is same as done equal, not in place. 

So, because this =0 is a linear equation in the higher of x space, basically, what we are saying is that the data lies in some low dimensional space in this map space. So, you have the data in two dimension, you mapped it to six dimension. And now, we suddenly observed that, well, the data is not really, truly in 6 dimension, it is in a low dimensional space in the 6 

dimensional space. So, now the question is, well, what, what is the use of this? So why? Fine, so, this is fine. 

(Refer Slide Time: 11:56) 





So, but how can we convert this into an idea? Well, here is the idea. The idea is the following. Now, given a data transform features, from low dimension R<sup>d</sup> to high dimension R<sup>D</sup> , so, you have x which is  in R<sup>d</sup> , and now you apply some and then map it to D, where you hope that the data lives in a low dimensional subspace. Now, a big low dimensional linear subspace, so, and because the data lives in a low dimensional linear subspace in this map dimension, now, we know already how to extract this low dimensional linear subspace. 

So, the important directions corresponding to this low dimensional linear subspace, that is what our PCA anyway does. So now, because you are doing this mapping, you are increasing the dimension. So, which means your d could be really large. But now, we already know how to handle the case when d is much larger. 




So, we already know how to handle case when d is much, much larger than n. How do we do<br>that? Well, we know that we have to look at the covariance matrix, but we can look at this matrix<br>which is the other way around. So instead of  , you we will look  in the usual PCA.<br>But now, because the data points are no longer x, they are . So, what you do is you look at<br>. So instead of  , when you say  , it means that I am applying the phi<br>function to every vector in my in my data set. So that is, that is, I mean, a slight abuse of<br>notation. But that is what I mean when I say   apply to matrix it applies column wise.<br>So, so this seems like a great idea. It is in the sense that we know how to solve issue one, which<br>is when d is much much larger, we know how to you know, solve that problem. Now, we are<br>saying that in the case of nonlinear relationships, you map your data points to higher dimensional<br>space, where these nonlinear relationships are captured better. Now, where is the non-linearity<br>coming from? Now, the non-linearity is basically, absorbed into this   map. It is a   map has all<br>possible nonlinear relationships captured.<br>Once you do that, then yes, so in the high dimensional space, you can find a linear relationship<br>using your PCA because B is much much larger than n, you can still run your PCA. So, it seems<br>like a reasonable idea to start with. And it is. So, that is what we are going to see how to convert<br>this into a like a solid idea. But then we will hit a lot of bottlenecks, we will hit a lot of issues,<br>and then we will have to handle them.<br>

So, we already know how to handle case when d is much, much larger than n. How do we do that? Well, we know that we have to look at the covariance matrix, but we can look at this matrix which is the other way around. So instead of , you we will look in the usual PCA. 

But now, because the data points are no longer x, they are . So, what you do is you look at . So instead of , when you say , it means that I am applying the phi function to every vector in my in my data set. So that is, that is, I mean, a slight abuse of notation. But that is what I mean when I say apply to matrix it applies column wise. 

So, so this seems like a great idea. It is in the sense that we know how to solve issue one, which is when d is much much larger, we know how to you know, solve that problem. Now, we are saying that in the case of nonlinear relationships, you map your data points to higher dimensional space, where these nonlinear relationships are captured better. Now, where is the non-linearity coming from? Now, the non-linearity is basically, absorbed into this map. It is a map has all possible nonlinear relationships captured. 

Once you do that, then yes, so in the high dimensional space, you can find a linear relationship using your PCA because B is much much larger than n, you can still run your PCA. So, it seems like a reasonable idea to start with. And it is. So, that is what we are going to see how to convert this into a like a solid idea. But then we will hit a lot of bottlenecks, we will hit a lot of issues, and then we will have to handle them. 

(Refer Slide Time: 15:15) 






The first issue, the most important issue perhaps is the following. Let us say you had four<br>features, and you wanted to capture cubic relations. Think of these four features as height,<br>weight, a gender, let us say. So, when you say cubic relationships, it means that I should be able<br>to capture relationships such as height x weight x gender, or height x weight 2  x age, sorry, not<br>that that would be fourth power, but let us say heightxweight 2 , or weight 2 xh, it is all possible<br>combinations where if you sum up the power of the combinations, there will be 3. So, in this<br>case, so the number of, so basically, if I do the mapping,  , which captures all cubic<br>relationships in remember, there is a different final from the   that we used earlier.<br>Now, this   will have all possible cubic relationships. Now, this is going to be a constant f1, f2,<br>f3, f4, well, these are the relationships which are to the power 1. To the power 2 would have f1,<br>f2, f1, f3, and so on, till f3f4. And then there will be  4 C2 , so this is2 , so this is , so this is 4 C0, this is 0, this is , this is  4 C1, the 4 is the 1, the 4 is the , the 4 is the<br>number of features that you have case,  4 Ck , where k is the number of the power that you are k , where k is the number of the power that you are  , where k is the number of the power that you are<br>talking about.<br>This will be  4 C2, and then there'll be f1 f2 f3, f1 f2 f4, and so on. So, there will 2, and then there'll be f1 f2 f3, f1 f2 f4, and so on. So, there will , and then there'll be f1 f2 f3, f1 f2 f4, and so on. So, there will  4 C3 of these guys. 3 of these guys.  of these guys.<br>

The first issue, the most important issue perhaps is the following. Let us say you had four features, and you wanted to capture cubic relations. Think of these four features as height, weight, a gender, let us say. So, when you say cubic relationships, it means that I should be able to capture relationships such as height x weight x gender, or height x weight<sup>2</sup> x age, sorry, not that that would be fourth power, but let us say heightxweight<sup>2</sup> , or weight<sup>2</sup> xh, it is all possible combinations where if you sum up the power of the combinations, there will be 3. So, in this case, so the number of, so basically, if I do the mapping, , which captures all cubic relationships in remember, there is a different final from the that we used earlier. 

Now, this will have all possible cubic relationships. Now, this is going to be a constant f1, f2, f3, f4, well, these are the relationships which are to the power 1. To the power 2 would have f1, f2, f1, f3, and so on, till f3f4. And then there will be<sup>4</sup> C2 , so this is2 , so this is , so this is<sup>4</sup> C0, this is 0, this is , this is<sup>4</sup> C1, the 4 is the 1, the 4 is the , the 4 is the number of features that you have case,<sup>4</sup> Ck , where k is the number of the power that you are k , where k is the number of the power that you are  , where k is the number of the power that you are talking about. 

This will be<sup>4</sup> C2, and then there'll be f1 f2 f3, f1 f2 f4, and so on. So, there will 2, and then there'll be f1 f2 f3, f1 f2 f4, and so on. So, there will , and then there'll be f1 f2 f3, f1 f2 f4, and so on. So, there will<sup>4</sup> C3 of these guys. 3 of these guys.  of these guys. Then we stop at that, because we only care about cubic features, let us say. So now the total dimension of this map is 1+4+6+4. So, this is<sup>4</sup> C1 ,<sup>4</sup> C2,<sup>4</sup> C3 . Now, the question is, how does this grow? So, if I had d features, so in general, if I had d features, and if I care about the pth 

power, so d features and want model pth power relationship, up to pth power. Let us say, less than or equal to pth power. 

(Refer Slide Time: 17:38) 



Then, how many features would the map have? If you think about it, that it is going to be . That is what it would be. And one can show that this is something like this grow something like d<sup>p</sup> P. Now, what does this tell us? This tells us that if d is let us say, 10, and I cared about some kind of 15th power relationship, let us say, so now that would mean I would the map, would have 10<sup>15</sup> features, the original dimension had only 10. But then in the map space, these are going to be 10<sup>15</sup> . 

So, if you even if you had just two features, but then if you wanted to for whatever reason, your relationships were so complicated that you need 20th power, then it would be you would have to map your two-dimensional feature to a 2<sup>20</sup> dimensional space. And that is going to be simply too hard to work with, so as the numbers the power increases, and as the features increase, so this will become harder and harder.
