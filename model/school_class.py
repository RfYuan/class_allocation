from __future__ import annotations

from typing import List

from model.student import Student


class SchoolClass:
    students: List[Student]

    def __init__(self, students=None):
        if students:
            self.students = students
        else:
            self.students = []

    @property
    def student_count(self):
        return len(self.students)

    def _total_score(self):
        return sum(s.total for s in self.students)

    @property
    def avg_score(self):
        return self._total_score() / self.student_count

    def _total_math(self):
        return sum(s.math for s in self.students)

    @property
    def avg_math(self):
        return self._total_math() / self.student_count

    def _total_chinese(self):
        return sum(s.chinese for s in self.students)

    @property
    def avg_chinese(self):
        return self._total_chinese() / self.student_count

    def _total_english(self):
        return sum(s.english for s in self.students)

    @property
    def avg_english(self):
        return self._total_english() / self.student_count

    def _total_sex(self):
        return sum(s.sex for s in self.students)

    @property
    def avg_sex(self):
        return self._total_sex() / self.student_count

    def get_score(self, mid: MeanClass):
        return abs(mid.avg_score - self.avg_score) + abs(mid.avg_chinese - self.avg_chinese) + \
               abs(mid.avg_english - self.avg_english) + abs(mid.avg_math - self.avg_math) + \
               abs(mid.avg_sex - self.avg_sex)

    def get_info(self):
        return f"Class Info: \n avgerage score {self.avg_score} \n average sex {self.avg_sex} \n " \
               f" average math {self.avg_math} \n average chinese {self.avg_chinese} \n average english {self.avg_english} "


class MeanClass:
    avg_score: float
    avg_math: float
    avg_chinese: float
    avg_english: float
    avg_sex: float
    pass