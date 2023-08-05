import isort


# This is the only way to use isort with custom config file
# and not set project root to cq directory
Config = isort.settings.Config(
	atomic = True,
	ensure_newline_before_comments = True,
	force_grid_wrap = 0,
	from_first = True,
	include_trailing_comma = True,
	indent = 'Tab',
	line_length = 110,
	lines_after_imports = 2,
	multi_line_output = 3,
	order_by_type = True,
	use_parentheses = True,
	extra_standard_library = (
		'typing',
		'ql_types',
		'typing_extensions',
		'mypy_extensions',
		'pyspark.sql.types',
	),
)
