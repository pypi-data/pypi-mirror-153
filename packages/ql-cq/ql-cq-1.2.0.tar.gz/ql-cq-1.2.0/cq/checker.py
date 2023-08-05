from typing import List, NamedTuple, Optional
import abc


class ResultLine(NamedTuple):
	file: Optional[str]
	line: Optional[int]
	message: str
	is_error: bool


class CheckerResult(NamedTuple):
	checker_name: str
	help_line: Optional[str]
	return_code: int
	output: List[ResultLine]


class Checker(abc.ABC):
	NAME: str
	DESCRIPTION: str

	@abc.abstractmethod
	def run(self, modules: List[str]) -> CheckerResult:
		pass
