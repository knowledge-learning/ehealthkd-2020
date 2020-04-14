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

.PHONY: evaltrain
evaltrain:
	python3 -m scripts.evaltest --plain --mode train

.PHONY: build_corpus
build_corpus:
	python3 -m scripts.build_corpus

.PHONY: clean
clean:
	git clean -fxd

.PHONY: codalab
codalab:
	(cd data && zip -r ../codalab/gold.zip testing development)

	cp -r scripts codalab/program/
	cp codalab/program/metadata-dev codalab/program/metadata
	(cd codalab/program && zip -r ../score_dev.zip metadata scripts eval.sh)

	cp codalab/program/metadata-test codalab/program/metadata
	(cd codalab/program && zip -r ../score_test.zip metadata scripts eval.sh)

	(cd codalab && zip codalab.zip *)

.PHONY: test-codalab
test-codalab:
	cp -r data/development codalab/ref/development
	cp -r data/testing codalab/ref/testing
	cp -r data/submissions/baseline/* codalab/res
	rm codalab/program/scripts
	ln -s `pwd`/scripts codalab/program/scripts
