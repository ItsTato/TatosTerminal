class Package:
    def __init__(self, package_name:str, package_pypi_name:str="") -> None:
        self.__package_name:str = package_name
        if package_pypi_name != "":
            self.__package_pypi_name:str = package_pypi_name
        else:
            self.__package_pypi_name:str = self.__package_name
    @property
    def name(self) -> str:
        return self.__package_name
    @property
    def pypi(self) -> str:
        return self.__package_pypi_name