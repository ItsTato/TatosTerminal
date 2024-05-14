from os import name, path, getlogin, listdir, system
from platform import node
import lupa
import json
from colorama import just_fix_windows_console, Fore, Style
from typing import Union, Any

from TatosTerminal.TTPaths import CWD, PD
from .Errors import IncompleteInstallation, InvalidPackage
from .Message import createMessage, WARNING, ERROR

just_fix_windows_console()

lua:lupa.LuaRuntime = lupa.LuaRuntime(unpack_returned_tuples=True)
running:bool = True

def clear_console() -> None: system("cls" if name in ["nt","dos"] else "clear")

def Terminal(file_name:str,smush:bool,ignore_bad_package:bool,ignore_bad_install:bool) -> None:
	clear_console()

	cwd:str = CWD.get().replace("\\","/")
	pd:str = PD.get(file_name).replace("\\","/")

	os:str = name.lower()
	os = os.replace("nt","win").replace("dos","win")
	os = os.upper()

	current_app:str = f"{Fore.LIGHTMAGENTA_EX}TT{Fore.LIGHTYELLOW_EX}-{Fore.LIGHTMAGENTA_EX}{os}" ## i.e. TT-WIN
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
		if not ignore_bad_install:
			raise IncompleteInstallation("Required directory /scripts/ is missing!\nLaunch with --ignore-bad-install to continue loading anyways.")
		else:
			createMessage([ERROR],"Required directory /scripts/ is missing!")()
	raw_scripts:list = listdir(script_dir)
	scripts:list = []
	for index, script in enumerate(raw_scripts):
		if path.isdir(path.join(script_dir,script)):
			scripts.append(script)

	if "builtin" not in scripts:
		if not ignore_bad_install:
			raise IncompleteInstallation("Missing pre-installed package \"builtin\" (1.0.0)!\nLaunch with --ignore-bad-install to continue loading anyways.")
		else:
			createMessage([WARNING],"Missing pre-installed package \"builtin\" (1.0.0)!")()
	if "susm" not in scripts:
		if not ignore_bad_install:
			raise IncompleteInstallation("Missing pre-installed package \"susm\" (1.0.0)!\nLaunch with --ignore-bad-install to continue loading anyways.")
		else:
			createMessage([WARNING],"Missing pre-installed package \"susm\" (1.0.0)!")()

	for script in scripts:
		script_at:str = path.join(script_dir,script)
		if not path.exists(path.join(script_at,"manifest.json")):
			if not ignore_bad_package:
				raise InvalidPackage(f"Package {script} is missing required file \"manifest.json\"!\nLaunch with --ignore-bad-package to continue loading anyways.")
			else:
				createMessage([ERROR],f"Package {script} is missing required file \"manifest.json\'!")()

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

	def __import_or_from(_,parts_pname:Union[str,dict],p_name:str=None):
		if p_name is None:
			if isinstance(parts_pname,str):
				return __import__(parts_pname)
			if len(parts_pname) > 1:
				table:dict = {}
				for i in parts_pname:
					table[parts_pname[i]] = __import__(parts_pname[i])
				return table
		if not isinstance(parts_pname,str) and len(parts_pname) > 1:
			table:dict = {}
			for i in parts_pname:
				table[parts_pname[i]] = getattr(__import__(p_name),parts_pname[i])
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

	def __table_find(table:dict,o:Any) -> Any:
		for i in table:
			if table[i] == o: return o
		return None
	def __table_has(table:dict,o:Any) -> Any:
		return True if __table_find(table,o) is not None else False

	__TTMeta:dict = {
		"directory": pd.replace("\\","/")
	}
	__Session:dict = {
		"cwd": cwd.replace("\\","/"),
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
		"curate": __to_lua_list
	}

	lua.globals().TTMeta = __TTMeta
	lua.globals().Session = __Session
	lua.globals().Python = __Python
	lua.globals().list = __list

	lua.globals().table.find = __table_find
	lua.globals().table.has = __table_has

	while globals().get("running"):
		if not smush:
			prompt:str = f"{current_app} {Fore.LIGHTYELLOW_EX}|> {user_at_host}\n{at_directory}{Fore.LIGHTYELLOW_EX}%{Fore.LIGHTWHITE_EX} "
		else:
			prompt:str = f"{current_app}{Fore.LIGHTYELLOW_EX}|>{user_at_host} {at_directory}{Fore.LIGHTYELLOW_EX}%{Fore.LIGHTWHITE_EX} "

		not_parsed:str = ""
		try:
			not_parsed = input(prompt)
		except KeyboardInterrupt:
			clear_console()
			print(f"Have you tried running the {Style.BRIGHT}exit{Style.RESET_ALL} command?")

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
