.PHONY: run export-all install venv-activate install-cli uninstall-cli setup

install:
	@if [ ! -d .venv ]; then \
		echo "[install] Creating virtual environment at .venv"; \
		python3 -m venv .venv; \
	else \
		echo "[install] Reusing existing virtual environment at .venv"; \
	fi
	. .venv/bin/activate; python -m pip install --upgrade pip setuptools wheel
	. .venv/bin/activate; pip install -r requirements.txt

run:
	. .venv/bin/activate; python3 main.py

export-all:
	@mkdir -p z_project_list
	@echo "Mengekspor semua file ke z_project_list/listing.txt"
	@rm -f z_project_list/listing.txt
	@for f in $$(find . -type f \
		-not -path '*/\.*' \
		-not -path '*/__pycache__/*' \
		-not -name ".gitkeep" \
		| sort); do \
			echo "=== $$f ===" >> z_project_list/listing.txt; \
			cat $$f >> z_project_list/listing.txt; \
			echo "\n" >> z_project_list/listing.txt; \
	done

venv-activate:
	@echo "To activate the virtual environment, run:"
	@echo "  source .venv/bin/activate"

setup: install install-cli
	@echo "Asterix CLI installed. Ensure $$HOME/.local/bin is in your PATH, then run: asterix"

install-cli:
	@mkdir -p $(HOME)/.local/bin
	@echo "Menginstal launcher ke $(HOME)/.local/bin/asterix"
	@echo '#!/usr/bin/env bash' > $(HOME)/.local/bin/asterix
	@echo 'APPDIR="$(shell pwd)"' >> $(HOME)/.local/bin/asterix
	@echo 'VENVDIR="$$APPDIR/.venv"' >> $(HOME)/.local/bin/asterix
	@echo 'PY="$$VENVDIR/bin/python"' >> $(HOME)/.local/bin/asterix
	@echo 'if [ -x "$$PY" ]; then' >> $(HOME)/.local/bin/asterix
	@echo '  exec "$$PY" "$$APPDIR/main.py" "$$@"' >> $(HOME)/.local/bin/asterix
	@echo 'else' >> $(HOME)/.local/bin/asterix
	@echo '  exec python3 "$$APPDIR/main.py" "$$@"' >> $(HOME)/.local/bin/asterix
	@echo 'fi' >> $(HOME)/.local/bin/asterix
	@chmod +x $(HOME)/.local/bin/asterix
	@echo "Selesai. Pastikan $(HOME)/.local/bin ada di PATH Anda. Coba jalankan: asterix"

uninstall-cli:
	@rm -f $(HOME)/.local/bin/asterix
	@echo "Launcher dihapus: $(HOME)/.local/bin/asterix"
