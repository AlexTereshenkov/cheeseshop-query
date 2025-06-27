build:
	bazel mod tidy
	bazel run //tools:tabulate -- -1 -s "," -f github $(realpath tools/table.txt)
	bazel run //:main
	bazel build //:python-helper && cat bazel-bin/data.json
	# run with a local Python 3.12 interpreter
	bazel run --//:py=local-3_12 //:main

run-python-interpreter:
	# run a specific Python interpreter
	# @rules_python//python/config_settings:python_version is a build setting defined by the rules_python ruleset
	bazel run \
		@rules_python//python/bin:python \
		--@rules_python//python/config_settings:python_version=3.10 \
		-- -c "import sys; print(f'Python {sys.version_info.major}.{sys.version_info.minor}')"

	bazel run \
		@rules_python//python/bin:python \
		--@rules_python//python/config_settings:python_version=3.11 \
		-- -c "import sys; print(f'Python {sys.version_info.major}.{sys.version_info.minor}')"
