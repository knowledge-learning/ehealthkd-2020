.PHONY: submit-all
submit-all:
	python -m scripts.baseline \
		--test \
		--dev \
		--train

.PHONY: evaltest
evaltest:
	python -m scripts.evaltest data/submissions/ --plain --mode test

.PHONY: evaldev
evaldev:
	python -m scripts.evaltest data/submissions/ --pretty --mode dev

.PHONY: build_corpus
build_corpus:
	python -m scripts.build_corpus

.PHONY: clean
clean:
	git clean -fxd