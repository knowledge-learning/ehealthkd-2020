import sys
from pathlib import Path

from scripts.utils import Collection


def filter(collection: Collection, sentences):
    # return Collection([s for s in collection.sentences if s.text in sentences])

    def find(text):
        for s in collection.sentences:
            if s.text == text:
                return s
        raise Exception("Not found! " + text)

    return Collection([find(text) for text in sentences])


def main(path2sentences, path2corpus, path2output):
    sentences = path2sentences.read_text().splitlines()
    print(len(sentences))
    collection = Collection().load_dir(path2corpus, legacy=True, attributes=False)
    print(len(collection))
    collection = filter(collection, sentences)
    print(len(collection))
    collection.dump(path2output)


if __name__ == "__main__":
    path2sentences = Path(sys.argv[1])
    path2corpus = Path(sys.argv[2])
    path2output = Path(sys.argv[3])

    for source in path2sentences.iterdir():
        if source.is_dir():
            finput = next(source.glob("input_*.txt"))
            print(finput)
            main(finput, path2corpus, path2output / finput.name)
