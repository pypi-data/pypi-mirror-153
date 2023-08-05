from typing import List

import cq.fixer
import cq.utils


class OrangeFixer(cq.fixer.Fixer):
	NAME = 'orange'
	DESCRIPTION = 'Formats code with the `orange` code style.'

	def run(self, modules: List[str]) -> int:
		return cq.utils.run_external_fixer('orange', modules)
