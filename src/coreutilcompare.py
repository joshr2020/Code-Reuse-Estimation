'''
Copyright (C) 2017 Aurin Chakravarty & Joshua Russo
'''
import subprocess
import os
import sys

def main(argv):
	filenames = os.listdir(sys.argv[1])

	filepaths = []
	for name in filenames:
		filepaths.append(str(sys.argv[1]) + name)
	write_out = open('GNUanalysis.txt', 'w')

	for x in range(0, int(sys.argv[2])):
		for y in range(x, int(sys.argv[2])):
			if x == y:
				continue
				pass
			try:
				subprocess.run(['python3.6', 'binary_compare.py', filepaths[x], filepaths[y]], stdout=write_out)
			except Exception as invalid:
				print(invalid)
			pass
		pass

	write_out.close()

if __name__ == "__main__":
    main(sys.argv[0:])
