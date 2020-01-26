.PHONY: submit-all
submit-all:
	python -m scripts.baseline \
		--test \
		--dev \
		--custom data/training/scenario.txt train scenario

.PHONY: clean
clean:
	git clean -fxd