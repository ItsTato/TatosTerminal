from os import path

def get(file_name:str) -> str:
	dir_name, _ = path.split(path.abspath(file_name))
	return dir_name