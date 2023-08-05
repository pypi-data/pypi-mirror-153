from typing import List, Optional

import cq.checker
import cq.utils


class MypyChecker(cq.checker.Checker):
	NAME = 'mypy'
	DESCRIPTION = 'Run mypy on given modules.'
	HELP_LINE = 'use `# type: ignore` for disabling mypy on particular line'

	def run(self, modules: List[str]) -> cq.checker.CheckerResult:
		options = [
			'--no-error-summary',
			'--show-error-codes',
		]
		stdout, return_code = cq.utils.run_external_checker('mypy', options + modules)

		output: List[cq.checker.ResultLine] = []

		for output_line in stdout.split('\n'):
			if not output_line:
				continue

			try:
				file, line, *msg = output_line.split(':')
			except ValueError:
				output.append(cq.checker.ResultLine(file = None, line = None, message = output_line, is_error = True))

				continue

			line_number: Optional[int]
			try:
				line_number = int(line)
			except ValueError:
				line_number = None

			output.append(
				cq.checker.ResultLine(
					file = None if line_number is None else file,
					line = line_number,
					message = output_line if line_number is None else ':'.join(msg).lstrip(),
					is_error = True,
				)
			)

		return cq.checker.CheckerResult(
			checker_name = self.NAME,
			help_line = self.HELP_LINE,
			return_code = return_code,
			output = output,
		)
