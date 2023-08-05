from typing import Any, Dict, List, Tuple, Union, cast
import distutils.core  # pylint: disable = no-name-in-module, import-error, deprecated-module
import os

import pkg_resources
import requirements

import cq.checker
import cq.utils


try:
	# To allow working `cq` with multiple versions of setuptools we need
	# to try import from extern package (which works for versions
	# > 20.0.0 but not >34.0.0,<36.0.0, if it is not working we import
	# another Version source code that worked in <39.0.0

	import pkg_resources.extern.packaging.version

	Version = Union[
		pkg_resources.extern.packaging.version.Version,
		pkg_resources.extern.packaging.version.LegacyVersion,
	]
	BASE_VERSION = pkg_resources.extern.packaging.version.Version
except ImportError:
	Version = Union[  # type: ignore
		pkg_resources.SetuptoolsVersion,  # type: ignore
		pkg_resources.SetuptoolsLegacyVersion,  # type: ignore
	]
	BASE_VERSION = pkg_resources._SetuptoolsVersionMixin  # type: ignore # pylint: disable = protected-access


class RequirementsvalidatorChecker(cq.checker.Checker):
	NAME = 'requirements-validator'
	DESCRIPTION = 'Validation of requirements.txt file (see https://pip.pypa.io/en/latest/reference/pip_check/)'

	def run(self, modules: List[str]) -> cq.checker.CheckerResult:
		output: List[cq.checker.ResultLine] = []
		message, return_code = cq.utils.run_external_checker('pip', ['check'])

		if return_code:
			output.append(
				cq.checker.ResultLine(file = 'requirements.txt', line = None, message = message, is_error = True)
			)

		return cq.checker.CheckerResult(
			checker_name = self.NAME,
			help_line = None,
			return_code = return_code,
			output = output,
		)


class MinVersion(BASE_VERSION):  # type: ignore
	def __init__(self) -> None:
		self._key = self

	def __str__(self) -> str:
		return 'MIN'

	def __repr__(self) -> str:
		return "<Version('MIN')>"

	def __lt__(self, other: Any) -> bool:
		return True

	def __le__(self, other: Any) -> bool:
		return True

	def __gt__(self, other: Any) -> bool:
		return False

	def __ge__(self, other: Any) -> bool:
		return False

	def __eq__(self, other: Any) -> bool:
		return isinstance(other, self.__class__)

	def __ne__(self, other: Any) -> bool:
		return not self.__eq__(other)


class MaxVersion(BASE_VERSION):  # type: ignore
	def __init__(self) -> None:
		self._key = self

	def __str__(self) -> str:
		return 'MAX'

	def __repr__(self) -> str:
		return "<Version('MAX')>"

	def __lt__(self, other: Any) -> bool:
		return False

	def __le__(self, other: Any) -> bool:
		return False

	def __gt__(self, other: Any) -> bool:
		return True

	def __ge__(self, other: Any) -> bool:
		return True

	def __eq__(self, other: Any) -> bool:
		return isinstance(other, self.__class__)

	def __ne__(self, other: Any) -> bool:
		return not self.__eq__(other)


MIN_VERSION = MinVersion()
MAX_VERSION = MaxVersion()


class VersionRange:
	def __init__(
		self,
		lower: Version,
		upper: Version,
		lower_inclusive: bool = True,
		upper_inclusive: bool = False,
	) -> None:
		self.lower = lower
		self.upper = upper
		self.lower_inclusive = lower_inclusive
		self.upper_inclusive = upper_inclusive

	@classmethod
	def from_specs(cls, specs: List[Tuple[str, str]]) -> 'VersionRange':
		lower = MIN_VERSION  # type: Version
		upper = MAX_VERSION  # type: Version
		lower_inclusive = True
		upper_inclusive = True
		for sign, version_str in specs:
			if sign == '==':
				lower = pkg_resources.parse_version(version_str)
				upper = pkg_resources.parse_version(version_str)
			elif sign.startswith('>'):
				lower = pkg_resources.parse_version(version_str)
				lower_inclusive = sign.endswith('=')
			elif sign.startswith('<'):
				upper = pkg_resources.parse_version(version_str)
				upper_inclusive = sign.endswith('=')
		return cls(lower, upper, lower_inclusive, upper_inclusive)

	def __str__(self) -> str:
		if self.lower == self.upper:
			return f'=={self.lower}'
		first_sign = '>=' if self.lower_inclusive else '>'
		second_sign = '<=' if self.upper_inclusive else '<'
		return f'{first_sign}{self.lower},{second_sign}{self.upper}'

	def issubset(self, other: 'VersionRange') -> bool:
		if not isinstance(other, VersionRange):
			return NotImplemented

		if other.lower_inclusive or not self.lower_inclusive:
			lower_condition = other.lower <= self.lower
		else:
			lower_condition = other.lower < self.lower
		if other.upper_inclusive or not self.upper_inclusive:
			upper_condition = other.upper >= self.upper
		else:
			upper_condition = other.upper > self.upper

		# check that we overlap
		overlap_condition = other.upper >= self.lower and other.lower <= self.upper
		# mypy considers the condition as Any instead of bool
		return cast(bool, lower_condition and upper_condition and overlap_condition)


class RequirementsSetupCompatiblityChecker(cq.checker.Checker):
	NAME = 'requirements_setup_compatibility'
	DESCRIPTION = 'Validation of version compatibility in files setup.py and requirements.txt'

	SETUP_FILE = './setup.py'
	REQUIREMENTS_FILE = './requirements.txt'

	@staticmethod
	def _create_requirements_dict(source: str) -> Dict[str, List[Tuple[str, str]]]:
		result = {}
		for req in requirements.parse(source):
			result[req.name] = req.specs
		return result

	def _check_requirements_setup_compatibility(
		self,
		requirements_contents: str,
		setup_contents: str,
	) -> List[cq.checker.ResultLine]:
		'''
		Returns output messages for requirements that
		1) are present in requirements.txt and missing in setup.py
		2) their range in requirements.txt is not subset of range in setup.py
		'''
		output: List[cq.checker.ResultLine] = []
		requirements_dict = self._create_requirements_dict(requirements_contents)
		setup_dict = self._create_requirements_dict(setup_contents)

		for name, specs in requirements_dict.items():
			if name not in setup_dict:
				output.append(
					cq.checker.ResultLine(
						file = 'setup.py',
						line = None,
						message = f"setup.py: does not contain requirement '{name}' that is in requirements.txt",
						is_error = True,
					)
				)
			else:
				requirements_version_range = VersionRange.from_specs(specs)
				setup_version_range = VersionRange.from_specs(setup_dict[name])

				if not requirements_version_range.issubset(setup_version_range):
					output.append(
						cq.checker.ResultLine(
							file = 'setup.py',
							line = None,
							message = (
								f"setup.py: requirement '{name}' version in requirements.txt "
								f'({requirements_version_range}) does not lie in version '
								f'of setup.py ({setup_version_range})'
							),
							is_error = True,
						)
					)
		return output

	def _get_setup_py_requirements(self) -> str:
		distribution = distutils.core.run_setup(self.SETUP_FILE)
		# mypy doesn't know that distribution may contain install_requires
		setup_requirements = list(distribution.install_requires)  # type: ignore
		# get all requirements in extras_require
		# mypy complains that disribution does not have extras_require
		extras_require = distribution.extras_require if distribution.extras_require is not None else {}  # type: ignore
		setup_requirements += [
			requirement
			for extra_requirements in extras_require.values()
			for requirement in extra_requirements
		]
		return '\n'.join(setup_requirements)

	def _get_requirements_txt_requirements(self) -> str:
		with open(self.REQUIREMENTS_FILE, 'r', encoding = 'utf-8') as f:
			return f.read()

	def run(self, modules: List[str]) -> cq.checker.CheckerResult:  # pylint: disable = unused-argument
		# setup.py may miss for applications
		if not os.path.exists(self.SETUP_FILE):
			return cq.checker.CheckerResult(checker_name = self.NAME, help_line = None, return_code = 0, output = [])
		# warn if requirements file is missing
		if not os.path.exists(self.REQUIREMENTS_FILE):
			return cq.checker.CheckerResult(
				checker_name = self.NAME,
				help_line = None,
				return_code = 0,
				output = [
					cq.checker.ResultLine(
						file = self.REQUIREMENTS_FILE,
						line = None,
						message = f'Missing file {self.REQUIREMENTS_FILE}',
						is_error = False,
					)
				],
			)

		setup = self._get_setup_py_requirements()
		requirements = self._get_requirements_txt_requirements()

		output = self._check_requirements_setup_compatibility(requirements, setup)

		return cq.checker.CheckerResult(
			checker_name = self.NAME,
			help_line = None,
			return_code = 0 if not output else 1,
			output = output,
		)
