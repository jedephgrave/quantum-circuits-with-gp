from gp import Population
from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator
from qiskit_aer.noise import NoiseModel, depolarizing_error
from qiskit.primitives import StatevectorSampler
from qiskit.quantum_info import Statevector, DensityMatrix, state_fidelity
from .convert import QiskitBuilder
import numpy as np
from circuit import Circuit
from config import PARSIMONY_CONSTANT, NOISE_RESILIENCE
import random
from gp.data_process import get_data
from config import SUCCESS_VALUE

class CircuitFitness:
    def __init__(self, population: Population):
        self.population = population
        
        #self.qiskitcircuits = []
        #self.circuitlengths = []
        self.circuits = []
        self.fitnesses = []
        self.noisieness = []
        self.inputqubits = ['00']
        
    def makeqiskitcircuits(self):
        for circuit in self.population.members:
            qc = QiskitBuilder(circuit)

            # OLD - for handling within the class - too clunky
            #self.qiskitcircuits.append(qc.build())
            #self.circuitlengths.append(circuit.length)
            
            circuit.qiskit_representation = qc.build()
            self.circuits.append(circuit)
            
    def evaluatecircuit(self, circuit: Circuit, data: list[list[str], np.array]) -> float:

        total = 0
        count = 0
        noise_resilience = 1
        
        qc = circuit.qiskit_representation
        
        data = zip(data[0], data[1])
        
        for in_qubits, expected in data:

            output_state = compute_output(qc, in_qubits)

            total+= fidelity_evaluation(expected, output_state)
            count += 1
            
            if count == 1 and NOISE_RESILIENCE: # only run on first check and if meant to
                noisy_output_state = compute_noisy_output(qc, in_qubits)
                noise_resilience = noise_evaluation(output_state, noisy_output_state)
            
        fitness = total/count
        
        
        fitness = parsimony_pressure(fitness, circuit)
        
        return fitness, noise_resilience
      
    def makefitness(self, data: list[list[str], np.array]):
        # self.inputqubits = inputqubits
        for circuit in self.circuits:
            fitness, noise = self.evaluatecircuit(circuit, data)
            
            # if suspected perfect circuit - check again on all data 
            if fitness > SUCCESS_VALUE: 
                complete_data = get_data()
                fitness, noise = self.evaluatecircuit(circuit, complete_data)
                
            self.fitnesses.append(fitness)
            self.noisieness.append(noise)
            
            
        # automatically add fitness to the population after this?
        
def compute_output(qc, in_qubits):
    input_state = Statevector.from_label(in_qubits)
    output_state = input_state.evolve(qc)
    
    return output_state
     
def compute_noisy_output(qc, in_qubits):
    
    noise_model = NoiseModel()
    error_oneq = depolarizing_error(0.001, 1)
    error_twoq = depolarizing_error(0.01, 2)
    
    noise_model.add_all_qubit_quantum_error(error_oneq, ['h','x','y','z','s'])
    noise_model.add_all_qubit_quantum_error(error_twoq, ['cp','swap', 'cx','cz','cs'])
    
    noise_simulator = AerSimulator(method="density_matrix", noise_model=noise_model)
    
    input_state = Statevector.from_label(in_qubits)
    
    qc_dm = QuantumCircuit(qc.num_qubits)
    qc_dm.initialize(input_state.data, range(qc.num_qubits))

    qc_dm.compose(qc, inplace=True)

    qc_dm.save_density_matrix()

    tqc = transpile(qc_dm, noise_simulator)
    result = noise_simulator.run(tqc).result()

    noisy_output_state = DensityMatrix(result.data(0)['density_matrix'])

    return noisy_output_state

        
def fidelity_evaluation(expected, output_state):

    fidelity = abs(np.vdot(expected, output_state.data)) ** 2

    #total += (1-fidelity) # for minimising fitness
    
    return fidelity # sqrt just to change briefly

def noise_evaluation(output_state, noisy_output_state):
    
    fidelity = state_fidelity(output_state, noisy_output_state)
    return fidelity

    

def parsimony_pressure(fitness: float, circuit: Circuit):
    
    adjustment = PARSIMONY_CONSTANT * circuit.length
    
    if adjustment > fitness:
        print("Can't adjust fitness")
    
    # adjust fitness and avoid negatives
    adjusted_fitness = fitness-adjustment if fitness > adjustment else fitness 
    
    return adjusted_fitness
    
"""
def test_evaluation(expected, output_state):
    candidate = output_state.data
    target = expected

    # amlpitude fitness
    amp_error = np.linalg.norm(np.abs(target) - np.abs(candidate))
    F_amp = 1 / (1 + amp_error)

    # relative phase fitness
    ref = np.argmax(np.abs(target))

    phase_diff = np.angle(candidate * np.conj(target))

    # normalise relative to reference phase
    rel_phase_error = np.linalg.norm(phase_diff - phase_diff[ref])
    F_phase = 1 / (1 + rel_phase_error)

    # fidelity
    fidelity = abs(np.vdot(target, candidate)) ** 2
    F_fid = fidelity

    w_amp = 0.4
    w_phase = 0.3
    w_fid = 0.3

    return (w_amp * F_amp + w_phase * F_phase + w_fid * F_fid)
"""