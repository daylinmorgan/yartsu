VERSION ?= $(shell git describe --tags --always --dirty=-dev | sed 's/^v//g')
SRC_FILES := $(wildcard yartsu/*)

.PHONY: lint typecheck build format

check: lint typecheck ## apply formatting, linting and typechecking (default)
typecheck: ## perform typechecking
	pdm run mypy yartsu

lint: ## format/lint with pre-commit(black,isort,flake8)
	pdm run pre-commit run --all

.PHONY: dist release release-assets dist build

release-assets: build/x86_64-unknown-linux-gnu/release/install/yartsu/yartsu check-version
	tar czf build/yartsu-$(VERSION)-x86_64-linux.tar.gz \
		build/x86_64-unknown-linux-gnu/release/install/yartsu

release: check-tag release-assets ## create github release and attach gzipped binary
	gh release create $(TAG) build/yartsu-$(VERSION)-x86_64-linux.tar.gz -p -d

publish: check-version dist ## publish to pypi with twine
	twine upload dist/*

dist: ## build wheel/targz with pdm
	pdm build

build: build/x86_64-unknown-linux-gnu/release/install/yartsu/yartsu  ## build with pyoxidizer

build/x86_64-unknown-linux-gnu/release/install/yartsu/yartsu: $(SRC_FILES)
	@echo "==> Building yartsu w/ pyxoxidizer <=="
	@pdm install
	@pyoxidizer build --release

.PHONY: install.bin install.shiv

install-bin: build/x86_64-unknown-linux-gnu/release/install/yartsu/yartsu ## install pyoxidizer binary
	@echo "==> Installing yartsu to ~/bin <=="
	@cp ./build/x86_64-unknown-linux-gnu/release/install/yartsu/yartsu ~/bin

DOCS_RECIPES := $(patsubst %,docs-%,theme diff svg demo)
.PHONY: docs $(DOCS_RECIPES)
docs: $(DOCS_RECIPES) ## generate docs/svg

docs-theme:
	@./scripts/theme-showcase-gen

docs-diff:
	@./scripts/rich-diff > docs/rich-diff.md

docs-svg:
	@lolcat -F .5 -S 9 -f assets/logo.txt | yartsu -o assets/logo.svg
	@yartsu -o assets/help.svg -t "yartsu --help" -- yartsu -h

clean: ## cleanup build and loose files
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

-include .task.cfg.mk
