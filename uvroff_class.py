 #!/usr/bin/env python3
 # Ronald Liu	V00838627 

import sys
import string
import fileinput
import numbers


class UVroff:
	
	def __init__(self, file, list):
		
		self.output_list = [""]
		
		self.width = 0
		self.left = 0
		self.linespacing = 0
		self.formatting = 0
		self.current_width = 0
		
		self.line2 = ""
		self.second_newline = "no"
	
		if ( list != None ):
			self.list_input(list)
			
		else:
			if ( file != "stdin" ):
				try:
					file_test = open( file )
					file_test.close()
				except FileNotFoundError :
					print ( " ***invalid file_name*** " )
					exit()
			
			for line in fileinput.input(): 
				self.uvr2(line)	
				
			if ( len(self.line2) > 2 and self.line2.endswith('\n') and self.formatting == 1 ):		# case for last line is empty line
				self.output_list[0] = self.output_list[0] + '\n'
	
					
	def printing(self,word):
		
		if ( self.left > 0 and self.current_width == 0 and self.formatting == 1 ):			# adding the left spacing
			k = 0
			for k in range(self.left):
				self.output_list[0] = self.output_list[0] + ' ' 
				self.current_width = self.current_width + 1
		
		if ( (self.current_width + len(word) ) > self.width and self.formatting == 1 ):		# add to new line if exceed the width
		
			if ( self.linespacing > 0 ):
				self.output_list[0] = self.output_list[0] + '\n'
				k = 0
				for k in range(self.linespacing):
					self.output_list[0] = self.output_list[0] + '\n'
			else:
				self.output_list[0] = self.output_list[0] + '\n'
		
			self.current_width = 0

			if ( self.left > 0 ):
				k = 0
				for k in range(self.left):
					self.output_list[0] = self.output_list[0] + ' '
					self.current_width = self.current_width + 1
		
		if ( self.current_width == self.left ):									# normal printing for the first word
			self.output_list[0] = self.output_list[0] + word
			self.current_width = self.current_width + len(word) + 1
		else:
			self.output_list[0] = self.output_list[0] + ' ' + word								# normal printing for the second and later word
			self.current_width = self.current_width + len(word) + 1

	def print_newline(self):

		self.output_list[0] = self.output_list[0] + '\n'
		self.output_list[0] = self.output_list[0] + '\n'
		if ( self.linespacing > 0 ):
			k = 0
			for k in range(self.linespacing-1):
				self.output_list[0] = self.output_list[0] + '\n'			
		if ( self.linespacing > 0 ):
			self.output_list[0] = self.output_list[0] + '\n'
			k = 0
			for k in range(self.linespacing):
				self.output_list[0] = self.output_list[0] + '\n'
		
	def print_newline2(self):

		self.output_list[0] = self.output_list[0] + '\n'
		if ( self.linespacing > 0 ):
			self.output_list[0] = self.output_list[0] + '\n'
			k = 0
			for k in range(self.linespacing):
				self.output_list[0] = self.output_list[0] + '\n'

	def LM(self,second_word):

		if ( second_word.isdigit() ):		
			self.left = int(second_word)
			return 1
					
		if ( second_word.startswith('+') and second_word[1:].isdigit() ):
							
			self.left = self.left + int(second_word[1:])			
			if ( self.left > self.width - 20 ):
				self.left = self.width - 20
			return 1
			
		if ( second_word.startswith('-') and second_word[1:].isdigit() ):
			if ( int(second_word[1:]) > self.left ):
				self.left = 0
			else:
				self.left = self.left - int(second_word[1:])
			return 1
			
		return 0

	def list_input(self, list):
	
		tmp = [ self.uvr2(elem) for elem in list ]
		
		if ( len(self.line2) > 2 and self.line2.endswith('\n') and self.formatting == 1 ):		# case for last line is empty line
			self.output_list[0] = self.output_list[0] + '\n'
		

		
	def uvr2(self, line):

			
		first_word = "yes"
		self.line2 = line
		i = 0
		words = line.split()
				
		if ( line == '\n' and self.formatting == 1 and self.second_newline == "no" ):			# for the case of empty line
			self.current_width = 0
			self.print_newline()
			self.second_newline = "yes"		
							
		elif ( line == '\n' and self.formatting == 1 and self.second_newline == "yes" ): 		 # for the case of 2nd or more new line
			self.current_width = 0
			self.print_newline2()


		while ( i < len(words) ):
					
			if ( words[i] == ".LW" and first_word == "yes" ):			# case for LW
				if ( words[i+1].isdigit() ):
					self.formatting = 1
					self.width = int(words[i+1])
					i = i + 1

			elif ( words[i] == ".LM" and first_word == "yes" ):			# case for LM
				second_word = words[i+1]
				i = i + self.LM(second_word)
					
			elif ( words[i] == ".LS" and first_word == "yes" ):			# case for LS
				if ( words[i+1].isdigit() ):
				
					if ( int(words[i+1]) > 2 ):
						print( 'the input linespacing value is larger than 2' )
						exit()
					
					self.linespacing = int(words[i+1])
					i = i + 1
		
			elif ( words[i] == ".FT" and first_word == "yes" ):			# case for FT	
				if ( words[i+1] == 'on' ):
					self.formatting = 1
					i = i + 1
				elif ( words[i+1] == 'off' ):
					self.formatting = 0
					i = i + 1
					new_line = line.split("off ")
					if (len(new_line) > 1):
						line = "" + new_line[1]
					else:
						line = ""

			elif ( words[i] != "" and self.formatting == 1 ):				# the case for normal printing words
				first_word = "no"
				self.second_newline = "no"
				self.printing( words[i] )
					
			i = i + 1
			first_word = "no"
				
		if ( line != "" and self.formatting == 0 ):							# case for printing whole line when FT off
			self.output_list[0] = self.output_list[0] + line

	
			
	def get_lines(self):
		
		self.output_list[0] = self.output_list[0][0:(len(self.output_list[0])-1)]  		# for deleting the last space line
		
		return self.output_list
		
		
		
