from sys import argv

from .TTSession import Terminal

def main() -> None:
	smush:bool = False
	if len(argv) > 1:
		if "--smush" in argv:
			smush = True
	Terminal(__file__,smush)
	print("\n\nTatosTerminal session was closed.")
	return