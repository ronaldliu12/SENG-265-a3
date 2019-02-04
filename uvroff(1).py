 #!/usr/bin/env python3
 # Ronald Liu	V00838627 

import sys
import string
import fileinput
import numbers


current_width = 0		# global variable for checking current location width 
width = 0
left = 0
linespacing = 0
formatting = 0

				
def printing(word):

	global current_width
	
	if ( left > 0 and current_width == 0 and formatting == 1 ):			# adding the left spacing
		k = 0
		for k in range(left):
			print(" ", end='')
			current_width = current_width + 1
	
	if ( (current_width + len(word) ) > width and formatting == 1 ):		# add to new line if exceed the width
	
		if ( linespacing > 0 ):
			print()
			k = 0
			for k in range(linespacing):
				print()
		else:
			print()
	
		current_width = 0

		if ( left > 0 ):
			k = 0
			for k in range(left):
				print(" ", end='')
				current_width = current_width + 1
	
	if ( current_width == left ):									# normal printing for the first word
		print(word, end='')
		current_width = current_width + len(word) + 1
	else:
		print(' ' + word, end='')									# normal printing for the second and later word
		current_width = current_width + len(word) + 1
	

def print_newline():

	print()
	print()	
	if ( linespacing > 0 ):
		k = 0
		for k in range(linespacing-1):
			print()			
	if ( linespacing > 0 ):
		print()
		k = 0
		for k in range(linespacing):
			print()	
	
def print_newline2():

	print()
	if ( linespacing > 0 ):
		print()
		k = 0
		for k in range(linespacing):
			print()

def LM(second_word):

	global left

	if ( second_word.isdigit() ):		
		left = int(second_word)
		return 1
				
	if ( second_word.startswith('+') and second_word[1:].isdigit() ):
						
		left = left + int(second_word[1:])			
		if ( left > width - 20 ):
			left = width - 20
		return 1
		
	if ( second_word.startswith('-') and second_word[1:].isdigit() ):
		if ( int(second_word[1:]) > left ):
			left = 0
		else:
			left = left - int(second_word[1:])
		return 1
		
	return 0

	
def main():
	
	global width
	global left
	global linespacing
	global formatting
	global current_width
	line2 = ""
	second_newline = "no"
	

	#with open(sys.argv[1], "r") as f:					# read the file
	
	for line in fileinput.input(): 					# read by line
		
		first_word = "yes"
		line2 = line
		i = 0
		words = line.split()
			
		if ( line == '\n' and formatting == 1 and second_newline == "no" ):			# for the case of empty line
			current_width = 0
			print_newline()
			second_newline = "yes"		
						
		elif ( line == '\n' and formatting == 1 and second_newline == "yes" ): 		 # for the case of 2nd or more new line
			current_width = 0
			print_newline2()


		while ( i < len(words) ):
				
			if ( words[i] == ".LW" and first_word == "yes" ):			# case for LW
				if ( words[i+1].isdigit() ):
					formatting = 1
					width = int(words[i+1])
					i = i + 1

			elif ( words[i] == ".LM" and first_word == "yes" ):			# case for LM
				second_word = words[i+1]
				i = i + LM(second_word)
					
			elif ( words[i] == ".LS" and first_word == "yes" ):			# case for LS
				if ( words[i+1].isdigit() ):
					linespacing = int(words[i+1])
					i = i + 1
	
			elif ( words[i] == ".FT" and first_word == "yes" ):			# case for FT	
				if ( words[i+1] == 'on' ):
					formatting = 1
					i = i + 1
				elif ( words[i+1] == 'off' ):
					formatting = 0
					i = i + 1
					new_line = line.split("off ")
					if (len(new_line) > 1):
						line = "" + new_line[1]
					else:
						line = ""

			elif ( words[i] != "" and formatting == 1 ):				# the case for normal printing words
				first_word = "no"
				second_newline = "no"
				printing( words[i] )
				
			i = i + 1
			first_word = "no"
			
		if ( line != "" and formatting == 0 ):							# case for printing whole line when FT off
			print(line, end='')
			
	if ( len(line2) > 2 and line2.endswith('\n') and formatting == 1 ):		# case for last line is empty line
		print()


if __name__ == "__main__":
	main()

	