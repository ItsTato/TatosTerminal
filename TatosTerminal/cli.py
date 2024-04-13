import sys

from .TTSession import Terminal

def main() -> None:
	commands:list = sys.argv[1].split(";;")

	session:Terminal = Terminal()

	print("TatosTerminal session was closed.")
	return