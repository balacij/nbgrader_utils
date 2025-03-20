.PHONY: test
test:
	pytest

.PHONY: format fmt
format fmt:
	black .
