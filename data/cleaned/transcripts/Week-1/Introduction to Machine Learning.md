# **Machine Learning Techniques Professor Arun Rajkumar Department of Computer Science and Engineering Indian Institute of Technology, Madras Introduction to Machine Learning**

Hello everyone and welcome to this Machine Learning Techniques course of the online B.Sc. in Programming and Data Science Program. My name is Arun Rajkumar and I will be the instructor for this course. So, what we are going to do now is start with the very high level introduction to what machine learning is. Of course, if you had taken a previous prerequisite course, which is the machine learning foundations course.

You will have a fair enough idea of what machine learning is, what kind of problems are being solved using machine learning. Nevertheless, to keep this course a little bit self-contained what I thought was I will just go through a very high level introduction  to try and give a flavor for what is going to be covered in this course, what types of problems we will try to solve and things like that; so we will get started.

### Timestamp: 01:01

 The first question we’ll ask is  why are you trying to take this course,

what is the reason? There could be several reasons, but one

of the very compelling reasons is that the there are several applications of what you might see in this course. So, for example, the top ten digital transformation trends as listed by Forbes magazine a couple of years back, listed a couple of things  which are highlighted here in red, including analytics, AI and machine learning, conversational AI, autonomous drones, and so on.

All of these things depend on one way or the other machine learning algorithms. As you can see, machine learning is in some sense, fundamental to several applications, practical applications; and you will see many more applications as we go along in this course. So, that is the why part.

### Timestamp: 01:56

So, now you can  also ask how popular is machine learning? I do not have to really answer that question, if you have been following the technical digital trends and things like that. Nevertheless, what I did was, I did today, a search for the term machine learning on Google, Google Trends. And then I also added, I am also showing you the trends for the word search for the keyword deep learning and for the keyword artificial intelligence.

The one in machine learning is blue, deep learning is in red and artificial intelligence is in yellow. And as you can see in the last couple of years, let us say from 2016 onwards, there has been a boom in these in these keyword searches. So, just indicating the amount of popularity and the amount of applications that algorithms and machine learning have had an impact on.

So, of course, deep learning is a subset of machine learning, which will also be covered in one of the elective courses in this program. Artificial intelligence was originally the idea of making a computer trying to, in some sense mimic a human; so you would see a lot of artificial intelligence based searches in the early 2000s and so on, as the yellow curve indicates here.

But, then there as machine learning kind of took over, so the broader term artificial intelligence had gained lesser and lesser popularity. But, now recently with more recent advent of several

new ideas in artificial intelligence, including causality and things like that, so that also has seemed to  have picked up a lot.

### Timestamp: 03:39

So, now let us ask the question, where can we apply machine learning algorithms? So, for this I
would like to imagine a prototypical human being, and the type of activities a human being does.
If you really want machines to learn and mimic humans, we should first understand what are the
things that come naturally to humans; and see how we can make a machine mimic these.
So, for this, one of the main or one of the major areas of areas where machine learning is applied
is in vision, what is called as a computer vision, which just tries to understand  how you can
make a computer see. So, how can you provide the ability of vision to a computer if you will,
which means to understand a very very complicated organ like the eye which has evolved over
several millions of years.
The human eye, where it can take in information, process it using the brain, and then take
decisions based on that. So, now if you want to mimic that, so there are lot of challenges. So, for
example,  how does the human eye kind of look at a picture and then say, hey, this is a picture of

So, now let us ask the question, where can we apply machine learning algorithms? So, for this I would like to imagine a prototypical human being, and the type of activities a human being does. If you really want machines to learn and mimic humans, we should first understand what are the things that come naturally to humans; and see how we can make a machine mimic these.

So, for this, one of the main or one of the major areas of areas where machine learning is applied is in vision, what is called as a computer vision, which just tries to understand  how you can make a computer see. So, how can you provide the ability of vision to a computer if you will, which means to understand a very very complicated organ like the eye which has evolved over several millions of years.

The human eye, where it can take in information, process it using the brain, and then take decisions based on that. So, now if you want to mimic that, so there are lot of challenges. So, for example,  how does the human eye kind of look at a picture and then say, hey, this is a picture of a tree. So, now if you want the computer to do that, to do things like object recognition, so now we need to develop algorithms,  which more or less try to mimic the human eye.

So,  that is a broader area, where you might see machine learning algorithms often being applied. Speech is another thing where, speech is  in some sense an unstructured data; where  different

people say the same thing in different ways, and yet as humans we make meaning out of this. So, very easily naturally over time, we have learned to understand human speech.

Now, , how can we make a computer do the same, that would be learning to understand natural language for instance, that would be the speech part of it. Text is another important source of inputs; documents, there are billions and billions of documents, I mean, millions generated as we speak on the internet; and all of these are unstructured.

inputs; documents, there are billions and billions of documents, I mean, millions generated as we
speak on the internet; and all of these are unstructured.
Again, people write in different ways the same thing, but then, can we somehow understand the
semantics of text. So, from just written text or it could be even simpler problem like, can you
look at a text and then look at the handwriting; and then figure out what is being written in this
and so on. So, there are a broad range of applications there as well.
Of course, the holy grail is to crack the human brain. How does the brain work? So, brain is such
a complicated organ with millions and millions of neurons interconnected in complicated
fashions, and then produces decisions. How can we understand that from a more abstract
computational point of view; so that is how can you learn, like how our human brain learns. So,
that is another major area of course, the holy grail of machine learning.
We are nowhere close to doing that, but then we are making slow baby steps progresses. Of
course, these are the human sensory applications, but then there are several others. So, you can
think of,  any experiment that generates a lot of data is amenable to analysis. In fact, you can
learn and predict from data; so that is the whole idea of machine learning.
Stock markets, financial sector is another major area, where machine learning algorithms are
typically used to predict whether a stock will go up or not; you have to see how the stock has
performed over time, and then make models and then use that to predict and so on. Experiments,
again biological experiments, chemistry experiments, and so many other materials engineering
for instance; so, there are  innumerable number of applications in science and engineering.
Two other examples that I just want to highlight are one in sports. So, sports analytics is a big

Again, people write in different ways the same thing, but then, can we somehow understand the semantics of text. So, from just written text or it could be even simpler problem like, can you look at a text and then look at the handwriting; and then figure out what is being written in this and so on. So, there are a broad range of applications there as well.

Of course, the holy grail is to crack the human brain. How does the brain work? So, brain is such a complicated organ with millions and millions of neurons interconnected in complicated fashions, and then produces decisions. How can we understand that from a more abstract computational point of view; so that is how can you learn, like how our human brain learns. So, that is another major area of course, the holy grail of machine learning.

We are nowhere close to doing that, but then we are making slow baby steps progresses. Of course, these are the human sensory applications, but then there are several others. So, you can think of,  any experiment that generates a lot of data is amenable to analysis. In fact, you can learn and predict from data; so that is the whole idea of machine learning.

Stock markets, financial sector is another major area, where machine learning algorithms are typically used to predict whether a stock will go up or not; you have to see how the stock has performed over time, and then make models and then use that to predict and so on. Experiments, again biological experiments, chemistry experiments, and so many other materials engineering for instance; so, there are  innumerable number of applications in science and engineering.

Two other examples that I just want to highlight are one in sports. So, sports analytics is a big area in itself, where you want to predict which team would perhaps win the next IPL match, would it be Chennai or would it be Bangalore? So, of course being  a Chennai fan, I would say that perhaps Chennai would win, and maybe many of you might agree with that.

Nevertheless, if you want to confirm that with the computers’ prediction; you can take a lot of data and then  run it using algorithms; and then it would give you a prediction as well. And finally, not finally, one other example to just give you a flavor is e-commerce. We all use e- commerce websites on a perhaps on a daily basis; your Amazons and Flipkarts and what not, where you purchase a lot of, you go there to purchase some productand then immediately you get a recommendation saying that if you like this product, maybe you should buy this product as well. So, which means that there is some machine learning algorithm under the hoods, which is trying to figure out, this person is trying to buy this product and there are these people who are similar to this person, who have bought similar products.

a recommendation saying that if you like this product, maybe you should buy this product as
well. So, which means that there is some machine learning algorithm under the hoods, which is
trying to figure out, this person is trying to buy this product and there are these people who are
similar to this person, who have bought similar products.
So, why not recommend that product to this person? So, there is this algorithm at the back which
decides, which kind of predicts, which is the product that should be shown to this person, which
will perhaps maximize his chance of buying it; so that the company can make money. So, these
are some applications of machine learning; there are many more.
And you can think of, I mean, you can try to think of different applications not listed here, by
just observing your workplace or  your areas of interest. I am sure there will be some application
of machine learning, whenever there is a lot of data involved.

So, why not recommend that product to this person? So, there is this algorithm at the back which decides, which kind of predicts, which is the product that should be shown to this person, which will perhaps maximize his chance of buying it; so that the company can make money. So, these are some applications of machine learning; there are many more.

And you can think of, I mean, you can try to think of different applications not listed here, by just observing your workplace or  your areas of interest. I am sure there will be some application of machine learning, whenever there is a lot of data involved.

### Timestamp: 09:27

So, now let us ask the question, what is machine learning? So,  we know why we are learning
this topic; and we kind of know, have a high level view of where, where it is appliedbut then we
want to understand what it is? So, the way I want to think about this is first, let me tell you what
is not machine learning; and then we will try to compare and contrast with what is machine
learning.
So, what is not machine learning? Machine learning is not a procedural approach to doing things.
For those who have a computer science background you must be very used to an algorithmic way
of thinking about things. You have a problem, you write an algorithm and the algorithm solves
the problem right.
So, a simple example would be tax calculation, give the input as my salary, my savings; and then
there is a  set of rules that you apply; and then outcomes  the tax that you need to pay. So, there
is no learning happening here per se. So, this is a procedure that you follow, which takes as
input, does some series of steps in an algorithmic fashion, and outcomes an output. So, there is
nothing that is being learnt here.

So, now let us ask the question, what is machine learning? So,  we know why we are learning this topic; and we kind of know, have a high level view of where, where it is appliedbut then we want to understand what it is? So, the way I want to think about this is first, let me tell you what is not machine learning; and then we will try to compare and contrast with what is machine learning.

So, what is not machine learning? Machine learning is not a procedural approach to doing things. For those who have a computer science background you must be very used to an algorithmic way of thinking about things. You have a problem, you write an algorithm and the algorithm solves the problem right.

So, a simple example would be tax calculation, give the input as my salary, my savings; and then there is a  set of rules that you apply; and then outcomes  the tax that you need to pay. So, there is no learning happening here per se. So, this is a procedure that you follow, which takes as input, does some series of steps in an algorithmic fashion, and outcomes an output. So, there is nothing that is being learnt here.

It is just a procedure, which maps an input to the output; that is not machine learning. So, there has to be a learning component and will see what this learning component is as we go along in this course. An important and perhaps the most important point about what is not machine learning is that machine learning is not memorization.

To give an example, let us say we want we want to compute the; I mean we want to perform the task of recognizing a tree in a picture, let us say. So, now let us say you have thousand pictures of trees and thousand pictures of which does not contain a tree; so now you have 2000 pictures. You can look at these 2000 pictures, memorize which ones have trees and which ones do not have trees. Now, does that mean you have understood the concept of a tree?

How do you for instance, will you be able to predict whether a picture has a tree or not? In a
given picture, which is not in these 2000 pictures that have been shown to you? Perhaps not,
because what you have done is just memorizing. And then if you are shown a picture, which is
already there at the set from which you have memorized, perhaps you would be able to answer
well. So, on the other hand, if you are shown something which which has a treebut then, it  was
never a part of your data that was shown to you. Unless you understood what it means to be a
tree,  what what does it mean for a picture to contain a tree; you would not really be able to
answer that question. So, it is another example; think of it as  if  you are being taught a lot of
things in this course and you solve all your assignment problems.
And if your final exam is going to just test you only on the problems that you solved during your
assignments; then of course, it is not going to be too hard. So, you can simply memorize all the
steps for all the problems in the assignment, and then you would score the highest amount of
marks. But, that does not mean necessarily that you have learned the subject.
So, this memorization does not imply your learning; that is the point I am trying to push here.
We will see what it actually then means to learn, in a minute. Of course, another popular
misconception is that, we see machine learning as a buzzword that has been thrown around in
different contexts all around the place; artificial intelligence, deep learning, machine learning,
you keep hearing these buzzwords, it feels like magic.
So, there are so many things that  these complicated algorithms have achieved today that it feels
like magic; whereas, of course it is not. But, then if it is not magic, what is it? So, let us try to go

How do you for instance, will you be able to predict whether a picture has a tree or not? In a given picture, which is not in these 2000 pictures that have been shown to you? Perhaps not, because what you have done is just memorizing. And then if you are shown a picture, which is already there at the set from which you have memorized, perhaps you would be able to answer well. So, on the other hand, if you are shown something which which has a treebut then, it  was never a part of your data that was shown to you. Unless you understood what it means to be a tree,  what what does it mean for a picture to contain a tree; you would not really be able to answer that question. So, it is another example; think of it as  if  you are being taught a lot of things in this course and you solve all your assignment problems.

And if your final exam is going to just test you only on the problems that you solved during your assignments; then of course, it is not going to be too hard. So, you can simply memorize all the steps for all the problems in the assignment, and then you would score the highest amount of marks. But, that does not mean necessarily that you have learned the subject.

So, this memorization does not imply your learning; that is the point I am trying to push here. We will see what it actually then means to learn, in a minute. Of course, another popular misconception is that, we see machine learning as a buzzword that has been thrown around in different contexts all around the place; artificial intelligence, deep learning, machine learning, you keep hearing these buzzwords, it feels like magic.

So, there are so many things that  these complicated algorithms have achieved today that it feels like magic; whereas, of course it is not. But, then if it is not magic, what is it? So, let us try to go over these three points and then try to actually see what they actually mean in a machine learning context. If machine learning is not procedural than what is it?

What is it? So, there is a secret sauce which does not make it procedural and what is that? Well, that is data; so all your machine learning algorithms are going to work on some data. It is going

to learn from this data, and then use this learning to make predictions, or whatever the task that you want to solve on a test data. So, the secret sauce for machine learning is data; so it is of course algorithmic.

So, we are going to see algorithms and so on. But, then how does it differentiate from a standard computer science algorithm is that there is this extra bit which is the data. We will see more about, what does it mean to say you are learning from data and so on? I mean, that is the point of this course anyway. If it does not memorize, then what does it do?

computer science algorithm is that there is this extra bit which is the data. We will see more
about, what does it mean to say you are learning from data and so on? I mean, that is the point of
this course anyway. If it does not memorize, then what does it do?
We want machine learning algorithms to generalize; so, that is the technical term that we use in
the machine learning literature. What does it mean to generalize? In layman's term, it means that
you actually learn, not just memorize; so that you re able to predict, you do well on an unseen
data. That is you are able to generalize your understanding from the data that you see to unseen
data.
So, you are not like specific to the data that you have seen only which would be easy to do,
which you can simply memorize; whereas, if you do not want to be specific, you must be general
enough. When can you be general enough? When you actually learn. So, we want our algorithms
to learn. We want our algorithms to generalize, to do well on unseen data. How do you do that?
That is what this course is about. If it is not magic, what is it then?
It is basically math. So, it just uses a lot of mathematical ideas and will see some of the
prerequisites. Of course, if you have taken a machine learning foundation course in this in online
B.Sc. course you would already know what these prerequisites are, and I mean we are going to
cover them. But then these are basically mathematical ideas that we need to do well in machine
learning; I mean to understand and appreciate the machine learning algorithms.

We want machine learning algorithms to generalize; so, that is the technical term that we use in the machine learning literature. What does it mean to generalize? In layman's term, it means that you actually learn, not just memorize; so that you re able to predict, you do well on an unseen data. That is you are able to generalize your understanding from the data that you see to unseen data.

So, you are not like specific to the data that you have seen only which would be easy to do, which you can simply memorize; whereas, if you do not want to be specific, you must be general enough. When can you be general enough? When you actually learn. So, we want our algorithms to learn. We want our algorithms to generalize, to do well on unseen data. How do you do that? That is what this course is about. If it is not magic, what is it then?

It is basically math. So, it just uses a lot of mathematical ideas and will see some of the prerequisites. Of course, if you have taken a machine learning foundation course in this in online B.Sc. course you would already know what these prerequisites are, and I mean we are going to cover them. But then these are basically mathematical ideas that we need to do well in machine learning; I mean to understand and appreciate the machine learning algorithms.

### Timestamp: 15:38

So, with that short introduction, let me give you some concrete examples of machine learning
problems. And then will quickly try to understand what are the broader paradigms of machine
learning; so here are some problems. One of the problems, very popular problem is to predict
whether a given email or let us say even an SMS is a spam email or a non-spam e-mail.
So, basically your spam filters  in your email inbox, most email providers have a spam filter;
which means that automatically you do not do anything. Automatically the email is tagged as
spam or not and then it automatically goes to a spam filter. Of course, it makes mistakes
sometimes, but most of the times it gets it right.
So, how does this happen? The spam filter itself is an algorithm  which has had access to a lot of
data; a lot of which are spam, a lot of which are not spam, from which it has learned to
differentiate a spam email from a non-spam email. So, that is an example. Forecasting rainfall, if
you have data about how much did it rain in the last 15 years, let us say.
And you want to forecast whether it will rain tomorrow or not. Of course, you might have a lot
of other features associated with this. For instance, you might know the precipitation levels, the

So, with that short introduction, let me give you some concrete examples of machine learning problems. And then will quickly try to understand what are the broader paradigms of machine learning; so here are some problems. One of the problems, very popular problem is to predict whether a given email or let us say even an SMS is a spam email or a non-spam e-mail.

So, basically your spam filters  in your email inbox, most email providers have a spam filter; which means that automatically you do not do anything. Automatically the email is tagged as spam or not and then it automatically goes to a spam filter. Of course, it makes mistakes sometimes, but most of the times it gets it right.

So, how does this happen? The spam filter itself is an algorithm  which has had access to a lot of data; a lot of which are spam, a lot of which are not spam, from which it has learned to differentiate a spam email from a non-spam email. So, that is an example. Forecasting rainfall, if you have data about how much did it rain in the last 15 years, let us say.

And you want to forecast whether it will rain tomorrow or not. Of course, you might have a lot of other features associated with this. For instance, you might know the precipitation levels, the atmospheric pressure, humidity whatnot, about every single day in the in the last 10 or 15 years that you have. And you have to use that to somehow figure out whether on this particular day, which is tomorrow let us say, will it rain or not.

Even if you know these other parameters, let us say precipitation or pressure temperature and so on, can you forecast rainfall? Another example is recommending movies of course. If you use an OTT platform; let us say and you login to it, you are going to be shown a list of movies. And then these might be categorized as new arrivals, whatnot and so on. But then you might also see a topic which says that movies that you might like or recommended for you.

So,  that is a set of movies, which are very very specific to you, as opposed to your friend who
might also have the same account. I mean, who might have an account in the same OTT
platform, but then might get a different set of recommendations. So, which means that depending
on what kind of movies you watch, what kind of genres  you like, so you get a list of tailor-made
suggestions for you; that might be one again, machine learning application.
Friend’s suggestions: so if you are in social media, or even in a professional social network, such
as such as LinkedIn, let us say. So, you might, you might often see people you may know, or
people you may want to be friends with kind of list that that gets automatically generated. So,
these are people  with whom you are not friends or connections, a priori, but then the system
suggests you these things.
So, which means there is an algorithm which uses a lot of data to figure out what kind of people
are more likely to be friends; and then uses that to give you a list of suggestions, an ordered list
of suggestions. As a slightly different example, you can look at voice/instrument separation; let
say you have an mp3 of a beautiful song, sung by a favorite singer.
And for whatever reasons, you may want to separate the voice, the singer's voice from the
instrument. So, now,  how can you do this automatically? So, there is  some structure in how
voice signals are, some structure in how instruments signals are. But then what you have in an
mp3 is a combined effect of these two.
But, how can we actually separate these out,  let us say if I give you a lot of voice, only mp3s ,
lot of instrument only mp3s  somehow can we learn how to separate voice from instrument in a

So,  that is a set of movies, which are very very specific to you, as opposed to your friend who might also have the same account. I mean, who might have an account in the same OTT platform, but then might get a different set of recommendations. So, which means that depending on what kind of movies you watch, what kind of genres  you like, so you get a list of tailor-made suggestions for you; that might be one again, machine learning application.

Friend’s suggestions: so if you are in social media, or even in a professional social network, such as such as LinkedIn, let us say. So, you might, you might often see people you may know, or people you may want to be friends with kind of list that that gets automatically generated. So, these are people  with whom you are not friends or connections, a priori, but then the system suggests you these things.

So, which means there is an algorithm which uses a lot of data to figure out what kind of people are more likely to be friends; and then uses that to give you a list of suggestions, an ordered list of suggestions. As a slightly different example, you can look at voice/instrument separation; let say you have an mp3 of a beautiful song, sung by a favorite singer.

And for whatever reasons, you may want to separate the voice, the singer's voice from the instrument. So, now,  how can you do this automatically? So, there is  some structure in how voice signals are, some structure in how instruments signals are. But then what you have in an mp3 is a combined effect of these two.

But, how can we actually separate these out,  let us say if I give you a lot of voice, only mp3s , lot of instrument only mp3s  somehow can we learn how to separate voice from instrument in a different mp3 file which has both overlaid over each other. That might be a machine learning problem too.

Grouping pictures and phone, so you have your favorite smartphone, where you take a lot of pictures; but then you do not tell who is in which picture. But the system automatically says, hey

these pictures, it looks like they all have the same person. These pictures might have been taken in different angles, might have been taken in different backgrounds, different locations, different time of the day. So still, the algorithm in your smartphone is able to figure out that it looks like these pictures contain the same person.

It may not know who that person is, and that is why it is asking you to tag that person with a
name. But then it knows by just looking at these face similarity that  well, all these seem to have
the same person; so that might be a machine learning problem. It means that you need to figure
out using a lot of face data, how our faces related to each other.
So I mean,  what distinguishes one face from the other, so things like that. That is a slightly more
complicated example. You might want to think about things like robot navigation, maybe there is
a robot that is in one end of the room; and then the goal of the robot is to reach the other end, and
then there is a lot of obstacles in between.
Now,  from the standard machine learning problem, this might be slightly different; because
here, the robot has to make a decision to move either forward, left, right, back. And then after it
makes a decision, it is given some feedback. So, and meaning if it if it moves forward, maybe
goes and hits against a wall; and that is a feedback to the robot that this is the wrong direction to
move. But, moving forward might be a good direction in a different place.
So, it is not like moving forward is always a bad direction, bad decision to take. So, it has to
learn where to take which decision by making mistakes; so that is that is again a learning
problem, it is learning by experience. So that is that is the standard example or a little bit
complicated example than the algorithms that we will see in this course, nevertheless, a machine
learning problem.
Stock market prediction, as I said you would want to predict whether a  a particular stock will go
up or not on a day; of course you do not know that. So, you make the prediction in the morning,
and then in the evening you observe how much did the stock go up or down. So, based on that,

It may not know who that person is, and that is why it is asking you to tag that person with a name. But then it knows by just looking at these face similarity that  well, all these seem to have the same person; so that might be a machine learning problem. It means that you need to figure out using a lot of face data, how our faces related to each other.

So I mean,  what distinguishes one face from the other, so things like that. That is a slightly more complicated example. You might want to think about things like robot navigation, maybe there is a robot that is in one end of the room; and then the goal of the robot is to reach the other end, and then there is a lot of obstacles in between.

Now,  from the standard machine learning problem, this might be slightly different; because here, the robot has to make a decision to move either forward, left, right, back. And then after it makes a decision, it is given some feedback. So, and meaning if it if it moves forward, maybe goes and hits against a wall; and that is a feedback to the robot that this is the wrong direction to move. But, moving forward might be a good direction in a different place.

So, it is not like moving forward is always a bad direction, bad decision to take. So, it has to learn where to take which decision by making mistakes; so that is that is again a learning problem, it is learning by experience. So that is that is the standard example or a little bit complicated example than the algorithms that we will see in this course, nevertheless, a machine learning problem.

Stock market prediction, as I said you would want to predict whether a  a particular stock will go up or not on a day; of course you do not know that. So, you make the prediction in the morning, and then in the evening you observe how much did the stock go up or down. So, based on that, maybe you change and then make a prediction for the next day; and then again, only in the evening, you get the feedback whether the stock went up or not.

So, the over time, I mean, what is a good metric to say that, is your algorithm successful or not? Maybe how much money did you make? How many missed chances were there and things like

that? Nevertheless, the main point is you are trying to learn over the time. So,  this is also a learning problem. So, you may not learn in one shot, but then you may want to learn over the time. So, that is an example of a stock market prediction problem.

So, these are some examples; of course you can think of, I mean your own examples of where machine learning problem can be applied.

machine learning problem can be applied.