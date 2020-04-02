import bisect
import warnings
from pathlib import Path

from scripts.utils import Collection, Keyphrase, Relation, Sentence

warnings.warn(
    """The `script.legacy` module is deprecated!
    Consider using `CollectionV1Handler` from `scripts.utils` instead."""
)


class eHealth2019:
    @classmethod
    def load_input(cls, collection: Collection, finput: Path):
        sentences = [s.strip() for s in finput.open(encoding="utf8").readlines() if s]
        sentences_obj = [Sentence(text) for text in sentences]
        collection.sentences.extend(sentences_obj)

    @classmethod
    def load_keyphrases(cls, collection: Collection, finput: Path):
        cls.load_input(collection, finput)

        input_a_file = finput.parent / ("output_a_" + finput.name.split("_")[1])

        sentences_length = [len(s.text) for s in collection.sentences]
        for i in range(1, len(sentences_length)):
            sentences_length[i] += sentences_length[i - 1] + 1

        sentence_by_id = {}

        for line in input_a_file.open(encoding="utf8").readlines():
            lid, spans, label, _ = line.strip().split("\t")
            lid = int(lid)

            spans = [s.split() for s in spans.split(";")]
            spans = [(int(start), int(end)) for start, end in spans]

            # find the sentence where this annotation is
            i = bisect.bisect(sentences_length, spans[0][0])
            # correct the annotation spans
            if i > 0:
                spans = [
                    (
                        start - sentences_length[i - 1] - 1,
                        end - sentences_length[i - 1] - 1,
                    )
                    for start, end in spans
                ]
                spans.sort(key=lambda t: t[0])
            # store the annotation in the corresponding sentence
            the_sentence = collection.sentences[i]
            keyphrase = Keyphrase(the_sentence, label, lid, spans)
            the_sentence.keyphrases.append(keyphrase)

            if len(keyphrase.spans) == 1:
                keyphrase.split()

            sentence_by_id[lid] = the_sentence

        return sentence_by_id

    @classmethod
    def load(cls, collection: Collection, finput: Path):
        input_b_file = finput.parent / ("output_b_" + finput.name.split("_")[1])

        sentence_by_id = cls.load_keyphrases(collection, finput)

        for line in input_b_file.open(encoding="utf8").readlines():
            label, src, dst = line.strip().split("\t")
            src, dst = int(src), int(dst)

            the_sentence = sentence_by_id[src]

            if the_sentence != sentence_by_id[dst]:
                warnings.warn(
                    "In file '%s' relation '%s' between %i and %i crosses sentence boundaries and has been ignored."
                    % (finput, label, src, dst)
                )
                continue

            assert sentence_by_id[dst] == the_sentence

            the_sentence.relations.append(
                Relation(the_sentence, src, dst, label.lower())
            )

        return collection
