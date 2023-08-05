from typing import List

import isort

import cq.checkers.isort_config
import cq.fixer
import cq.utils


class IsortFixer(cq.fixer.Fixer):
	NAME = 'isort'
	DESCRIPTION = 'Sorts imports according to the code style.'

	def run(self, modules: List[str]) -> int:
		for python_file in cq.utils.get_all_python_files(modules):
			isort.file(python_file, config = cq.checkers.isort_config.Config)
		return 0
