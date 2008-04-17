import nw, sys
import cProfile

def main(argv=sys.argv):
	n = nw.AlignNW()
	cProfile.runctx("n.align('"+argv[1]+"', '"+argv[2]+"')", globals(), locals())
	

if __name__ == "__main__":
    sys.exit(main())
