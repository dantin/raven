
.PHONY: test
test:
	@echo "Run unit tests"
	@tox

.PHONY: clean
clean:
	@echo "Clean temp files"
	@rm -f *.jl
	@rm -f *.log
	@rm -rf tmp/
	@rm -rf htmlcov/
