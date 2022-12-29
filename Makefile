check:
	./pants update-build-files fmt lint test check ::
	./pants project-version --as-json cheeseshop:
	./pants project-version --no-as-json cheeseshop:
	yamllint .github --no-warnings
package:
	./pants package cheeseshop/cli:cheeseshop-query
