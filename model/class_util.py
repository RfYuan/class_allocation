from typing import List

from model.school_class import SchoolClass


def get_all_classes_info(school_classes: List[SchoolClass])->str:
    return "\n\n".join(s.get_info() for s in school_classes)