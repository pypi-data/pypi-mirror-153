import json
from pathlib import Path
from typing import List

import pytest
from pysegmenters_blingfire.blingfire import BlingFireSegmenter, BlingFireParameters
from pymultirole_plugins.v1.schema import Document, DocumentList


def test_blingfire_en():
    TEXT = """CLAIRSSON INTERNATIONAL REPORTS LOSS

Clairson International Corp. said it expects to report a net loss for its
second quarter ended March 26. The company doesn’t expect to meet analysts’ profit
estimates of $3.9 to $4 million, or 76 cents a share to 79 cents a share, for its
year ending Sept. 24, according to Pres. John Doe."""
    model = BlingFireSegmenter.get_model()
    model_class = model.construct().__class__
    assert model_class == BlingFireParameters
    segmenter = BlingFireSegmenter()
    parameters = BlingFireParameters()
    docs: List[Document] = segmenter.segment([Document(text=TEXT)], parameters)
    doc0 = docs[0]
    assert len(doc0.sentences) == 2
    sents = [doc0.text[s.start:s.end] for s in doc0.sentences]
    assert sents[0] == """CLAIRSSON INTERNATIONAL REPORTS LOSS

Clairson International Corp. said it expects to report a net loss for its
second quarter ended March 26."""
    assert sents[1] == """The company doesn’t expect to meet analysts’ profit
estimates of $3.9 to $4 million, or 76 cents a share to 79 cents a share, for its
year ending Sept. 24, according to Pres. John Doe."""


@pytest.mark.skip(reason="Not a test")
def test_summarizer_mazars():
    testdir = Path(__file__).parent / "data"
    json_file = testdir / "mazars_test_qualite_26avril-documents.json"
    with json_file.open("r") as fin:
        docs = json.load(fin)
    docs = [Document(**doc) for doc in docs]
    nb_segs = sum([len(doc.sentences) for doc in docs])
    parameters = BlingFireParameters()
    segmenter = BlingFireSegmenter()

    docs = segmenter.segment(docs, parameters)
    for doc in docs:
        doc.altTexts = None
    nb_segs2 = sum([len(doc.sentences) for doc in docs])
    assert nb_segs2 <= nb_segs
    seg_file = (
        testdir / "mazars_test_qualite_26avril-documents_blingfire.json"
    )
    dl = DocumentList(__root__=docs)
    with seg_file.open("w") as fout:
        print(dl.json(exclude_none=True, exclude_unset=True, indent=2), file=fout)
