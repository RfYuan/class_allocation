import csv
import logging
from typing import List

from model.school_class import SchoolClass
from model.student import Student, STUDENT_COL_TITLE
from model.student_attr import score_from_str, to_sex, to_class_type, ExtraType

logger = logging.getLogger(__name__)
INPUT_FILE_PATH = r".\cleaned_input.csv"
OUTPUT_FILE_PATH = r".\output.csv"


def read_from_file() -> List[Student]:
    students = []

    with open(INPUT_FILE_PATH, encoding='utf-8') as csvfile:
        spamreader = csv.reader(csvfile, )
        next(spamreader)
        i = 0
        for row in spamreader:
            i += 1
            try:
                tmp = to_student(row)
                students.append(tmp)
            except RuntimeError as e:
                logger.debug(f"failed to parse row {i}, {row}, with exception {e}")
    return students


def split_student_by_class_type(students: List[Student]):
    hard = []
    medium = []
    for s in students:
        if s.class_type == ExtraType.Hard:
            hard.append(s)
        else:
            medium.append(s)
    return hard, medium


def to_student(row) -> Student:
    return Student(
        name=row[2],
        class_type=to_class_type(row[10]),
        total=score_from_str(row[4]),
        chinese=score_from_str(row[5]),
        math=score_from_str(row[6]),
        english=score_from_str(row[7]),
        sex=to_sex(row[9])
    )


COLS = ["班级"] + STUDENT_COL_TITLE


def write_to_file( allocated_classes: List[SchoolClass], path:str=OUTPUT_FILE_PATH):
    with open(path, "w", newline='', encoding='utf-8-sig') as csvfile:
        writer = csv.writer(csvfile, )
        writer.writerow(COLS)
        i = 0
        for school_class in allocated_classes:
            i += 1
            for student in school_class.students:
                row = student.to_csv()
                row.insert(0, i)
                writer.writerow(row)
