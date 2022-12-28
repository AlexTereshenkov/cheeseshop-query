check:
	./pants update-build-files fmt lint test check ::
	./pants project-version cheeseshop:
	yamllint .github --no-warnings
package:
	./pants package cheeseshop/cli:cheeseshop-query
