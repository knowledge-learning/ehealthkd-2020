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
	zip -j gold.zip data/*
	cp codalab/program/metadata_dev codalab/program/metadata
	zip -j -r score_dev.zip codalab/program/metadata scripts
	cp codalab/program/metadata_test codalab/program/metadata
	zip -j -r score_test.zip codalab/program/metadata scripts

.PHONY: test-codalab
test-codalab-dev:
	cp -r data/development codalab/ref/development
	cp -r data/testing codalab/ref/testing
	cp -r data/submissions/baseline/* codalab/res
	rm codalab/program/scripts
	ln -s `pwd`/scripts codalab/program/scripts
