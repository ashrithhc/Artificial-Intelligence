## Project 02: Multi-Agent Pac-Man (100 points, Due Wed Oct 04 before midnight)

<img src="/images/MultiAgentPacMan.png" width="50%"/>

### Introduction

Pacman, now with ghosts. Minimax, Expectimax.

In this project, you will design agents for the classic version of Pacman, including ghosts. Along the way, you will implement both minimax and expectimax search.

The code base has not changed much from the previous project, but please start with a fresh installation, rather than intermingling files from project 1.

As in project 1, this project includes an autograder for you to grade your answers on your machine. This can be run on all questions with the command:

    python autograder.py
    
It can be run for one particular question, such as q2, by:

    python autograder.py -q q2

It can be run for one particular test by commands of the form:

    python autograder.py -t test_cases/q2/0-small-tree

By default, the autograder displays graphics with the -t option, but doesn't with the -q option. You can force graphics by using the --graphics flag, or force no graphics by using the <code>--no-graphics</code> flag.

### Files you'll edit:

    multiAgents.py - Where all of your multi-agent search agents will reside.
    
    pacman.py - The main file that runs Pacman games. This file also describes a Pacman <code>GameState</code> type, which you will use extensively in this project
    
    game.py - The logic behind how the Pacman world works. This file describes several supporting types like AgentState, Agent, Direction, and Grid.

    util.py - Useful data structures for implementing search algorithms.
    
### Files you can ignore:

    graphicsDisplay.py - Graphics for Pacman
    
    graphicsUtils.py - Support for Pacman graphics
    
    textDisplay.py - ASCII graphics for Pacman

    ghostAgents.py - Agents to control ghosts

    keyboardAgents.py - Keyboard interfaces to control Pacman

    layout.py - Code for reading layout files and storing their contents 

    autograder.py - Project autograder

    testParser.py - Parses autograder test and solution files

    testClasses.py - General autograding test classes

    test_cases/ - Directory containing the test cases for each question 
    
    multiagentTestClasses.py - Project 2 specific autograding test classes
    
#### Reflex Agent

    python pacman.py -p ReflexAgent -l testClassic
    
    python pacman.py --frameTime 0 -p ReflexAgent -k 1
    
    python pacman.py --frameTime 0 -p ReflexAgent -k 2

    python autograder.py -q q1
    
    python autograder.py -q q1 --no-graphics

#### Minimax

    python autograder.py -q q2

    python autograder.py -q q2 --no-graphics

#### Alpha-Beta Pruning

    python pacman.py -p AlphaBetaAgent -a depth=3 -l smallClassic

    python autograder.py -q q3
    
    python autograder.py -q q3 --no-graphics
    
#### Expectimax

    python autograder.py -q q4
    
    python pacman.py -p AlphaBetaAgent -l trappedClassic -a depth=3 -q -n 10
    
    python pacman.py -p ExpectimaxAgent -l trappedClassic -a depth=3 -q -n 10
