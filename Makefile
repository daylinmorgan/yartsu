SRC_FILES := $(wildcard yartsu/*)
VERSION := $(shell pdm show | grep "Installed" | awk -F ":" 'gsub(/ /, ""){print $$2}')

.PHONY: list lint build typing format dist check-tag release-asset

lint: format typing

typing:
	pdm run mypy yartsu

format:
	pdm run pre-commit run --all

check-tag:
	@[ "${TAG}" ] || ( echo ">> TAG is not set"; exit 1 )
	@git describe HEAD --tags --exact-match

check-version:
	@if [[ "${VERSION}" == *"+"* ]]; then \
		echo ">> VERSION is dev"; \
		echo ">> $(VERSION)"; \
		exit 1; \
	fi

release-assets: build/x86_64-unknown-linux-gnu/release/install/yartsu/yartsu check-version
	tar czf build/yartsu-$(VERSION)-x86_64-linux.tar.gz \
		build/x86_64-unknown-linux-gnu/release/install/yartsu

release: check-tag release-assets
	gh release create $(TAG) build/yartsu-$(VERSION)-x86_64-linux.tar.gz -p -d

publish: check-version dist
	twine upload dist/*

dist:
	pdm build

build: build/yartsu

build/shiv/yartsu: $(SRC_FILES)
	mkdir -p build/shiv
	shiv \
		-c yartsu \
		-o ./build/shiv/yartsu \
		--preamble scripts/preamble.py \
		--reproducible \
		.

build/x86_64-unknown-linux-gnu/release/install/yartsu/yartsu: $(SRC_FILES)
	pdm install
	pyoxidizer build --release

install-bin: build/x86_64-unknown-linux-gnu/release/install/yartsu/yartsu
	cp ./build/x86_64-unknown-linux-gnu/release/install/yartsu/yartsu ~/bin

install-shiv: build/shiv/yartsu
	cp ./build/shiv/yartsu ~/bin

.PHONY: svg-docs theme-docs diff-docs demo-docs docs

docs: svg-docs theme-docs demo-docs diff-docs

theme-docs:
	./scripts/theme-showcase-gen

diff-docs:
	./scripts/code_svg_format_diff.py >docs/rich-diff.md

svg-docs:
	lolcat -F .5 -S 9 -f assets/logo.txt | yartsu -o assets/logo.svg
	yartsu -o assets/yartsu.svg -t "yartsu --help" -- yartsu -h

demo-docs:
	python -c \
		"from rich.console import Console; \
			console = Console(force_terminal=True); \
			console.print('\n:snake: [b i]Emoji\'s!'); \
			console.print('  [cyan]Nerd Fonts!');" | \
		yartsu -w 25 -o assets/demo.svg

clean:
	rm -rf build dist capture.svg

# https://stackoverflow.com/a/26339924
list:
	@LC_ALL=C $(MAKE) -pRrq -f $(lastword $(MAKEFILE_LIST)) : 2>/dev/null | awk -v RS= -F: '/^# File/,/^# Finished Make data base/ {if ($$1 !~ "^[#.]") {print $$1}}' | sort | egrep -v -e '^[^[:alnum:]]' -e '^$@$$'
