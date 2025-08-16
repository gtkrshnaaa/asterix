.PHONY: run export-all

run:
	python3 main.py

export-all:
	@mkdir -p z_project_list
	@echo "Mengekspor semua file ke z_project_list/listing.txt"
	@rm -f z_project_list/listing.txt
	@for f in $$(find . -type f \
		-not -path '*/\.*' \
		-not -name ".gitkeep" \
		| sort); do \
			echo "=== $$f ===" >> z_project_list/listing.txt; \
			cat $$f >> z_project_list/listing.txt; \
			echo "\n" >> z_project_list/listing.txt; \
	done
