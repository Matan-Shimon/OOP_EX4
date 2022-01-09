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

# bg image
bg = pygame.image.load("..\\Images\\background.jpg").convert()


client = Client()
# start the connection with the server
client.start_connection(HOST, PORT)

pokemons = client.get_pokemons()

pokemons1 = json.loads(pokemons)

pokemons_obj = json.loads(pokemons, object_hook=lambda d: SimpleNamespace(**d))

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

eps = 0.001
p = pokemons1['Pokemons']
poke_list = []
agent_list = []
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
            else:
                client.add_agent('{\"id\":'+str(edge["dest"])+'}')

# this command starts the server - the game is running now
client.start()

agents_str = client.get_agents()
agents = json.loads(agents_str)
a = agents['Agents']

for agent in a:
    ag = Agent(agent['Agent'])
    agent_list.append(ag)

BLUE = (0,0,255)
BLACK = (0,0,0)
WHITE = (240,248,255)



'''
Function to decide which next pokemon the agent will hunt
'''
def closest_pokemon(agent1, pokemons1):
    max_utility = 0
    algo.Dijkstra(agent1.src)
    shortest_path = 0
    i = 0
    pok_index = 0
    if len(pokemons1) > 0:
        for pok in pokemons1:
            if pok.eaten == False:
                    time = algo.graph.get_node(pok.edge.src).weight / agent1.speed
                    time += pok.edge.weight / agent1.speed
                    utility = pok.value / time
                    if utility > max_utility:
                        max_utility = utility
                        src = pok.edge.src
                        pok_index = i
            i += 1
    pokemons1[pok_index].eaten = True
    agent1.pokemon = pokemons1[pok_index]
    agent1.path = algo.shortest_path(agent1.src, pokemons1[pok_index].edge.src)[1]
    agent1.path.append(pokemons1[pok_index].edge.dest)
    return pokemons1

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
            if pokemon.type < 0:
                # src > dest
                if algo.graph.get_node(edge['src']).node_id > algo.graph.get_node(edge['dest']).node_id:
                    real_edge = Edge_Data(edge['src'], edge['dest'], edge['w'], 0)
                    pokemon.edge = real_edge
                else:
                    real_edge = Edge_Data(edge['dest'], edge['src'], edge['w'], 0)
                    pokemon.edge = real_edge
                break
            elif pokemon.type > 0:
                # dest > src
                if algo.graph.get_node(edge['dest']).node_id > algo.graph.get_node(edge['src']).node_id:
                    real_edge = Edge_Data(edge['src'], edge['dest'], edge['w'], 0)
                    pokemon.edge = real_edge
                else:
                    real_edge = Edge_Data(edge['dest'], edge['src'], edge['w'], 0)
                    pokemon.edge = real_edge
                break

'''
Function that checks for new pokemons that came
'''
def refresh_pock_list():
    pokemons_str = client.get_pokemons()
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

should_move = 0
'''
This code below will till the server will disconnect us after a specific amount of time,
or after we will force stop the connection from the server by clicking the "stop" button.
'''
while client.is_running() == 'true':
    # loading the pokemons from the server
    pokemons = json.loads(client.get_pokemons(),
                          object_hook=lambda d: SimpleNamespace(**d)).Pokemons
    pokemons = [p.Pokemon for p in pokemons]
    # scaling the pokemons
    for p in pokemons:
        x, y, _ = p.pos.split(',')
        p.pos = SimpleNamespace(x=my_scale(
            float(x), x=True), y=my_scale(float(y), y=True))
    # loading the agents from the server
    agents = json.loads(client.get_agents(),
                        object_hook=lambda d: SimpleNamespace(**d)).Agents
    agents = [agent.Agent for agent in agents]
    # scaling the agents
    for a in agents:
        x, y, _ = a.pos.split(',')
        a.pos = SimpleNamespace(x=my_scale(
            float(x), x=True), y=my_scale(float(y), y=True))

    # check events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit(0)

    # refresh background
    bg = pygame.transform.scale(bg, screen.get_size())
    screen.blit(bg, (0, 0))

    # stop button
    font = pygame.font.Font('freesansbold.ttf', 32)
    button_col = (0, 0, 0)
    hover_col = (75, 225, 255)
    click_col = (50, 150, 255)
    text_col = (255, 255, 255)
    clicked = False
    pos = pygame.mouse.get_pos()


    class Button:
        def __init__(self):
            pass

        def draw_button(self):
            global clicked
            action = False
            button_rect = Rect(0,0,180,32)
            if button_rect.collidepoint(pos):
                if pygame.mouse.get_pressed()[0] == 1:
                    clicked = True
                    action = True
                    pygame.draw.rect(screen, click_col, button_rect)
                elif pygame.mouse.get_pressed()[0] == 0 and clicked == True:
                    clicked = False
                    action = True
                else:
                    pygame.draw.rect(screen, hover_col, button_rect)
            else:
                pygame.draw.rect(screen, button_col, button_rect)

            text_img = font.render("stop", True, text_col)
            text_rect = text_img.get_rect()
            screen.blit(text_img, text_rect)
            return action

    button = Button()
    if button.draw_button():
        client.stop_connection()

    # the score itself
    info_str = client.get_info()
    info_dic = json.loads(info_str)
    grade = info_dic['GameServer']['grade']
    # score
    text = font.render('score: '+str(grade), True, WHITE, BLACK)
    textRect = text.get_rect()
    screen.blit(text, (0,33,62,32))

    # moves
    moves = info_dic['GameServer']['moves']
    text = font.render('moves: ' + str(moves), True, WHITE, BLACK)
    textRect = text.get_rect()
    screen.blit(text, (0,66,124,32))

    # nodes
    for n in graph.Nodes:
        x = my_scale(n.pos.x, x=True)
        y = my_scale(n.pos.y, y=True)

        # its just to get a nice antialiased circle
        gfxdraw.filled_circle(screen, int(x), int(y),
                              radius, Color(64, 80, 174))
        gfxdraw.aacircle(screen, int(x), int(y),
                         radius, Color(255, 255, 255))

        # the node id
        id_srf = FONT.render(str(n.id), True, Color(255, 255, 255))
        rect = id_srf.get_rect(center=(x, y))
        screen.blit(id_srf, rect)

    # edges
    for e in graph.Edges:
        # find the edge nodes
        src = next(n for n in graph.Nodes if n.id == e.src)
        dest = next(n for n in graph.Nodes if n.id == e.dest)

        # scaled positions
        src_x = my_scale(src.pos.x, x=True)
        src_y = my_scale(src.pos.y, y=True)
        dest_x = my_scale(dest.pos.x, x=True)
        dest_y = my_scale(dest.pos.y, y=True)

        # the line
        pygame.draw.line(screen, Color(255,97,3),
                         (src_x, src_y), (dest_x, dest_y))

    # agents
    agent_img = pygame.image.load('..\\Images\\001-pokeball.png')
    for agent in agents:
        screen.blit(agent_img, (int(agent.pos.x)-15, int(agent.pos.y)-20))

    pokemon_img = pygame.image.load('..\\Images\\002-pikachu.png')
    for p in pokemons:
        screen.blit(pokemon_img, (int(p.pos.x)-15, int(p.pos.y)-20))

    # update screen changes
    display.update()

    # updating the current src and dest for each agent
    agents2 = json.loads(client.get_agents(),
                         object_hook=lambda d: SimpleNamespace(**d)).Agents
    agents2 = [agent.Agent for agent in agents2]

    index = 0
    for agent in agents2:
        agent_list[index].src = agent.src
        agent_list[index].dest = agent.dest
        x,y,z = agent.pos.split(",")
        point = Point2D(float(x), float(y), 0)
        agent_list[index].pos = point
        index += 1

    # checking if there are pokemons that are going to be eaten "on the way".
    for agent in agent_list:
        for pok in poke_list:
            src_ind = -1
            dest_ind = -1
            ind1 = 0
            for p in agent.path:
                if p == pok.edge.src:
                    src_ind = ind1
                if p == pok.edge.dest:
                    dest_ind = ind1
                ind1 += 1
            if src_ind+1 == dest_ind:
                pok.eaten = True

    # refresh rate
    clock.tick(60)
    # the proccess itself
    for agent in agent_list:
        if agent.dest == -1:
            if len(agent.path) > 0:
                client.choose_next_edge('{"agent_id":'+str(agent.id)+', "next_node_id":'+str(agent.path[0])+'}')
                agent.path.pop(0)
            else:
                refresh_pock_list()
                poke_list = closest_pokemon(agent, poke_list)
    pygame.time.delay(100)
    client.move()

    if int(client.time_to_end()) < 20:
        client.stop_connection()