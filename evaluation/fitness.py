from gp import Population
from qiskit import QuantumCircuit
from qiskit.primitives import StatevectorSampler
from qiskit.quantum_info import Statevector
from .convert import QiskitBuilder
import numpy as np
from circuit import Circuit
from config import PARSIMONY_CONSTANT

class CircuitFitness:
    def __init__(self, population: Population):
        self.population = population
        
        #self.qiskitcircuits = []
        #self.circuitlengths = []
        self.circuits = []
        self.fitnesses = []
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
        
        qc = circuit.qiskit_representation
        
        
        data = zip(data[0], data[1])
        
        for in_qubits, expected in data:

            input_state = Statevector.from_label(in_qubits)
            output_state = input_state.evolve(qc)

            total+= fidelity_evaluation(expected, output_state)
            count += 1
            
        fitness = total/count
        
        adjusted_fitness = parsimony_pressure(fitness, circuit)
        
        return adjusted_fitness
      
    def makefitness(self, data: list[list[str], np.array]):
        # self.inputqubits = inputqubits
        for circuit in self.circuits:
            self.fitnesses.append(self.evaluatecircuit(circuit, data))
            
            
        # automatically add fitness to the population after this?
        
def fidelity_evaluation(expected, output_state):

    fidelity = abs(np.vdot(expected, output_state.data)) ** 2

    #total += (1-fidelity) # for minimising fitness
    
    return fidelity # sqrt just to change briefly

def parsimony_pressure(fitness: float, circuit: Circuit):
    constant = PARSIMONY_CONSTANT
    circuit_length = circuit.length
    
    return fitness - (constant * circuit_length)
    
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