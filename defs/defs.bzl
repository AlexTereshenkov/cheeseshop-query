load("@rules_python//python:py_test.bzl", "py_test")

def pytest_test(name, srcs, deps = [], **kwargs):
    py_test(
        name = name,
        srcs = srcs + ["//tools:pytest_runner.py"],
        main = "pytest_runner.py",
        deps = deps,
        **kwargs
    )
