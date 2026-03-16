# crossover (selection too) and mutation functions needed
from .population import Population
from circuit import Circuit
from config import TOURNAMENT_SIZE, GATE_SET, MUTANT_INSERT_SIZE, MUTANT_SHRINK_SIZE
import random, math
from .initialisation import create_random_circuit, create_random_gate

def selection(population: Population):
    # select based on tournmanet size
    
    sample = population.sample_population(TOURNAMENT_SIZE)
    
    best_fitness = 0
    best_circuit = None
    
    for index in range(TOURNAMENT_SIZE):
        member_fitness = sample.fitnesses[index]
        member_circuit = sample.member(index)
        
        if member_fitness > best_fitness:
            best_fitness = member_fitness
            best_circuit = member_circuit
            
    return best_circuit

def pareto_tournament_selection(population: Population):
    # select based on tournament size and pareto dominance
    
    sample = population.sample_population(TOURNAMENT_SIZE)
    best = sample.member(0)
    
    for i in range(1, TOURNAMENT_SIZE):
        candidate = sample.member(i)
        
        if dominates(candidate, best):
            best = candidate
        elif dominates(best, candidate):
            continue
        else:
            # tie break - p% to compare fitness, (100-p)% to compare noise
            if random.random() < 0.80:
                if candidate.fitness > best.fitness:
                    best = candidate
            else:
                if candidate.noise > best.noise:
                    best = candidate
                    
    return best

# for minimising fitness function - depends on it
# LEGACY
def selection_min(population: Population):
    # select based on tournmanet size
    
    sample = population.sample_population(TOURNAMENT_SIZE)
    
    best_fitness = math.inf
    best_circuit = None
    
    for index in range(TOURNAMENT_SIZE):
        member_fitness = sample.fitnesses[index]
        member_circuit = sample.member(index)
        
        if member_fitness < best_fitness:
            best_fitness = member_fitness
            best_circuit = member_circuit
            
    return best_circuit

def dominates(circuit_one: Circuit, circuit_two: Circuit):
    not_worse = (circuit_one.fitness >= circuit_two.fitness) and (circuit_one.noise >= circuit_two.noise)
    one_better = (circuit_one.fitness > circuit_two.fitness) or (circuit_one.noise > circuit_two.noise)
    
    return not_worse and one_better
 
def crossover(parent_one: Circuit, parent_two: Circuit) -> list[Circuit]:
    #pick two random points (one on each circuit)
    # split at random point - 1 -> 1.1 and 1.2, 2 -> 2.1 and 2.2
    # Circuit 1.1 merge with circuit 2.2, Circuit 1.2 merge with circuit 2.1
    # return them (new children) in an array
    
    split_one = random.randint(0, parent_one.length - 2)
    split_two = random.randint(0, parent_two.length - 2)
    
    parent_one_a, parent_one_b = parent_one.split(split_one)
    parent_two_a, parent_two_b = parent_two.split(split_two)
    
    children = [parent_one_a.combine(parent_two_b), parent_two_a.combine(parent_one_b)]
    
    return children

def mutation(parent: Circuit) -> Circuit:
    # mutate one gate in the circuit to another random one 
    
    child = parent.copy()
    
    new_gate = random.choice(GATE_SET)
    position = random.randint(0, child.length - 1)
    
    child.swap(position, new_gate)
    
    return child

def wire_mutation(parent: Circuit) -> Circuit:
    
    # copy child and generate wire values
    child = parent.copy()
    num_wires = child.num_wires
    wire_values = list(range(0, num_wires))
      
    # get random gate and change wires to random
    position = random.randint(0, child.length - 1)
    gate = child.circuit[position]
    gate.wires = random.sample(wire_values, gate.arity)

    return child

# a generalised crossover - can be any given middle section from the circuit (cut at two points)
def insertion(parent_one: Circuit, parent_two: Circuit) -> list[Circuit]:
    # takes chunk from each circuit 
    # swaps chunks between them
    # generalised crossover
    
    split_one_a = random.randint(0, parent_one.length - 2)
    split_one_b = random.randint(split_one_a, parent_one.length - 2)
    
    split_two_a = random.randint(0, parent_two.length - 2)
    split_two_b = random.randint(split_two_a, parent_two.length - 2)
    
    parent_one_left, parent_one_middle, parent_one_right = parent_one.split_three(split_one_a, split_one_b)
    parent_two_left, parent_two_middle, parent_two_right = parent_two.split_three(split_two_a, split_two_b)
    
    child_one = parent_one_middle.insert_between(parent_two_left, parent_two_right)
    child_two = parent_two_middle.insert_between(parent_one_left, parent_one_right)
    
    return [child_one, child_two]

def insert_mutation(parent: Circuit) -> Circuit:
    
    mutant_circuit = create_random_circuit(MUTANT_INSERT_SIZE['min'], MUTANT_INSERT_SIZE['max'])
    split_point = random.randint(0, parent.length - 2) # split point to add new
    
    left, right = parent.split(split_point)
    child = mutant_circuit.insert_between(left, right)
    
    return child

def shrink_mutation(parent: Circuit) -> Circuit:
    
    if parent.length > 2:
        mutant_gate = create_random_gate()
        remove_size = random.randint(MUTANT_SHRINK_SIZE['min'], MUTANT_SHRINK_SIZE['max'])
        
        remove_point = random.randint(0, parent.length-remove_size)
        
        parent.swap(remove_point, mutant_gate)
        parent.remove_gates(remove_point+1, remove_size-1)
    
    return parent
    
    
    
    