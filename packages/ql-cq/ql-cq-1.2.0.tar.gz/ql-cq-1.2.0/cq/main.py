from typing import Any, Callable, Iterable, List, NamedTuple, Optional, Tuple
import concurrent.futures
import logging
import sys
import time

import click

import cq.checker
import cq.checkers.bellybutton
import cq.checkers.git
import cq.checkers.init
import cq.checkers.isort
import cq.checkers.mypy
import cq.checkers.orange
import cq.checkers.pyflakes
import cq.checkers.pylint
import cq.checkers.regex
import cq.checkers.requirements
import cq.checkers.safety
import cq.checkers.setup
import cq.fixer
import cq.fixers.isort_fixer
import cq.fixers.orange


checkers: List[cq.checker.Checker] = [
	cq.checkers.pylint.PylintChecker(),
	cq.checkers.mypy.MypyChecker(),
	cq.checkers.bellybutton.BellybuttonChecker(),
	cq.checkers.pyflakes.PyflakesExtChecker(),
	cq.checkers.regex.GrammarNaziChecker(),
	cq.checkers.regex.DumbStyleChecker(),
	cq.checkers.requirements.RequirementsSetupCompatiblityChecker(),
	cq.checkers.requirements.RequirementsvalidatorChecker(),
	cq.checkers.setup.SetupChecker(),
	cq.checkers.git.BranchNameChecker(),
	cq.checkers.init.InitChecker(),
	cq.checkers.orange.OrangeChecker(),
	cq.checkers.isort.IsortChecker(),
	cq.checkers.safety.SafetyChecker(),
]
fixers: List[cq.fixer.Fixer] = [
	cq.fixers.isort_fixer.IsortFixer(),
	cq.fixers.orange.OrangeFixer(),
]


CHECK_MARK = '\u2713'
FAIL_X = '\u2717'


def help_callback(ctx: click.Context, _param: Any, value: Any) -> None:
	if not value:
		return

	formatter = ctx.make_formatter()
	ctx.command.format_usage(ctx, formatter)
	formatter.write('\nAvailable Checkers:\n')
	for checker in checkers:
		formatter.write(' - {}: {}\n'.format(checker.NAME, checker.DESCRIPTION))
	formatter.write('\nAvailable Fixers:\n')
	for fixer in fixers:
		formatter.write(' - {}: {}\n'.format(fixer.NAME, fixer.DESCRIPTION))
	ctx.command.format_help_text(ctx, formatter)
	ctx.command.format_options(ctx, formatter)
	ctx.command.format_epilog(ctx, formatter)
	click.echo(formatter.getvalue())
	ctx.exit()


class ModuleTime(NamedTuple):
	name: str
	time: float


module_time_elapsed: List[ModuleTime] = []


def measure_time(
	logger: logging.Logger,
	module_name: str,
	runner: Callable[..., cq.checker.CheckerResult],
	*args: Any,
	**kwargs: Any,
) -> Callable[[], cq.checker.CheckerResult]:
	def wrapper() -> cq.checker.CheckerResult:
		logger.debug('starting module %s', module_name)
		time_started = time.monotonic()

		result = runner(*args, **kwargs)

		time_elapsed = time.monotonic() - time_started
		logger.debug('module %s ended; time elapsed %.3f s', module_name, time_elapsed)
		module_time_elapsed.append(ModuleTime(name = module_name, time = time_elapsed))

		return result

	return wrapper


def run_checkers(
	list_modules: List[str],
	disable: Iterable[str],
	logger: logging.Logger,
	debug: bool,
	show_warnings: bool,
	threads: Optional[int],
) -> int:
	if debug:
		logging.debug('cq started in debug mode')

	cq_started = time.monotonic()

	if debug:
		logging.debug('using %s threads', threads or 'maximum available')

	exit_code = 0
	with concurrent.futures.ThreadPoolExecutor(max_workers = threads) as executor:
		futures = []

		for checker in checkers:
			if checker.NAME in disable:
				if debug:
					logging.debug('module %s disabled -> skipping', checker.NAME)

				continue

			if debug:
				runner = measure_time(logger, checker.NAME, checker.run, list_modules)
				futures.append(executor.submit(runner))
			else:
				futures.append(executor.submit(checker.run, list_modules))

		for future in concurrent.futures.as_completed(futures):
			result = future.result()

			exit_code = max(result.return_code, exit_code)

			if result.output:
				header_text = result.checker_name

				if result.help_line:
					header_text += f'\nHint: {result.help_line}'

				# with `show_warnings` disabled, only print header if there was an error
				if show_warnings or result.return_code:
					click.secho(header_text, bg = 'white', fg = 'black', bold = True, underline = True)

				for line_of_output in result.output:
					filename = ''
					if line_of_output.file is not None:
						filename += f'{line_of_output.file}:'

					if line_of_output.line is not None:
						filename += f'{line_of_output.line}:'

					if show_warnings or line_of_output.is_error:
						if filename:
							click.secho(f'{filename} {line_of_output.message}', bold = line_of_output.is_error)
						else:
							click.secho(line_of_output.message, bold = line_of_output.is_error)

	if debug:
		time_elapsed = time.monotonic() - cq_started
		logging.debug('cq ended, time elapsed: %.3f s', time_elapsed)

		logger.debug('slowest runners:')

		module_time_elapsed.sort(key = lambda x: x.time, reverse = True)

		for run in module_time_elapsed[:3]:
			logger.debug('%s with %.3f s', run.name, run.time)
	return exit_code


def run_fixers(
	list_modules: List[str],
	disable: Iterable[str],
	debug: bool,
) -> int:
	if debug:
		logging.debug('cq started fixing in debug mode')
	exit_code = 0
	return_codes: List[int] = []

	for fixer in fixers:
		if fixer.NAME in disable:
			if debug:
				logging.debug('module %s disabled -> skipping', fixer.NAME)
			continue
		click.secho(fixer.NAME, bg = 'white', fg = 'black', bold = True, underline = True)
		return_codes.append(fixer.run(list_modules))
	exit_code = max(return_codes)
	return exit_code


@click.command()
@click.option('--debug', help = 'Display debbuging information.', is_flag = True)
@click.option('--fix', help = 'Run fixers instead of checkers', is_flag = True)
@click.option('--show-warnings', help = 'Display warnings.', is_flag = True)
@click.option('-j', default = None, type = int, help = 'Number of threads to use.')
@click.option(
	'--disable',
	'-d',
	multiple = True,
	help = 'Disable some of the checkers or fixers, e.g. -d pyflakes-ext -d mypy.',
)
@click.option(
	'--help',
	'-h',
	callback = help_callback,
	is_flag = True,
	expose_value = False,
	is_eager = True,
	help = 'Show this message and exit.',
)
@click.argument('modules', nargs = -1)
def main(
	debug: bool,
	fix: bool,
	show_warnings: bool,
	j: Optional[int],
	disable: Tuple[str],
	modules: Tuple[str],
) -> None:
	logging.basicConfig(
		format = '%(asctime)s: %(levelname)s: %(message)s',
		handlers = [
			logging.StreamHandler(),
		],
		level = logging.DEBUG if debug else logging.INFO,
	)

	logger = logging.getLogger(__name__)

	if not modules:
		list_modules = ['.']
	else:
		list_modules = list(modules)

	result_char = CHECK_MARK
	result_color = 'green'

	if fix:
		exit_code = run_fixers(
			list_modules,
			disable,
			debug,
		)
	else:
		exit_code = run_checkers(list_modules, disable, logger, debug, show_warnings, j)

	if exit_code > 0:
		result_char = FAIL_X
		result_color = 'red'

	click.secho(result_char, fg = result_color)
	sys.exit(exit_code)


if __name__ == '__main__':
	main()  # pylint: disable = no-value-for-parameter
