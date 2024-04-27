from sys import argv

from .TTSession import Terminal

def main() -> None:
	smush:bool = False
	ignore_bad_package:bool = False
	ignore_bad_install:bool = False
	if len(argv) > 1:
		if "--smush" in argv:
			smush = True
		if "--ignore-bad-package" in argv:
			ignore_bad_package = True
		if "--ignore-bad-install" in argv:
			ignore_bad_install = True
	Terminal(__file__,smush,ignore_bad_package,ignore_bad_install)
	print("Goodbye traveler! TatosTerminal session has been closed.")
	return