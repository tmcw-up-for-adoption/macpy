import Image, ImageDraw, sys, nw
import seq

# First test

ssize = 20

strings = seq.sim_string("TCCAGCCCCAGGATATTTCAGGGAGGAGTCAGTATGACTAT", 2, 10)

n = nw.AlignNW()
n.viz = True
n.align(strings[0], strings[1])
w = n.matrix.shape[0] * ssize # width
h = n.matrix.shape[1] * ssize # height

im = Image.new("RGBA", (w,h))

draw = ImageDraw.Draw(im)
draw.line((0, 0) + im.size, fill=128)
draw.line((0, im.size[1], im.size[0], 0), fill=128)

m = n.matrix[n.matrix.shape[0] - 1, n.matrix.shape[1] - 1]

for x in range(n.matrix.shape[0]):
	for y in range(n.matrix.shape[1]):
		if [x, y] in n.path:
			draw.rectangle([(x * ssize, y * ssize), ((x * ssize) + ssize, (y * ssize) + ssize)], fill="#fff")
			draw.text((x * ssize + (ssize / 4), y * ssize + (ssize / 4)), str(n.matrix[x, y]), fill="#000")
		else: # this calculates a color based on present / max
			# casting into floats is necessary because NumPy has all elements as ints, so they would otherwise yield 0 or 1
			draw.rectangle([(x * ssize, y * ssize), ((x * ssize) + ssize, (y * ssize) + ssize)], fill="rgb("+str(int((float(n.matrix[x, y]) / float(m))*255))+", 0, 0)")
			draw.text((x * ssize + (ssize / 4), y * ssize + (ssize / 4)), str(n.matrix[x, y]))

del draw 

# write to stdout
im.save("lena.png")
