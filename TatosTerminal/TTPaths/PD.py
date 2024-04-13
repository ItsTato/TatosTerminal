from os import path

def get(file_name:str) -> str:
	return path.abspath(file_name).replace("__main__.py","")