build:
	bazel mod tidy
	bazel run //tools:tabulate -- -1 -s "," -f github $(realpath tools/table.txt)
	bazel run //:main
	bazel build //:python-helper && cat bazel-bin/data.json
