# **Machine learning techniques Professor Arun Rajkumar Department of Computer Science and Engineering Indian Institute of Technology, Madras Supervised Learning**

### Timestamp: 00:14

Hello, everyone, welcome back. Today we are going to look at part 2 of this course. In part 1, we looked at unsupervised learning. And then we looked at a lot of different types of unsupervised learning, including representation learning, clustering, and estimation for unsupervised learning.

Now, we are moving into a totally different paradigm of machine learning, perhaps a popular paradigm more popular paradigm of machine learning, called supervised learning. So, and from this lecture onwards, our focus is going to be primarily on supervised learning, where we learn a lot of algorithms. And we will understand why certain algorithms are better than others, and so on.

So, what is supervised learning? In supervised learning, as we have already seen in the introductory video, nevertheless, I’ll again, recap what is supervised learning. We have a bunch of data points, x1 to xn, where all data points are in Rd. So, this is our usual unsupervised learning data set. So, the same exactly similar, so where you have features, or also called as attributes, statisticians would call it predictors, predictor variables, what not, we’ll stick to features in this course. In addition to this, you also have supervision in terms of what we are going to call as labels.

So, these y1 to yn corresponding to these x1 to xn are what we will call as labels. It is like saying, you have some features, and you also have some labels associated with it. And this labels is the supervised supervision part. So, this is the supervised. This is why it is called supervised learning. In addition to just the data points, you also are given some kind of supervision.

So, what does it mean to say, these labels or supervision what what values do these labels take? Well, there are different types of values this way labels can take, and depending on that, we will have different types of supervised learning problems. If the labels take just two values, let’s say in this they come from the set +1 or -1, or they come from the set 0 or 1 these are almost equivalent most of the times for us, when this happens, such a problem is called as a binary classification problem.

Why? Because there are two labels, the labels can take only 2 values, hence the term binary. And given a new feature, which you will perhaps not seen in your data set, you would want to predict whether the label is +1 or -1. So, you want to classify the feature as falling in the +1 bucket or the -1 bucket. So, hence, it is called as a classification problem.

Because there are only 2 labels, we call it binary classification. Of course, you do not have to necessarily have just 2 labels. But then let us quickly look at an example for binary classification before motivating other types of classification. So, let’s say a simple example for this would be given an email classify, whether it is spam, or non spam. Here, you

somehow convert your emails into some features, we will talk about how to what are good ways to do this later.

But for now, assume that every email somehow has been converted into a bunch of numbers, which you are calling as features. Now, somebody comes and looks at these emails, and tells us that some emails are spam, some emails are not spam. Now, this is our data set, where the spam or not spam classification of these emails are the labels associated they are the y1 to yn. And now given a new email, a spam classifier would like to say if the email is spam, email or non spam email automatically. And so this is a binary classification problem.

As I said, you do not necessarily have to have just 2 classes or 2 labels, you might have multiple classes, for example, there might be a problem where you might have 0 to 9 as your possible classes. Now, what might be an example where this happens? So, if this happens, it is called as multi-class classification. But I would like you to think about an example where you might have the labels from the set 0 to 9. Well, pause and think about it, and I’ll tell you the answer now. One simple example where this might be the labels is digit classification problem. So, you might have a written digit and then you will want to classify what is the digit that has been written.

So, the the image itself is your feature. And then the label is the digit that has been written in this image. Of course, people write the same digit different ways. And still, we would want to recognize this as a learning system. And so this is a multi class classification problem.

In general, you do not necessarily have to have only 0 to 9, this could be 0 to some k, but then a finite set of classes. Example is a digit classification problem where you have labels 0 to 9.

### Timestamp: 05:23

Another popular type of supervised learning problem is when the labels can belong to all real numbers, it can be any number between -∞ to +∞. Now, when this happens, we call this problem as a regression problem. And this is perhaps one of the earliest supervised learning problem, which has a lot of statistical roots to it.

So, what might be an example of a regression problem? Where would you want to have features and then the label says a real number. Again, you can pause and think about it. I will give you one example. This is not the only example. But this is nevertheless a standard example, where you might have let us say, it is features, temperature, precipitation, atmospheric pressure, and things like this.

And then you would want to predict the amount of rainfall that might occur on a particular day. Now, this amount of rainfall is a real number, it can take any value. So, 100.23 centimeters, for example. So, it can take any real number. So, we are going to call this regression problem example, rainfall prediction.

So, we will see that each of these types of supervised learning problems would need different types of algorithms. And I will try to justify why you would need different types of algorithms as we go along in this in this course. But we will start with the perhaps the classically, the earliest supervised learning problem, which is regression.

In this course, what we are going to do is talk a bit about regression for a couple of weeks, and then we will look at binary classification for for a long time. And then I’ll, I’ll kind of

briefly talk about how you can use ideas in binary classification to also come up with models for algorithms for multi class classification. Multi class will not be a very predominant focus in this course, but we will look at some ideas where you can use binary classification techniques to do multi class classification.

Nevertheless, the first thing that we are going to start with today is the problem of supervised learning specifically the problem of regression.