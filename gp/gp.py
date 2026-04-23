# representation [[gate, wires, params], ...]

from config import NUM_GENERATIONS, CUMULATIVE_PROB, build_cumulative_prob, ELITE_COUNT, SUBSET_PROPORTION, SUCCESS_VALUE
from .initialisation import init_population
from evaluation import CircuitFitness
from .operations import *
from .population import Population
from .data_process import get_data, sample_data
import random, csv
import numpy as np

from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator
from qiskit_aer.noise import NoiseModel, depolarizing_error
from qiskit.primitives import StatevectorSampler
from qiskit.quantum_info import Statevector, DensityMatrix, state_fidelity

def evolution() -> Population:
    
    with open(r'data/fitness_output.csv', 'w') as f:
        titles = ['gen', 'average', 'best', 'numgood', 'mean_size', 'median_size', '10_percentile_size', '90_percentile_size', 'best_noise', 'avg_noise']
        writer = csv.writer(f)
        writer.writerow(titles)
        
    
        
    with open(r'data/all_genome_fitnesses.csv', 'w') as f:
            titles = ['fitness']
            writer = csv.writer(f)
            writer.writerow(titles)
    
    valid_circuit_set = []
    
    # initialisation 
    population = init_population()
    
    #process data here - create two arrays- input and expected_out
    
    data = get_data()
    build_cumulative_prob()
    
    best_fitness_sofar = 0
    mean_fitness_sofar = 0
    
    goal_size = population.size - ELITE_COUNT

    for num_gen in range(NUM_GENERATIONS):
        
        # sample data
        if SUBSET_PROPORTION < 1:
            data = sample_data(data)

        #evaluate 
        cf = CircuitFitness(population)
        cf.makeqiskitcircuits()
        cf.makefitness(data)
        population.fitnesses = cf.fitnesses
        population.noisieness = cf.noisieness
        
        with open(r'data/all_genome_fitnesses.csv', 'a') as f:
            writer = csv.writer(f)
            for fitness in population.fitnesses:
                row = [fitness]
                writer.writerow(row)
        
        # measure noise resilience on best in population
        
            
        best_fitness_sofar = max(population.fitnesses)
        mean_fitness_sofar = np.mean(population.fitnesses)
        average_circuit_length = np.mean(population.get_lengths())
        median_circuit_length = np.percentile(population.get_lengths(), 50)
        lower_percentile_length = np.percentile(population.get_lengths(), 10)
        upper_percentile_length = np.percentile(population.get_lengths(), 90)
        best_noise_resilience = max(population.noisieness)
        mean_noise_sofar = np.mean(population.noisieness)
        
        
        valid_circuit_count = 0
        for circuit, fitness in zip(population.members, population.fitnesses):
            if fitness > SUCCESS_VALUE:
                valid_circuit_count += 1
                valid_circuit_set.append(circuit)
        
        next_population = Population([])
        
        while next_population.size < goal_size:
            r = random.random()
            
            if r < CUMULATIVE_PROB['crossover'] and next_population.size + 2 <= goal_size:
                parent_one = selection(population)
                parent_two = selection(population)
                
                children = crossover(parent_one, parent_two)
                next_population.add_member(children[0])
                next_population.add_member(children[1])
                
            elif r < CUMULATIVE_PROB['insertion'] and next_population.size + 2 <= goal_size:
                parent_one = selection(population)
                parent_two = selection(population)
                
                children = insertion(parent_one, parent_two)
                next_population.add_member(children[0])
                next_population.add_member(children[1])
                
            elif r < CUMULATIVE_PROB['mutation']:
                parent = selection(population)
                child = mutation(parent)
                
                next_population.add_member(child)
                
            elif r < CUMULATIVE_PROB['wire_mutation']:
                parent = selection(population)
                child = wire_mutation(parent)
                
                next_population.add_member(child)
                
            elif r < CUMULATIVE_PROB['insert_mutation']:
                parent = selection(population)
                child = insert_mutation(parent)
                
                next_population.add_member(child)
                
            else: # shrink mutation
                parent = selection(population)
                child = shrink_mutation(parent)
                
                next_population.add_member(child)
                
        # get elite
        elite_circuits = population.get_best(ELITE_COUNT)

        for ec in elite_circuits:
            next_population.add_member(ec)
            
        population.overwrite_from(next_population)
            
        # output info to terminal
        print(f"Population size: {population.size}")
        
        print(f"Generation {num_gen+1}/{NUM_GENERATIONS}\nBest so far: {best_fitness_sofar}\nAverage so far: {mean_fitness_sofar}\n")
        
        # write data to csv file 
        with open(r'data/fitness_output.csv', 'a') as f:
            row = [num_gen+1, mean_fitness_sofar, best_fitness_sofar, valid_circuit_count, average_circuit_length, median_circuit_length, lower_percentile_length, upper_percentile_length, best_noise_resilience, mean_noise_sofar]
            writer = csv.writer(f)
            writer.writerow(row)
    
    
    
    # final circuit population checks    
    cf = CircuitFitness(population)
    cf.makeqiskitcircuits()
    
    # make fitness should take in the processed data - dont need to loop over
    # then the 
    
    cf.makefitness(data)
    population.fitnesses = cf.fitnesses
    
    
    for circuit, fitness in zip(population.members, population.fitnesses):
        if fitness > SUCCESS_VALUE:
            valid_circuit_set.append(circuit)
            
    # check and add valid circuits to data
    with open('data/found_circuits.txt', 'w') as f:
        for c in valid_circuit_set:
            f.write(f"{str(c)}\n") 
    
    print("\n------------------------------------------------------------\n")
    print("BEST FITNESSES: ", max(population.fitnesses))
    print("\n------------------------------------------------------------\n")
    
    print("\n------------------------------------------------------------\n")
    print("AVERAGE FITNESSES: ", np.mean(population.fitnesses))
    print("\n------------------------------------------------------------\n")
        
    return population


def noise_reslience(circuit: Circuit):
    
    qc = circuit.qiskit_representation
    input_state = Statevector.from_label('000')
    
    # compute standard output
    output_state = input_state.evolve(qc)
    
    noise_model = NoiseModel()
    error_oneq = depolarizing_error(0.001, 1)
    error_twoq = depolarizing_error(0.01, 2)
    
    noise_model.add_all_qubit_quantum_error(error_oneq, ['h','x'])
    noise_model.add_all_qubit_quantum_error(error_twoq, ['cp', 'swap'])
    
    noise_simulator = AerSimulator(method="density_matrix", noise_model=noise_model)
    
    
    
    qc_dm = QuantumCircuit(qc.num_qubits)
    qc_dm.initialize(input_state.data, range(qc.num_qubits))

    qc_dm.compose(qc, inplace=True)

    qc_dm.save_density_matrix()

    tqc = transpile(qc_dm, noise_simulator)
    result = noise_simulator.run(tqc).result()

    noisy_output_state = DensityMatrix(result.data(0)['density_matrix'])
    
    fidelity = state_fidelity(output_state, noisy_output_state)

    return fidelity