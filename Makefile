
.PHONY: test
test:
	@echo "Run unit tests"
	@tox

.PHONY: clean
clean:
	@echo "Clean temp files"
	@rm -f *.log
	@rm -rf htmlcov/
	@find . -type d -path ./.tox -prune -false -o -name '__pycache__' -print0 | xargs -0 rm -rf

.PHONY: db-init
db-init:
	@sudo -u postgres psql < misc/db-create.sql

.PHONY: db-destroy
db-destroy:
	@sudo -u postgres psql < misc/db-destroy.sql

.PHONY: babel-extract
babel-extract:
	@cd raven; FLASK_APP=app flask fab babel-extract

# init translation
#
# pybabel init -i ./babel/messages.pot -d app/translations -l en
#
.PHONY: babel-compile
babel-compile:
	@cd raven; FLASK_APP=app flask fab babel-compile
