from typing import Callable

from colorama import Fore, Back, Style

class Tag:
	def __init__(self,name:str,back_color:str=Back.RESET,fore_color:str=Fore.RESET,style:str=Style.BRIGHT) -> None:
		self.__name:str = name
		self.__back_color:str = back_color
		self.__fore_color:str = fore_color
		self.__style:str = style
	@property
	def Name(self) -> str:
		return self.__name
	@Name.setter
	def Name(self,new_name:str) -> None:
		self.__name = new_name
	def gen_tag(self) -> str:
		return f"{self.__style}{self.__back_color}{self.__fore_color} {self.__name} {Fore.RESET}{Back.RESET}{Style.RESET_ALL} "

WARNING:Tag = Tag("WARN",Back.LIGHTYELLOW_EX,Fore.LIGHTWHITE_EX)
ERROR:Tag = Tag("ERROR",Back.LIGHTRED_EX,Fore.LIGHTWHITE_EX)
GOOD:Tag = Tag("GOOD",Back.LIGHTGREEN_EX,Fore.LIGHTWHITE_EX)
OK:Tag = Tag("OK",Back.GREEN,Fore.LIGHTWHITE_EX)

def createMessage(tags:list[Tag],message:str) -> Callable:
	assert len(tags) > 0, "Must use at least 1 tag!"
	assert message is not None, "Must provide a message!"
	final:str=""
	for tag in tags:
		final = f"{final}{tag.gen_tag()}"
	def _() -> None:
		print(f"{final}{message}")
	return _