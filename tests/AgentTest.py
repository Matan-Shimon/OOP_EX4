import unittest
from Data_Structure.Agent import Agent

class MyTestCase(unittest.TestCase):
    dict = {"id": "0", "value": "0", "src": "0", "dest": "-1", "speed": "10", "pos": "1,1,1"}
    agent = Agent(dict)

    def test_pokemon(self):
        self.assertEqual(self.agent.pokemon,0)



    def test_get_speed(self):
        self.assertEqual(self.agent.speed,'10')


    def test_get_src(self):
        self.assertEqual(self.agent.src,'0')



    def test_get_dest(self):
        self.assertEqual(self.agent.dest,'-1')