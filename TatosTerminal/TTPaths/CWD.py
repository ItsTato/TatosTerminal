from os import path, getcwd

def get() -> str:
	return path.abspath(getcwd()).replace("\\","/")