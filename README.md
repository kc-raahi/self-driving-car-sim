Self-Driving Car Simulation
===========================

![gif](frames\animated3.gif)

### What this is:
This is a simulation of "driving" (blue) cars navigating 
through fixed patterns of traffic (green) cars.
They use sensors connected to neural networks in an attempt 
to train a single network that can navigate more unpredictable 
traffic patterns. Users can specify the number of driving cars 
to use in each generation, the number of generations, the 
traffic pattern, and whether to use a saved neural network 
or generate one randomly.
### Libraries used:
* Pygame
* Pytest
* math
* random
* argparse
* pickle
### Technologies used:
* Neural Network
* Sensors
### Acknowledgements: 
* [Radu's JS Self-Driving Car Course](https://www.youtube.com/watch?v=Rs_rAxEsAvI)
### Conclusions:
Given three methodical traffic patterns 
(upward cascade, downward cascade, and 1-2 patterns) on which 
the given neural network .pickle file was trained, this neural 
network can also navigate two randomly generated traffic patterns 
it has not previously navigated on the first attempts.

### Contact: 
klarchaudhurir@gmail.com