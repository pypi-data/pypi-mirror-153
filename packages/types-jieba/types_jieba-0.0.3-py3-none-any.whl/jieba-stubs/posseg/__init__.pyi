from typing import List, Optional, Pattern, Generator, Dict, Tuple
from io import TextIOWrapper

TransType = Dict[Tuple[str, str], Dict[Tuple[str, str], float]]
StartType = Dict[Tuple[str, str], float]
EmitType = Dict[Tuple[str, str], Dict[str, float]]
StatesType = Dict[str, Tuple[Tuple[str, str], ...]]

PROB_START_P: str
PROB_TRANS_P: str
PROB_EMIT_P: str
CHAR_STATE_TAB_P: str

re_han_detail: Pattern[str]
re_skip_detail: Pattern[str]
re_han_internal: Pattern[str]
re_skip_internal: Pattern[str]

re_eng: Pattern[str]
re_num: Pattern[str]

re_eng1: Pattern[str]


class pair(object):
    word: str
    flag: str

    def __init__(self, word: str, flag: str):
        ...

    def encode(self, arg: str) -> bytes:
        ...


class POSTokenizer(object):
    def initialize(self, dictionary: Optional[str] = ...) -> None:
        ...

    def load_word_tag(self, f: TextIOWrapper) -> None:
        ...

    def makesure_userdict_loaded(self) -> None:
        ...

    def cut(self, sentence: str, HMM: bool = ...) -> Generator[pair, None, None]:
        ...

    def lcut(self, sentence: str, HMM: bool = ...) -> List[pair]:
        ...


dt: POSTokenizer

initialize = dt.initialize


def cut(
    sentence: str, HMM: bool = ..., use_paddle: bool = ...
) -> Generator[pair, None, None]:
    ...


def lcut(sentence: str, HMM: bool = ..., use_paddle: bool = ...) -> List[pair]:
    ...
