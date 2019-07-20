import random
from Genome import Genome
from Connection import Connection
from Node import Node
from copy import deepcopy


# In this implementation, nodes are assigned an id number on the basis of the input and output nodes of the connection
# that has been divides in add-node mutation. So in all the genome,the nodes that have been created by dividing the
# connection between node 1 and node 3 receive same id number. This information is stored in id_dict which is a python
# dictionary
# There is also an alternative method as shown in line 112.
class Population:

    def __init__(self, t_population, input_n, output_n, target_fitness):

        self.t_pop = t_population
        self.input_n = input_n
        self.output_n = output_n
        self.innov_dict = {}
        self.id_dict = {}
        # id_dict is dictionary that has the tuple of id number of two nodes joined by a connection as key and the id
        # number of node created by dividing the connection as value of the key
        self.id_timer = {}
        self.population = []
        self.species = []
        self.species_fitness_counter = []
        self.species_max_fitness = []
        self.population_max = 0
        self.population_max_timer = 0
        self.best_genome = Genome()  # The fittest genome to ever exist in the population
        self.target = target_fitness
    # creates and returns a new genome
    def create_genome(self):

        gen = Genome()
        for i in range(self.input_n):
            N = Node(i+1, 0)
            gen.inp.append(N)
            gen.nodes.append(N)
        for o in range(self.output_n):
            N = (Node(o+1+self.input_n, 1))
            gen.out.append(N)
            gen.nodes.append(N)
        for n in gen.nodes:
            if n.layer == 0:
                for m in gen.nodes:
                    if m.layer == 1:
                        c, self.innov_dict = Connection.create_connection(n, m, self.innov_dict)
                        gen.connections.append(c)
                        gen.connection_set.add((n.id_n, m.id_n))
        for c in gen.connections:
            c.out.in_con.append(c)
        return gen

    # creates population with given number of genome
    def create_pop(self):
        for i in range(self.t_pop):
            gen = self.create_genome()
            self.population.append(gen)

    # removes entries from id_dict if they have existed for more than 20 generations
    def update_id_dict(self):
        dic = {}
        for k, v in self.id_timer.items():
            if v < 20:
                dic[k] = v+1
            else:
                del self.id_dict[k]

        self.id_timer = dic

    # mutates the given genome: which includes adding new node or changing connection weight or adding new connection
    def mutate(self, genome):

        if random.uniform(0, 1) < 0.9:  # random.randint(0, 100)/100 < 0.9:  # best 0.9

            for c in genome.connections:
                if random.uniform(0, 1) < 0.01:  # toggles the enabling of the connection
                    c.enabled = not c.enabled
                if random.uniform(0, 1) < 0.9:
                    if random.uniform(0, 1) < 0.5:
                        c.weight -= c.weight*0.2
                    else:
                        c.weight += c.weight*0.2

                    if c.weight > 50:
                        c.weight = 50
                    if c.weight < -50:
                        c.weight = -50
                else:
                    c.weight = random.uniform(-5, 5)

        if random.uniform(0, 1) < 0.01:  # adds new node the genome
            c = random.choice(genome.connections)
            redo = False
            if c in self.id_dict:
                if self.id_dict[c] in genome.node_ids():
                    redo = True
            counter = 0
            while not c.enabled or redo:  # checks if the connection is enabled and if the connection has already been divided
                redo = False
                c = random.choice(genome.connections)
                if c in self.id_dict:
                    if self.id_dict[c] in genome.node_ids():
                        redo = True
                counter += 1
                if counter >= 20:
                    return
            c.enabled = False
            N, self.id_dict, self.id_timer = Node.create_node(c, self.id_dict, self.id_timer, self.input_n+self.output_n)
            # N = Node(max(genome.node_ids())+1,2) # alternative way to create a node, which doesn't use id_dict and the
            # id number given to the new node is maximum of the genome + 1
            # if you want to use it just uncomment the line and comment the upper line
            genome.nodes.append(N)
            c1, self.innov_dict = Connection.create_connection(c.inp, N, self.innov_dict)
            c1.weight = 1
            genome.connections.append(c1)
            genome.connection_set.add((c.inp.id_n, N.id_n))
            N.in_con.append(c1)
            c2, self.innov_dict = Connection.create_connection(N, c.out, self.innov_dict)
            c2.weight = c.weight
            genome.connections.append(c2)
            genome.connection_set.add((N.id_n, c.out.id_n))
            c2.out.in_con.append(c2)

        if random.uniform(0, 1) < 0.1:  # adds new connection in the connection list
            n1, n2 = random.sample(genome.nodes, 2)
            counter = 0
            while (n1.id_n, n2.id_n) in genome.connection_set or (n2.id_n, n1.id_n) in genome.connection_set or n1 in genome.out or n2 in genome.inp:
                n1, n2 = random.sample(genome.nodes, 2)
                counter += 1
                if counter >= 20:
                    return
            c, self.innov_dict = Connection.create_connection(n1, n2, self.innov_dict)
            genome.connections.append(c)
            genome.connection_set.add((n1.id_n, n2.id_n))
            n2.in_con.append(c)

    # produces new offspring by crossover of two parent genome
    def crossover(self, genome1, genome2):

        gen = self.create_genome()
        dominant = genome1 if genome1.fitness > genome2.fitness else genome2  # more fit parent is called dominant
        recessive = genome1 if genome1.fitness <= genome2.fitness else genome2  # less fit parent is called recessive

        for cd in dominant.connections:

            for cr in recessive.connections:

                if cd.innov_no == cr.innov_no:

                    g = random.choice([cd, cr])
                    g1 = deepcopy(g)
                    g1.enabled = g1.enabled

                    if not cd.enabled and not cr.enabled:

                        if random.uniform(0, 1) < 0.25:
                            g1.enabled = True
                    elif not cd.enabled or not cr.enabled:

                        if random.uniform(0, 1) < 0.08:
                            g1.enabled = False
                    else:
                        g1.enabled = True

                    gen.add_connection(g1)
                    break

                if genome1.fitness == genome2.fitness:

                    dis = (genome1.gen_innov() ^ genome2.gen_innov()) - gen.gen_innov()

                    if cr.innov_no in dis:

                        g1 = deepcopy(cr)
                        gen.add_connection(g1)

                    if cd.innov_no in dis:

                        g1 = deepcopy(cd)
                        gen.add_connection(g1)

        # adds genes of more fit parent
        if genome1.fitness != genome2.fitness:

            for cd in dominant.connections:

                if cd.innov_no not in gen.gen_innov():

                    g1 = deepcopy(cd)
                    gen.add_connection(g1)

        return gen

    # finds compatibility between two genomes
    @staticmethod
    def compatibility( genome1, genome2, c1=1, c2=1, c3=0.2):

        g1 = genome1.gen_innov()
        g2 = genome2.gen_innov()

        t = min(max(g1), max(g2))
        excess = {x for x in g1 ^ g2 if x > t}
        disjoint = {x for x in g1 ^ g2 if x <= t}
        weight_diff = 0

        for c_1 in genome1.connections:
            for c_2 in genome2.connections:
                if c_1.innov_no == c_2.innov_no:
                    weight_diff += abs(c_1.weight - c_2.weight)
                    break

        N = max(len(g1), len(g2)) if max(len(g1), len(g2)) > 20 else 1  # it is written in the paper but the author has
        # said in neat user page that it is not necessary . So N can be set to be always equal to 1
        compatibility = (c1*len(excess) + c2*len(disjoint)) / N + (c3*weight_diff)

        return compatibility

    # finds the species to which a genome belongs and adds it to the species
    def find_species(self, genome1, thresh=3.0, new_species=None):
        # it compares given genome with first genome of each species and adds to new species if given else it adds to
        # self.species
        for i, s in enumerate(self.species):
            gen = list(s)[0]
            if self.compatibility(gen, genome1) < thresh:
                if new_species is None:
                    s[genome1] = 0
                else:
                    new_species[i][genome1] = 0
                return
        if new_species is None:
            self.species.append({genome1: 0})

        else:
            for i in range(len(self.species), len(new_species)):
                s = new_species[i]
                gen = list(s)[0]
                if self.compatibility(gen, genome1) < thresh:
                    s[genome1] = 0

                    return
            new_species.append({genome1: 0})

    # creates a mating pool and produces offsprings for next generation
    def reproduce(self):

        self.update_species()
        self.population = []
        fitness_list = []
        new_species = []
        for s in self.species:
            fitness_list.append(sum(list(s.values()))/len(s))
            new_species.append({})
        t_fitness = sum(fitness_list)
        prob_list = [round(x*self.t_pop/t_fitness) for x in fitness_list]
        self.find_species(self.best_genome, new_species=new_species)
        self.population.append(self.best_genome)
        for s, j in zip(self.species, prob_list):

            if len(s) == 1:
                for k in range(j):
                    offspring0 = list(s)[0]
                    offspring = deepcopy(offspring0)
                    self.mutate(offspring)
                    self.find_species(offspring, new_species=new_species)
                    self.population.append(offspring)
                continue

            for k in range(j):

                if len(s) > 5 and k == 0:
                    offspring0 = max(s, key=s.get)  # adds the fittest genome of species with more than 5 genome
                    offspring = deepcopy(offspring0)   # and deletes the lowest performing genomes
                    for _ in range(round(len(s)/5)):
                        del s[min(s, key=s.get)]

                else:

                    if random.uniform(0, 1) < 0.25:  # 25% of next generation is created by mutation without crossover
                        offspring0 = random.choice(list(s))
                        offspring = deepcopy(offspring0)
                        self.mutate(offspring)
                    else:
                        a, b = random.sample(list(s), 2)
                        offspring = self.crossover(a, b)
                        self.mutate(offspring)
                self.find_species(offspring, new_species=new_species)
                self.population.append(offspring)
        self.calc_fitness(new_species)
        remove = []

        for i in range(len(new_species)):
            if len(new_species[i]) == 0:
                remove.append(i)
        remove.sort(reverse=True)
        for i in remove:
            del new_species[i]
            del self.species_fitness_counter[i]
            del self.species_max_fitness[i]
        self.species = new_species

    # calculates fitness of a genome for XOR problem
    # you should change this function to use for other problems
    def calc_fitness(self, species):

        for s in species:
            sp_list = list(s)
            for g in sp_list:
                fit = 0
                fit = abs(sum(g.output([0, 0])))+abs(sum(g.output([1, 0]))-1)+abs(sum(g.output([0, 1]))-1)+abs(sum(g.output([1, 1])))
                fit = (4 - fit)**2
                g.fitness = fit
                if g.fitness > self.population_max:
                    self.best_genome = g
                s[g] = fit

    # removes stagnant species whose max fitness has not increased for 15 consecutive generations
    def update_species(self):

        remove = []
        for i in range(len(self.species)):
            if i < len(self.species_max_fitness):
                if max(self.species[i].values()) > self.species_max_fitness[i]:
                    self.species_max_fitness[i] = max(self.species[i].values())
                    self.species_fitness_counter[i] = 0
                else:
                    self.species_fitness_counter[i] += 1
            else:
                self.species_max_fitness.append(0)
                self.species_fitness_counter.append(0)
            if self.species_fitness_counter[i] > 15:
                remove.append(i)

        remove.sort(reverse=True)

        for i in remove:
            del self.species_fitness_counter[i]
            del self.species_max_fitness[i]
            del self.species[i]
        # only the top two species are allowed to reproduce if the maximum fitness of the whole population has not
        # increased for 20 consecutive generations
        if max(self.species_max_fitness) > self.population_max:
            self.population_max = max(self.species_max_fitness)
            self.population_max_timer = 0
        else:
            self.population_max_timer += 1

        if self.population_max_timer > 20:
            new = sorted(self.species, key=lambda x: max(x.values()), reverse=True)
            self.species = new[:2]
            self.species_max_fitness = [max(x.values()) for x in self.species]
            self.species_fitness_counter = [0, 0]
            self.population_max_timer = 0

    # creates new generations
    def run(self, generation):
        self.create_pop()
        for g in self.population:
            self.find_species(g)
        self.species_fitness_counter = [0 for _ in self.species]
        self.calc_fitness(self.species)
        self.species_max_fitness = [max(x.values()) for x in self.species]
        for i in range(generation):
            print('generation:', i)
            print('maximum fitness:', self.population_max)  # prints maximum of the population
            self.reproduce()
            self.update_id_dict()  # it is not completely necessary and you may comment it out
            if self.population_max >= self.target:
                return

