.PHONY: baseline
baseline:
	python -m scripts.baseline \
		--test \
		--dev \
		--train

.PHONY: evaltest
evaltest:
	python -m scripts.evaltest --plain --mode test

.PHONY: evaldev
evaldev:
	python -m scripts.evaltest --plain --mode dev

.PHONY: build_corpus
build_corpus:
	python -m scripts.build_corpus

.PHONY: clean
clean:
	git clean -fxd

.PHONY: codalab
codalab:
	zip -j testing.zip testing/*
	zip -j training.zip training/*
	zip score.zip score.py
