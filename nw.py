import numpy
from fasta import Fasta
from Numeric import *

'''
	Author Tom MacWright
	Needleman-Wunsch Algorithm
	Requires NumPy
'''

'''
	Align via Needleman-Wunsch
	Time efficiency of O(k^2)
	Which in this case is O( (len(a) + len(b))^2 )
'''

class AlignNW(object):
	smiss = 1
	smatch = 0
	sspace = 1
	def __init__(self):
		self.f_parser = Fasta()
		self.viz = False
		self.a = ""
		self.b = ""
		self.a_res = ""
		self.b_res = ""
		self.path = []
		self.steps = []
		self.score = 0

	def sim(self, a, b):
		if a == b:
			return 1
		else:
			return -1

	def falign(self, fasta_file):
		seqs = self.f_parser.read(fasta_file)
		self.align(seqs[0][1], seqs[1][1])

	def align(self, a, b):
		matrix = self.build_matrix(a, b)
		i = len(a)
		j = len(b)
		ao = ""
		bo = ""
		while i > 0 and j > 0:
			current = 	matrix[i, j]
			diagonal = 	matrix[i - 1, j - 1]
			up = 				matrix[i, j - 1]
			left =			matrix[i - 1, j]
			# Diagonal
			if self.viz:
				self.path.append([i, j]) # append this coordinate to the path through the matrix
			if current == diagonal + self.sim(a[i - 1], b[j - 1]):
				ao = a[i - 1] + ao
				bo = b[j - 1] + bo
				i = i - 1
				j = j - 1
			# Left
			elif current == left:
				ao = a[i - 1] + ao
				bo = "-" + bo
				i = i - 1
				self.score = self.score + self.sspace
			# Up
			elif current == up:
				ao = "-" + ao
				bo = b[j - 1] + bo
				j = j - 1
				self.score = self.score + self.sspace
		# Stuck on the top?
		while i > 0:
			ao = a[i - 1] + ao
			bo = "-" + bo
			i = i - 1
			self.score = self.score + self.sspace
		# Stuck on the right
		while j > 0:
			ao = "-" + ao
			bo = b[j - 1] + bo
			j = j - 1
			self.score = self.score + self.sspace
		self.a_res = ao
		self.b_res = bo
		self.matrix = matrix
		return self.score
	def build_matrix(self, a, b):
		d = 0
		matrix = zeros((len(a) + 1, len(b) + 1))
		for y in range(len(a)):
			matrix[y, 0] = d * y
		for x in range(len(b)):
			matrix[0, x] = d * x
		for y in range(1, len(a) + 1):
			for x in range(1, len(b) + 1):
				matrix[y, x] = max(
					[ matrix[y - 1, x - 1] + self.sim(a[y-1], b[x -1]),
						matrix[y - 1, x] + d,
						matrix[y, x - 1] + d ])
		return matrix
	def trace(self, format="text"):
		if self.viz == False:
			print "You need to enable visualization with .viz = True"
			return False
		else:
			for x in range(self.matrix.shape[0]):
				for y in range(self.matrix.shape[1]):
					if [x, y] in self.path:
						print "["+str(self.matrix[x, y])+"]", 
					else:
						print " "+str(self.matrix[x,y])+" ",
				print ""


'''
	Align via generalized NW
	Requires O(n^3) space
'''

class AlignSP:
	def __init__(self):
		self.f_parser = Fasta()
	# Three-way score function.
	def sim(self, a, b, c):
		if a == b == c:
			return 1
		else:
			return -1
	def build_matrix(self, a, b, c):
		self.score =  zeros((len(a) + 1, len(b) + 1, len(c) + 1)) # pg. 12
		self.option = zeros((len(a) + 1, len(b) + 1, len(c) + 1)) # pg. 12
		d = 0
		for x in range(len(a)):
			self.score[x, 0, 0] = d * x
		for y in range(len(b)):
			self.score[0, y, 0] = d * y
		for z in range(len(c)):
			self.score[0, 0, z] = d * z
		for x in range(1, len(a) + 1):
			for y in range(1, len(b) + 1):
				for z in range(1, len(c) + 1):
					# 7 possibilities here. Just imagine a hypercube with one section taken out.
					# (2 * 2 * 2) - 1 = 7
					print "in loop:", x, y, z
					options = [
							# Diagonal							
							self.score[x - 1, y - 1, z - 1] + self.sim(a[x - 1], b[y - 1], c[z - 1]), #0
							self.score[x - 1, y - 1, z], #1
							self.score[x - 1, y,     z], #2
							self.score[x - 1, y,     z - 1], #3
							self.score[x    , y - 1, z], #4
							self.score[x    , y,     z - 1], #5
							self.score[x    , y - 1, z - 1] ]
					m = None
					index = None					
					for i in range(len(options)):
						if options[i] > m:
							m = options[i]
							index = i
					self.score [x, y, z] = m
					self.option[x, y, z] = index
		return self.score
	def falign(self, fasta_file):
		seqs = self.f_parser.read(fasta_file)
		self.align(seqs[0][1], seqs[1][1], seqs[2][1])
	def align(self, a, b, c):
		self.build_matrix(a, b, c)
		ao = ""
		bo = ""
		co = ""
		x = len(a)
		y = len(b)
		z = len(c)
		while x > 0 and y > 0 and z > 0:
			if self.option[x, y, z] == 0:
				ao = a[x - 1] + ao
				bo = b[y - 1] + bo
				co = c[z - 1] + co 
				x = x - 1
				y = y - 1
				z = z - 1
			elif self.option[x, y, z] == 1:
				ao = a[x - 1] + ao
				bo = b[y - 1] + bo
				co = "-" + co
				x = x - 1
				y = y - 1
			elif self.option[x, y, z] == 2:
				ao = a[x - 1] + ao
				bo = "-" + bo
				co = "-" + co
				x = x - 1
			elif self.option[x, y, z] == 3:
				ao = a[x - 1] + ao
				bo = "-" + bo
				co = c[z - 1] + co
				x = x - 1
				z = z - 1
			elif self.option[x, y, z] == 4:
				ao = "-" + ao
				bo = b[y - 1] + bo
				co = "-" + co
				y = y - 1
			elif self.option[x, y, z] == 5:
				ao = "-" + ao
				bo = "-" + bo
				co = c[z - 1] + co
				z = z -1
			elif self.option[x, y, z] == 6:
				ao = "-" + ao
				bo = b[y - 1] + bo
				co = c[z - 1] + co
				y = y - 1
				z = z - 1
			self.a_res = ao
			self.b_res = bo
			self.c_res = co




class AlignMP:
	# Three-way score function.
	def sim(self, a, b, c):
		if a == b == c:
			return 1
		else:
			return -1
	def build_matrix(self, a, b, c):
		self.score =  zeros((len(a) + 1, len(b) + 1, len(c) + 1)) # pg. 12
		self.option = zeros((len(a) + 1, len(b) + 1, len(c) + 1)) # pg. 12
		d = 0
		for x in range(len(a)):
			self.score[x, 0, 0] = d * x
		for y in range(len(b)):
			self.score[0, y, 0] = d * y
		for z in range(len(c)):
			self.score[0, 0, z] = d * z
		for x in range(1, len(a) + 1):
			for y in range(1, len(b) + 1):
				for z in range(1, len(c) + 1):
					# 7 possibilities here. Just imagine a hypercube with one section taken out.
					# (2 * 2 * 2) - 1 = 7
					options = [
							# Diagonal							
							self.score[x - 1, y - 1, z - 1] + self.sim(a[x - 1], b[y - 1], c[z - 1]), #0
							self.score[x - 1, y - 1, z], #1
							self.score[x - 1, y,     z], #2
							self.score[x - 1, y,     z - 1], #3
							self.score[x    , y - 1, z], #4
							self.score[x    , y,     z - 1], #5
							self.score[x    , y - 1, z - 1] ]
					m = None
					# it seems like we'll need to keep track of every pairwise score in the traceback step
					# this could be tricky.
					index = None					
					for i in range(len(options)):
						if options[i] > m:
							m = options[i]
							index = i
					self.score [x, y, z] = m
					self.option[x, y, z] = index
		return self.score
	def align(self, a, b, c):
		self.build_matrix(a, b, c)
		ao = ""
		bo = ""
		co = ""
		x = len(a)
		y = len(b)
		z = len(c)
		while x > 0 and y > 0 and z > 0:
			if self.option[x, y, z] == 0:
				ao = a[x - 1] + ao
				bo = b[y - 1] + bo
				co = c[z - 1] + co 
				x = x - 1
				y = y - 1
				z = z - 1
			elif self.option[x, y, z] == 1:
				ao = a[x - 1] + ao
				bo = b[y - 1] + bo
				co = "-" + co
				x = x - 1
				y = y - 1
			elif self.option[x, y, z] == 2:
				ao = a[x - 1] + ao
				bo = "-" + bo
				co = "-" + co
				x = x - 1
			elif self.option[x, y, z] == 3:
				ao = a[x - 1] + ao
				bo = "-" + bo
				co = c[z - 1] + co
				x = x - 1
				z = z - 1
			elif self.option[x, y, z] == 4:
				ao = "-" + ao
				bo = b[y - 1] + bo
				co = "-" + co
				y = y - 1
			elif self.option[x, y, z] == 5:
				ao = "-" + ao
				bo = "-" + bo
				co = c[z - 1] + co
				z = z -1
			elif self.option[x, y, z] == 6:
				ao = "-" + ao
				bo = b[y - 1] + bo
				co = c[z - 1] + co
				y = y - 1
				z = z - 1
		


#nw = AlignNW()
#nw.viz = True
#nw.falign("test.fasta")
#print nw.a_res
#print nw.b_res

sp = AlignSP()
sp.falign("sample.fasta")
print sp.a_res
print sp.b_res
print sp.c_res
#nw.trace()

#sp(["TCC", "TA", "TCG"])

