import sys
import os
from solver import run

if __name__ == '__main__':
	total_iterations = 2000 if len(sys.argv) < 2 else int(sys.argv[1])
	success = 0

	backup_stdout = sys.stdout
	sys.stdout = open(os.devnull, "w")

	for _ in range(total_iterations):
		success += not run()

	sys.stdout = backup_stdout

	print(f"Success rate: {round((success/total_iterations) * 100, 2)}%")