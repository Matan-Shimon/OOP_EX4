# OOP - Ex4
In this task we were required to create a structure that will present a graph.
We were given a server that provides the agents and pokemons on the graph for each moment.
We were required to build an algorithm that makes the agents move simultaneously and "eat" pokemons.
Each time a pokemon has been eaten, a new pokemon arrives from the server on a random location on the graph.
We need to eat as much pokemons as possible.
Eventually, we created a GUI that draws the graph, and shows the pokemons and agent location on the graph.

# Main Algorithm logic
The algorithm logic is based on the following:
1) while the program is running we always update our current pokemons.
2) we will also update the src, dest and position for each agent.
3) we will also update the pokemons that going to be eaten by a certain agent on the way, that means that if a certain agent has a path and on the way there's a pokemon, we will mark that pokemon as "eaten" too.
4) we will run on the agent list, if the dest of current agent is -1, means that the agent has no mission.
5) if it is, we will check if we already gavev him a mission (by looking at his current path).
6) if the current agent path len is 0, means the agent has no mission, we will assign him a new mission by calling the "closest_pokemon"  function.
7) the closest pokemon function calculates the closest pokemon (who's eaten attribute is different from True) by position and the pokemon value.

# Shortest Path Algorithm logic
The Shortest Path algorithm logic is based on the following:
1) copying the graph and creating a list of NodeData.
2) sending the source and dest nodes to the Shortest Path Distance Algorithm.
2) if it won't return us -1, that means that there's a track between them.
3) we will transpose the copied graph.
4) now we will start from the dest node, add it to the list, and check for his neighbors which neighbor weight + edge weight = dest weight.
5) the one node that will give us the equality is our next node, we will add it to the list, and now check on this node, the previous question.
6) we will continue doing that until we will get to the source node.
7) in the end, we will reverse the list.
8) checking the weight of the dest node.

## Project structure
# client
Class name | description
--- | ---
client | the client code we recieved from our proffesor, this is the class that connect us to the server.

# Data structures
Class name | description
--- | ---
Point2D | present a location of graph node.
Node_Data | present a graph node.
Edge_Data | Present a graph edge.
DiGraph | Present a graph.
GraphAlgo | Present a class to perform algorithms on a graph.
Agent | present an agent we recieved from the client.
Pokemon | present a pokemon we recieved from the client.

# Game
Class name | description
--- | ---
game | the main class that has the whole algorithm proccess.
GUI | the class that draws everything, the graph, pokemons and agents.

# UML
https://github.com/Matan-Shimon/OOP_EX4/blob/main/Images/uml.jpeg

# How to run
1. Install python 3 on your pc.
2. Download (clone) the project.
3. open the terminal on your web development.
4. write "java -jar Ex4_Server_v0.0.jar (0-15)", there are 15 cases, choose one you wish to do.
5. cliick enter and run the game class.

# Project creators
Matan Yarin Shimon & Yarin Hindi
