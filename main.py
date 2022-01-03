from types import SimpleNamespace
from client_python.client import Client
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
#HOST = '127.0.0.1'


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    client = Client()
    #client.start_connection(HOST, PORT)

    pokemons = client.get_pokemons()
    pokemons_obj = json.loads(pokemons, object_hook=lambda d: SimpleNamespace(**d))

    agents = client.get_agents()

    graph_json = client.get_graph()
    algo = GraphAlgo()
    algo.json_from_string(graph_json, "case.json")

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
