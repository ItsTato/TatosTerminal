class RequiredPackageIsNotInstalled(Exception):
	def __init__(self,message:str) -> None:
		super().__init__(message)
		self.__message:str = message
		return
	@property
	def message(self) -> str:
		return self.__message