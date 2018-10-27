# MooshLeap

### A Tkinter GUI for analyzing and visualizing data from test cabins

![](https://raw.githubusercontent.com/Hugo-Nattagh/MooshLeap/master/images/GH1.PNG)

When I worked at General Electric Healthcare, my service would expose X-rays tube (in their casing) to a few tests before sending them to medical institutions, for executing chest and heart scans. 

One of those test is the Functional Test, in which the tube is exposed to different values of tension and current in a cabin.

We had 4 cabins, and each run would create a csv file with the details of the run. 

I worked along with an engineer who needed to make sense of all of the data (since 2009)
to improve the process of the test and get more efficiency.

![](https://raw.githubusercontent.com/Hugo-Nattagh/MooshLeap/master/images/GH2.PNG)

#### What's going on

I was asked for certain results from the data. I condensed them in 3 axis, 3 functions that give graphs and descriptions.

To make it user-friendly so that any employee could see the results and tweak the settings, I built it all in a Tkinter 
GUI.

![](https://raw.githubusercontent.com/Hugo-Nattagh/MooshLeap/master/images/GH3.PNG)

#### Files Description

- `mooshLeap.py`: Script containing the GUI and the functions
- `xxxxxxGIx.csv`: Those files contain the raw data.