export PROJECT := tuxrun
export TUXPKG_MIN_COVERAGE := 97

check: typecheck test spellcheck stylecheck

include $(shell tuxpkg get-makefile)

.PHONY: htmlcov tags

htmlcov:
	python3 -m pytest --cov=tuxrun --cov-report=html

stylecheck: style flake8

spellcheck:
	codespell \
		--check-filenames \
		--skip '.git,public,dist,*.sw*,*.pyc,tags,*.json,.coverage,htmlcov,*.jinja2'

integration:
	python3 test/integration.py

doc: docs/index.md
	mkdocs build

docs/index.md: README.md scripts/readme2index.sh
	scripts/readme2index.sh $@

doc-serve:
	mkdocs serve

flit = flit
publish-pypi:
	$(flit) publish

tags:
	ctags -R tuxrun/ test/
