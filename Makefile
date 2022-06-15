SRC_FILES = $(wildcard yartsu/*)

.PHONY: list lint build svg-docs theme-docs docs typing format
lint: format typing

typing:
	pdm run mypy yartsu

format:
	pdm run pre-commit run --all

build: build/yartsu

build/yartsu: $(SRC_FILES)
	mkdir -p build
	shiv \
    	-c yartsu \
    	-o ./build/yartsu \
    	--preamble scripts/preamble.py \
    	--reproducible \
    	.

install-bin: build/yartsu
	cp ./build/yartsu ~/bin

docs: svg-docs theme-docs demo-docs

theme-docs:
	./scripts/theme-showcase-gen

svg-docs:
	lolcat -F .5 -S 9 -f assets/logo.txt | yartsu -o assets/logo.svg
	yartsu -o assets/yartsu.svg -t "yartsu --help" -- yartsu -h

demo-docs:
	python -c \
		"from rich.console import Console; \
		console = Console(force_terminal=True); \
		console.print('\n:snake: [b i]Emoji\'s!'); \
		console.print('  [cyan]Nerd Fonts!');" \
		| yartsu -w 25 -o assets/demo.svg

# https://stackoverflow.com/a/26339924
list:
	@LC_ALL=C $(MAKE) -pRrq -f $(lastword $(MAKEFILE_LIST)) : 2>/dev/null | awk -v RS= -F: '/^# File/,/^# Finished Make data base/ {if ($$1 !~ "^[#.]") {print $$1}}' | sort | egrep -v -e '^[^[:alnum:]]' -e '^$@$$'
