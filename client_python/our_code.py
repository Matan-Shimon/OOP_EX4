import time
from types import SimpleNamespace
from client import Client
import json
from Data_Structure.GraphAlgo import GraphAlgo
from Data_Structure.Pokemon import Pokemon
from Data_Structure.Agent import Agent

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

graph_json = client.get_graph()
graph_dic = json.loads(graph_json)
algo = GraphAlgo()
algo.json_from_dic(graph_dic, "case.json")
algo.load_from_json("case.json")

# adding agents and giving them a starting node
eps = 0.001
p = pokemons['Pokemons']
poke_list = []
agent_list = []
for pokemon in p:
    poke = Pokemon(pokemon['Pokemon'])
    x, y, z = poke.pos.x, poke.pos.y, poke.pos.z
    typ = poke.type
    for edge in algo.get_graph().get_edges():
        # edge dist
        po_src = algo.get_graph().get_node(edge['src']).point
        x_src, y_src = po_src.x, po_src.y
        po_dest = algo.get_graph().get_node(edge['dest']).point
        x_dest, y_dest = po_dest.x, po_dest.y
        dist = ((x_dest - x_src) * 2 + (y_dest - y_src) * 2) ** 0.5

        # src to pokemon + pokemon to dest
        d1 = ((float(x) - x_src) * 2 + (float(y) - y_src) * 2) ** 0.5
        d2 = ((x_dest - float(x)) * 2 + (y_dest - float(y)) * 2) ** 0.5
        d3 = d1 + d2
        # checking if it's on the same edge
        if abs(d3 - dist) < eps:
            poke.set_edge(edge)
            if typ > 0:
                client.add_agent('{\"id\":'+str(edge["src"])+'}')

            else:
                client.add_agent('{\"id\":'+str(edge["dest"])+'}')
    poke_list.append(poke)


agents_str = client.get_agents()
agents = json.loads(agents_str)
a = agents['Agents']
print(a)
for agent in a:
    ag = Agent(agent['Agent'])
    agent_list.append(ag)


def closest_pokemon(agent1, pokemons1):
    max_utility = 0
    algo.Dijkstra(agent1.src)
    shortest_path = 0
    dest = 0
    i = 0
    check =0
    pok_index = 0
    for pok in pokemons1:
        if pok.typ < 0:
            time = algo.graph.get_node(pok.edge.dest) / agent1.speed
            po_dest = algo.get_graph().get_node(pok.edge.dest).point
            po_src = algo.get_graph().get_node(pok.edge.src).point
            x_dest, y_dest = po_dest.x, po_dest.y
            dist_dest_pok = ((x_dest - pok.pos.x) * 2 + (y_dest - pok.pos.y) * 2) ** 0.5
            dist_dest_src = ((x_dest - x_src) * 2 + (y_dest - y_src) * 2) ** 0.5
            add = (dist_dest_pok / dist_dest_src) * pok.edge.weight / agent1.speed
            time += add
            utility = pok.value / time
            if utility > max_utility:
                max_utility = utility
                dest = pok.dest
                pok_index = i
                check=1
        else:
            # pok.typ > 0
            time = algo.graph.get_node(pok.edge.src) / agent1.speed
            po_dest = algo.get_graph().get_node(pok.edge.dest).point
            po_src = algo.get_graph().get_node(pok.edge.src).point
            x_dest, y_dest = po_dest.x, po_dest.y
            dist_src_pok = ((x_src - pok.pos.x) * 2 + (y_src - pok.pos.y) * 2) ** 0.5
            dist_dest_src = ((x_dest - x_src) * 2 + (y_dest - y_src) * 2) ** 0.5
            add = (dist_src_pok / dist_dest_src) * pok.edge.weight / agent1.speed
            time += add
            utility = pok.value / time
            if utility > max_utility:
                max_utility = utility
                dest = pok.src
                pok_index = i
                check=2
        i += 1
    pokemons1[pok_index].eat_pokemon()
    agent1.pokemon = pokemons1[pok_index]
    agent1.path = algo.shortest_path(agent1.src, dest)[1]
    if check == 1:
        agent1.path.append(pok.src)
    else:
        agent1.path.append(pok.dest)

def run_prog(curr_agent):
    node = algo.graph.get_node(curr_agent.src)
    while len(curr_agent.path) > 0:
        client.choose_next_edge('{"agent_id":' + str(curr_agent.id) + ', "next_node_id":' + str(curr_agent.path[0]) + '}')
        curr_agent.set_location(algo.graph.get_node(curr_agent.path[0]).point)
        if len(curr_agent.path) == 2:
            node = algo.graph.get_node(curr_agent.path[0])
        if len(curr_agent.path) == 1:
            node_dest = algo.graph.get_node(curr_agent.path[0])
            x_dest, y_dest = po_dest.x, po_dest.y
            dist_src_dest = ((node.point.x - node_dest.point.x) * 2 + (node.point.y - node_dest.point.y) * 2) ** 0.5
            dist_src_pok = ((node.point.x - curr_agent.pokemon.pos.x) * 2 + (node.point.y - curr_agent.pokemon.pos.y) * 2) ** 0.5
            add = (dist_src_pok / dist_src_dest) * curr_agent.pokemon.edge.weight / curr_agent.speed
            time.sleep(add)
            client.move()
        curr_agent.path.remove(0)


# client.start()
# while client.is_running() == 'true':
#     print("hi")