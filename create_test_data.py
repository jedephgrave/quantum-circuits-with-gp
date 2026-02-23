import random
import csv
import numpy as np
from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector

#important = ['000', '001', '010', '011', '100', '101', '110', '111', '+++', '+00', '0+0', '00+']


# ----------------------------------
# 1. Build an n-qubit QFT circuit
# ----------------------------------
"""
def build_qft(n_qubits, do_swaps=True):
    qc = QuantumCircuit(n_qubits)

    for j in range(n_qubits):
        qc.h(j)
        for k in range(j + 1, n_qubits):
            qc.cp(np.pi / (2 ** (k - j)), k, j)

    if do_swaps:
        for i in range(n_qubits // 2):
            qc.swap(i, n_qubits - i - 1)

    return qc
""" 

def build_qft_2():
    qc = QuantumCircuit(2)
    
    qc.h(0)
    qc.cs(1,0)
    qc.h(1)
    qc.swap(0,1)
    
    print(qc)
    
    return qc

def build_qft_3():
    qc = QuantumCircuit(3)
    
    qc.h(0)
    qc.cp(np.pi/2,1,0)
    qc.cp(np.pi/4,2,0)
    qc.h(1)
    qc.cp(np.pi/2,2,1)
    qc.h(2)
    qc.swap(0,2)

    print(qc)
    return qc

def build_qft_4():
    qc = QuantumCircuit(4)
    
    qc.h(0)
    qc.cp(np.pi/2,1,0)
    qc.cp(np.pi/4, 2, 0)
    qc.cp(np.pi/8, 3, 0)
    
    qc.h(1)
    qc.cp(np.pi/2, 2, 1)
    qc.cp(np.pi/4, 3, 1)
    
    qc.h(2)
    qc.cp(np.pi/2, 3, 2)
    
    qc.h(3)
    
    qc.swap(0, 3)
    qc.swap(1, 2)
    
    print(qc)
    
    return qc
# ----------------------------------
# 2. Generate random unique inputs
# ----------------------------------
def generate_random_inputs(n_qubits, n_inputs):
    """
    Generate unique labels like:
    01+, +0-, 110, etc.
    """
    symbols = ['0', '1', '+', '-']

    all_possible = [
        ''.join(state)
        for state in np.ndindex(*(4,) * n_qubits)
        for state in [[symbols[i] for i in state]]
    ]

    if n_inputs > len(all_possible):
        raise ValueError(
            f"Requested {n_inputs} inputs, but only "
            f"{len(all_possible)} unique states exist."
        )

    return random.sample(all_possible, n_inputs)


# ----------------------------------
# 3. Generate dataset
# ----------------------------------
def generate_qft_dataset(
    n_qubits,
    n_inputs,
    output_csv="qft_dataset.csv"
):
    
    type_dict = {
        2: build_qft_2,
        3: build_qft_3,
        4: build_qft_4,
    }
    
    qc = type_dict[n_qubits]()

    inputs = generate_random_inputs(n_qubits, n_inputs)
    
    #inputs += important

    rows = []
    for label in inputs:
        input_state = Statevector.from_label(label)
        output_state = input_state.evolve(qc)

        rows.append([
            label,
            str(output_state.data.tolist())
        ])

    with open(output_csv, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["qubit_input", "expected_output"])
        writer.writerows(rows)

    print(
        f"Saved {n_inputs} samples for "
        f"{n_qubits}-qubit QFT to {output_csv}"
    )


# ----------------------------------
# 4. Run
# ----------------------------------
if __name__ == "__main__":
    generate_qft_dataset(
        n_qubits=2,      # ← change this freely
        n_inputs=8,     # ← change this freely
        output_csv="data/test_data.csv"
    )
