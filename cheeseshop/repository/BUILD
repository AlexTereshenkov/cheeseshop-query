python_sources()

__dependencies_rules__(
    (
        "*",  # applies to everything in this BUILD file
        "/**",  # allow all dependencies in this subtree
        "//requirements#*",
        "//cheeseshop/cli/**",  # may not depend on cheeseshop/cli
        "*",
    )
)
