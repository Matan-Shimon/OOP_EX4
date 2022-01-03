from types import SimpleNamespace
from client import Client
import json
from Data_Structure.GraphAlgo import GraphAlgo
from Data_Structure.DiGraph import DiGraph

from pygame import gfxdraw
import pygame
from pygame import *

# init pygame
WIDTH, HEIGHT = 1080, 720

# default port
PORT = 6666
# server host (default localhost 127.0.0.1)
HOST = '127.0.0.1'

client = Client()
client.start_connection(HOST, PORT)

pokemons_str = client.get_pokemons()
pokemons = json.loads(pokemons_str)
print(pokemons)
agents = client.get_agents()

graph_json = client.get_graph()
graph_dic = json.loads(graph_json)
algo = GraphAlgo()
algo.json_from_dic(graph_dic, "case.json")
algo.load_from_json("case.json")



# for agent in agents:
#     x = pokemons[0].pos.x
#     y = pokemons[0].pos.y

eps = 0.001
p = pokemons['Pokemons']
for pokemon in p:
    x, y, z = pokemon['Pokemon']['pos'].split(',')
    typ = pokemon['Pokemon']['type']
    for edge in algo.get_graph().get_edges():
        po_src = algo.get_graph().get_node(edge['src']).point
        x_src, y_src = po_src.x, po_src.y
        po_dest = algo.get_graph().get_node(edge['dest']).point
        x_dest, y_dest = po_dest.x, po_dest.y
        dist = ((x_dest - x_src) ** 2 + (y_dest - y_src) ** 2) ** 0.5

        # src to pokemon
        d1 = ((float(x) - x_src) ** 2 + (float(y) - y_src) ** 2) ** 0.5
        d2 = ((x_dest - float(x)) ** 2 + (y_dest - float(y)) ** 2) ** 0.5
        d3 = d1 + d2
        if abs(d3 - dist) < eps:
            if typ > 0:
                client.add_agent('{\"id\":'+str(edge["src"])+'}')
                #client.add_agent(f'{"id":{str(edge["src"])}}')
            else:
                client.add_agent('{\"id\":'+str(edge["dest"])+'}')
                #client.add_agent(f'{"id":{str(edge["dest"])}}')
agents = client.get_agents()
print(agents)
info = client.get_info()
print(info)