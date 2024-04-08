.PHONY: install frontend messages pip node_modules requirements upgrade

install: pip node_modules frontend

pip:
	pip install -r requirements/dev.txt

requirements: requirements/base.in
	pip-compile --output-file requirements/base.txt requirements/base.in

upgrade:
	pip install pip-tools pur
	pur --patch=Django -r requirements/base.in
	pur --no-recursive -r requirements/docker.txt
	pur --no-recursive -r requirements/dev.txt
	pip-compile -v --upgrade --output-file requirements/base.txt requirements/base.in

node_modules:
	npm install

frontend:
	test -e node_modules || npm install
	npm run webpack

watch:
	npm run watch

messages:
	django-admin.py compilemessages

clean:
	npm run gulp clean

test:
	py.test --reuse-db --nomigrations

coverage:
	pytest --reuse-db --nomigrations --cov --cov-report=term-missing
