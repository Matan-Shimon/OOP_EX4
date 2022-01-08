from Data_Structure.Edge_Data import Edge_Data
from Data_Structure.Point2D import Point2D


class Pokemon:
    def __init__(self, pok_dict):
        self.value = pok_dict['value']
        self.type = pok_dict['type']
        x, y, z = pok_dict['pos'].split(',')
        self.pos = Point2D(float(x), float(y), float(z))
        self.eaten = False
        self.edge = None

    def __str__(self):
        return f"value: {self.value}, type: {self.type}, pos: {self.pos}\neaten: {self.eaten}, edge: {self.edge}"

    def __repr__(self):
        return f"value: {self.value}, type: {self.type}, pos: {self.pos}\neaten: {self.eaten}, edge: {self.edge}"