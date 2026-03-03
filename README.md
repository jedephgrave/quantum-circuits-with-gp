### Automatic design of quantum circuits with genetic programming

Able to evolve an appropriately sized 3 qubit quantum fourier transform circuit 
(7 Gates)

**Current setup includes functionality for:**
- Tournament selection (with elitism)
- Crossover, Insertion
- Mutation, Wire mutation
- Insertion and Shrink mutation
- Parismony pressure 

**Specifics of the genetic program can be tweaked in config.py, such as:**
- Gate set
- Initial solution size, population size and elite count
- Probability of given operations occuring, with size details for insertion and shrinking
- Selection parameters and parimony constant for bloat

**Information for data collection**
- Build dataset for goal circuit - *create_test_data.py*
- Create simple plots (showing solution fitness and solution size through the run) - *create_plots.py*

**To be added:**
- Multi objective functionality to be developed (for noise resiliency)



