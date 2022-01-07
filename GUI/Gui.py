"""
@author AchiyaZigi
OOP - Ex4
Very simple GUI example for python client to communicates with the server and "play the game!"
"""
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

bg = pygame.image.load("..\\Images\\background.jpg").convert()

#INSIDE OF THE GAME LOOP


client = Client()
client.start_connection(HOST, PORT)

pokemons = client.get_pokemons()

pokemons1 = json.loads(pokemons)

pokemons_obj = json.loads(pokemons, object_hook=lambda d: SimpleNamespace(**d))

print(pokemons)

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
                #client.add_agent(f'{"id":{str(edge["src"])}}')
            else:
                client.add_agent('{\"id\":'+str(edge["dest"])+'}')
                #client.add_agent(f'{"id":{str(edge["dest"])}}')
# client.add_agent("{\"id\":1}")
# client.add_agent("{\"id\":2}")
# client.add_agent("{\"id\":3}")

# this commnad starts the server - the game is running now

"""
The code below should be improved significantly:
The GUI and the "algo" are mixed - refactoring using MVC design pattern is required.
"""
BLUE = (0,0,255)
BLACK = (0,0,0)
WHITE = (240,248,255)

while client.is_running() == 'true':
    pokemons = json.loads(client.get_pokemons(),
                          object_hook=lambda d: SimpleNamespace(**d)).Pokemons
    pokemons = [p.Pokemon for p in pokemons]
    for p in pokemons:
        x, y, _ = p.pos.split(',')
        p.pos = SimpleNamespace(x=my_scale(
            float(x), x=True), y=my_scale(float(y), y=True))
        #print(p.pos)
    agents = json.loads(client.get_agents(),
                        object_hook=lambda d: SimpleNamespace(**d)).Agents
    agents = [agent.Agent for agent in agents]
    for a in agents:
        x, y, _ = a.pos.split(',')
        a.pos = SimpleNamespace(x=my_scale(
            float(x), x=True), y=my_scale(float(y), y=True))
        #print(a.pos)

    # check events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit(0)

    # refresh background
    bg = pygame.transform.scale(bg, screen.get_size())
    screen.blit(bg, (0, 0))

    # draw stop button
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
                    #print(action)
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
    # draw score
    text = font.render('score: '+str(grade), True, WHITE, BLACK)
    textRect = text.get_rect()
    screen.blit(text, (0,33,62,32))

    # draw moves
    moves = info_dic['GameServer']['moves']
    text = font.render('moves: ' + str(moves), True, WHITE, BLACK)
    textRect = text.get_rect()
    screen.blit(text, (0,66,124,32))

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
        #pygame.draw.circle(screen, Color(0, 0, 255), (int(x), int(y)), 10)

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
        pygame.draw.line(screen, Color(255,97,3),
                         (src_x, src_y), (dest_x, dest_y))

    # draw agents
    agent_img = pygame.image.load('..\\Images\\001-pokeball.png')
    for agent in agents:
        screen.blit(agent_img, (int(agent.pos.x)-15, int(agent.pos.y)-20))
        #pygame.draw.circle(screen, Color(122, 61, 23),
        #                   (int(agent.pos.x), int(agent.pos.y)), 10)

    pokemon_img = pygame.image.load('..\\Images\\002-pikachu.png')
    # draw pokemons (note: should differ (GUI wise) between the up and the down pokemons (currently they are marked in the same way).
    for p in pokemons:
        screen.blit(pokemon_img, (int(p.pos.x)-15, int(p.pos.y)-20))
        #pygame.draw.circle(screen, Color(0, 255, 255), (int(p.pos.x), int(p.pos.y)), 10)
    #print(client.time_to_end())
    pygame.time.delay(100)



