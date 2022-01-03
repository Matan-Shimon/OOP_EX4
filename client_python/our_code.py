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

pokemons = client.get_pokemons()
pokemons_obj = json.loads(pokemons, object_hook=lambda d: SimpleNamespace(**d))

agents = client.get_agents()

graph_json = client.get_graph()
algo = GraphAlgo()
graph_dic = json.loads(graph_json, object_hook=lambda json_dict: SimpleNamespace(**json_dict))
graph = json.dumps(graph_dic)
file_name = json.loads(graph)
algo.load_from_json(file_name)

for agent in agents:
    x = pokemons[0].pos.x
    y = pokemons[0].pos.y


for pokemon in pokemons:
    x,y = pokemon.pos.x, pokemon.pos.y
