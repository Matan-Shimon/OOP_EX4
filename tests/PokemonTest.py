import unittest
from Data_Structure.Pokemon import Pokemon
from Data_Structure.Edge_Data import Edge_Data


class MyTestCase(unittest.TestCase):
    dict = {"value" : "5.0", "type": "-1 ", "pos" : "1.4,2.3,4.4"}
    poke = Pokemon(dict)

    def test_eaten(self):
        # dict = {"value : 5" ,"type: -1 ", "pos : 1.4,2.3,4.4"}
        # poke = Pokemon(dict)
        self.assertEqual(self.poke.eaten ,False ,"0")

    def test_set_edge(self):
        edge = Edge_Data(1, 2, 3, 0)
        self.assertEqual(self.poke.edge ,None ,"0")
        self.poke.set_edge(edge)
        self.assertEqual(self.poke.edge.src,edge.src)

    def test_lt(self):
        dict2= {"value": "6.0", "type": "-1 ", "pos": "1.4,2.3,4.4"}
        poke2 = Pokemon(dict2)
        self.assertEqual(self.poke._lt_(poke2),True)