build:
	bazel mod tidy
	# run tabulate console entry

	bazel run //tools:tabulate -- -1 -s "," -f github $(realpath tools/table.txt)

	# run a genrule accessing Python interpreter
	bazel build //:python-helper && cat bazel-bin/data.json

	# run with a toolchain Python 3.10
	bazel run //:main-3_10

	# run with a default Python 3.11 interpreter
	bazel run //:main

	# run with a local Python 3.12 interpreter
	bazel run --//:py=local-3_12 //:main

fmt:
	bazel run //:buildifier

run:
	bazel run //cheeseshop/cli -- list-versions \
	  --package="numpy" \
	  --package-type="bdist_wheel" \
	  --python-version="cp313" \
	  --platform="linux" \
	  --arch="aarch64" \
	  --stable-only

.PHONY: requirements
requirements:
	bazel run //requirements:requirements.update
	bazel run //requirements:requirements-test.update
	bazel run //requirements:requirements-tools.update

test:
	bazel test //tests/... --nocache_test_results

coverage:
	rm -rf genhtml
	bazel clean
	bazel coverage //tests/... \
		--nocache_test_results \
		--collect_code_coverage \
		--combined_report=lcov \
		--instrument_test_targets \
		--instrumentation_filter="^//cheeseshop[/:],^//tests[/:]"
	genhtml --output genhtml "$(shell bazel info output_path)/_coverage/_coverage_report.dat"

package:
	bazel clean
	bazel build //cheeseshop/cli:cli-pex
	bazel-bin/cheeseshop/cli/cli-pex.pex


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
