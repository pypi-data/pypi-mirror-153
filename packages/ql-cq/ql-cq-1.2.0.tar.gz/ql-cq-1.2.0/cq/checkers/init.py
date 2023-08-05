from typing import Iterator, List
import pathlib

import cq.checker


class InitChecker(cq.checker.Checker):
	NAME = 'init_checker'
	DESCRIPTION = 'Checks for `__init__.py` files in subdirectories containing `.py` files.'
	HELP_LINE = 'create `__init__.py` file in the particular directory'
	MESSAGE = 'Directory is missing `__init__.py` file.'

	def run(self, modules: List[str]) -> cq.checker.CheckerResult:
		missing_inits = list(
			result
			for module in modules
			if pathlib.Path(module).is_dir()
			for result in find_missing_inits(pathlib.Path(module))
		)
		output = [
			cq.checker.ResultLine(file = str(result), line = None, message = self.MESSAGE, is_error = False)
			for result in missing_inits
		]
		if output:
			header = '\n\nTo create missing __init__.py files, run:\n'
			cmd = f'touch {" ".join(str(path / "__init__.py") for path in missing_inits)}'
			output.append(
				cq.checker.ResultLine(file = None, line = None, message = f'{header}{cmd}', is_error = False)
			)
		return cq.checker.CheckerResult(
			checker_name = self.NAME,
			help_line = self.HELP_LINE,
			return_code = 0,
			output = output,
		)


def find_missing_inits(directory: pathlib.Path) -> Iterator[pathlib.Path]:
	'''
	Recursively yield subdirectories that contain *.py files but are missing __init__.py.
	Ignores hidden directories.
	'''
	for subdir in directory.iterdir():
		if subdir.is_dir() and not subdir.name.startswith('.'):
			if any(subdir.glob('*.py')) and not (subdir / '__init__.py').exists():
				yield subdir
			yield from find_missing_inits(subdir)
