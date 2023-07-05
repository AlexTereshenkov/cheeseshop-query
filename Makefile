check:
	black .
	flake8 cheeseshop tests
	mypy cheeseshop
package:
	python3 setup.py bdist_wheel
