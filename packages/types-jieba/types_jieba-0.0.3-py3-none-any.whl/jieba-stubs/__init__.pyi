from io import TextIOWrapper
from multiprocessing.pool import Pool
from typing import Dict, List, Optional, Tuple, Union, Generator
from re import Pattern
from threading import RLock

__version__: str
__license__: str


def _get_abs_path(path: str) -> str:
    ...


DEFAULT_DICT: Optional[str]
DEFAULT_DICT_NAME: str

DICT_WRITING: dict

pool: Optional[Pool]

re_userdict: Pattern[str]
re_eng: Pattern[str]
re_han_default: Pattern[str]
re_skip_default: Pattern[str]


DAGType = Dict[int, List[int]]
DictFileType = Union[str, TextIOWrapper]


def setLogLevel(log_level: int) -> None:
    ...


class Tokenizer(object):
    lock: RLock
    dictionary: str
    FREQ: Dict[str, int]
    user_word_tag_tab: Dict[str, str]
    total: int
    initialized: bool
    tmp_dir: Optional[str]
    cache_file: Optional[str]

    @staticmethod
    def gen_pfdict(f: DictFileType) -> Tuple[Dict[str, int], int]:
        ...

    def initialize(self, dictionary: Optional[str] = ...) -> None:
        ...

    def check_initialized(self) -> None:
        ...

    def calc(
        self,
        sentence: str,
        DAG: DAGType,
        route: Dict[int, Tuple[int, int]],
    ):
        ...

    def get_DAG(self, sentence: str) -> DAGType:
        ...

    def cut(
        self,
        sentence: str,
        cut_all: bool = ...,
        HMM: bool = ...,
        use_paddle: bool = ...,
    ) -> Generator[str, None, None]:
        ...

    def cut_for_search(
        self, sentence: str, HMM: bool = ...
    ) -> Generator[str, None, None]:
        ...

    def lcut(
        self,
        sentence: str,
        cut_all: bool = False,
        HMM: bool = True,
        use_paddle: bool = False,
    ) -> List[str]:
        ...

    def lcut_for_search(self, sentence: str, HMM: bool = ...) -> List[str]:
        ...

    def get_dict_file(self) -> TextIOWrapper:
        ...

    def load_userdict(self, f: DictFileType) -> None:
        ...

    def add_word(
        self, word: str, freq: Optional[int] = ..., tag: Optional[str] = ...
    ) -> None:
        ...

    def del_word(self, word: str) -> None:
        ...

    def suggest_freq(self, segment: Union[str, bytes], tune: bool = ...) -> int:
        ...

    def tokenize(
        self, unicode_sentence: str, mode: str = ..., HMM: bool = ...
    ) -> Generator[Tuple[str, int, int], None, None]:
        ...

    def set_dictionary(self, dictionary_path: str) -> None:
        ...


dt: Tokenizer

cut = dt.cut
add_word = dt.add_word
calc = dt.calc
cut = dt.cut
lcut = dt.lcut
cut_for_search = dt.cut_for_search
lcut_for_search = dt.lcut_for_search
del_word = dt.del_word
get_DAG = dt.get_DAG
get_dict_file = dt.get_dict_file
initialize = dt.initialize
load_userdict = dt.load_userdict
set_dictionary = dt.set_dictionary
suggest_freq = dt.suggest_freq
tokenize = dt.tokenize
user_word_tag_tab = dt.user_word_tag_tab


def get_FREQ(k: str, d: int) -> int:
    ...


def enable_parallel(processnum: Optional[int] = ...) -> None:
    """开启多进程。默认使用 cpu 数量，也可以指定数量"""
    ...


def disable_parallel() -> None:
    """关闭多进程"""
    ...
