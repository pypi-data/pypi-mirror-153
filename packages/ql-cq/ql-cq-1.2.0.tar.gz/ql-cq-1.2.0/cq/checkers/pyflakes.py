from typing import List, Optional

import cq.checker
import cq.utils


class PyflakesExtChecker(cq.checker.Checker):
	NAME = 'pyflakes-ext'
	DESCRIPTION = 'Our pyflakes version runner (see https://github.com/qntln/pyflakes-ext)'
	HELP_LINE = 'use `# NOQA` comment for disabling pyflakes on particular line'

	def run(self, modules: List[str]) -> cq.checker.CheckerResult:
		return_code: int = 0
		output: List[cq.checker.ResultLine] = []

		errors, subprocess_return_code = cq.utils.run_external_checker(
			'pyflakes-ext',
			list(cq.utils.get_path_generator(modules)),
		)

		if subprocess_return_code != 0:
			for line in errors.split('\n'):
				if not line:
					continue

				try:
					file_name, line_number, *error_message = line.split(':')
				except ValueError:
					output.append(cq.checker.ResultLine(file = None, line = None, message = line, is_error = True))

					continue

				linenum: Optional[int]
				try:
					linenum = int(line_number)
				except ValueError:
					output.append(cq.checker.ResultLine(file = None, line = None, message = line, is_error = True))

					continue

				output.append(
					cq.checker.ResultLine(
						file = file_name,
						line = linenum,
						message = ':'.join(error_message).lstrip(),
						is_error = True,
					)
				)

			return_code = max(return_code, subprocess_return_code)

		return cq.checker.CheckerResult(
			checker_name = self.NAME,
			help_line = self.HELP_LINE,
			return_code = return_code,
			output = output,
		)
