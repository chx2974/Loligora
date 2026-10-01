PY := .venv/bin/python
export PYTHONPATH := src
# Serialise builds when several agents work in parallel: a whole target runs under one lock.
LOCK := lockf -k .build.lock

.PHONY: build check proofs all clean serve release sources _build _check _proofs

build:
	$(LOCK) $(MAKE) --no-print-directory _build

check:
	$(LOCK) $(MAKE) --no-print-directory _check

proofs:
	$(LOCK) $(MAKE) --no-print-directory _proofs

all:
	$(LOCK) $(MAKE) --no-print-directory _build _check _proofs

# Writes sources/*.ufo + *.designspace (also done by every build).
sources:
	$(LOCK) $(PY) -m loligora.build sources

_build:
	$(PY) -m loligora.build
	$(PY) scripts/glyph_table.py

_check:
	$(PY) scripts/check_tabular.py
	$(PY) scripts/check_charset.py
	$(PY) scripts/check_outlines.py
	$(PY) scripts/check_marks.py

_proofs:
	$(PY) scripts/proofs.py

# Release package: build + check (each under the lock), then assemble dist/.
release:
	$(MAKE) --no-print-directory build
	$(MAKE) --no-print-directory check
	$(PY) scripts/release.py --no-build

clean:
	rm -rf build fonts/variable

serve:
	@echo "Specimen: http://localhost:8000/specimen/"
	$(PY) -m http.server 8000

.PHONY: qa
# Both Font Bakery profiles (reports in qa/). Non-zero exit (FAILs) does not stop make; read the reports.
qa:
	-$(PY) -m fontbakery check-universal --skip-network --ghmarkdown qa/fontbakery-universal.md "fonts/variable/Loligora[wght].ttf" "fonts/variable/Loligora-Italic[wght].ttf" </dev/null
	-$(PY) -m fontbakery check-googlefonts --skip-network --ghmarkdown qa/fontbakery-googlefonts.md "fonts/variable/Loligora[wght].ttf" "fonts/variable/Loligora-Italic[wght].ttf" </dev/null
