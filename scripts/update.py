import sys
from pathlib import Path

from scripts.utils import Collection
from scripts.legacy import eHealth2019


def filter(collection: Collection, sentences):
    # return Collection([s for s in collection.sentences if s.text in sentences])

    def find(text):
        for s in collection.sentences:
            if s.text == text:
                return s
        raise Exception("Not found! " + text)

    return Collection([find(text) for text in sentences])


def load_and_dump_from_corpus(path2sentences, path2corpus, path2output):
    sentences = path2sentences.read_text().splitlines()
    print(len(sentences))
    collection = Collection().load_dir(path2corpus, legacy=True, attributes=False)
    print(len(collection))
    collection = filter(collection, sentences)
    print(len(collection))
    collection.dump(path2output)


def from_corpus():
    path2sentences = Path(sys.argv[2])
    path2corpus = Path(sys.argv[3])
    path2output = Path(sys.argv[4])

    for source in path2sentences.iterdir():
        if source.is_dir():
            finput = next(source.glob("input_*.txt"))
            print(finput)
            load_and_dump_from_corpus(finput, path2corpus, path2output / finput.name)


def load_and_dump_from_scenario(finput: Path, foutput: Path):
    c = Collection()
    eHealth2019.load(c, finput).dump(foutput)


def from_scenario():
    path2input = Path(sys.argv[2])
    path2output = Path(sys.argv[3])

    if path2input.is_dir():
        for source in path2input.iterdir():
            finput = next(source.glob("input_*.txt"))
            print(finput)
            load_and_dump_from_scenario(finput, path2output / source.name)
    else:
        load_and_dump_from_scenario(path2input, path2output)


if __name__ == "__main__":
    if sys.argv[1] == "--scenario":
        from_scenario()
    elif sys.argv[1] == "--corpus":
        from_corpus()
    else:
        raise Exception("Expected `--scenario` or `--corpus`.")

