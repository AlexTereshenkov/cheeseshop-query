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
