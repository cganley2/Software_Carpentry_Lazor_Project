import math
import numpy as np

def read_bff_file(file_name):
    '''Decrypts and prints the messages stored in the messenger file msg_fptr
    if the usr inputs the right username and password combination
    as well a valid N and D.

    '''
    file_name += ".bff"  # #Adds extension to open file with .bff extension.
    print('Hello, welcome to the gameboard reader.')
    my_file = open(file_name, "r")
    board_info = [i.split("\n") for i in my_file]  # #a list of lists of encrypted message
    #print(board_info)
    for each_line in board_info:
    	if len(each_line) >1: 
        	del each_line[-1] #Remove the \n Except for last line which has no \n
    #print(board_info)
    board_info = [i for i in board_info if i != [""] ] # remove empty spaces
    print(board_info)

    board_info = [j for i in board_info for j in i]  # turn from list of lists to list of strings
    board_info = [i for i in board_info if i[0] != "#"]  # remove comments
    my_file.close()
    print(board_info)
    return board_info #returns list of all relevant lines

def interpretor(board_information):#, block=False, laser=False, point=False, board=False):
	board_layout = []
	blocks = []
	lasers = []
	points = []
	tries = 0

	for each_line in board_information: #find GRID START
		#print(each_line.lower())
		if each_line.lower() == "grid start":
			
			while tries <1:
				for i in board_information:
					if i.lower() == "grid stop":
						print("ok!")
						tries += 1
						break

					else:
						#print(i)
						board_layout.append(i)
		elif each_line[0].lower() in ["a","b","c"]:
			if each_line in board_layout:
				pass #Make sure board with 
				# letters does not go in this list e.g: B o o
			else:
				blocks.append(each_line)
		elif each_line[0].lower() == "l":
			lasers.append(each_line)
		elif each_line[0].lower() == "p":
			points.append(each_line)

	board_layout = board_layout[1:] #Remove Grid start that was appended

	print("blocks: " + f"{blocks}")
	print("lasers: " + f"{lasers}")
	print("points: " + f"{points}")
	print("board layout: "+ f"{board_layout}")

	#if board==True:
	return board_layout

	print(board_layout)

if __name__ == "__main__":
	interpretor(read_bff_file("mad_1"))

# ok