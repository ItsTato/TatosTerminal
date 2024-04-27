from .Errors import RequiredPackageIsNotInstalled

def Check(package_name) -> None:
	try:
		exec(f"import {package_name}")
	except ImportError:
		raise RequiredPackageIsNotInstalled(f"Package {package_name} is missing, please install it!")