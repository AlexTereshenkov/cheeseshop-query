python_sources()

# __dependents_rules__(
#  (
#    {"type": "*"},  # or {"path": "*"} if you prefer
#    "/**",  # current subtree, i.e. src/cli/utils/**
#    "/../cli/*", # src/cli/* may import files from src/cli/utils/** (the rules are inherited down the tree)
#    "!*",
#  )
# )

# alternative
__dependents_rules__(
    (
        {"type": "*"},  # or {"path": "*"} if you prefer
        "//cheeseshop/cli/utils/**",  # current subtree, i.e. src/cli/utils/**
        "//cheeseshop/cli/**",  # src/cli/* may import files from src/cli/utils/** (the rules are inherited down the tree)
        "!*",
    )
)

__dependencies_rules__(
    (
        "*",  # applies to everything in this BUILD file
        "/**",  # allow all dependencies in this subtree
        "?*",  # may not depend on anything else
    )
)
