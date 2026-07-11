# **Machine Learning Techniques Professor Arun Raj Kumar Department of Computer Science and Engineering Indian Institute of Technology Madras Paradigms of Machine Learning**

### Timestamp: 00:13

So, now these are examples. But now what I want to say is give a high level view of what are the broader paradigms of machine learning? And, then how do these examples fit into these paradigms. So, there are three major paradigms. The first one is called  supervised learning, where in addition to data, you also have some kind of supervision associated with the data.

For example, you might have a lot of emails with you, but then that is just data that does not have any supervision. But then some teacher or labeler, might come and say that, hey, these are the emails, which are spamming,  which the labeler labels, that these emails are spam, and then a bunch of other emails as non-spam emails. Now, you not only have data, you also have the labels associated with them.

And now your problem would be to learn how to differentiate one label from the other. In this
particular case, how to differentiate spam from the non-spam? So, using the data that is available
to you. So, that is what is called as a supervised learning problem where not only the data or the
features are available. In addition, you also have the labels, associated labels.
On the other hand, you might also have an unsupervised learning problem where you are just
given a bunch of dataset, data points, and then you are asked to make sense of that. For example,
if you have a lot of pictures, like the one that I am showing here, but they do not tell you, what
are the labels for these pictures? Now, what would we do? So, it does not seem like a very well
posed problem at this point.
For instance, you can group animals versus background that could be one way to group pictures.
I mean pictures that have animals in the foreground versus pictures that do not have these
animals. For instance, or it could be, pictures which have dogs can all be together versus pictures
which all have cats. Maybe, pictures which have four animals versus pictures which have six
animals.
Maybe, pictures which have animals, which are white in color versus pictures which have
animals, which are black in color or brown in color. So, whatever it is, or animals which are dogs
versus animals which are cats. So, there are multiple ways to group things. I mean,  basically
what I am trying to get at is, there may be multiple notions of similarity that you might want to
use to group things together.

And now your problem would be to learn how to differentiate one label from the other. In this particular case, how to differentiate spam from the non-spam? So, using the data that is available to you. So, that is what is called as a supervised learning problem where not only the data or the features are available. In addition, you also have the labels, associated labels.

On the other hand, you might also have an unsupervised learning problem where you are just given a bunch of dataset, data points, and then you are asked to make sense of that. For example, if you have a lot of pictures, like the one that I am showing here, but they do not tell you, what are the labels for these pictures? Now, what would we do? So, it does not seem like a very well posed problem at this point.

For instance, you can group animals versus background that could be one way to group pictures. I mean pictures that have animals in the foreground versus pictures that do not have these animals. For instance, or it could be, pictures which have dogs can all be together versus pictures which all have cats. Maybe, pictures which have four animals versus pictures which have six animals.

Maybe, pictures which have animals, which are white in color versus pictures which have animals, which are black in color or brown in color. So, whatever it is, or animals which are dogs versus animals which are cats. So, there are multiple ways to group things. I mean,  basically what I am trying to get at is, there may be multiple notions of similarity that you might want to use to group things together.

So,  once your notion of similarity is fixed, then, so let us say we fix cats versus dogs, then you can kind of try to group pictures, which have only cats, only dogs, both cats and dogs. So, these could be three different groups and for instance, this picture would fall into third category and so on.

So, this way of automatically figuring out groups from data is one example of an unsupervised learning problem. We will see more examples, but this is one, just one example. And the third broad paradigm is what is called a sequential learning; we would not really touch upon this. In this course, nevertheless, I just wanted to put it out there so that we are aware of, what it is that we would not be also seeing?

In this course, sequential learning is where as the name suggests, you do not learn in one shot.
But then you learn in a sequential fashion, meaning you make a decision, you observe a
feedback, and then based on the feedback, you make the next decision, you observe the next
feedback and so on. So, it is not as if all the data along with all the supervision is given to you.
It is as if you are given the data and asked to make a prediction, you make the prediction, and
then the supervision comes, that is the feedback. The feedback is a form of supervision. And now
you look at the feedback and see your own predictions and see what went wrong or what went
well. And based on that, you update your model. So, that you make better and better predictions
over time. So, that is the problem.
So sequential learning, we would not really see that in this course. Nevertheless, it is a good
thing to know at this point. So, each of these three broad paradigms have their subcategories.
Supervised learning, for instance, has classification, which is where the labels that are given to
you are just a finite set of things. For example, spam versus non spam, it is a classification
problem.
You just have two labels, spam as a label, non-spam as a label. Maybe, your number recognition
would be a problem with ten labels. So, 0, 1, 2, 3…. 9. But still, it is  finite, it is not a binary
classification problem. It is not two labels, but then it is still a finite set of labels. On the other
hand, you might have a regression problem where you do not have a finite label, but then you
want to predict, a continuous variable as output.

In this course, sequential learning is where as the name suggests, you do not learn in one shot. But then you learn in a sequential fashion, meaning you make a decision, you observe a feedback, and then based on the feedback, you make the next decision, you observe the next feedback and so on. So, it is not as if all the data along with all the supervision is given to you.

It is as if you are given the data and asked to make a prediction, you make the prediction, and then the supervision comes, that is the feedback. The feedback is a form of supervision. And now you look at the feedback and see your own predictions and see what went wrong or what went well. And based on that, you update your model. So, that you make better and better predictions over time. So, that is the problem.

So sequential learning, we would not really see that in this course. Nevertheless, it is a good thing to know at this point. So, each of these three broad paradigms have their subcategories. Supervised learning, for instance, has classification, which is where the labels that are given to you are just a finite set of things. For example, spam versus non spam, it is a classification problem.

You just have two labels, spam as a label, non-spam as a label. Maybe, your number recognition would be a problem with ten labels. So, 0, 1, 2, 3…. 9. But still, it is  finite, it is not a binary classification problem. It is not two labels, but then it is still a finite set of labels. On the other hand, you might have a regression problem where you do not have a finite label, but then you want to predict, a continuous variable as output.

So, we will see again, some examples of this as we go along. There are other methods of supervised learning like ranking, where you want to rank a set of objects, instead of just prediction, you  want a ranking, or structured learning where the labels themselves might have some structure. Maybe, there are some trees that you wish to predict, and so on.

We would not really be talking too much about the other problems like ranking and structure learning in this course. Whereas we will concentrate more on the basic fundamental ideas, including classification and regression in this course, with respect to unsupervised learning. Well, grouping objects is something that we spoke about, which comes under the topic of clustering.

We will also talk about what is called as representation learning, which is,  how do I represent a
data point in the best possible way. So that something becomes easier, whatever the something
is, depends on what your task is and so on. For example, if it is an image, so image can be
represented as just a bunch of pixel values, maybe that is not the best way to represent it. So,
maybe, can we learn better representation?
So, that recognizing, let us say, a tree in an image, might become an easier task. So, how do we
do this representation learning? Well, it can also be done in a supervised fashion. But then there
is also a notion of unsupervised representation learning which we will talk about in this course.
Sequential learning, I am not really going to dwell deeper in this topic in this course, whereas I
just want to let you know that there are, again, multiple types of sequential learning problems,
depending on what kind of feedback that we get.
Let us say you have a group of experts, from whom you take advice, whether I should invest in a
stock or not, and all these experts give you some advice and based on that advice, you make your
own decision, let us say, go ahead and invest in a stock. And then, you get a feedback, saying
that, well, your investment was wrong. So, meaning the stock actually went down on that
particular day.
Now, that is a feedback that you get, but then that is not a feedback just for you, but also to each
of the experts who made a prediction. So, some experts made up invest prediction, some experts
said, do not invest as their prediction. Now, depending on how the market reacts, you are getting
feedback, not just for your algorithm, but also for these, all these experts. That is what is called

We will also talk about what is called as representation learning, which is,  how do I represent a data point in the best possible way. So that something becomes easier, whatever the something is, depends on what your task is and so on. For example, if it is an image, so image can be represented as just a bunch of pixel values, maybe that is not the best way to represent it. So, maybe, can we learn better representation?

So, that recognizing, let us say, a tree in an image, might become an easier task. So, how do we do this representation learning? Well, it can also be done in a supervised fashion. But then there is also a notion of unsupervised representation learning which we will talk about in this course. Sequential learning, I am not really going to dwell deeper in this topic in this course, whereas I just want to let you know that there are, again, multiple types of sequential learning problems, depending on what kind of feedback that we get.

Let us say you have a group of experts, from whom you take advice, whether I should invest in a stock or not, and all these experts give you some advice and based on that advice, you make your own decision, let us say, go ahead and invest in a stock. And then, you get a feedback, saying that, well, your investment was wrong. So, meaning the stock actually went down on that particular day.

Now, that is a feedback that you get, but then that is not a feedback just for you, but also to each of the experts who made a prediction. So, some experts made up invest prediction, some experts said, do not invest as their prediction. Now, depending on how the market reacts, you are getting feedback, not just for your algorithm, but also for these, all these experts. That is what is called as a full information setting.

And, how do you develop algorithms in this setting to learn in a sequential fashion, is what is called as online learning. On the other hand, you might have a problem where you are a medical

doctor, let us say and the patient with certain symptoms comes in. And then, your algorithm says that, well, there are four different treatments that you can give for this particular patient. And your algorithm says, hey I prefer treatment number two, so depending on the symptoms as a doctor, maybe you take the advice of the algorithm, and then you go ahead and prescribe medication for treatment number two, and then maybe after a week, you know that the patient became healthy or not healthy. So, his health deteriorated, his or her health deteriorated. Now, that is a feedback that you get, but remember, now, this feedback is not the same as the previous feedback that we discussed here. You do get a feedback, but only for the treatment that you gave, whereas you do not know what would have happened had you prescribed a different treatment.

became healthy or not healthy. So, his health deteriorated, his or her health deteriorated. Now,
that is a feedback that you get, but remember, now, this feedback is not the same as the previous
feedback that we discussed here. You do get a feedback, but only for the treatment that you gave,
whereas you do not know what would have happened had you prescribed a different treatment.
So, this is called as a partial feedback setting, you get feedback only for the action that you
perform. This is slightly harder problem in some sense, as you can imagine. And how do you
solve this problem?  Studying algorithms for this problem is what is called as a multi armed
bandits problem and multi armed bandits algorithms who would typically solve this problem.
Again, we would not really cover that in this course.
And the final one, which we will also not cover but it would be good to know is what is called as
reinforcement learning. Here, as I said  typical example, prototypical example is the robot
navigation problem, where at every point in the space the robot has four possible decisions. Go
front, left, right or back and the robot has to make a decision based on where it is placed. And it
has to learn to make good decisions.
So, it has to learn a mapping from its location to a decision, which is typically called as a
mapping from a state to an action. State meaning every possible location is a state and the actions
in this case are just the four actions that are listed before. And this mapping from state to action
is what is called as a policy.
So, and the goal of the robot is  then to learn a good policy that will, eventually take it from one
end of the room to the other end of the room. So, how can it learn a good policy over time by

So, this is called as a partial feedback setting, you get feedback only for the action that you perform. This is slightly harder problem in some sense, as you can imagine. And how do you solve this problem?  Studying algorithms for this problem is what is called as a multi armed bandits problem and multi armed bandits algorithms who would typically solve this problem. Again, we would not really cover that in this course.

And the final one, which we will also not cover but it would be good to know is what is called as reinforcement learning. Here, as I said  typical example, prototypical example is the robot navigation problem, where at every point in the space the robot has four possible decisions. Go front, left, right or back and the robot has to make a decision based on where it is placed. And it has to learn to make good decisions.

So, it has to learn a mapping from its location to a decision, which is typically called as a mapping from a state to an action. State meaning every possible location is a state and the actions in this case are just the four actions that are listed before. And this mapping from state to action is what is called as a policy.

So, and the goal of the robot is  then to learn a good policy that will, eventually take it from one end of the room to the other end of the room. So, how can it learn a good policy over time by receiving feedback from the environment? Because, if nobody tells the robot anything about the environment, it kind of learns everything by doing.

So,  such algorithms are called as reinforcement learning algorithms and the setup itself is called reinforcement learning. Again, we would not discuss that as I mentioned in this course.

### Timestamp: 10:25

So, now quickly, let us try to put back, the examples that we saw earlier into buckets that we
have discussed. Now, the spam versus non spam problem is a classical standard problem, which
comes under the topic of binary classification. It is supervised learning problem, because you
have supervision in terms of labels, the labels are either spam or non-spam, there are only two
possible labels.
So, it is a binary problem. And then, because if you are trying to classify whether it is spam or
not, it is a binary classification problem. On the other hand, if you look at forecasting rainfall,
here, you have a bunch of features, and then you are trying to predict how much will it rain, and
this how much is a continuous number. So, it can rain  2.23 centimeters, or maybe 100.82
centimeters, depending on which location you are in, and so on.
So, that is a continuous number and that is, what is called as a regression problem. So, now there

So, now quickly, let us try to put back, the examples that we saw earlier into buckets that we have discussed. Now, the spam versus non spam problem is a classical standard problem, which comes under the topic of binary classification. It is supervised learning problem, because you have supervision in terms of labels, the labels are either spam or non-spam, there are only two possible labels.

So, it is a binary problem. And then, because if you are trying to classify whether it is spam or not, it is a binary classification problem. On the other hand, if you look at forecasting rainfall, here, you have a bunch of features, and then you are trying to predict how much will it rain, and this how much is a continuous number. So, it can rain  2.23 centimeters, or maybe 100.82 centimeters, depending on which location you are in, and so on.

So, that is a continuous number and that is, what is called as a regression problem. So, now there is also this problem of ordinal classification or ranking type of a problem where you not only have to recommend, decide whether a movie has to be recommended to a person or not, you also has to have to decide in which order they should be recommended.

So, again, you imagine your OTT platform, there is only so much space that the platform can actually use to recommend new movies, maybe five movies, which are shown to you at a time. And, it is critical for the platform that it shows you the right five movies in the right order. So, that  it maximizes the chance of you clicking on the first five movies.

So, if the movie that you like, has been found by the algorithm, but then it is somewhere in the
100th place that is not so useful. So, it also not only has to make the prediction well, it also has to
order these things carefully. So that is an ordinal classification problem. The friends suggestion
problem is a link prediction problem. Imagine a huge network with nodes and edges where nodes
represent people and then edges represent connections or friendship, relation between people.
And now, there are some links or some edges which are missing. Now, the question is, can that
edge actually exist in this network? Meaning,  those people on either ends of this edge, what is
the chance that they might actually become friends if a suggestion is given? That is what the
problem that the algorithm will try to solve, such a problem is called as a link prediction
problem.
Now, the voice/instrument separation is an unsupervised learning problem simply because
nobody is going to tell us  saying that looking at an mp3 at this second, you have a voice playing,
at this second you have an instrument playing. For two reasons, one, it is too tedious to do that
for every second of the mp3, the second reason, being that on several cases, it simply might not
be possible because the voice and the instrument might be playing together. So, now, how would
you say whether that second a voice is second or an instrument second? Typically, that might be
hard. So, can we do this in an automatic fashion? Would that be a question that one can ask?
Grouping pictures and phone is a typical example of a clustering problem, or a grouping problem
where you take a lot of pictures, but then you do not supervise telling that these pictures are of
me, these pictures are of a dog, and these pictures are of a tree or things like that. So, the system
automatically figures out that while these pictures look similar, it would not know that these

So, if the movie that you like, has been found by the algorithm, but then it is somewhere in the 100th place that is not so useful. So, it also not only has to make the prediction well, it also has to order these things carefully. So that is an ordinal classification problem. The friends suggestion problem is a link prediction problem. Imagine a huge network with nodes and edges where nodes represent people and then edges represent connections or friendship, relation between people.

And now, there are some links or some edges which are missing. Now, the question is, can that edge actually exist in this network? Meaning,  those people on either ends of this edge, what is the chance that they might actually become friends if a suggestion is given? That is what the problem that the algorithm will try to solve, such a problem is called as a link prediction problem.

Now, the voice/instrument separation is an unsupervised learning problem simply because nobody is going to tell us  saying that looking at an mp3 at this second, you have a voice playing, at this second you have an instrument playing. For two reasons, one, it is too tedious to do that for every second of the mp3, the second reason, being that on several cases, it simply might not be possible because the voice and the instrument might be playing together. So, now, how would you say whether that second a voice is second or an instrument second? Typically, that might be hard. So, can we do this in an automatic fashion? Would that be a question that one can ask?

Grouping pictures and phone is a typical example of a clustering problem, or a grouping problem where you take a lot of pictures, but then you do not supervise telling that these pictures are of me, these pictures are of a dog, and these pictures are of a tree or things like that. So, the system automatically figures out that while these pictures look similar, it would not know that these pictures are of a human face, or it would not know that these pictures are of a dog.

But then it knows that well, these pictures where this human face looks similar, more similar to each other than the pictures where there is a dog. So, that is a problem of clustering in an

unsupervised fashion. Robot navigation we have discussed, is a reinforcement learning problem. Stock market prediction is an online learning problem because you might have a bunch of friends whose advice you are taking and then you are making a decision.

And then, the stock market reacts at the end of the day, you have a feedback not just for you, but for how all your friends perform. And then you want to learn over time based on that. Of course, as I said, the last two are not something that we are going to, you know, think about in this

course.

### Timestamp: 14:47

So, now let us talk a bit about pre-requisites. The main pre requisites are those that are typically covered in your machine learning foundations course, which are linear algebra, probability, statistics, and basic high school calculus, a little bit of optimization would really come in handy. So, if you have done the ML foundations course already, and then you are coming to MLT, then you are pretty much, you have the pre-requisites, the necessary pre-requisites.

But then if you are watching this without having done an ML foundations course, but then if you know, this pre-requisite material, then you can still most likely follow most of the lectures. The idea is to keep the lecture self-contained as much as possible. I might use some results that you might have seen in a linear algebra class earlier, but then I will try to keep them as self-contained as possible. That will be the goal of this course as well.

### Timestamp: 15:50

To specifically state the goal of this course would be to put them down in points, mainly, what
we want to do is, at a basic level, get a very high-level clear understanding of what various
paradigms of machine learning are the ones that we saw, just a while ago. But then in much more
detail, in terms of algorithms and so on. Again, given a real-world problem, we should develop
an ability to pose it as a relevant machine learning problem.
So, because the applications are endless, so now, you might end up in a situation where you
have, well, you might encounter a problem, which is not the standard machine learning problem
that we discuss in this course. Nevertheless, the ideas in this course should help you, pose the
problem as a relevant machine learning problem, abstract out things, post it in as a supervised
learning problem or an unsupervised learning problem and things like that, and then try to see
which algorithms that we develop in this course, are best suited, and so on.
Of course, one of the major goals would be to understand key machine learning algorithms, their
differences, when what works and why their pros and cons, in situations where one might be

To specifically state the goal of this course would be to put them down in points, mainly, what we want to do is, at a basic level, get a very high-level clear understanding of what various paradigms of machine learning are the ones that we saw, just a while ago. But then in much more detail, in terms of algorithms and so on. Again, given a real-world problem, we should develop an ability to pose it as a relevant machine learning problem.

So, because the applications are endless, so now, you might end up in a situation where you have, well, you might encounter a problem, which is not the standard machine learning problem that we discuss in this course. Nevertheless, the ideas in this course should help you, pose the problem as a relevant machine learning problem, abstract out things, post it in as a supervised learning problem or an unsupervised learning problem and things like that, and then try to see which algorithms that we develop in this course, are best suited, and so on.

Of course, one of the major goals would be to understand key machine learning algorithms, their differences, when what works and why their pros and cons, in situations where one might be better than the other, all these are things that we will discuss in this course. So, we will try to cover in this course; we will lay as solid a foundation as possible. So, there are going to be, theoretical/statistical ideas that we will discuss as much as possible, it will be self-contained.

But then the goal is to make sure that we understand the inner workings of the ML algorithms are not just at a, like a black box level. Of course, we want to appreciate the mathematics involved in these algorithms. And if you have the prerequisites that are just listed before, we typically would be good to understand them. We also want you to develop the ability to implement these ML algorithms from scratch, and demonstrate the relevant output of interest using graphs and plots.

Of course, as part of this course, we hope to give you a lot of non-graded assignments where you can write code to develop these algorithms from scratch, and then, get some relevant results and then try to derive insights from them, and so on, so, of course, the discussion board would always be open. So, the more you discuss in the discussion forums, and so on, the more insight you would gain about these algorithms. So, I strongly encourage that as part of this course as

well.

### Timestamp: 18:31

What I am going to do is give a very, very simple example, something that you might have already seen if you're taking an MLF course. Nevertheless, we will quickly go through this example just to illustrate why these prerequisites are relevant. A simple example would be to take two values from a set of 100 people, one would be their height, and one would be their weight, and then plot it on a two-dimensional plane, you might get a set of points like this.

So, now, let us say your goal is to predict the height of a person, given just a weight, you do not know the height of that person, you want to make a prediction, but you only have the weight as input. Now, how can we use this data to learn a mapping from weight to height? But one simple observation here is that well, on an average, if the weight increases, the height also tends to increase. So, in a linear fashion, so, there is a linear relationship between weight and height.

So, we might want to find out that best linear relationship  that maps the weight to the height, right. So, in some sense, we want to find the line and then now once you have the line, if I just tell you the weight, you can use this line to make the prediction for the height. But the problem is there is not a single line, there are infinite possible lines on the two-dimensional plane. Even if you look at only lines passing through the origins, there are still an infinite number of them. How

do I find which is the best line?

### Timestamp: 19:56

Well, we somehow have to find what is the best line using some criteria. And using that criteria, we will then  find the best line and then use that best line to make predictions. So, essentially what we have done is, we are saying that, well, first thing we said is that the weight and height are linearly related, which means that the structure that relates the weight and height is a linear structure, which means we are looking for lines.

But as you can see, in this data, none of the data points pass through the line, which we think is the best line, yet we think that is the best line. So, one of the major things that would happen when you collect data from a large scale is that there is going to be  noise. So, there is going to be some kind of uncertainty associated with the data, either because of the nature of data collection or because some equipment was faulty, some data was missing.

There could be different reasons why uncertainty could arise. Nevertheless, uncertainty is an essential part that you need to deal with, if you are doing data science. And, that is one other thing to keep in mind. And finally, well, you have data, you somehow have figured out structure, in this case line, somehow you have figured out a way to deal with uncertainty.

And now how do you convert this data into decision? So, how can you figure out that this is the best client? So, what is best? In what sense is it best, these are the things that we need to talk about. So, once we have decided a notion of performance of a line, given a data set, then we can pick that line which performs the best. So, that, so basically, then we can convert your data into

decisions.

### Timestamp: 21:37

So, all these three are essential ingredients of a machine learning to develop a machine learning algorithm. And this is why these three become major pre requisites for this course, to understand structure, we need to understand basic structure, which is a linear structure, which will help us

develop algorithms to understand nonlinear structures later on. But to understand linear structure, we need to understand lines and the calculus of lines, which is linear algebra.

To deal with uncertainty, our  mathematical language to deal with uncertainty is probability. So, we would need probability. And finally, to convert data to decisions, you need to solve a problem that maximizes something or minimizes something. And then you would have to convert data to decisions, which is where your optimization comes into picture. So, these three become key prerequisites for this course.

### Timestamp: 22:44

So, this is a tentative roadmap for this course, most likely, I will try to follow this roadmap. So, basically, you are at the beginning of this course. So, let us assume this is you. And then you have a long way to go before you finish this course. And then, mount your flag on the castle of victory, whatever you want to call it.

So, on the way, you are going to see a lot of levels. So, the first one would be unsupervised learning, which includes representation learning, and then we will talk a bit about clustering in unsupervised learning. And then we will talk about estimation methods specifically tailored for unsupervised learning.

Then we will talk about supervised learning in the second part of the course, some basic algorithms for supervised learning, and some advanced algorithms for supervised learning.

Again, I would not talk about the exact algorithms. Now, as we go along, we will see what these algorithms are. And finally, we will talk about some advanced topics in supervised learning.

So, this would be the high level, roadmap for this course from, where you are right now to where you will be after you finish this course. Of course, there are going to be all these assignments in between, well, it is important that, we test ourselves where we stand, and so on. So, all these assignments will actually help you, understand these ideas that we go over in the course very well. So, that is the overall plan.

### Timestamp: 24:16

The high-level references, when I say high level, because I am not going to follow a single textbook for this course. But these might be useful references. So, for linear algebra, if you want to brush up linear algebra, you can look at the book by Professor Gilbert Strang on linear algebra and applications. For probability, a first course on probability should suffice by Sheldon Ross, which is a great book.

The go to reference, would for this course, would be the pattern recognition and machine learning book by Christopher M. Bishop. Though, we may not follow the notation of that book, we may not follow the order in which ideas are presented as that book, but then whatever we see in this book has a relevant topic in that in the VRML book by Christopher Bishop as well. So, you would be able to do that mapping yourself.

If you just search for things that are being taught in the class in that book, the book is, I think one of the editions of the book is freely available, as well. Another interesting book, which might be very useful for this course, is the mathematics for machine learning book. Again, a soft copy is available, which may available by authors for free, you can look at that.

So, this would try to, combine whatever you might have seen in your machine learning
foundations course, or pre-requisite courses that you might have taken, and then put them in a
machine learning context. So, very nice book, definitely recommend you to take a look at that as
well. Again, as I said, these are references.
These are not, we are not going to be following strictly in a textbook for this course, the class,
the lecture notes should suffice with respect to solving the assignments or solving the exam
problems for this course. But if you want to go over and beyond that, and learn a little bit more
deeper about some of the ideas that are being taught in this class, you can always refer to these
books. So, some of these, for instance, the PRML book would have a super set of ideas that are
being covered in this course.

So, this would try to, combine whatever you might have seen in your machine learning foundations course, or pre-requisite courses that you might have taken, and then put them in a machine learning context. So, very nice book, definitely recommend you to take a look at that as well. Again, as I said, these are references.

These are not, we are not going to be following strictly in a textbook for this course, the class, the lecture notes should suffice with respect to solving the assignments or solving the exam problems for this course. But if you want to go over and beyond that, and learn a little bit more deeper about some of the ideas that are being taught in this class, you can always refer to these books. So, some of these, for instance, the PRML book would have a super set of ideas that are being covered in this course.

### Timestamp: 26:27

So, with that we will stop the high-level introduction part of the course. So, I welcome you all to

the machine learning techniques course and wish you all the best and hopefully see you for the

next lecture. Thank you.