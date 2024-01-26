/Ant Colony Optimization for the Traveling Salesman Problem
//Overview
The code contained in this file is an implementation of an Ant Colony Optimization algorithm thats gives a suitible solution to the Traveling Salesman Problem giving the length of the final path found.

//Parameters

FILE_NAME: The name of the XML file containing each vertix and itts subsiquent edges.
ALPHA: The amount the pheromone matrtix influence the ant decisions.
BETA: The amount the heuristic matrtix influence the ant decisions.
NUM_ANTS: The number of ants used per cycle befor updating the pheromone matrix.
EVAPORATION_RATE: Rate at which pheromone evaporates.
PHEROMONE_DEPOSIT: Amount of pheromone deposited by each ant.

//Running
To run the programme you will need to have a version of [python](https://www.python.org/) install. Once a version of python is insalled either you can run the programme in a python IDE or via the command terminal by running the following command (python pathto file\main.py)

To change the algorithm to have specific perameters the user will need to open up the file and change the constants at the top of the file. Or if a user wants to add there own xml file they can do so by adding the file in the same directory and changing the FILE_NAME constant to contain a string of the filename

Note
The script is currently set to run for 10,000 fitness evaluations. To adjust the number of fitness evaluations for the algorithm one will need to open up the file and edit the antcolony() function. In the antcolony() function edit the while loop to say "while loop < num_fitness_evaluations" where num_fitness_evaluations = the number of time yo want to evaluate 
Finally if you want to implement elitism into the algorithm change the function call of updatePheromoneMatrix() to updatePheromoneMatrixElite() in antcolony()