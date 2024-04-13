
if __name__ != "__main__":
    exit(0)

# Tester, makes sure packages are installed,
# so I can freely import anything without using
# a requirements.txt file.

from TatosUtils import SafeImport
SafeImport("colorama").add()
SafeImport("tqdm").add()

from os import name, path, getcwd, getlogin, listdir
from platform import node
from random import choice
from colorama import Fore, Back, Style, init
from tqdm import tqdm
init(autoreset=True)

running:bool = True
farewells:list = [
    "Goodbye!",
    "Farewell!",
    "Code you later!",
    "¡Adios, mi amigo!",
    "Oh okay :<",
    "Shut down the mainframe!"
]
current_dir:str = path.abspath(getcwd()).replace("\\","/")

parent_dir:str = path.abspath(__file__).replace("main.py","")
scripts:list = listdir(f"{parent_dir}scripts")

#if "__pycache__" in scripts:
#    scripts.remove("__pycache__")

#for script in scripts:
#    if f"{script[0]}{script[1]}" == "__":
#        scripts.remove(script)

def parse_input(un_parsed:str) -> list:
    return un_parsed.split(";;")

while running:
    current_app:str = f"{Fore.LIGHTMAGENTA_EX}TT{Fore.LIGHTYELLOW_EX}-{Fore.LIGHTMAGENTA_EX}{name}{Fore.LIGHTYELLOW_EX} |> "
    user_at_host:str = f"{Fore.LIGHTGREEN_EX}{getlogin()}{Fore.LIGHTYELLOW_EX}@{Fore.LIGHTGREEN_EX}{node()}"
    if name in ["nt"]:
        temp:str = current_dir[1:]
        drive:str = current_dir[0]
        temp = temp.replace(":",f"{Fore.LIGHTCYAN_EX} {drive}~{Fore.LIGHTYELLOW_EX} ")
        at_directory:str = f"{Fore.LIGHTGREEN_EX}{temp}"
    else:
        temp:str = current_dir
        at_directory:str = f"{Fore.LIGHTYELLOW_EX}~{Fore.LIGHTGREEN_EX}{temp}"
    prompt:str = f"{current_app}{user_at_host}{at_directory}\n{Fore.LIGHTWHITE_EX}% "
    try:
        not_parsed:str = input(prompt)
    except KeyboardInterrupt:
        running = False
        break
    parsed:list = parse_input(not_parsed)
    #if "cls" in parsed or "clear" in parsed:
    #    system("cls" if name in ["nt"] else "clear")
    for cmd in parsed:
        args:list = cmd.split(" ")
        cmdName:str = args[0]
        location:str = ""
        exec(f"""
from scripts.{location} import {cmdName}
val = {cmdName}.run()
        """)

print(f"\n\n{choice(farewells)}")
exit(0)