import numpy
from Numeric import *

'''
	Author Tom MacWright
	Needleman-Wunsch Algorithm
	Requires NumPy
'''

def sim(a, b):
	if a == b:
		return 1
	else:
		return 0

def get_alignment(matrix, a, b):
	i = len(a)
	j = len(b)
	ao = ""
	bo = ""
	while i > 0 and j > 0:
		current = 	matrix[i, j]
		diagonal = 	matrix[i - 1, j - 1]
		up = 				matrix[i, j - 1]
		left =			matrix[i - 1, j]
		if current == diagonal + sim(a[i - 1], b[j - 1]):
			ao = a[i - 1] + ao
			bo = b[j - 1] + bo
			i = i - 1
			j = j - 1
		elif current == left:
			ao = a[i - 1] + ao
			bo = "-" + bo
			i = i - 1
		elif current == up:
			ao = "-" + ao
			bo = b[j - 1] + bo
			j = j - 1
	while i > 0:
		ao = a[i - 1] + ao
		bo = "-" + bo
		i = i - 1
	while j > 0:
		ao = "-" + ao
		bo = b[j - 1] + bo
		j = j - 1
	print ao
	print bo


def build_matrix(a, b):
	d = 0 #this should be changed in the final project
	# create the initial matrix	
	matrix = zeros((len(a) + 1, len(b) + 1))
	for y in range(len(a)):
		matrix[y, 0] = d * y
	for x in range(len(b)):
		matrix[0, x] = d * x
	for y in range(1, len(a) + 1):
		for x in range(1, len(b) + 1):
			matrix[y, x] = max(
				[ matrix[y - 1, x - 1] + sim(a[y-1], b[x -1]),
				  matrix[y - 1, x] + d,
					matrix[y, x - 1] + d ])
	return matrix

m = build_matrix("TCCAGCCCCAGGA", "TAGTCCTCA")
get_alignment(m, "TCCAGCCCCAGGA", "TAGTCCTCA")
