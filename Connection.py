import random


class Connection:

    def __init__(self, input_, out, innov_no):
        self.inp = input_
        self.out = out
        self.weight = random.gauss(0, 1.5)  # best gauss(0, 1)
        self.enabled = True
        self.innov_no = innov_no

    # It returns a connection given two nodes to be connected and assigns it innovation number from innpv_dict
    @classmethod
    def create_connection(cls, input_n, output_n, inno_dict):

        if (input_n.id_n, output_n.id_n) in inno_dict:
            return cls(input_n, output_n, inno_dict[input_n.id_n, output_n.id_n]), inno_dict

        m = max(inno_dict.values()) if len(inno_dict) > 0 else 0
        inno_dict[(input_n.id_n, output_n.id_n)] = m+1  # adds new innovation number entry if not already existing

        return cls(input_n, output_n, m+1), inno_dict