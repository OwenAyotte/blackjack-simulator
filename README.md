# Blackjack Algorithm Evaluation Program

A program for running and evaluating various Blackjack algorithms.

## Description

This program uses a set of sub-algorithms for various stages of the game (playing hand, counting cards and choosing betting amount) to constuct the algorithm to be evaluated. Once the algorithm is constructed, it is used to playthrough numerous games of blackjack. Then, the scores for each round are saved to a file, to be read by second file where various information about it is displayed and graphed.

Features: 

    - Customizable simulation parameters such as starting balance and base betting amount
    - Ability to attach notes to simulation runs
    - Toggleable graphing plots (scatter plot, average value and linear fit)
    - Ability to view data such as bust percentage, standard deviation, and net profit at any round cutoff


### How to Use

0. Adjust constants at the top of betting_simulation.py (Optional)

1. Run betting_simulation.py

2. Select sub-algorithms

3. Run simulation

4. Write notes on simulation and choose file name

5. Save file 

6. Run data_analysis.py

7. Type in file name

8. View data and graphs


### Prerequisites

- Python 3.x  
- matplotlib
- numpy

### Install

```bash
# Clone the repository
git clone https://github.com/yourusername/blackjack-simulator.git
cd blackjack-simulator

# Install dependencies
pip install -r requirements.txt

```

### Contributing

Contributions are unlikely to be accepted, unless a critical flaw is brought to my attention. This is a personal project, so I aim to make sure I am responsible for as much of the code as possible.

## License

This project is licensed under the MIT License - see the LICENSE.md file for details