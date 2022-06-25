SRC_FILES := $(wildcard yartsu/*)
VERSION := $(shell pdm show | grep "Installed" | awk -F ":" 'gsub(/ /, ""){print $$2}')

.PHONY: lint typecheck build format

## apply formatting, linting and typechecking (default)
check: lint typecheck

## perform typechecking
typcheck:
	pdm run mypy yartsu

## format/lint with pre-commit(black,isort,flake8)
lint:
	pdm run pre-commit run --all

.PHONY: dist release release.assets dist build

release.assets: build/x86_64-unknown-linux-gnu/release/install/yartsu/yartsu check-version
	tar czf build/yartsu-$(VERSION)-x86_64-linux.tar.gz \
		build/x86_64-unknown-linux-gnu/release/install/yartsu

## create github release and attach gzipped binary
release: check-tag release-assets
	gh release create $(TAG) build/yartsu-$(VERSION)-x86_64-linux.tar.gz -p -d

## publish to pypi with twine
publish: check-version dist
	twine upload dist/*

## build wheel/targz with pdm
dist:
	pdm build

## build with pyoxidizer
build: build/x86_64-unknown-linux-gnu/release/install/yartsu/yartsu

build/shiv/yartsu: $(SRC_FILES)
	@echo "==> Building yartsu w/ shiv <=="
	@mkdir -p build/shiv
	@shiv \
		-c yartsu \
		-o ./build/shiv/yartsu \
		--preamble scripts/preamble.py \
		--reproducible \
		.

build/x86_64-unknown-linux-gnu/release/install/yartsu/yartsu: $(SRC_FILES)
	@echo "==> Building yartsu w/ shiv <=="
	@pdm install
	@pyoxidizer build --release

.PHONY: install.bin install.shiv

## install pyoxidizer binary
install.bin: build/x86_64-unknown-linux-gnu/release/install/yartsu/yartsu
	@echo "==> Installing yartsu to ~/bin <=="
	@cp ./build/x86_64-unknown-linux-gnu/release/install/yartsu/yartsu ~/bin

## install shiv binary
install.shiv: build/shiv/yartsu
	@echo "==> Installing yartsu to ~/bin <=="
	@cp ./build/shiv/yartsu ~/bin

DOCS_RECIPES := $(patsubst %,docs.%,theme diff svg demo)

.PHONY: docs $(DOCS_RECIPES)

## generate docs/svg
docs: $(DOCS_RECIPES)

docs.theme:
	@./scripts/theme-showcase-gen

docs.diff:
	@./scripts/rich-diff > docs/rich-diff.md

docs.svg:
	@lolcat -F .5 -S 9 -f assets/logo.txt | yartsu -o assets/logo.svg
	@yartsu -o assets/help.svg -t "yartsu --help" -- yartsu -h

docs.demo:
	@python -c \
		"from rich.console import Console; \
			console = Console(force_terminal=True); \
			console.print('\n:snake: [b i]Emoji\'s!'); \
			console.print('  [cyan]Nerd Fonts!');" | \
		yartsu -w 25 -o assets/demo.svg

## cleanup build and loose files
clean:
	@rm -rf build dist capture.svg

# conditionals
check-tag:
	@[ "${TAG}" ] || ( echo ">> TAG is not set"; exit 1 )
	@git describe HEAD --tags --exact-match

check-version:
	@if [[ "${VERSION}" == *"+"* ]]; then \
		echo ">> VERSION is dev"; \
		echo ">> $(VERSION)"; \
		exit 1; \
	fi

.PHONY: help list

FILL = 15
## Display this help screen
help: ## try `make help`
	@awk '/^[a-z.A-Z_-]+:/ { helpMessage = match(lastLine, /^##(.*)/); \
    if (helpMessage) { helpCommand = substr($$1, 0, index($$1, ":")-1); \
    helpMessage = substr(lastLine, RSTART + 3, RLENGTH); printf "\033[36m%-$(FILL)s\033[0m%s\n"\
    , helpCommand, helpMessage;}} { lastLine = $$0 }' $(MAKEFILE_LIST)
