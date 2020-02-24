.PHONY: baseline
baseline:
	python3 -m scripts.baseline \
		--test \
		--dev \
		--train

.PHONY: evaltest
evaltest:
	python3 -m scripts.evaltest --plain --mode test

.PHONY: evaldev
evaldev:
	python3 -m scripts.evaltest --plain --mode dev

.PHONY: build_corpus
build_corpus:
	python3 -m scripts.build_corpus

.PHONY: clean
clean:
	git clean -fxd

.PHONY: codalab
codalab:
	zip -j testing.zip testing/*
	zip -j training.zip training/*
	zip score.zip score.py

.PHONY: test-codalab-dev
test-codalab-dev:
	cp -r data/development codalab/ref/development
	cp -r data/testing codalab/ref/testing
	cp -r data/submissions/baseline codalab/res
