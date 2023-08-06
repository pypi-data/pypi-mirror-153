from io import BufferedReader, TextIOWrapper
from typing import Dict, Tuple, Type, Union

check_paddle_install: Dict[str, bool]

default_encoding: str

text_type: Type[str]
string_types: Tuple[Type[str]]


def get_module_res(
    *res: str,
) -> BufferedReader:
    ...


def strdecode(sentence: Union[str, bytes]) -> str:
    ...


def resolve_filename(f: Union[str, TextIOWrapper]) -> str:
    ...
