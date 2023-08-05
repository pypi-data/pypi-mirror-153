from typing import List
import os.path
import re

import cq.checker
import cq.utils


class SetupChecker(cq.checker.Checker):
	NAME = 'setup_check'
	DESCRIPTION = (
		'Checks setup.py validity (see https://docs.python.org/3/distutils/examples.html#checking-a-package)'
	)

	def run(self, modules: List[str]) -> cq.checker.CheckerResult:  # pylint: disable = unused-argument
		if not os.path.exists('setup.py'):
			return cq.checker.CheckerResult(checker_name = self.NAME, help_line = None, return_code = 0, output = [])

		stdout, _ = cq.utils.run_external_checker('python3', ['setup.py', 'check', '--metadata', '--strict'])
		output = re.sub(r'running check', '', stdout)

		output_object = cq.checker.ResultLine(file = 'setup.py', line = None, message = output, is_error = True)

		return cq.checker.CheckerResult(
			checker_name = self.NAME,
			help_line = None,
			return_code = 0 if not output else 1,
			output = [] if not output else [output_object],
		)
