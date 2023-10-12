import enum


class Score(enum.IntEnum):
    Aplus = 6
    A = 5
    Bplus = 4
    B = 3
    Cplus = 2
    C = 1


SCORE_STR_MAP = {
    Score.Aplus: "A+",
    Score.A: "A",
    Score.Bplus: "B+",
    Score.B: "B",
    Score.Cplus: "C+",
    Score.C: "C",
}
STR_SCORE_MAP = {k: v for (v, k) in SCORE_STR_MAP.items()}


def score_from_str(s: str) -> Score:
    # let it throw if score is unrecognized
    return STR_SCORE_MAP.get(s)


def score_to_str(s: Score) -> str:
    return SCORE_STR_MAP.get(s)


class Sex(enum.IntEnum):
    Male = 0
    Female = 1


def to_sex(s: str) -> Sex:
    if s == "男":
        return Sex.Male
    elif s == "女":
        return Sex.Female
    raise RuntimeError(f"could not recognize sex: {s}")


def from_sex(s: Sex) -> str:
    return "男" if s == Sex.Male else "女"


class ExtraType(enum.Enum):
    Medium = 1
    Hard = 0


def to_class_type(s: str) -> ExtraType:
    if s == "精进班":
        return ExtraType.Medium
    elif s == "卓越班":
        return ExtraType.Hard
    raise RuntimeError(f"could not recognize class: {s}")


def from_class_type(s: ExtraType) -> str:
    return "精进班" if s == ExtraType.Medium else "卓越班"
