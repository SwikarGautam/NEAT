class Node:

    def __init__(self, id_n, layer):
        self.id_n = id_n
        self.value = 0
        self.layer = layer
        self.in_con = []

    # It returns a node assigning it a suitable id number from the id_dict
    @classmethod
    def create_node(cls, c, id_dict, id_timer, m):

        if c in id_dict:               # Checks if a node has been created between given two nodes
            return cls(id_dict[c], 2), id_dict, id_timer

        if len(id_dict) > 0:
            m = max(id_dict.values())

        id_dict[c] = m+1  # adds new key to id_dict if the connection has been divided for first time
        id_timer[c] = 0

        return cls(m+1, 2), id_dict, id_timer  # returns a node with maximum id number in the whole population