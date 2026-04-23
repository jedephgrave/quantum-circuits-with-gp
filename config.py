from circuit import Gate 

GATE_SET = [
    Gate('H', 1, 0),   
    Gate('CS', 2, 0),
    Gate('CP4', 2, 0),
    Gate('X', 1, 0),
    Gate('SWAP', 2, 0),
    Gate('CP8', 2, 0),
]

# dont use this - just to list extra gates not currently being used
SPARE_GATE_SET = [
    Gate('CN', 2, 0),
    Gate('S', 1, 0),
    Gate('CP8', 2, 0),
    Gate('CZ', 2, 0),
    Gate('Y', 1, 0),
    Gate('Z', 1, 0)
]

NUM_WIRES = 3

# gp hyperparameters go here 500+ population, 50 gens?
POPULATION_SIZE = 1000
NUM_GENERATIONS = 50
# 1000, 60

TOURNAMENT_SIZE = 6

ELITE_COUNT = int(POPULATION_SIZE/100)


# INCREASE THE RANGE OF THIS? 6-10 for 3qb 6-12? for 4qb
INITIAL_SIZE = {'max': 9,
                'min': 5
                }

# maybe add a max insertion size for the chunks?

MUTANT_INSERT_SIZE = {'max': 3,
                      'min': 2
                      }
MUTANT_SHRINK_SIZE = {'max': 2,
                      'min': 1
                      }

PROB_DICT = {'crossover' : 0.0,
             'insertion': 0.5,
             'mutation': 0,
             'wire_mutation': 0.45,
             'insert_mutation': 0.0,
             'shrink_mutation': 0.05
             }

CUMULATIVE_PROB = dict()

def build_cumulative_prob():
    s = 0
    for key in PROB_DICT:
        s += PROB_DICT[key]
        CUMULATIVE_PROB[key] = s

# ensure to run this before gp begins run
check_prob = (sum(PROB_DICT.values()) == 1)
    

# data creation

NUMBER_INPUTS = 30 # 40 - 4qb, 30 - 3qb

# evaluation variables

SUBSET_PROPORTION = 1
SUBSET_SIZE = int(SUBSET_PROPORTION * NUMBER_INPUTS)

# bloat control values

PARSIMONY_CONSTANT = 0 # change to 0.003 for 3qb 0.0008 4qb

NOISE_RESILIENCE = False

SUCCESS_VALUE = round((NUMBER_INPUTS - 1) / NUMBER_INPUTS, 5)

