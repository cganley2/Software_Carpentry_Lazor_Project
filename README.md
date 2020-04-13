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

As of submission, the solver does NOT work for boards mad_4, mad_7, and yarn_5.