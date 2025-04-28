# League Model UI Project Using PyQT6
Final Project for CPSC 4970 - Python Programming

## Overview
This project is the culmination of the league model program that has been built throughout the semester.
A UI has been created for the league model that allows users to create and edit leagues. Within each league
users can edit teams, and team members, all contained within the league. Teams can be imported into a 
league or exported to a csv file. Finally, the league's main window allows users to load previously edited leagues
and save the current league being edited to a database file.

The UI was created using PyQT6. Please see the requirements.txt file contained in the module06 package for 
all third party libraries needed to execute this program.


## Project Structure
The entire program is stored in the module06 package. Within the module06 package, project files
are contained in either the league_model package or ui package. In addition, the requirements.txt
file containing the 3rd party libraries needed to run the project is also contained within the 
module06 package.

* **module06/league_model** This package contains all the source code needed for the league model built in previous modules
  * **module06/league_model/data** This package contains saved database and csv files
* **module06/ui** The package contains all the source code for the UI component of the program

## How to Execute the UI
1. Load all necessary third party libraries as noted in the requirements.txt file
2. Open the main_window.py file contained in the module06/ui package in PyCharm
3. Click the run button ensuring the main_window.py file is the one being run

