from typing import Any, Callable, Iterable, Iterator, List, Match, Pattern, Tuple, cast
import pathlib
import re

import toolz

import cq.checker
import cq.utils


MessageGenerator = Callable[[str, Match], str]
Condition = Callable[[str, Match], bool]
Rule = Tuple[Pattern, MessageGenerator, Condition]


def compile_rule_specs(*rule_specs: Tuple[str, int, MessageGenerator, Condition]) -> List[Rule]:
	return [
		(re.compile(pattern, flags = flags), message_generator, condition)
		for (pattern, flags, message_generator, condition) in rule_specs
	]


def check_file_lines(preprocessor: Callable[[str], str], rules: List[Rule], file: pathlib.Path) -> str:
	output: List[str] = []
	with file.open() as f:
		content = f.read()
		preprocessed = preprocessor(content)
		for i, (line, original_line) in enumerate(zip(preprocessed.split('\n'), content.split('\n'))):
			for complaint in check_line(line, original_line, rules):
				output.append('{file}:{line_no}: {complaint}'.format(file = file, line_no = i + 1, complaint = complaint))
	return '\n'.join(output)


def check_line(line: str, original_line: str, rules: Iterable[Rule]) -> Iterator[str]:
	for pattern, message_generator, condition in rules:
		match = pattern.search(line)
		if match is not None:
			if condition(original_line, match):
				yield message_generator(line, match)


def _const(msg: str) -> Callable[[Any, Any], str]:
	return lambda _, __: msg


class GrammarNaziChecker(cq.checker.Checker):
	NAME = 'grammar_nazi'
	DESCRIPTION = 'Checks grammar rules in files'
	HELP_LINE = (
		'use `# grammar_chcker: disable=<violation name>` for disabling line check. '
		'Violations: 3rd-person-singular, happend, it-self, insturment, splitted.'  # grammar_checker: disable = happend, grammar_checker: disable = insturment, grammar_checker: disable = splitted
	)
	RULES = compile_rule_specs(
		(
			r'(does|may|might|can) not exists',
			re.IGNORECASE,
			lambda _, match: (
				'Use "{verb} not exist", not "{verb} not exists". '
				'The "{verb}" verb already is in third person singular.'
			).format(verb = match.group(1)),
			lambda original_line, _: re.search(r'grammar_checker:\s*disable\s*=\s*3rd-person-singular', original_line)
			is None,
		),
		(
			r'happend',  # grammar_checker: disable = happend
			re.IGNORECASE,
			_const(
				'"happend" is not a word. You either mean "happen" (present tense) or "happened" (past tense).'  # grammar_checker: disable = happend
			),
			lambda original_line, _: re.search(
				r'grammar_checker:\s*disable\s*=\s*happend',  # grammar_checker: disable = happend
				original_line,
			)
			is None,
		),
		(
			r'\bit self',
			re.IGNORECASE,
			_const('"itself" is one word.'),
			lambda original_line, _: re.search(r'grammar_checker:\s*disable\s*=\s*it-self', original_line) is None,
		),
		(
			r'insturment',  # grammar_checker: disable = insturment
			re.IGNORECASE,
			_const('"insturment", did you mean "instrument"'),  # grammar_checker: disable = insturment
			lambda original_line, _: re.search(
				r'grammar_checker:\s*disable\s*=\s*insturment',  # grammar_checker: disable = insturment
				original_line,
			)
			is None,
		),
		(
			r'splitted',  # grammar_checker: disable = splitted
			re.IGNORECASE,
			_const('The past tense of "to split" is "split", not "splitted".'),  # grammar_checker: disable = splitted
			lambda original_line, _: re.search(
				r'grammar_checker:\s*disable\s*=\s*splitted',  # grammar_checker: disable = splitted
				original_line,
			)
			is None,
		),
	)

	def run(self, modules: List[str]) -> cq.checker.CheckerResult:
		output: List[cq.checker.ResultLine] = []

		for file in cq.utils.get_all_python_files(modules):
			result = check_file_lines(preprocessor = lambda x: x, rules = self.RULES, file = pathlib.Path(file))

			for line in result.split('\n'):
				if not line:
					continue

				try:
					file, linenum, *msg = line.split(':')
				except ValueError:  # fallback solution, so it won't crash cq
					output.append(cq.checker.ResultLine(file = None, line = None, message = line, is_error = True))

					continue

				output.append(
					cq.checker.ResultLine(
						file = file,
						line = int(linenum),
						message = ':'.join(msg).lstrip(),
						is_error = True,
					)
				)

		return cq.checker.CheckerResult(
			checker_name = self.NAME,
			help_line = self.HELP_LINE,
			return_code = 0 if not output else 1,
			output = output,
		)


# This regexp is not perfect but we don't want to go crazy from this, do we.
# https://stackoverflow.com/a/14366904
_STRING_PATTERN = re.compile(r'''(\"\"\"|\'\'\'|\"|\')(((?<!\\)\\\1|.)*?)\1''', flags = re.DOTALL)
_COMMENT_PATTERN = re.compile(r'\#.*')


def clobber_string_literals(source: str) -> str:
	'''
	Hide string literal content by overwriting it with '.' characters.
	'''
	return _STRING_PATTERN.sub(_string_literal_cloberrer, source)


def _string_literal_cloberrer(match: Match) -> str:
	delimiter = match.group(1)
	content = match.group(2)
	clobbered = re.sub(r'\S', '.', content)
	# mypy considers the variables as Any
	return cast(str, delimiter + clobbered + delimiter)


def clobber_comments(source: str) -> str:
	'''
	Hide comment content by overwriting it with '#' characters.
	Make sure we don't identify '#' inside string literals as comments.

	>>> clobber_comments('x = 1 # 123')
	'x = 1 #####'
	>>> clobber_comments('x = "#"')
	'x = "#"'
	>>> clobber_comments('x = "#" + "x # y"  # comment')
	'x = "#" + "x # y"  #########'
	'''
	lines = []
	for line in source.split('\n'):
		index = line.find('#')
		while index > -1:
			for string_literal in _STRING_PATTERN.finditer(line):
				start, stop = string_literal.span()
				if start < index < stop:
					# The '#' character is inside a string literal. Don't clobber it and go looking for the next '#' on this line.
					index = line.find('#', index + 1)
					break
			else:
				# The '#' character is not inside any string literal => clobber the rest of the line.
				comment = line[index:]
				line = line[:index] + '#' * len(comment)
				break

		lines.append(line)

	return '\n'.join(lines)


def _match_surrounding(line: str, match: Match) -> str:
	return line[max(0, match.start() - 20) : min(len(line), match.end() + 20)]


class DumbStyleChecker(cq.checker.Checker):
	NAME = 'dumb_style_checker'
	DESCRIPTION = 'Checks some basic Pyhon mistakes'

	# '=' must come after '==' so that '==' matches first!
	_EQUALS_OPERATORS = ('==', '!=', '<=', '>=', '-=', '+=', '*=', '/=', '|=', '&=', '^=', ':=', '=')

	RULES = compile_rule_specs(
		(
			'((?<![ {other_chars}\t])({operators}))|(({operators})(?=[^ {other_chars}]))'.format(
				other_chars = ''.join({re.escape(op[0]) for op in _EQUALS_OPERATORS}),
				operators = '|'.join(re.escape(op) for op in _EQUALS_OPERATORS),
			),
			0,
			lambda line, match: 'Put exactly one space before and after `{}`  [... {} ...].'.format(
				match.group(0),
				_match_surrounding(line, match),
			),
			lambda *_: True,
		),
		(
			'^.*(([a-z]+)(?<!oauth)(2|4)[a-z]+)',
			re.IGNORECASE,
			lambda line, match: 'Do not spell `{}` as the digit `{}`. [... {} ...]'.format(
				'to' if match.group(3) == '2' else 'for',
				match.group(3),
				_match_surrounding(line, match),
			),
			lambda original_line, _: re.search(r'dumb_style_checker:\s*disable\s*=\s*word_as_a_digit', original_line)
			is None,
		),
		(
			r'\bprint\b',
			0,
			lambda line, match: (
				'It seems that you have forgotten about a print statement. '
				'If this is intentional, disable this check by # dumb_style_checker:disable = print-statement'
			),
			lambda original_line, _: re.search(r'dumb_style_checker:\s*disable\s*=\s*print-statement', original_line)
			is None,
		),
	)

	def run(self, modules: List[str]) -> cq.checker.CheckerResult:
		output: List[cq.checker.ResultLine] = []

		for file in cq.utils.get_all_python_files(modules):
			result = check_file_lines(
				preprocessor = toolz.compose(clobber_string_literals, clobber_comments),
				rules = self.RULES,
				file = pathlib.Path(file),
			)

			for line in result.split('\n'):
				if not line:
					continue

				try:
					file, linenum, *msg = line.split(':')
				except ValueError:
					output.append(cq.checker.ResultLine(file = None, line = None, message = line, is_error = True))

					continue

				output.append(
					cq.checker.ResultLine(
						file = file,
						line = int(linenum),
						message = ':'.join(msg).lstrip(),
						is_error = True,
					)
				)

		return cq.checker.CheckerResult(
			checker_name = self.NAME,
			help_line = None,
			return_code = 0 if not output else 1,
			output = output,
		)
