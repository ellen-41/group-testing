# group-testing

Contained within this repo is code to simulate the running of particular group testing algorithms, to accompany my final year maths project.

---

`algorithms.py` instantiates a test set object and contains the COMP and DD algorithms.
`simulations.py` runs each of these algorithms a given number of times for fixed *n* and *k*, and plots the number of tests against success probability, as well as giving the counting bound on the same plot. This saves the plot produced as a .png, example below.

![alt text](https://i.postimg.cc/qBSQVL5w/n500k10.png "Example graph")
