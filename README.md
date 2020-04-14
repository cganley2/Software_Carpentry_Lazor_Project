# software_carpentry_lazor_project
# Team: Connor Ganley and Nelson Ndahiro

This is a program that can read and solve a lazor puzzle.

In order to use the program, open run.py and edit board_path (line 7) to the 
board file you would like to solve. The boards are located in the 'boards' 
directory, so the path string should begin with 'boards/'. Then, sit back,
relax, and wait for the solver to do its magic.

The output will be the winning play grid, which shows lines and spaces, and the
winning board configuration, which only shows spaces. The winning board
configuration will be written to a file in the 'solutions/' folder, and it
will be titled the board name appended with '\_solution.bff'.

To see some unit tests demonstrating how lasers interact with each type of
block (A - reflect, B - opaque, C - refract), consider running
unit_test_script.py.

As of submission, the solver does NOT work for boards mad_1.

OPTIONAL/BONUS RESPONSE:
To simulate the laser moving around the grid, all the possible ways
of placing the blocks on the grid are generated into a list of scenarios.
However, using the itertools combination method would generate
an extremely large list (On order of *number_of_free_spaces*!) for
example 24! for mad_7. Python cannot make lists of that many items.
So, instead we generated lists of the positions to be occupied since their
total number doesnt change. This changed the permutation generation from
97E6+ permutations to ~100E3 which is manageable for Python.