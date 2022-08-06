## Overview

## Development

```
$ ./pants fmt test lint ::
```

## Tests

```
$ ./pants test ::
```

## Docs generation

## Packaging

```
$ python3 setup.py bdist_pex
$ dist/cheeseshop-query*.pex --help
```

or

```
$ ./pants package ::
$ dist/**/*/cheeseshop*.pex --help
```

## Running

```
$ ./pants run cheeseshop/cli/cli.py -- list-versions --help
```
