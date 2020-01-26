.PHONY: submit-all
submit-all:
	python -m scripts.baseline \
		--test \
		--dev \
		--custom data/training/scenario.txt train scenario

.PHONY: evaltest
evaltest:
	python -m scripts.evaltest --pretty data/submissions/ data/testing

.PHONY: clean
clean:
	git clean -fxd