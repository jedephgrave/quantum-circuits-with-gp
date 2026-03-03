from circuit import Gate 

GATE_SET = [
    Gate('H', 1, 0),   
    Gate('CS', 2, 0),
    Gate('CP4', 2, 0),
    Gate('CP8', 2, 0),
    Gate('X', 1, 0),
    Gate('SWAP', 2, 0),
]

# dont use this - just to list extra gates not currently being used
SPARE_GATE_SET = [
    Gate('X', 1, 0),
    Gate('CN', 2, 0),
    Gate('S', 1, 0),
    Gate('SWAP', 2, 0),
]

NUM_WIRES = 4

# gp hyperparameters go here 
POPULATION_SIZE = 400

ELITE_COUNT = 4

INITIAL_SIZE = {'max': 9,
                'min': 8
                }

# maybe add a max insertion size for the chunks?

MUTANT_INSERT_SIZE = {'max': 3,
                      'min': 2
                      }
MUTANT_SHRINK_SIZE = {'max': 2,
                      'min': 1
                      }

PROB_DICT = {'crossover' : 0.50,
             'insertion': 0.0,
             'mutation': 0.1,
             'wire_mutation': 0.4,
             'insert_mutation': 0.0,
             'shrink_mutation': 0.0
             }

CUMULATIVE_PROB = dict()

def build_cumulative_prob():
    s = 0
    for key in PROB_DICT:
        s += PROB_DICT[key]
        CUMULATIVE_PROB[key] = s

# ensure to run this before gp begins run
check_prob = (sum(PROB_DICT.values()) == 1)
    
    
# gp variables

NUM_GENERATIONS = 200

TOURNAMENT_SIZE = 6

# bloat control values

PARSIMONY_CONSTANT = 0.001 # change to 2/3

