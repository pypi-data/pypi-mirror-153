from abc import ABC
from typing import Type, List

from blingfire import text_to_sentences_and_offsets
from pydantic import BaseModel
from pymultirole_plugins.v1.processor import ProcessorParameters, ProcessorBase
from pymultirole_plugins.v1.schema import Document, Sentence
from pymultirole_plugins.v1.segmenter import SegmenterParameters, SegmenterBase


class BlingFireParameters(SegmenterParameters, ProcessorParameters, ABC):
    pass


class BlingFireSegmenter(SegmenterBase, ProcessorBase, ABC):
    """[BlingFire](https://github.com/microsoft/BlingFire) segmenter.
    """

    def segment(self, documents: List[Document], parameters: SegmenterParameters) \
            -> List[Document]:
        for document in documents:
            document.sentences = []
            result = text_to_sentences_and_offsets(document.text)
            if result:
                for start, end in result[1]:
                    document.sentences.append(Sentence(start=start, end=end))
        return documents

    def process(self, documents: List[Document], parameters: ProcessorParameters) \
            -> List[Document]:
        return self.segment(documents, parameters)

    @classmethod
    def get_model(cls) -> Type[BaseModel]:
        return BlingFireParameters
