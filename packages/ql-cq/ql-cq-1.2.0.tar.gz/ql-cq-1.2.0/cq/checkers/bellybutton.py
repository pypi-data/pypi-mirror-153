from typing import List, Set
import os.path

import bellybutton.cli
import bellybutton.parsing

import cq.checker
import cq.utils


class BellybuttonChecker(cq.checker.Checker):
	NAME = 'bellybutton'
	DESCRIPTION = 'Launch Bellybutton linter on given modules.'
	HELP_LINE = 'use `# bb: ignore` for disabling bellybutton on particular line'

	def run(self, modules: List[str]) -> cq.checker.CheckerResult:
		files: Set[str] = set()

		for file in cq.utils.get_all_python_files(modules):
			files.add(file)

		bellybutton_conf = os.path.join(os.path.abspath(os.path.dirname(__file__)), '.bellybutton.yml')
		with open(bellybutton_conf, 'r', encoding = 'utf-8') as f:
			rules = bellybutton.parsing.load_config(f)

		results = bellybutton.cli.linting_failures(files, rules)

		output: List[cq.checker.ResultLine] = []
		for result in results:
			output.append(
				cq.checker.ResultLine(
					file = result.path,
					line = result.lineno,
					message = result.rule.description,
					is_error = True,
				)
			)

		return cq.checker.CheckerResult(
			checker_name = self.NAME,
			help_line = self.HELP_LINE,
			return_code = 0 if not output else 1,
			output = output,
		)
