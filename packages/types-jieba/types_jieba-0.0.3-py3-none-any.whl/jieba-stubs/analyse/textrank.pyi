from collections import defaultdict
from jieba import Tokenizer
from jieba.posseg import pair
from .tfidf import KeywordExtractor
from typing import List, Set, Tuple, Union


class UndirectWeightedGraph:
    d: float
    graph: defaultdict[float, List[Tuple[float, float, float]]]

    def addEdge(self, start: float, end: float, weight: float):
        ...

    def rank(self) -> defaultdict[float, float]:
        ...


class TextRank(KeywordExtractor):
    tokenizer: Tokenizer
    postokenizer = tokenizer
    stop_words: Set[str]
    pos_filt: frozenset[str]
    span: int

    def pairfilter(self, wp: pair) -> bool:
        ...

    def textrank(
        self,
        sentence: str,
        topK: int = ...,
        withWeight: bool = ...,
        allowPOS: Tuple[str, ...] = ...,
        withFlag: bool = ...,
    ) -> List[Union[Tuple[str, float], str]]:
        ...
