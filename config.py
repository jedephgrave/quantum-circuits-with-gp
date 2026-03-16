from circuit import Gate 

GATE_SET = [
    Gate('H', 1, 0),   
    Gate('CS', 2, 0),
    Gate('CP4', 2, 0),
    Gate('X', 1, 0),
    Gate('SWAP', 2, 0),
]

# dont use this - just to list extra gates not currently being used
SPARE_GATE_SET = [
    Gate('X', 1, 0),
    Gate('CN', 2, 0),
    Gate('S', 1, 0),
    Gate('SWAP', 2, 0),
    Gate('CP8', 2, 0),
]

NUM_WIRES = 3

# gp hyperparameters go here 
POPULATION_SIZE = 300
NUM_GENERATIONS = 150

TOURNAMENT_SIZE = int(0.02 * POPULATION_SIZE)

ELITE_COUNT = 4


# INCREASE THE RANGE OF THIS?
INITIAL_SIZE = {'max': 10,
                'min': 6
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
             'mutation': 0.05,
             'wire_mutation': 0.4,
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

NUMBER_INPUTS = 30

# evaluation variables

SUBSET_PROPORTION = 0.4
SUBSET_SIZE = int(SUBSET_PROPORTION * NUMBER_INPUTS)

# bloat control values

PARSIMONY_CONSTANT = 0.003 # change to 0.003

NOISE_RESILIENCE = False

SUCCESS_VALUE = round((NUMBER_INPUTS - 1) / NUMBER_INPUTS, 5)

