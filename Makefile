PYTEST_ARGS ?= 

ifdef NOISY
	PYTEST_ARGS := --capture=tee-sys
endif

.PHONY: test
test:
	@pytest $(PYTEST_ARGS)

.PHONY: format fmt
format fmt:
	@black .
