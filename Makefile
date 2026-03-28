BUF ?= buf

.PHONY: generate lint deps

deps:
	$(BUF) dep update

generate:
	rm -rf gen/go gen/ts
	mkdir -p gen/go gen/ts
	$(BUF) generate

lint:
	$(BUF) lint
