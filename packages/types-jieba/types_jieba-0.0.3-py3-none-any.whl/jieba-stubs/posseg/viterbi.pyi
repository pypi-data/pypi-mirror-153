from typing import List, Tuple
from . import StatesType, StartType, TransType, EmitType

MIN_FLOAT: float
MIN_INF: float


def viterbi(
    obs: str,
    states: StatesType,
    start_p: StartType,
    trans_p: TransType,
    emit_p: EmitType,
) -> Tuple[str, List[Tuple[str, str]]]:
    ...
