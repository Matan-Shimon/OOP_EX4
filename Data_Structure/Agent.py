# from Data_Structure import Point2D
from Data_Structure.Point2D import Point2D


class Agent:

    def __init__(self, agent_dict) -> None:
        self.id = agent_dict["id"]
        self.value = agent_dict["value"]
        self.src = agent_dict["src"]
        self.dest = agent_dict["dest"]
        self.speed = agent_dict["speed"]
        x, y, z = agent_dict["pos"].split(',')
        self.pos = Point2D(float(x), float(y), float(z))
        self.path = []

    def get_id(self):
        return  self.id

    def get_speed(self):
        return self.speed

    def set_speed(self, new_speed):
        self.speed = new_speed

    def get_src(self):
        self.src

    def get_dest(self):
        self.dest

    def set_src(self, new_src):
        self.src

    def set_dest(self, new_dest):
        self.dest

    def set_location(self, new_point):
        self.pos = new_point

    def __str__(self):
        return f"id: {self.id}, src: {self.src}, dest: {self.dest}, speed: {self.speed}, value: {self.value}"

    def __repr__(self):
        return f"id: {self.id}, src: {self.src}, dest: {self.dest}, speed: {self.speed}, value: {self.value}"