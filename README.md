# Simulated Annealing Algorithm for Ranking Optimization

This code implements the Simulated Annealing algorithm for ranking optimization. It takes a file as input and uses the provided data to determine the optimal rankings for a given set of racers.

## How to Use

To run the code, execute the following command in the command line:

python3 SimulatedAnnealing.py {insert file here}.wmg

The wmg file must be in the same format as the `1994_Formula_One.wmg` file provided in this repository

## Input File Format

The input file is expected to follow a specific format:

- The first line of the file should contain the number of racers.
- The following lines should list the racers' names and rankings.
- The remaining lines should specify the wins and losses between racers.

Please ensure that your input file adheres to this format for the code to work correctly.

## Code Overview

The code consists of the following main components:

1. **Neighbour Generation**: The `find_next_neighbour` function randomly selects two drivers and swaps their rankings to generate a neighbouring solution.

2. **Weight Calculation**: The `calculate_kemeny_ranking` function calculates the increase or decrease in weight (Kemeny score) resulting from a ranking change.

3. **Simulated Annealing**: The `sim_annealing` function implements the Simulated Annealing algorithm. It generates a neighbouring solution and decides whether to accept it based on the current temperature and the difference in Kemeny score.

4. **Main Algorithm**: The main algorithm reads the input file, initializes the rankings, and runs the Simulated Annealing algorithm until the stopping criterion is met.

5. **Data Structures**: The code uses dictionaries to store the racers, winners, and losers information.

## Output

The code outputs the optimal rankings for the racers, their corresponding Kemeny score, and the runtime of the algorithm in milliseconds.
