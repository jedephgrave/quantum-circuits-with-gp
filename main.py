from gp import gp
from config import check_prob

def main():
    if check_prob: 
        p = gp.evolution()
        
        best_fitness = 0
        best_circuit = None
        for i in range(0, p.size):
            if p.fitnesses[i] > best_fitness:
                best_fitness = p.fitnesses[i]
                best_circuit = p.member(i)
                
        print(best_circuit)
        print("\n")
        print(best_fitness)
    else:
        print("Check operation probabilities sum to 1")
    

if __name__ == "__main__":
    main()