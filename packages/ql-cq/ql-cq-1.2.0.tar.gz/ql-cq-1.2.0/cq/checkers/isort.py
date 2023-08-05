from typing import List
import contextlib
import os

import isort

import cq.checker
import cq.checkers.isort_config
import cq.utils


class IsortChecker(cq.checker.Checker):
	NAME = 'isort'
	HELP_LINE = 'Run `cq --fix`'
	DESCRIPTION = 'Checks whether imports are sorted according to the code style.'

	def run(self, modules: List[str]) -> cq.checker.CheckerResult:
		# This redirects all stderr to /dev/null.
		# Because of multithreading, all checkers running in parallel will have stderr redirected as well.
		# This doesn't cause problems now (while checkers use stdout) but might in the future.
		with open(os.devnull, 'w', encoding = 'utf-8') as devnull, contextlib.redirect_stderr(devnull):
			results = {
				python_file: isort.check_file(python_file, config = cq.checkers.isort_config.Config)
				for python_file in cq.utils.get_all_python_files(modules)
			}

		return cq.checker.CheckerResult(
			checker_name = self.NAME,
			help_line = self.HELP_LINE,
			return_code = 0,
			output = [
				cq.checker.ResultLine(
					file = filename,
					line = None,
					message = 'Imports are incorrectly sorted and/or formatted.',
					is_error = False,
				)
				for filename, result in results.items()
				if result is False
			],
		)
