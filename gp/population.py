from circuit import Circuit, Gate
from config import POPULATION_SIZE
import random


class Population:

    def __init__(self, members: list[Circuit]):
        self.members = members
        self.size = len(members)
        self.fitnesses = [None] * self.size
        self.noisieness = [] 
        
    def add_member(self, circuit: Circuit):
        if self.size == POPULATION_SIZE:
            return ValueError(f"Population at limit of {POPULATION_SIZE}.")
        
        self.members.append(circuit)
        self.size += 1
        
    @property
    def fitnesses(self) -> list[float]:
        return self._fitnesses
    
    @fitnesses.setter
    def fitnesses(self, fitnesses: list[float]):
        if fitnesses and len(fitnesses) != self.size:
            raise ValueError(f"List of size {self.size} expected, size of {len(fitnesses)} given.")
        
        for i in range(len(self.members)):
            self.members[i].fitness = fitnesses[i]
        
        self._fitnesses = fitnesses
        
    @property
    def noisieness(self) -> list[float]:
        return self._noisieness
    
    @noisieness.setter
    def noisieness(self, noisieness: list[float]):
        if noisieness and len(noisieness) != self.size:
            raise ValueError(f"List of size {self.size} expected, size of {len(noisieness)} given.")
        
        for i in range(len(self.members)):
            self.members[i].noise = noisieness[i]
        
        self._noisieness = noisieness
        
    def member(self, index: int):
        if index >= self.size or index < 0:
            return ValueError(f"Index between 0 and {self.size-1} expected, index of value {index} given.") 
        
        return self.members[index]
    
    # return one random member of the population
    def rand_member(self):
        r = random.randint(0, self.size-1)
        
        return self.members[r]

    # return a given number of random members from the population
    def rand_members(self, number):
        if number > self.size or self.size <= 0:
            return ValueError(f"Number between 1 and {self.size} expected, number less than or greater than population size given.")
        
        return random.sample(self.members, number)
    
    def sample_population(self, sample_size) -> "Population":
        if sample_size > self.size or sample_size <= 0:
            return ValueError(f"Number between 1 and {self.size} expected, number less than or greater than population size given.")
        
        if len(self.fitnesses) == 0:
            return ValueError(f"Population has no fitnesses attributed to it")

        pop_indexes = random.sample(list(range(0, self.size)), sample_size)
        
        sample_pop = Population([])
        sample_fitnesses = []
        
        for index in pop_indexes:
            sample_pop.add_member(self.member(index))
            sample_fitnesses.append(self.fitnesses[index])
            
        sample_pop.fitnesses = sample_fitnesses
        
        return sample_pop
    
    def get_best(self, num_best: int) -> list[Circuit]:
        if num_best > self.size:
            return ValueError(f"Number between 1 and {self.size} expected, number higher than {self.size} given")

        zipped = list(zip(self.members, self.fitnesses))
        sorted_circuits = sorted(zipped, key = lambda x: x[1], reverse=True)
        
        c, f = list(zip(*sorted_circuits))
        
        best_n = c[:num_best]
        
        return best_n
    
    def get_lengths(self) -> list[int]:
        circuit_lengths = []
        for member in self.members:
            circuit_lengths.append(member.length)
        
        return circuit_lengths
    
    def overwrite_from(self, new_population):
        self.__dict__.clear()
        self.__dict__.update(new_population.__dict__)
        return 
        
    # return formatted string of circuit strings and their respective fitnesses    
    def __str__(self) -> str:
        population_array = []
        
        if len(self.fitnesses) == 0:
            for circuit in self.members:
                population_array.append(str(circuit))
        else:
            for index in range(self.size):
                population_array.append(f"{str(self.member(index))} : {self.fitnesses[index]}")
        
        return f"{population_array}"