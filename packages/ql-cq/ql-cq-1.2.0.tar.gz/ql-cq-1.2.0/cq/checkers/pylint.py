from typing import IO, List, Optional, Tuple
import configparser
import os.path
import re
import subprocess
import tempfile

import cq.checker
import cq.utils


class PylintChecker(cq.checker.Checker):
	NAME = 'pylint'
	DESCRIPTION = 'Runs pylint on given path.'
	HELP_LINE = 'use `# pylint: disable=<violation name>` for disabling line check. For a list of violations, see `pylint --list-msgs`'

	@staticmethod
	def _get_pylint_rc_file(default_rcfile_path: str) -> Tuple[str, Optional[IO[str]]]:
		'''
		Try to find .pylintr rc in $PWD and if found merge it with the default one
		for usage with pylint checker
		'''
		override_rcfile_path = os.path.join(os.getcwd(), '.pylintrc')
		if os.path.exists(override_rcfile_path):
			config = configparser.ConfigParser()
			config.read(default_rcfile_path)
			config.read(override_rcfile_path)
			tmp_file = tempfile.NamedTemporaryFile(mode = 'w+')
			# a bug of tempfile typeshed https://github.com/python/typeshed/issues/434
			config.write(tmp_file)
			tmp_file.flush()
			return tmp_file.name, tmp_file

		return default_rcfile_path, None

	@staticmethod
	def _setup_pylint() -> Tuple[List[str], Optional[IO[str]]]:
		'''
		Setup pylint.

		:return path to the configuration file; if not None, this is file handle for temporarily created conf. file
		'''
		# --rcfile must be always last!
		pylint_options = ['--reports=no', '--score=no', '--rcfile']
		rcfile_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'pylintrc')
		effective_rcfile_path: str
		tmp_file: Optional[IO[str]]
		effective_rcfile_path, tmp_file = PylintChecker._get_pylint_rc_file(rcfile_path)
		pylint_options.append(effective_rcfile_path)

		return pylint_options, tmp_file

	@staticmethod
	def _cleanse_packages(package_list: List[str]) -> List[str]:
		'''
		Remove packages from list, that are childs of each other.
		'''
		modules: List[str] = []
		for module in package_list:
			for added_module in modules:
				# we should not add module that is subpath of already added module
				# except ending with .py (so tests without __init__.py are also included)
				if module.startswith(added_module) and module != added_module and not module.endswith('.py'):
					break
			else:
				modules.append(module)
		return modules

	@staticmethod
	def _process_line(line: str) -> Tuple[Optional[str], Optional[int], str, bool]:
		'''
		Process single output line.

		:param line: Line to parse.
		:return: Parsed output in Tuple[file name, line number, message, is_error]
		'''
		if not line:
			return None, None, '', False

		if line.startswith('************* '):
			return None, None, '', False

		try:
			file, linenum, *msg = line.split(':')
		except ValueError:
			return None, None, line, False

		if not msg:
			return None, None, line, False

		message = ':'.join(msg).lstrip()

		is_error = True
		if re.search(r'\[[CRI]{1}\d{4}\([-\w]+\).*\]', message):
			is_error = False

		try:
			return file, int(linenum), message, is_error
		except ValueError:  # int conversion failed
			return None, None, line, False

	def run(self, modules: List[str]) -> cq.checker.CheckerResult:
		packages_to_cleanse = list(
			filter(lambda module: not module.endswith('fabfile.py'), cq.utils.get_path_generator(modules))
		)

		# remove packages, that are childs of other
		pylint_modules_to_check = PylintChecker._cleanse_packages(packages_to_cleanse)

		pylint_options, tmp_file = PylintChecker._setup_pylint()

		# redirect stderr to /dev/null because it contains line: Using config file .pylintrc
		stdout, pylint_return_code = cq.utils.run_external_checker(
			'pylint',
			pylint_options + pylint_modules_to_check,
			stderr = subprocess.DEVNULL,
		)

		if tmp_file:
			tmp_file.close()

		# Pylint should leave with following status code:
		# 0 if everything went fine
		# 1 if a fatal message was issued
		# 2 if an error message was issued
		# 4 if a warning message was issued
		# 8 if a refactor message was issued
		# 16 if a convention message was issued
		# 32 on usage error
		# status 1 to 16 will be bit-ORed so you can know which different
		# categories has been issued by analysing pylint output status code

		return_code = 0
		if pylint_return_code & 4 or pylint_return_code & 2 or pylint_return_code & 1:
			# Warning, error or fatal message occured
			return_code = 1
		elif pylint_return_code == 32:
			# PyLint usage error
			return_code = 2

		output: List[cq.checker.ResultLine] = []

		for line in stdout.split('\n'):
			file, linenum, message, is_error = PylintChecker._process_line(line)

			if not message:
				continue

			output.append(cq.checker.ResultLine(file = file, line = linenum, message = message, is_error = is_error))

		return cq.checker.CheckerResult(
			checker_name = self.NAME,
			help_line = self.HELP_LINE,
			return_code = return_code,
			output = output,
		)
