import unittest
from Data_Structure.Agent import Agent
from Data_Structure.Pokemon import Pokemon
from Data_Structure.Point2D import Point2D
from Data_Structure.DiGraph import DiGraph
from Data_Structure.GraphAlgo import GraphAlgo
from GUI import gameLogic


class MyTestCase(unittest.TestCase):
    agent_dict = {"id": "0", "value": "0", "src": "0", "dest": "-1", "speed": "10", "pos": "1,1,1"}
    agent = Agent(agent_dict)
    pok_dict1 = {"value": "5.0", "type": "-1 ", "pos": "2.5,2.5,0"}
    poke1 = Pokemon(pok_dict1)
    pok_dict2 = {"value": "5.0", "type": "1 ", "pos": "1.5,1.5,0"}
    poke2 = Pokemon(pok_dict2)
    pok_dict3 = {"value": "5.0", "type": "-1 ", "pos": "3.5,3.5,0"}
    poke3 = Pokemon(pok_dict3)
    poke_list = []
    poke_list.append(poke1)
    poke_list.append(poke2)
    poke_list.append(poke3)
    graph = DiGraph()
    graph.add_node(0, Point2D(0,0,0))
    graph.add_node(1, Point2D(1,1,1))
    graph.add_node(2, Point2D(2,2,2))
    graph.add_node(3, Point2D(3,3,3))
    graph.add_node(4, Point2D(4,4,4))
    graph.add_edge(0,1,1)
    graph.add_edge(1,2,1)
    graph.add_edge(2,3,1)
    graph.add_edge(3,4,1)
    algo = GraphAlgo(graph)

    def test_find_pok_edge(self):
        for pok in self.poke_list:
            gameLogic.find_pok_edge(pok, self.algo)
        edge = self.algo.graph.get_edge(1,2)
        self.assertEqual(self.poke_list[1].edge.src, edge.src)
        self.assertEqual(self.poke_list[1].edge.dest, edge.dest)

    def test_closest_pokemon(self):
        for pok in self.poke_list:
            gameLogic.find_pok_edge(pok, self.algo)
        gameLogic.closest_pokemon(self.agent, self.poke_list, self.algo)
        self.assertEqual(self.agent.pokemon, self.poke2)


if __name__ == '__main__':
    unittest.main()
