help:

	@echo "Usage:"
	@echo "  make install        # install dev dependencies from $(REQ_DEV)"
	@echo "  make test           # run pytest (no coverage)"
	@echo "  make coverage       # run tests with coverage, show summary and write data"
	@echo "  make report         # show coverage report in terminal"
	@echo "  make html           # generate HTML coverage report (in $(COV_HTML_DIR))"
	@echo "  make xml            # generate XML coverage report ($(COV_XML))"

test:
	python3 -m pytest

coverage:
	coverage run --source='.' manage.py test airport-API-service

report:
	coverage report -m

html:
	coverage html
	@echo "HTML report generated in htmlcov/index.html"
