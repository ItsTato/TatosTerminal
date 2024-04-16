from os import name, path, getlogin, listdir
from platform import node
import colorama, lupa, json
from colorama import Fore, Style
from typing import Union, Any

from TatosTerminal.TTPaths import CWD, PD
from .Errors import IncompleteInstallation

colorama.init(autoreset=True)
lua:lupa.LuaRuntime = lupa.LuaRuntime(unpack_returned_tuples=True)
running:bool = True

def Terminal(file_name:str,smush:bool) -> None: #commands:list = sys.argv[1].split(";;")
	cwd:str = CWD.get().replace("\\","/")
	pd:str = PD.get(file_name).replace("\\","/")

	current_app:str = f"{Fore.LIGHTMAGENTA_EX}TT{Fore.LIGHTYELLOW_EX}-{Fore.LIGHTMAGENTA_EX}{name}" ## i.e. TT-nt
	user_at_host:str = f"{Fore.LIGHTMAGENTA_EX}{getlogin()}{Fore.LIGHTYELLOW_EX}@{Fore.LIGHTMAGENTA_EX}{node()}" # i.e. ItsTato@ItsTatoPC

	if name == "nt":
		temp:str = cwd[1:]
		drive:str = cwd[0]
		temp = temp.replace(":",f"{Fore.LIGHTBLUE_EX}{Style.BRIGHT}{drive}~{Style.RESET_ALL}{Fore.LIGHTBLUE_EX}")
		at_directory:str = f"{temp}".replace("/",f"{Fore.LIGHTYELLOW_EX}{Style.BRIGHT}/{Style.RESET_ALL}{Fore.LIGHTBLUE_EX}")
	else:
		temp:str = cwd
		at_directory:str = f"{Fore.LIGHTBLUE_EX}{Style.BRIGHT}Penguin~{Style.RESET_ALL}{Fore.LIGHTBLUE_EX}{temp}".replace("/",f"{Fore.LIGHTYELLOW_EX}{Style.BRIGHT}/{Style.RESET_ALL}{Fore.LIGHTBLUE_EX}")

	script_dir = path.join(pd,"scripts")
	if not path.exists(script_dir):
		raise IncompleteInstallation("Required directory /scripts/ is missing!")
	scripts:list = listdir(script_dir)
	for index, script in enumerate(scripts):
		if not path.isdir(path.join(script_dir,script)):
			del scripts[index]

	if not path.exists(path.join(script_dir,"index.json")):
		data:dict = {
			"packages": [
				{"builtin": "1.0.0"},
				{"susm": "1.0.0"}
			],
			"commands": {}
		}
		with open(path.join(script_dir,"index.json"),"w") as file:
			json.dump(data,file)

	def __import_or_from(_,parts_pname:Union[str,dict],p_name:str=""):
		if p_name == "":
			if isinstance(parts_pname,str):
				return __import__(parts_pname)
			if len(parts_pname) > 1:
				table:dict = {}
				for index in parts_pname:
					table[parts_pname[index]] = __import__(parts_pname[index])
				return table
		if not isinstance(parts_pname,str) and len(parts_pname) > 1:
			table:dict = {}
			for index in parts_pname:
				table[parts_pname[index]] = getattr(__import__(p_name),parts_pname[index])
			return table
		if not isinstance(parts_pname,str):
			return getattr(__import__(p_name),parts_pname[1])
		return getattr(__import__(p_name),parts_pname)

	def __Exit(_) -> None: global running; running = False; return
	def __get_running(_) -> bool: return globals().get("running")

	def __to_lua_list(py_list:list) -> list:
		py_list.insert(0,None)
		py_list.append(None)
		return py_list
	def __remove_from_lua_list(lua_list:list,pos:int):
		print(pos)
		del lua_list[pos]

	__TTMeta:dict = {
		"directory": pd
	}
	__Session:dict = {
		"cwd": cwd,
		"Exit": __Exit,
		"isRunning": __get_running
	}
	__Python:dict = {
		"Import": __import_or_from,
		"Require": __import_or_from,
		"Module": __import_or_from,
		"Using": __import_or_from,
		"Package": __import_or_from
	}
	__list:dict = {
		"curate": __to_lua_list,
		"remove": __remove_from_lua_list
	}

	lua.globals().TTMeta = __TTMeta
	lua.globals().Session = __Session
	lua.globals().Python = __Python
	lua.globals().list = __list

	while globals().get("running"):
		if not smush:
			prompt:str = f"{current_app} {Fore.LIGHTYELLOW_EX}|> {user_at_host}\n{at_directory}{Fore.LIGHTYELLOW_EX}%{Fore.LIGHTWHITE_EX} "
		else:
			prompt:str = f"{current_app}{Fore.LIGHTYELLOW_EX}|>{user_at_host} {at_directory}{Fore.LIGHTYELLOW_EX}%{Fore.LIGHTWHITE_EX} "

		not_parsed:str = ""
		try:
			not_parsed = input(prompt)
		except KeyboardInterrupt:
			#global running
			#running = False
			print("")

		if not_parsed == "exit":
			file = open(f"{pd}/scripts/builtin/exit.lua","r")
			lua.execute(file.read())()
			file.close()

		if not_parsed == "susm list":
			file = open(f"{pd}/scripts/susm/susm list.lua","r")
			try:
				lua.execute(file.read())()
			except Exception as e:
				print(e)
			file.close()
	return
