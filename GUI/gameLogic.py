from types import SimpleNamespace
from client_python.client import Client
import json
from pygame import gfxdraw
import pygame
from pygame import *

from Data_Structure.GraphAlgo import GraphAlgo
from Data_Structure.Edge_Data import Edge_Data
from Data_Structure.Pokemon import Pokemon
from Data_Structure.Agent import Agent
from Data_Structure.Point2D import Point2D
#
# # default port
# PORT = 6666
# # server host (default localhost 127.0.0.1)
# HOST = '127.0.0.1'
#
#
# client = Client()
# # start the connection with the server
# client.start_connection(HOST, PORT)
#
# pokemons = client.get_pokemons()
#
# pokemons1 = json.loads(pokemons)
#
# pokemons_obj = json.loads(pokemons, object_hook=lambda d: SimpleNamespace(**d))
#
# graph_json = client.get_graph()
# graph_dic = json.loads(graph_json)
# algo = GraphAlgo()
# algo.json_from_dic(graph_dic, "case.json")
# algo.load_from_json("case.json")
#
# FONT = pygame.font.SysFont('Arial', 20, bold=True)
# # load the json string into SimpleNamespace Object
#
# graph = json.loads(
#     graph_json, object_hook=lambda json_dict: SimpleNamespace(**json_dict))
#
# for n in graph.Nodes:
#     x, y, _ = n.pos.split(',')
#     n.pos = SimpleNamespace(x=float(x), y=float(y))
#
# eps = 0.001
# p = pokemons1['Pokemons']
# poke_list = []
# agent_list = []
# for pokemon in p:
#     x, y, z = pokemon['Pokemon']['pos'].split(',')
#     typ = pokemon['Pokemon']['type']
#     for edge in algo.get_graph().get_edges():
#         po_src = algo.get_graph().get_node(edge['src']).point
#         x_src, y_src = po_src.x, po_src.y
#         po_dest = algo.get_graph().get_node(edge['dest']).point
#         x_dest, y_dest = po_dest.x, po_dest.y
#         dist = ((x_dest - x_src) ** 2 + (y_dest - y_src) ** 2) ** 0.5
#
#         # src to pokemon
#         d1 = ((float(x) - x_src) ** 2 + (float(y) - y_src) ** 2) ** 0.5
#         d2 = ((x_dest - float(x)) ** 2 + (y_dest - float(y)) ** 2) ** 0.5
#         d3 = d1 + d2
#         if abs(d3 - dist) < eps:
#             if typ > 0:
#                 client.add_agent('{\"id\":'+str(edge["src"])+'}')
#             else:
#                 client.add_agent('{\"id\":'+str(edge["dest"])+'}')
#
# # this command starts the server - the game is running now
# client.start()
#
# agents_str = client.get_agents()
# agents = json.loads(agents_str)
# a = agents['Agents']
#
# for agent in a:
#     ag = Agent(agent['Agent'])
#     agent_list.append(ag)

eps = 0.001
'''
Function to decide which next pokemon the agent will hunt
'''
def closest_pokemon(agent1, pokemons1, graphAlgo):
    max_utility = 0
    print(graphAlgo.graph.get_nodes())
    print(agent1.src)
    graphAlgo.Dijkstra(int(agent1.src))
    shortest_path = 0
    i = 0
    pok_index = 0
    if len(pokemons1) > 0:
        for pok in pokemons1:
            if pok.eaten == False:
                    time = graphAlgo.graph.get_node(pok.edge.src).weight / int(agent1.speed)
                    time += pok.edge.weight / int(agent1.speed)
                    utility = float(pok.value) / time
                    if utility > max_utility:
                        max_utility = utility
                        src = pok.edge.src
                        pok_index = i
            i += 1
    pokemons1[pok_index].eaten = True
    agent1.pokemon = pokemons1[pok_index]
    agent1.path = graphAlgo.shortest_path(int(agent1.src), pokemons1[pok_index].edge.src)[1]
    agent1.path.append(pokemons1[pok_index].edge.dest)
    return pokemons1

'''
Function to add the right edge that the pokemon is on
'''
def find_pok_edge(pokemon, graphAlgo):
    x, y, z = pokemon.pos.x, pokemon.pos.y, pokemon.pos.z
    typ = pokemon.type
    for edge in graphAlgo.get_graph().get_edges():
        # edge dist
        po_src = graphAlgo.get_graph().get_node(edge['src']).point
        x_src, y_src = po_src.x, po_src.y
        po_dest = graphAlgo.get_graph().get_node(edge['dest']).point
        x_dest, y_dest = po_dest.x, po_dest.y
        dist = ((x_dest - x_src) ** 2 + (y_dest - y_src) ** 2) ** 0.5
        # src to pokemon + pokemon to dest
        d1 = ((float(x) - x_src) ** 2 + (float(y) - y_src) ** 2) ** 0.5
        d2 = ((x_dest - float(x)) ** 2 + (y_dest - float(y)) ** 2) ** 0.5
        d3 = d1 + d2
        # checking if it's on the same edge
        if abs(d3 - dist) < eps:
            if int(pokemon.type) < 0:
                # src > dest
                if graphAlgo.graph.get_node(edge['src']).node_id > graphAlgo.graph.get_node(edge['dest']).node_id:
                    real_edge = Edge_Data(edge['src'], edge['dest'], edge['w'], 0)
                    pokemon.edge = real_edge
                else:
                    real_edge = Edge_Data(edge['dest'], edge['src'], edge['w'], 0)
                    pokemon.edge = real_edge
                break
            elif int(pokemon.type) > 0:
                # dest > src
                if graphAlgo.graph.get_node(edge['dest']).node_id > graphAlgo.graph.get_node(edge['src']).node_id:
                    real_edge = Edge_Data(edge['src'], edge['dest'], edge['w'], 0)
                    pokemon.edge = real_edge
                else:
                    real_edge = Edge_Data(edge['dest'], edge['src'], edge['w'], 0)
                    pokemon.edge = real_edge
                break

'''
Function that checks for new pokemons that came
'''
# def refresh_pock_list():
#     pokemons_str = client.get_pokemons()
#     pokemons = json.loads(pokemons_str)
#     p = pokemons['Pokemons']
#     for pokemon in p:
#         poke = Pokemon(pokemon['Pokemon'])
#         find_pok_edge(poke)
#         add = True
#         x, y = poke.pos.x, poke.pos.y
#         for our_poke in poke_list:
#             if our_poke.pos.x == float(x) and our_poke.pos.y == float(y):
#                 add = False
#         if add:
#             poke_list.append(poke)
