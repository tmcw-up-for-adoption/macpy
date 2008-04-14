import numpy
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
		self.viz = False
		self.a = ""
		self.b = ""
		self.a_res = ""
		self.b_res = ""
		self.path = []
		self.score = 0

	def sim(self, a, b):
		if a == b:
			return 0
		else:
			return 1

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
# End AlignNW

class AlignSP:
	def build_matrix(self, a, b, c):
		score =  zeros((len(a), len(b), len(c))) # pg. 12
		option = zeros((len(a), len(b), len(c))) # pg. 12
		d = 0
		for x in range(len(a)):
			score[x, 0, 0] = d * x
		for y in range(len(b)):
			score[0, y, 0] = d * y
		for z in range(len(c)):
			score[0, 0, z] = d * z
		for x in range(1, len(a) + 1):
			for y in range(1, len(b) + 1):
				for z in range(1, len(c) + 1):
					


nw = AlignNW()
nw.viz = True
print nw.align("TCCAGCCCCAGGA", "TCCAGCCCCAGGA")
nw.trace()
#m = build_matrix("TCCAGCCCCAGGA", "TAGTCCTCA")
#get_alignment(m, "TCCAGCCCCAGGA", "TAGTCCTCA")

#sp(["TCC", "TA", "TCG"])
