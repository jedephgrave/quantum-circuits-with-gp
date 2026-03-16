from .gate import Gate
import copy
from qiskit import QuantumCircuit

class Circuit:
    
    def __init__(self, circuit: list[Gate], num_wires: int):
        self.circuit = circuit
        self.length = len(circuit)
        self.num_wires = num_wires
        
        self.qiskit_representation = None
        
        self.fitness = 0
        self.noise = 0
        
    def add_gate(self, gate: Gate):
        self.circuit.append(gate)
        self.length += 1
        
    def split(self, cutoff: int) -> tuple["Circuit"]:
        if not(0 <= cutoff < self.length-1 ):
            raise ValueError(f"Cutoff between 0 and {self.length - 1} expected, value of {cutoff} given.")
        
        # split circuit into two seperate circuit objects 
        left = self.circuit[:cutoff+1:]
        right = self.circuit[cutoff+1::]
        
        return Circuit(left, self.num_wires), Circuit(right, self.num_wires)
        
    def combine(self, circuit: "Circuit"):
        left = self.circuit
        right = circuit.circuit
        
        combination = left + right
        
        return Circuit(combination, self.num_wires)
    
    def split_three(self, cutoff_one: int, cutoff_two: int) -> tuple["Circuit"]:
        
        if not(0 <= cutoff_one < self.length - 1):
            raise ValueError(f"First cutoff between 0 and {self.length - 1} expected, value of {cutoff_one} given.")
        
        if not(cutoff_one <= cutoff_two < self.length - 1):
            raise ValueError(f"Second cutoff between {cutoff_one} and {self.length - 1} expected, value of {cutoff_two} given")

        left = self.circuit[:cutoff_one:]
        middle = self.circuit[cutoff_one:cutoff_two+1:]
        right = self.circuit[cutoff_two+1::]
        
        return Circuit(left, self.num_wires), Circuit(middle, self.num_wires), Circuit(right, self.num_wires)
    
    def insert_between(self, left_circuit: "Circuit", right_circuit: "Circuit") -> "Circuit":
        left = left_circuit.circuit
        middle = self.circuit
        right = right_circuit.circuit
        
        combination = left + middle + right
        
        return Circuit(combination, self.num_wires)
    
    def swap(self, index: int, new_gate: Gate):
        # takes gate at defined index and swaps for given gate
        
        if not(0 <= index < self.length):
            raise ValueError(f"Index between 0 and {self.length} expected, value of {index} given")
        
        left = self.circuit[0:index]
        right = self.circuit[index+1::]
        
        left.append(new_gate)
        
        self.circuit = left + right
        
    def remove_gates(self, index: int, num_removals: int = 1):
        
        end = (index+num_removals) - 1
        
        if not(0 <= end< self.length):
            raise ValueError(f"Range between 0 and {self.length} expected, removing from {index} to {end} is outside the range")
        
        
        for _ in range(index, index + num_removals):
            self.circuit.pop(index)
            self.length -= 1
            
    @property
    def qiskit_representation(self) -> QuantumCircuit:
        return self._qiskit_representation
    
    @qiskit_representation.setter
    def qiskit_representation(self, qiskit_representation: QuantumCircuit):
        self._qiskit_representation = qiskit_representation
            
    def copy(self) -> "Circuit":
        return copy.deepcopy(self)
            

    def __str__(self) -> str:
        circuit_array = []
        for gate in self.circuit:
            circuit_array.append(str(gate))
        
        return f"{circuit_array}"


    
        
    