import random

# source: original string
# n: # strings needed
# entropy: difference level, 0 to 100
def sim_string(source, n, entropy):
	out = []
	for i in range(n):
		o = ""
		for a in range(len(source)):
			if random.random() * 100 < entropy:
				# deletion happens here
				pass
			else:
				o = o + source[a]
		out.append(o)
	return out
