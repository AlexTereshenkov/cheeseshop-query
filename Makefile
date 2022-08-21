check:
	./pants update-build-files fmt lint test check ::
package:
	./pants package cheeseshop/cli:cheeseshop-query

