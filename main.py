from Population import Population


pop = Population(100, 2, 1, 13)
pop.run(100)

fittest = pop.best_genome

inp = [[0, 0], [1, 0], [0, 1], [1, 1]]
out = [0, 1, 1, 0]

correct = 0
for i, o in zip(inp, out):
    prediction = fittest.output(i)
    if o == round(*prediction):
        correct += 1

print(correct)
