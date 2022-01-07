"""
@author AchiyaZigi
OOP - Ex4
Very simple GUI example for python client to communicates with the server and "play the game!"
"""
from types import SimpleNamespace
from client import Client
import json
from pygame import gfxdraw
import pygame
from pygame import *

from Data_Structure.GraphAlgo import GraphAlgo
from Data_Structure.Pokemon import Pokemon
from Data_Structure.Agent import Agent
from Data_Structure.Edge_Data import Edge_Data

# init pygame
WIDTH, HEIGHT = 1080, 720

# default port
PORT = 6666
# server host (default localhost 127.0.0.1)
HOST = '127.0.0.1'
pygame.init()

screen = display.set_mode((WIDTH, HEIGHT), depth=32, flags=RESIZABLE)
clock = pygame.time.Clock()
pygame.font.init()

client = Client()
client.start_connection(HOST, PORT)
pokemons_str = client.get_pokemons()
pokemons = json.loads(pokemons_str)
print(pokemons)
print("david")

graph_json = client.get_graph()
graph_dic = json.loads(graph_json)
algo = GraphAlgo()
algo.json_from_dic(graph_dic, "case.json")
algo.load_from_json("case.json")

FONT = pygame.font.SysFont('Arial', 20, bold=True)
# load the json string into SimpleNamespace Object

graph = json.loads(
    graph_json, object_hook=lambda json_dict: SimpleNamespace(**json_dict))

for n in graph.Nodes:
    x, y, _ = n.pos.split(',')
    n.pos = SimpleNamespace(x=float(x), y=float(y))

 # get data proportions
min_x = min(list(graph.Nodes), key=lambda n: n.pos.x).pos.x
min_y = min(list(graph.Nodes), key=lambda n: n.pos.y).pos.y
max_x = max(list(graph.Nodes), key=lambda n: n.pos.x).pos.x
max_y = max(list(graph.Nodes), key=lambda n: n.pos.y).pos.y


def scale(data, min_screen, max_screen, min_data, max_data):
    """
    get the scaled data with proportions min_data, max_data
    relative to min and max screen dimentions
    """
    return ((data - min_data) / (max_data-min_data)) * (max_screen - min_screen) + min_screen


# decorate scale with the correct values

def my_scale(data, x=False, y=False):
    if x:
        return scale(data, 50, screen.get_width() - 50, min_x, max_x)
    if y:
        return scale(data, 50, screen.get_height()-50, min_y, max_y)


radius = 15

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
        dist = ((x_dest - x_src) ** 2 + (y_dest - y_src) ** 2) ** 0.5

        # src to pokemon + pokemon to dest
        d1 = ((float(x) - x_src) ** 2 + (float(y) - y_src) ** 2) ** 0.5
        d2 = ((x_dest - float(x)) ** 2 + (y_dest - float(y)) ** 2) ** 0.5
        d3 = d1 + d2
        # checking if it's on the same edge
        if abs(d3 - dist) < eps:
            real_edge = Edge_Data(edge['src'], edge['dest'], edge['w'], 0)
            poke.set_edge(real_edge)
            if typ > 0:
                client.add_agent('{\"id\":'+str(edge["src"])+'}')
            else:
                client.add_agent('{\"id\":'+str(edge["dest"])+'}')
    poke_list.append(poke)

# this commnad starts the server - the game is running now
client.start()

"""
The code below should be improved significantly:
The GUI and the "algo" are mixed - refactoring using MVC design pattern is required.
"""
'''
Function to add the right edge that the pokemon is on
'''
def find_pok_edge(pokemon):
    x, y, z = pokemon.pos.x, pokemon.pos.y, pokemon.pos.z
    typ = pokemon.type
    for edge in algo.get_graph().get_edges():
        # edge dist
        po_src = algo.get_graph().get_node(edge['src']).point
        x_src, y_src = po_src.x, po_src.y
        po_dest = algo.get_graph().get_node(edge['dest']).point
        x_dest, y_dest = po_dest.x, po_dest.y
        dist = ((x_dest - x_src) ** 2 + (y_dest - y_src) ** 2) ** 0.5
        # src to pokemon + pokemon to dest
        d1 = ((float(x) - x_src) ** 2 + (float(y) - y_src) ** 2) ** 0.5
        d2 = ((x_dest - float(x)) ** 2 + (y_dest - float(y)) ** 2) ** 0.5
        d3 = d1 + d2
        # checking if it's on the same edge
        if abs(d3 - dist) < eps:
            real_edge = Edge_Data(edge['src'], edge['dest'], edge['w'], 0)
            pokemon.set_edge(real_edge)

'''
Function that checks for new pokemons that came
'''
def refresh_pock_list():
    pokemons_str = client.get_pokemons()
    print("pokes: ",pokemons_str)
    pokemons = json.loads(pokemons_str)
    p = pokemons['Pokemons']
    for pokemon in p:
        poke = Pokemon(pokemon['Pokemon'])
        find_pok_edge(poke)
        add = True
        x, y = poke.pos.x, poke.pos.y
        for our_poke in poke_list:
            if our_poke.pos.x == float(x) and our_poke.pos.y == float(y):
                add = False
        if add:
            poke_list.append(poke)


'''
Function to decide which next pokemon the agent will hunt
'''
def closest_pokemon(agent1, pokemons1):
    max_utility = 0
    #print("SRC: ",agent1.src)
    algo.Dijkstra(agent1.src)
    shortest_path = 0
    dest = 0
    i = 0
    check =0
    pok_index = 0
    #print("POKEMONSSSS ",pokemons1)
    for pok in pokemons1:
        if pok.eaten == False:
            if pok.type < 0:
                time = algo.graph.get_node(pok.edge.src).weight / agent1.speed
                po_dest = algo.get_graph().get_node(pok.edge.dest).point
                po_src = algo.get_graph().get_node(pok.edge.src).point
                x_dest, y_dest = po_dest.x, po_dest.y
                dist_dest_pok = ((x_dest - pok.pos.x) ** 2 + (y_dest - pok.pos.y) ** 2) ** 0.5
                dist_dest_src = ((x_dest - x_src) ** 2 + (y_dest - y_src) ** 2) ** 0.5
                add = (dist_dest_pok / dist_dest_src) * pok.edge.weight / agent1.speed
                time += add
                utility = pok.value / time
                if utility > max_utility:
                    max_utility = utility
                    dest = pok.edge.src
                    pok_index = i
                    check = 1
            else:
                # pok.typ > 0
                time = algo.graph.get_node(pok.edge.dest) / agent1.speed
                po_dest = algo.get_graph().get_node(pok.edge.src).point
                po_src = algo.get_graph().get_node(pok.edge.dest).point
                x_dest, y_dest = po_dest.x, po_dest.y
                dist_src_pok = ((x_src - pok.pos.x) * 2 + (y_src - pok.pos.y) * 2) ** 0.5
                dist_dest_src = ((x_dest - x_src) * 2 + (y_dest - y_src) * 2) ** 0.5
                add = (dist_src_pok / dist_dest_src) * pok.edge.weight / agent1.speed
                time += add
                utility = pok.value / time
                if utility > max_utility:
                    max_utility = utility
                    dest = pok.edge.dest
                    pok_index = i
                    check=2
        i += 1
    pokemons1[pok_index].eaten = False
    agent1.pokemon = pokemons1[pok_index]
    #print("CHOSEN POKEMON: ", agent1.pokemon)
    agent1.path = algo.shortest_path(agent1.src, dest)[1]
    print("PATH: ",agent1.path)
    if check == 1:
        agent1.path.append(pok.edge.dest)
    else:
        agent1.path.append(pok.edge.src)


node = -1


def run_prog(curr_agent):
    global node
    #print("ID:",client.get_agents())
    while 0 < len(curr_agent.path):
        client.choose_next_edge('{"agent_id":' + str(curr_agent.id) + ', "next_node_id":' + str(curr_agent.path[0]) + '}')
        curr_agent.path.pop(0)
        if len(curr_agent.path) == 1:
            node = curr_agent.path[0]
        #print(curr_agent.path)
        # print(client.get_info())
        client.move()
    curr_agent.src = node
    # print(poke_list)
    #print(poke_list)
should_run = True

while client.is_running() == 'true':
    pokemons = json.loads(client.get_pokemons(),
                          object_hook=lambda d: SimpleNamespace(**d)).Pokemons
    pokemons = [p.Pokemon for p in pokemons]
    for p in pokemons:
        x, y, _ = p.pos.split(',')
        p.pos = SimpleNamespace(x=my_scale(
            float(x), x=True), y=my_scale(float(y), y=True))
    agents = json.loads(client.get_agents(),
                        object_hook=lambda d: SimpleNamespace(**d)).Agents
    agents = [agent.Agent for agent in agents]
    for a in agents:
        x, y, _ = a.pos.split(',')
        a.pos = SimpleNamespace(x=my_scale(
            float(x), x=True), y=my_scale(float(y), y=True))
    # check events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit(0)

    # refresh surface
    screen.fill(Color(0, 0, 0))

    # draw nodes
    for n in graph.Nodes:
        x = my_scale(n.pos.x, x=True)
        y = my_scale(n.pos.y, y=True)

        # its just to get a nice antialiased circle
        gfxdraw.filled_circle(screen, int(x), int(y),
                              radius, Color(64, 80, 174))
        gfxdraw.aacircle(screen, int(x), int(y),
                         radius, Color(255, 255, 255))

        # draw the node id
        id_srf = FONT.render(str(n.id), True, Color(255, 255, 255))
        rect = id_srf.get_rect(center=(x, y))
        screen.blit(id_srf, rect)

    # draw edges
    for e in graph.Edges:
        # find the edge nodes
        src = next(n for n in graph.Nodes if n.id == e.src)
        dest = next(n for n in graph.Nodes if n.id == e.dest)

        # scaled positions
        src_x = my_scale(src.pos.x, x=True)
        src_y = my_scale(src.pos.y, y=True)
        dest_x = my_scale(dest.pos.x, x=True)
        dest_y = my_scale(dest.pos.y, y=True)

        # draw the line
        pygame.draw.line(screen, Color(61, 72, 126),
                         (src_x, src_y), (dest_x, dest_y))

    # draw agents
    for agent in agents:
        pygame.draw.circle(screen, Color(122, 61, 23),
                           (int(agent.pos.x), int(agent.pos.y)), 10)
    # draw pokemons (note: should differ (GUI wise) between the up and the down pokemons (currently they are marked in the same way).
    for p in pokemons:
        pygame.draw.circle(screen, Color(0, 255, 255), (int(p.pos.x), int(p.pos.y)), 10)

    # update screen changes
    display.update()

    # refresh rate
    clock.tick(60)

    # choose next edge
    agents_check_str = client.get_agents()
    agents_check = json.loads(agents_check_str)
    a_check = agents_check['Agents']
    ind = 0
    # print(agent.p)
    for agent in agent_list:
        print("SRC: ", agent.src)
        x1 = 0
        x2 = 0
        y1 = 0
        y2 = 0
        if agent.start == False:
            x1 = algo.graph.get_node(node).point.x
            id1 = algo.graph.get_node(node).node_id
            # print("x1: ",x1,'id: ',id1)
            y1 = algo.graph.get_node(node).point.y
            # print(a_check[ind]['Agent']['pos'])
            x2, y2, z2 = a_check[ind]['Agent']['pos'].split(',')
            # print("x2: ",x2)
        if abs(x1 - float(x2)) < eps and abs(y1 - float(y2)) < eps or agent.start:
            if agent.start == False:
                # print("before ",poke_list)
                poke_list.remove(agent.pokemon)
                # print("after ", poke_list)
                refresh_pock_list()
            agent.start = False
            # print("before: ", agent.path)
            closest_pokemon(agent, poke_list)
            print("path: ", agent.path)
            should_run = True
        ind += 1

    if len(agent_list) >= 1:
        for agent in agent_list:
            if should_run:
                run_prog(agent)
            should_run = False
    client.move()

    print(client.get_agents())
    client.move()
# game over:
