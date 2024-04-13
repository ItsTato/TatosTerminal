from os import system

from .extra_classes import Package

class SafeImport:
    def __init__(self,pckg_name:str,pckg_pypi:str="") -> None:
        self.__package:Package = Package(pckg_name,pckg_pypi)
    def add(self):
        try:
            exec(f"import {self.__package.name}")
        except Exception:
            system(f"python -m pip install -U {self.__package.pypi}")
            exec(f"import {self.__package.name}")