from typing import List
import abc


class Fixer(abc.ABC):
	NAME: str
	DESCRIPTION: str

	@abc.abstractmethod
	def run(self, modules: List[str]) -> int:
		pass
