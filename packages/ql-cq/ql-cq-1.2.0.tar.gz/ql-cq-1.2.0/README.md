# CQ

Code quality checker package

## Usage
### Checking

Just run `cq` in the root of your package.

```
$ cq
requirements_setup_compatibility
setup.py: setup.py: does not contain requirement 'coverage' that is in requirements.txt
dumb_style_checker
setup.py:20: Put exactly one space before and after `=`  [...     name='.........', ...].
package/api.py:191: Put exactly one space before and after `=`  [... def fake_localtime(t=None): ...].
pyflakes-ext
Hint: use `# NOQA` comment for disabling pyflakes on particular line
./tests/test_warnings.py:4: 'types' imported but unused
mypy
Hint: use `# type: ignore` for disabling mypy on particular line
package/api.py:42: error: Need type annotation for 'freeze_factories' (hint: "freeze_factories: List[<type>] = ...")
pylint
Hint: use `# pylint: disable=<violation name>` for disabling line check. For a list of violations, see `pylint --list-msgs`
package/api.py:56: [W0212(protected-access), ] Access to a protected member _uuid_generate_time of a client class
```
You can specify path to packages that you want to test, if you want to test whole library/app.
```
$ cq package_1 package_2
```
Checkers are run in threads. Some of them (e.g. pylint, mypy) spawn an external process so this checkers run in parallel.

To disable certain checker for the whole run add option `-d`:
```
$ cq -d pylint -d branch_name_check
```

Warnings are hidden by default. To display them, run cq with `--show-warnings`
```
$ cq --show-warnings
```

If something takes too long use debug output, which will print timing for each checker:
```
$ cq --debug
```

Most of the checkers support disabling the error in the comment on the respective line. For example in `pylint` you can use
```
# pylint: disable = protected-access
```
to disable protected access check in the current context.

### Fixing

Just run `cq --fix` with the same options as regular `cq`.

## Checkers
- [`pylint`](https://www.pylint.org/) - comprehensive linter
- [`mypy`](http://mypy-lang.org/) - checks python typing
- [`bellybutton`](https://github.com/hchasestevens/bellybutton) - checks based on abstract syntax tree analysis
- [`pyflakes-ext`](https://pypi.org/project/pyflakes-ext/) - another general linter
- `grammar_nazi` - grammar/spelling errors
- `dumb_style_checker` - basic python mistakes (e.g. use of print in a library)
- `requirements_setup_compatibility` - validation of version compatibility between setup.py and requirements.txt
- [`requirements-validator`](https://pip.pypa.io/en/latest/reference/pip_check/) - requirements.txt validation
- [`setup_check`](https://docs.python.org/3/distutils/examples.html#checking-a-package) - setup.py validator
- `branch_name_check` - check whether current branch name comply with Quantlane standards
- [`orange`](https://gitlab.com/quantlane/meta/orange) - code formatter based on `black`
- [`isort`](https://github.com/PyCQA/isort) - isort your imports, so you don't have to
- [`safety`](https://github.com/pyupio/safety) - checks installed dependencies for known security vulnerabilities

## Fixers
- [`orange`](https://gitlab.com/quantlane/meta/orange) - code formatter based on `black`
- [`isort`](https://github.com/PyCQA/isort) - isort your imports, so you don't have to

### pylint

You can override the packaged pylint rules in `.pylintrc` in the root of your project (actually in `$PWD/.pylintrc` for `cq` run)

Pylint checker can output two types of issues: warning and error. Errors are in bold typeset. Warnings can (but should not) be ignored.

### mypy

Config can be overridden by having `mypy.ini` in the root of your project
