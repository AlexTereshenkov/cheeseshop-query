## Overview

Run Python tools (console entry points):

```
$ bazel run //:tabulate -- -1 -s "," -f github $(realpath table.txt)
| Food   | Type   |
|--------|--------|
| Spam   | Yummy  |
| Eggs   | Yummy  |
```

Run entry point:

```shell
$ bazel run //cheeseshop/cli -- list-versions \
  --package="numpy" \
  --package-type="bdist_wheel" \
  --python-version="cp313" \
  --platform="linux" \
  --arch="aarch64" \
  --stable-only
```

Generate code coverage:

```shell
$ bazel coverage //tests/... \
    --nocache_test_results \
    --collect_code_coverage \
    --combined_report=lcov \
    --instrumentation_filter="^//cheeseshop[/:],^//tests[/:]"
```

`lcov --list` might expects function and branch data, which Bazel's Python coverage tooling does
not provide, so it defaults to 0% even if line coverage is present:

```shell
$ lcov --list "$(bazel info output_path)/_coverage/_coverage_report.dat"
```

Use `genhtml` instead:

```shell
$ genhtml --output genhtml "$(bazel info output_path)/_coverage/_coverage_report.dat"
```
