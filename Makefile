.PHONY: run list

run:
	python3 main.py

list:
	@echo "Project file listing:"
	@find . -type f \
		-not -path '*/\.*' \
		-not -name ".gitkeep" \
		| sort
