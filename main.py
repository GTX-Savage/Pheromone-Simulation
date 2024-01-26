import random
import copy

#Perameters for the algorithm
FILE_NAME = "Burma.xml"
ALPHA = 1
BETA = 4
NUM_ANTS = 100
EVAPORATION_RATE = 0.1
PHEROMONE_DEPOSIT = 3

def fileReader(FILE_NAME):
    '''reads the data from an xml file that contins vertecies and edges'''
    file = open(FILE_NAME, "r")
    row = []
    row2 = []
    heuristic_matrix = []
    distance_matrix = []
    city_counter = 0
    #loops through all lines in the file
    for line in file:
        space_split = line.split(" ")
        stripped_line = line.strip()
        #checks to see if the line is a vetex or a edge
        if stripped_line == "</vertex>" and len(row) != 0:
            #creates a new list for the weights assoated witht the vetex
            row.insert(city_counter,0)
            row2.insert(city_counter,0)
            city_counter = city_counter + 1
            heuristic_matrix.append(row)
            distance_matrix.append(row2)
            row = []
            row2 = []
        elif space_split[0] == "<edge":
            #adds a new weight to the vetex list
            weight_list = (space_split[1].split("\"")[1]).split("e+")
            weight = float(weight_list[0])*(10**int(weight_list[1]))
            row.append(1/weight)
            row2.append(weight)
    file.close()
    return heuristic_matrix, distance_matrix

def pheromoneMatrix(heuristic_matrix):
    '''creates a pheromone matrix'''
    row_count = len(heuristic_matrix)
    coloum_count = len(heuristic_matrix[0])
    pheromone_matrix = []
    for j in range (row_count):
        pheromone_matrix.append([])
        for i in range (coloum_count):
            #assigns a random value from 0 -> 1 for each position in the matrix
            pheromone_level = random.uniform(0,1)
            pheromone_matrix[j].append(pheromone_level)
    return pheromone_matrix

def probabilityMatrix(heuristic_matrix,pheromone_matrix,ALPHA,BETA,ant):
    '''creates a matrix to represent the probabitity of an ant taking a specific route'''
    #sets the coloums of the vertacies that the ant has been to as 0
    for row in heuristic_matrix:
        row[ant[len(ant)-1]] = 0
    probability_matrix = []
    #applies a formula to adjust the values ependent on the amount of pheromone in a location
    for i in range(len(heuristic_matrix[0])):
        probability = ((pheromone_matrix[ant[len(ant)-1]][i]**ALPHA) * (heuristic_matrix[ant[len(ant)-1]][i]**BETA))
        probability_matrix.append(probability)
    #devides all elements in a row by the total in the row to get the chance of the ant taking that route 
    total = sum(probability_matrix)
    if total != 0:
        for i in range(len(probability_matrix)):
            probability_matrix[i] = probability_matrix[i]/total    
    return probability_matrix

def nextLocation(probability_matrix, ant):
    '''retrieves the next loaction the ant will go too'''
    #creaates a random number
    destination_roll = random.uniform(0,1)
    cummulative_prob = 0
    #calculates which path is taken by cummulative_prob
    for i in range(len(probability_matrix)):
        cummulative_prob = cummulative_prob + probability_matrix[i]
        if cummulative_prob >= destination_roll:
            #appends the next position to the list of visited nodes for the ant
            ant.append(i)
            break
    return ant


def updatePheromoneMatrix(pheromone_matrix,EVAPORATION_RATE,ants,PHEROMONE_DEPOSIT,distance,loop,best_path):
    '''updates the values in the pheromone matrix by reducing by the evapotation rate and adding the pheromones each ant added'''
    #decreases each element by the evaporation rate
    pheromone_matrix = [[ (1-EVAPORATION_RATE)*pheromone_matrix[i][j] for j in range(len(pheromone_matrix))] for i in range(len(pheromone_matrix[0]))]
    #adds the pheromones that each ant deposited devided by the total length of the route
    for ant in ants:
        length = 0
        ant.append(0)
        #gets total length of route
        for i in range(len(ant) - 1):
            length += distance[ant[i]][ant[i+1]]
        #adds each pheromone
        for i in range(len(ant) - 1):
            pheromone_matrix[ant[i]][ant[i+1]] += PHEROMONE_DEPOSIT/length
        loop = loop + 1
        if best_path[0] == None or best_path[0] >= length:
            best_path[0] = length
            best_path[1] = ant
    return pheromone_matrix,loop,best_path

def updatePheromoneMatrixElite(pheromone_matrix,EVAPORATION_RATE,ants,PHEROMONE_DEPOSIT,distance,loop,best_path):
    '''updates the values in the pheromone matrix by reducing by the evapotation rate and adding the pheromones each ant added'''
    #decreases each element by the evaporation rate
    pheromone_matrix = [[ (1-EVAPORATION_RATE)*pheromone_matrix[i][j] for j in range(len(pheromone_matrix))] for i in range(len(pheromone_matrix[0]))]
    #adds the pheromones that the top 20 ant deposited devided by the total length of the route
    lengths = []
    top_three = []
    for ant in ants:
        length = 0
        ant.append(0)
        loop = loop + 1
        #gets total length of route
        for i in range(len(ant) - 1):
            length += distance[ant[i]][ant[i+1]]
        lengths.append(length)
    for i in range(20):
        best = ants[lengths.index(max(lengths))]
        best_length = max(lengths)
        top_three.append([best_length,best])
        lengths.remove(best_length)
        #adds each pheromone
    for ant in top_three:
        for i in range(len(ant) - 1):
            pheromone_matrix[ant[1][i]][ant[1][i+1]] += PHEROMONE_DEPOSIT/ant[0]
        if best_path[0] == None or best_path[0] >= ant[0]:
            best_path[0] = ant[0]
            best_path[1] = ant[1]
    return pheromone_matrix,loop,best_path

def path(pheromone_matrix,NUM_CITIES,heuristic_matrix):
    '''calculates the final result calculated based on the pheromone matrix'''
    temp = 0
    position = 0
    visited = [0]
    #calculates the first position that the ant goes to
    for i in range(1,NUM_CITIES):
        if pheromone_matrix[0][i] >= temp:
            #find the max pheromone for each weight in the first vertex
            temp = pheromone_matrix[0][i]
            nextposition = i
    visited.append(nextposition)
    #calculates the rest of the route take by the ant
    for j in range(NUM_CITIES-2):
        temp = 0
        for i in range(NUM_CITIES):
            if pheromone_matrix[nextposition][i] >= temp and i not in visited:
                #find the max pheromone for each weight in the current vertex
                temp = pheromone_matrix[nextposition][i]
                position = i
        nextposition = position
        visited.append(nextposition)
    visited.append(0)
    length = 0
    #finds the length of the route calculated
    for i in range(NUM_CITIES):
        length += 1/(heuristic_matrix[visited[i]][visited[i+1]])
    #print(visited)
    print(length)
    
    
def antcolony(FILE_NAME,ALPHA,BETA,NUM_ANTS,EVAPORATION_RATE,PHEROMONE_DEPOSIT):
    '''contains the main method for creating an ant colony optermisation for the traverlling salesman problem'''
    #creates the inistale matracies
    heuristic_matrix, distance = fileReader(FILE_NAME)
    pheromone_matrix = pheromoneMatrix(heuristic_matrix)
    NUM_CITIES = len(heuristic_matrix)
    loop = 0
    best_path =[None,[]]
    #repeates the algorithm for the number of iterations
    while loop < 10000:
        ants = []
        #starts all ants at position 0
        for i in range(NUM_ANTS):
            ants.append([0])
        for ant in ants:  
            #creates a copy of the heuristic for an ant so it can be edited during run time
            instanced_heuristic_matrix = copy.deepcopy(heuristic_matrix) 
            for t in range(NUM_CITIES):  
                #gets the next position the ant will take
                probability_matrix = probabilityMatrix(instanced_heuristic_matrix,pheromone_matrix,ALPHA,BETA,ant)
                ant = nextLocation(probability_matrix, ant)
        #updates the pheromone matrix
        pheromone_matrix, loop, best_path = updatePheromoneMatrix(pheromone_matrix,EVAPORATION_RATE,ants,PHEROMONE_DEPOSIT,distance,loop,best_path)
    #calculates the final path
    #path(pheromone_matrix, NUM_CITIES,heuristic_matrix)
    print(best_path[0])
        


#main call for the algorithm
antcolony(FILE_NAME,ALPHA,BETA,NUM_ANTS,EVAPORATION_RATE,PHEROMONE_DEPOSIT)


