from os import path
from json import load, dump

from .TTImportTester import CheckForPackage
from .TTPaths import CWD, PD
from .cli import main

cwd:str = CWD.get()
pd:str = PD.get(__file__)

if not path.exists(f"{pd}/depend.json"):
	with open(f"{pd}/depend.json","w") as file:
		dependencies:list = ["colorama"]
		dump(dependencies,file)
else:
	with open(f"{pd}/depend.json","r") as file:
		dependencies:list = load(file)

for dependency in dependencies:
	CheckForPackage(dependency)

main()