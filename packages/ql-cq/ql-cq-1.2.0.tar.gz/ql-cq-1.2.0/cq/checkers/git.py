from typing import List
import os
import re

import cq.checker
import cq.utils


class BranchNameChecker(cq.checker.Checker):
	NAME = 'branch_name_check'
	DESCRIPTION = 'Checks, whether current branch name comply with Quantlane standards'

	def run(self, modules: List[str]) -> cq.checker.CheckerResult:
		result = cq.checker.CheckerResult(checker_name = self.NAME, help_line = None, return_code = 0, output = [])

		try:
			branch_name = os.environ['CI_COMMIT_REF_NAME']
		except KeyError:
			branch_name, return_code = cq.utils.run_external_checker('git', ['symbolic-ref', 'HEAD', '--short'])

			if return_code != 0:
				return result

		if re.match('master|main|feature/.*|release/.*|fix/.*|version/.*', branch_name):
			return result

		return cq.checker.CheckerResult(
			checker_name = self.NAME,
			help_line = None,
			return_code = 1,
			output = [
				cq.checker.ResultLine(
					file = None,
					line = None,
					message = (
						f"Branch '{branch_name}' doesn't comply with Quantlane standarts. "
						f'It should be in form of: master, feature/.*, release/.*, fix/.*, version/.*'
					),
					is_error = True,
				)
			],
		)
