## Project 01: The Searchin' Pac-Man (100 points, Due Wed Sep 20 before midnight)
<img src="../images/SearchingPacMan.png" width="50%"/>


### Introduction
In this project, your Pac-Man agent will find paths through its maze world, both to reach a particular location and to collect food efficiently. You will build general search algorithms and apply them to Pac-Man scenarios.
This is a somewhat long project with several components. You are advised to start early!
The code for this project consists of several Python files, some of which you will need to read and understand in order to complete the assignment, and some of which you can ignore. You can download all the code and supporting files (including this description) as a zip archive.

#### Files you'll edit:
    search.py - Where all of your search algorithms will reside.

    searchAgents.py - Where all of your search-based agents will reside.
    
#### Files you might want to look at:
    pacman.py - The main file that runs Pac-Man games. This file describes a Pac-Man GameState type, which you use in this project.
    
    game.py - The logic behind how the Pac-Man world works. This file describes several supporting types like AgentState, Agent, Direction, and Grid.
    
    util.py - Useful data structures for implementing search algorithms.
    
#### Supporting files you can ignore:
    graphicsDisplay.py - Graphics for Pac-Man
    
    graphicsUtils.py - Support for Pac-Man graphics
    
    textDisplay.py - ASCII graphics for Pac-Man
    
    ghostAgents.py - Agents to control ghosts
    
    keyboardAgents.py - Keyboard interfaces to control Pac-Man
    
    layout.py - Code for reading layout files and storing their contents
    
    
### Welcome to Pac-Man
After downloading the code, unzipping it and changing to the search directory, you should be able to play a game of Pac-Man by typing the following at the command line:

    python pacman.py

Note: Make sure you are running a recent version of Python (2.5 or later). If you get error messages regarding python-tk, use your package manager to install python-tk, or see this page for more detailed instructions.
Pac-Man lives in a shiny blue world of twisting corridors and tasty round treats. Navigating this world efficiently will be Pac-Man's first step in mastering its domain.
The simplest agent in <code>searchAgents.py</code> is called the <code>GoWestAgent</code>, which always goes West (a trivial reflex agent). This agent can occasionally win:

    python pacman.py --layout testMaze --pacman GoWestAgent
    
But, things get ugly for this agent when turning is required:

    python pacman.py --layout tinyMaze --pacman GoWestAgent
    
If pacman gets stuck, you can exit the game by typing CTRL-c into your terminal. Soon, your agent will solve not only tinyMaze, but any maze you want. Note that <code>pacman.py</code> supports a number of options that can each be expressed in a long way (e.g., --layout) or a short way (e.g., -l). You can see the list of all options and their default values via:

    python pacman.py -h
    
Also, all of the commands that appear in this project also appear in <code>commands.txt</code>, for easy copying and pasting. In UNIX/Mac OS X, you can even run all these commands in order with bash <code>commands.txt</code>.

#### Depth first search (DFS)

    python pacman.py -l tinyMaze -p SearchAgent
    
    python pacman.py -l mediumMaze -p SearchAgent
    
    python pacman.py -l bigMaze -z .5 -p SearchAgent
    
#### Breadth first search (BFS)

    python pacman.py -l mediumMaze -p SearchAgent -a fn=bfs 
    
    python pacman.py -l bigMaze -p SearchAgent -a fn=bfs -z .5
    
#### Eight Puzzle Problem
    
    python eightpuzzle.py
    
#### Uniform cost search (UCS)

    python pacman.py -l mediumMaze -p SearchAgent -a fn=ucs
    
    python pacman.py -l mediumDottedMaze -p StayEastSearchAgent

    python pacman.py -l mediumScaryMaze -p StayWestSearchAgent

#### A* search

    python pacman.py -l bigMaze -z .5 -p SearchAgent -a fn=astar,heuristic=manhattanHeuristic

#### Corners problem

    python pacman.py -l tinyCorners -p SearchAgent -a fn=bfs,prob=CornersProblem

    python pacman.py -l mediumCorners -p SearchAgent -a fn=bfs,prob=CornersProblem

#### Corners problem Heuristic

    python pacman.py -l testSearch -p AStarFoodSearchAgent Note: AStarFoodSearchAgent is a shortcut for -p SearchAgent -a fn=astar,prob=FoodSearchProblem,heuristic=foodHeuristic

#### Food Heuristic

    python pacman.py -l trickySearch -p AStarFoodSearchAgent
