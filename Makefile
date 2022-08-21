check:
	./pants update-build-files fmt lint test check ::
	yamllint .github --no-warnings
package:
	./pants package cheeseshop/cli:cheeseshop-query
