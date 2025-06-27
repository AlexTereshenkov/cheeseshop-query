## Overview

Run Python tools (console entry points):

```
bazel run //:tabulate -- -1 -s "," -f github $(realpath table.txt)
| Food   | Type   |
|--------|--------|
| Spam   | Yummy  |
| Eggs   | Yummy  |
```
