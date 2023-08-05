from typing import IO, Any, Iterable, Iterator, List, Tuple, Union
import os
import pathlib
import subprocess


def run_external_checker(
	cmd: str,
	options: List[str],
	stderr: Union[None, int, IO[Any]] = subprocess.STDOUT,
) -> Tuple[str, int]:
	'''
	Run cmd in subprocess, sanitize stdout
	'''
	p = subprocess.Popen([cmd] + options, stdout = subprocess.PIPE, stderr = stderr)

	stdout: bytes
	stdout, _ = p.communicate()

	return stdout.decode('utf-8').strip(), p.returncode


def run_external_fixer(
	cmd: str,
	options: List[str],
) -> int:
	'''
	Run cmd in subprocess, return exit code
	'''
	try:
		subprocess.run([cmd] + options, check = True)
	except subprocess.CalledProcessError:
		return 1
	else:
		return 0


def _is_any_path_part_hidden(path: str) -> bool:
	return any(part.startswith('.') and part not in {'.', '..'} for part in pathlib.Path(path).parts)


def get_path_generator(modules: Iterable[str], ignore_hidden: bool = True) -> Iterator[str]:
	'''
	Try to find any python file for pylint
	If path is already a python file or module continue
	Else, if directory, try to find any *.py file in the directory
	Continue recursively for all subdirectories
	'''
	for module in modules:
		if not (ignore_hidden and _is_any_path_part_hidden(module)):
			if module.endswith('.py'):
				yield module
			elif os.path.isdir(module):
				if os.path.exists(os.path.join(module, '__init__.py')):
					yield module
				else:
					yield from map(str, pathlib.Path(module).glob('*.py'))
				subdirs = [
					os.path.join(module, path)
					for path in os.listdir(module)
					if os.path.isdir(os.path.join(module, path))
				]
				if subdirs:
					yield from get_path_generator(subdirs)


def get_all_python_files(modules: Iterable[str], ignore_hidden: bool = True) -> Iterator[str]:
	for module in modules:
		if not (ignore_hidden and _is_any_path_part_hidden(module)):
			if os.path.isfile(module) and module.endswith('.py'):
				yield module
			elif os.path.isdir(module):
				for dirpath, _, filenames in os.walk(module):
					for file in filenames:
						path = os.path.join(dirpath, file)
						if not (ignore_hidden and _is_any_path_part_hidden(path)) and file.endswith('.py'):
							yield path
