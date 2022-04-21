install:
	poetry install

gendiff:
	poetry run page-loader

package-install:
	python3 -m pip install --force-reinstall dist/*.whl

publish:
	poetry publish --dry-run

lint:
	poetry run flake8 page_loader

test:
	poetry run pytest tests/test_download.py

check:
	make lint
	make test

build:
	make check
	poetry build