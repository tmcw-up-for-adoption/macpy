import sys


class Fasta(object):
	def __init__(self):
		self.seqs = []
	def read(filehandle):
		try:		
			f = open('test.fasta')
		except IOError:
			print "Fasta file did not exist"
			return		
		text = f.read()
		seqs = text.split('>')
		for s in seqs:
			parts = s.split('\n')
			self.seqs.append(
				[parts[0], ''.join(parts[1:])])
		return self.seqs
