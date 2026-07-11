# **Machine Learning Techniques Professor Arun Rajkumar Department of Computer Science and Engineering Indian Institute of Technology Madras Convex functions and Jensen’s Inequality**

(Refer Slide Time: 0:10)

So, it is a quick detour, a very quick high level primer about convex functions. Convexity is a fascinating topic, it has its own, you can do a whole course on convexity, but what we are going to do is only look at the bare essentials, which are necessary for our purposes.

So, what is convexity? Well, can we go first let me put down a picture and say what is a convex function, we want to understand certain types of class of functions which are very popular in machine learning in general, which have a lot of practical applications and one of that set of functions is the convex function. Convex functions have this property, so let us it the picture that one can think of is, something like this, where let us say you have two points, a and a point we will take a different point may be b . And the corresponding values that this function gives or let us say f (a) and f (b) .

Now, what I want to look at is some point here in between, which has value (a + b)/ 2. And I want to understand how does the f ((a+b) / 2) look like? So, it is the functions value is here. So, now, this is one value of interest.

The other value we look at is you imagine as if the function at this point from a to b was not that convex or not that function that we are looking at, but then like a straight line, look at a linear interpolation of this. And then that will give you some value here.

So, that at the point (a + b)/ 2, you get a value for this modified function, which is like interpolating between a and b linearly. So, now, what is well, this is, this value we know is f of let me write it in green f((a + b)/ 2).

What is this value? Can you can guess what this value would be? Well, this is linearly interpolating between f (a) and f(b) , so this is sitting exactly bang in the middle of f(a) and f(b) . So, this is going to be f(a)+ f(b) /2, halfway from f(a) to f(b)  /  2.

Now, from this picture, we see that f((a+ b) / 2) ≤ (f(a)+ f(b)) /2. Now, if this happens for every a , b , that the linear interpolation at two points has a strictly higher value than the function itself, then such a function is called a convex function.

If this happens, then it implies that this function is a convex function, it should happen for every every choice of a and b , I have just shown two choices of a and b now, try to convince yourself that for this curve that you have that I have drawn, you can take any two points, and then this property will hold.

### Timestamp: 03:48

If, if the other side holds, so, if the other way holds that if you have a function like this, which goes the other way, where the linear interpolation has value strictly less than the functions value, then such a function is called a concave function.

So, it is our usual convex mirrors and concave mirrors, if you remember from your high school physics. So, that is the idea. So, for all a , b , what should happen in a concave function is f((a + b)/ 2) ≥ (f(a)+ f(b) / 2). If this happens, then we will call this a concave function.

Now from this, an immediate question is are there functions which are both concave convex and concave? Well, if you look at the definition, it says less than or equal to and greater than or equal to, which means that if there is a function where the inequalities were actually equalities, then It means that it is both convex and concave.

### Timestamp: 04:58

But what does it mean to say that the inequality is equality, it means that f ((a + b)/ 2) = (f(a)+ f(b) /2) for all a,b. And what function satisfies that? Well, that means that the function is linear.

So, the input, you divide by 2, now the output also get added and divided by 2. So, it means it is a, that is the property of a linear function. So, if you have a linear function, well, then if you have a function like this, then I take any 2 points. And then if I linearly interpolate, well, of course, I am gonna get the same value. So, this is both concave, and convex.

The next question is, are there functions which are neither concave nor convex? Well, of course, there are functions which are neither concave or convex, can you think of shape, such a function will help? Well, I am just giving you some shape here for a function, maybe a function like this.

So, it is neither concave or convex, because I can choose 2 points, maybe I will choose 2 points here, where the linear interpolation is below the function value, so it can not be convex. And I will choose maybe a and b, and then I will choose a, b and c, where the linear interpolation is above the function value between b and c. So, it can not be convex also. So, it is neither concave or convex.

### Timestamp: 06:43

So, what we are interested in is convex or concave functions. And one way to think of this is as follows the definition that I wrote down, I am going to write it in a slightly different way, I wrote (a+ b) / 2 functions value evaluated at (a+ b) / 2, I can write it as a/2+ b/2 . So, now if it is convex, then this is at most,  f(a)/2+ f(b)/2.

Now, it happens that if this holds for every a and b, you can actually argue that this happens for any λ, f(λa+(1 - λ)b) ≤ λf(a)+ (1 - λ) f(b), where λ is any value between 0 and 1. So, if the first if you can argue that a function satisfies the first row first inequality, it also should satisfy the second inequality in pictures, this just says that, well, I drew the picture earlier.

So, you have this picture like this, you have a and b. And now we are saying, you can also alternatively, think of the definition of a convex function, as you know, I can take any point in

the line segment joining a and b, in the interval joining a and b, maybe this point here, that point will also be lower than this line.

So, every point here in this region, so every value in that region is lower than the line itself. So, the line segment joining a and b, f(a) and f(b). And so you can generally use any λ the as you vary λ, you are traveling from a to b, if λ is 0.

So, then this is b, if λ is 1, it is a and as you change λ, you move from a to b , and then the functions value is always strictly less, I mean less than or equal to the linear interpolation. So, of course, concavity also has a similar property, I would not write it, but then you just reverse the inequality.

### Timestamp: 09:07

Now, you can extend this to multiple points as well. So, this once you have this λ now, it also is true. So, if I have not just 2 points a and b, if I have a1, a2, …, ak, now I ask λ1 a1+ λ2 a2+,..., λk ak, where the λs will sum to 1, they are between 0 and 1.

Now for concave functions, I mean, I am writing it for concave but it is true for convex also the other way around and that is implied. So, this will be greater than or equal to λ1 f(a1)+,

𝑘 …,+ λk f(ak). Of course we will assume that f ∑ λi = 1, i = 1 to k and 0 < λi ≤1. 𝑖=1

So, essentially what in a slightly compact notation for concave functions, we are saying that

𝐾 𝐾 f( ∑ λk ak) ≥ ∑ λk f (ak). So, this is just a generalized definition. So, this is what is 𝑘=1 𝑘=1

called as typically should be called as the Jensen's inequality, Jensen's inequality.

### Timestamp: 10:39

One way to think about this is that, let us say you are I mean in if the function is from real to real, this does not really add any great intuition. But then if you if you imagine a function from, let us say, from are 2 dimensional plane, and if you have a concave function, this is kind of telling you that your concave function will somehow curve like this. And if you take any 3 points, it can take any number of points.

Let me explain using some a1, a2 and a3. Now, if you use λ1, λ2, λ3, and then combine these as λ1, a1+ λ2, a2+ λ3, a3, then you are going to get some point in what is called as the convex hull of these 3 points.

So, all the points here in this region can be obtained as some using some λ, like how, as you vary λ in the original, 1 dimensional case, you moved from f(a) to f(b), seamlessly, or a to b seamlessly.

Now, here you can move around in this region, which is called as a convex hull of these 3 points by varying your λ1, λ2, λ3, and maybe there is a point here, which is 0.1 a1,+ 0.5 a2+ 0.4 a3. Of course, the coefficients should add to 1 they should be between 0 and 1, which is

true here. I mean, the representation, I might not have gotten exactly the position correct. But then that is not the main point.

Now, what we are seeing is that, well, if I try to linearize, this curve, it is curving above the linearized version of this. So, if I look at the linearized version, at this point, maybe this is at this point, maybe this value is here, may be this value is here.

Now I look at the linear version of this curve, and the curve actually goes above this, this linear triangle in this case, that is what it means to say. I mean, that is what basically Jensen is saying, so it is saying that this happens, for any set of points you can look at, it is what is called as a convex hull, which is just the set of all points of the form sum over k λk, ak and then the function values about this.

So, the only thing we will need, for our purposes from convexity is this inequality that I put down here. And the reason why this inequality is useful for us, what is the connection to all this to log likelihood of Gaussian mixture model if you are wondering, the connection is the following.

### Timestamp: 13:31

So, the connection is, logarithm which we are using in the likelihood function is a concave function. This is where the connection comes from, which means that it satisfies Jensen's so why is logarithm a concave function? So, take this as an exercise. So, we have put down the definition of concavity, function being concave.

This is one way to define convex concavity, they are equivalent definitions, but you just looking at this definition, can we prove can you prove that logarithm is a concave function take this as a quick exercise as a homework problem.

What we are now interested in let us assume logarithm is a concave function. That is the let us assume that fact. Now how can we exploit this basically, Jensen's, which is what we want to exploit for performing maximum likelihood and we will see why it might make sense to do this.

It should also already somehow hint as to what we are trying to do? We are thinking of a some inside logarithms and that was causing the problem. And now Jensen's kind of tells us that well, you can write it as combination of you know, can remove the sum inside the logarithm inside the function.

That is what Jensen's is telling us. Of course, at a cost, this is not an equality this is greater than or equal to so that has to be somehow dealt with. But somehow this is kind of making perhaps making life easier for us that is the hope and let us see how that actually happens.