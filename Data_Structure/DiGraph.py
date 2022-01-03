from Data_Structure.Node_Data import Node_Data
from Data_Structure.Edge_Data import Edge_Data
from Data_Structure.Point2D import Point2D
import random


class DiGraph:
    """""
   node_map - gonna represent the node by a hash map,the key gonna be the node.key and the value gonna be the NodeData
   edge_map - gonna represent the edges between the node by a hash map,the key gonna be src node and the value
   gonna be a hash map which is  the key gonna be the dest node and the value gonna be the EdgeData.
   edgeSize - gonna help us later to know how much edge we got at all
   nodeSize - same as edgeSize gonna help us later.
   MC - with MC we track how many changes we made in the graph.
    """""
    def __init__(self, nodeSize=0, edgeSize=0, node_map={}, edge_map={}, MC=0) -> None:
        self.nodeSize = nodeSize
        self.edgeSize = edgeSize
        self.MC = MC
        self.node_map = {}
        self.edge_map = {}

    def v_size(self) -> int:
        return self.nodeSize

    def e_size(self) -> int:
        return self.edgeSize
    """""
    this function return an dict for all nodes in graph
    key is node_id and value is Node_Data
    """""
    def get_all_v(self) -> dict:
        v_dic = {}
        for node, node_data in self.node_map.items():
            from_node = len(self.all_out_edges_of_node(node))
            to_node = len(self.all_in_edges_of_node(node))
            N = self.get_node(node)
            N.out_edges = from_node
            N.in_edges = to_node
            v_dic[node] = N
        return v_dic
    """""
    Return the node by the key if not existed return None
    """""
    def get_node(self, id):
        try:
            return self.node_map[id]
        except:
            return None

    """""
       Return the edge by if not existed return None
    """""
    def get_edge(self, src_id, dest_id):
        try:
            return self.edge_map[src_id][dest_id]
        except:
            return None
    """""
    this function return an dict for all edges that going in from node_id in graph.
    """""
    def all_in_edges_of_node(self, id1: int) -> dict:
        inside = {}
        node_keys = self.node_map.keys()
        for i in node_keys:
            if self.get_edge(i, id1) != None:
                inside[i] = self.get_edge(i, id1).getWeight()
        return inside
    """""
    this function return an dict for all edges that going out from node_id in graph.
    """""
    def all_out_edges_of_node(self, id1: int) -> dict:
        outside = {}
        for dest_key, edge_data in self.edge_map[id1].items():
            outside[dest_key] = edge_data.getWeight()
        return outside
    """""
    MC is a variable that indicate how many changes we did on the graph
    """""
    def get_mc(self) -> int:
        return self.MC

    """""
    this function add a node to the hash map that keep nodes
    and return true if we deed add him.
    """""
    def add_node(self, node_id: int, pos: tuple = None) -> bool:
        if self.get_node(node_id) != None:
            print("The node is already exist")
            return False
        else:
            if pos == None:
                x = random.random()
                y = random.random()
                x *= 10
                y *= 10
                z = 0
                pos = Point2D(x,y,0)
            node_data = Node_Data(pos, 0, self.nodeSize, 0)
            self.node_map[node_id] = node_data
            self.edge_map[node_id] = {}
            self.nodeSize += 1
            self.MC += 1
            return True
    """""
    this function connect two node and adding an edge between them.
    """""
    def add_edge(self, id1: int, id2: int, weight: float) -> bool:
        if weight >= 0:
            if self.get_node(id1) == None or self.get_node(id1) == None:
                print("One or more of the given nodes is not exist")
                return False
            else:
                if self.get_edge(id1,id2) != None:
                    print("The edge is already exists")
                    return False
                else:
                    edge_data = Edge_Data(id1, id2, weight, 0)
                    self.edge_map[id1][id2] = edge_data
                    self.edgeSize += 1
                    self.MC += 1
                    return True
        else:
            print("Edge weight cannot be negative")
            return False
    """""
    this function return the if we deed remove the node.
    this function remove also all edges that going out from this node and to him.
    we put in try and catch cause we might try removing a node that node existed.  
    """""

    def remove_node(self, node_id: int) -> bool:
        if self.get_node(node_id) == None:
            print("The node does not exist")
            return False
        else:
            # removing all the out edges
            self.edge_map.pop(node_id)
            # removing all the in edges
            node_keys = self.node_map.keys()
            for node in node_keys:
                if self.get_edge(node, node_id) != None:
                    self.edge_map[node].pop(node_id)

            # removing the node itself
            self.node_map.pop(node_id)
            self.nodeSize -= 1
            self.MC += 1
            return True
    """""
     this function return the True if we deed remove the node
     if the node isn't exist we return false 
    """""
    def remove_edge(self, node_id1: int, node_id2: int) -> bool:
        if self.get_edge(node_id1, node_id2) == None:
            print("The edge does not exist")
            return False
        else:
            self.edge_map[node_id1].pop(node_id2)
            self.edgeSize -= 1
            self.MC += 1
            return True

    def get_nodes(self):
        nodes = []
        for id,node_data in self.node_map.items():
            pos = f"{node_data.point.x},{node_data.point.y},{node_data.point.z}"
            dic = {"pos":pos,"id":id}
            nodes.append(dic)
        return nodes

    def get_edges(self):
        edges = []
        for src,src_edges in self.edge_map.items():
            for dest, edge_data in src_edges.items():
                dic = {"src":src,"w":edge_data.weight,"dest":dest}
                edges.append(dic)
        return edges

    def __str__(self):
        return f"Graph: |V|={self.nodeSize} , |E|={self.edgeSize}"

    def __repr__(self):
        return f"Graph: |V|={self.nodeSize} , |E|={self.edgeSize}"