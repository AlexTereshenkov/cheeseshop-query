python_sources()

resource(
    name="project-version",
    source="VERSION",
)


# ./pants project-version cheeseshop:
# (ProjectVersionFileView(path='cheeseshop/VERSION', version='0.0.1'),)

custom_target(name="custom1", source="VERSION", custom_field="cheeseshop/VERSION")
# custom_target(name="custom2", source="cheeseshop/VERSION2", custom_field="cheeseshop/VERSION2")

