.PHONY: submit-all
submit-all:
	python -m scripts.baseline \
		--test \
		--dev \
		--custom data/training/scenario.txt train scenario

.PHONY: evaltest
evaltest:
	python -m scripts.evaltest --pretty data/submissions/ data/testing

.PHONY: build_corpus
build_corpus:
	python -m scripts.build_corpus

.PHONY: clean
clean:
	git clean -fxd