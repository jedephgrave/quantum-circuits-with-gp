from qiskit import QuantumCircuit
from circuit import Circuit, Gate
import numpy as np


class QiskitBuilder:
    def __init__(self, circuit: Circuit):
        self.circuit = circuit
        self.qc = QuantumCircuit(self.circuit.num_wires) # create qiskit object with matching qubit num
        
        self.gates = {
            "H": self.hadamard,
            "CN": self.cnot,
            "X": self.paulix,
            "SWAP": self.swapgate,
            "S": self.sgate,
            "CS": self.cs,
            "CP4": self.cp4,
            "CP8": self.cp8,
        }
        
    # class methods:
        # builder methods
        # methods for each 
        
    # add error for unknown gate?
        
    def build(self) -> QuantumCircuit:
        for gate in self.circuit.circuit:
            self.gates[gate.name](gate.wires)
        
        return self.qc
        
    def hadamard(self, wires: list[int]):
        self.qc.h(wires[0])
    
    def cnot(self, wires: list[int]):
        self.qc.cx(wires[0], wires[1])

    def paulix(self, wires: list[int]):
        self.qc.x(wires[0])
        
    def swapgate(self, wires: list[int]):
        self.qc.swap(wires[0], wires[1])
        
    def sgate(self, wires: list[int]):
        self.qc.s(wires[0])
        
    def cs(self, wires: list[int]):
        self.qc.cs(wires[0], wires[1])
        
    def cp4(self, wires: list[int]):
        self.qc.cp(np.pi/4, wires[0], wires[1])
        
    def cp8(self, wires: list[int]):
        self.qc.cp(np.pi/8, wires[0], wires[1])

# call fitness on whole population - 
# take in a given circuit
# convert the circuit 
# return the qiskit circuit
# evaluate the qiskit circuit and return this evaluation