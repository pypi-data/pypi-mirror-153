from typing import List

import cq.checker
import cq.utils


class OrangeChecker(cq.checker.Checker):
	NAME = 'orange'
	HELP_LINE = 'run `cq --fix` and make sure that you have pre-commit hooks installed with `pre-commit install`'
	DESCRIPTION = 'Checks whether code complies with the `orange` code style.'
	ORANGE_NOT_INSTALLED = "It looks like you don't have `orange` in this project."

	def run(self, modules: List[str]) -> cq.checker.CheckerResult:
		try:
			orange_output, return_code = cq.utils.run_external_checker('orange', ['--check'] + modules)
		except FileNotFoundError:
			# This means that orange is not available.
			# Projects is probably not yet formatted with orange.
			# We should ignore it for now.
			return cq.checker.CheckerResult(
				checker_name = self.NAME,
				help_line = self.HELP_LINE,
				return_code = 0,
				output = [
					cq.checker.ResultLine(
						file = None,
						line = None,
						message = self.ORANGE_NOT_INSTALLED,
						is_error = False,
					),
				],
			)

		# orange can exit with 1 or 123 if something fails
		if return_code == 0:
			return cq.checker.CheckerResult(
				checker_name = self.NAME,
				help_line = self.HELP_LINE,
				return_code = 0,
				output = [],
			)
		return cq.checker.CheckerResult(
			checker_name = self.NAME,
			help_line = self.HELP_LINE,
			return_code = 1,
			output = [
				cq.checker.ResultLine(
					file = None,
					line = None,
					# Sample output: "1 file would be reformatted."
					message = orange_output.split('\n')[-1],
					is_error = True,
				),
			],
		)
