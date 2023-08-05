from typing import List, NamedTuple
import json

import cq.checker
import cq.utils


SAFETY_CONNECTION_WARNING = 'warning: safety checker cannot download vulnerability database, skipping'
SAFETY_OTHER_ERROR = 'safety checker encountered an error'
SAFETY_DECODE_ERROR = 'error when decoding safety checker output'


class SafetyReportEntry(NamedTuple):
	package: str
	affected: str
	installed: str
	advisory: str
	id: str
	cvssv2: str
	cvssv3: str


class SafetyChecker(cq.checker.Checker):
	NAME = 'safety'
	DESCRIPTION = 'Checks installed dependencies for known security vulnerabilities.'

	def run(self, modules: List[str]) -> cq.checker.CheckerResult:
		stdout, return_code = cq.utils.run_external_checker(self.NAME, ['check', '--json'])

		# 0 is returned when safety does not find a vulnerability
		# 255 is returned when safety finds a vulnerability
		# everything else should be considered as warning or error in cq
		if return_code not in (0, 255):
			if return_code == 1 and any(keyword in stdout for keyword in ('NewConnectionError', 'socket.gaierror')):
				# we never want to fail cq because of connection error of safety checker
				return_code = 0
				output = [
					cq.checker.ResultLine(
						file = None,
						line = None,
						message = SAFETY_CONNECTION_WARNING,
						is_error = False,
					)
				]
			else:
				# if the reason for safety checker error is not connection error, let it fail cq
				output = [
					cq.checker.ResultLine(
						file = None,
						line = None,
						message = SAFETY_OTHER_ERROR,
						is_error = True,
					)
				]
		else:
			try:
				output = [SafetyChecker.entry_to_result_line(output_entry) for output_entry in json.loads(stdout)]
			except (json.decoder.JSONDecodeError, TypeError):
				output = [
					cq.checker.ResultLine(
						file = None,
						line = None,
						message = SAFETY_DECODE_ERROR,
						is_error = True,
					)
				]

		return cq.checker.CheckerResult(
			checker_name = self.NAME,
			help_line = None,
			return_code = return_code,
			output = output,
		)

	@staticmethod
	def entry_to_result_line(output_entry: List[str]) -> cq.checker.ResultLine:
		safety_report_entry = SafetyReportEntry(*output_entry)

		return cq.checker.ResultLine(
			file = None,
			line = None,
			message = f'package: {safety_report_entry.package}, '
			f'affected: {safety_report_entry.affected}, '
			f'installed: {safety_report_entry.installed}',
			is_error = True,
		)
