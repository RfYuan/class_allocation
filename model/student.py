from dataclasses import dataclass

from model.student_attr import score_to_str, from_class_type, from_sex, Sex, ExtraType, Score


@dataclass()
class Student:
    name: str
    class_type: ExtraType
    total: Score
    chinese: Score
    english: Score
    math: Score
    sex: Sex

    def to_csv(self):
        return [self.name,
                from_sex(self.sex),
                from_class_type(self.class_type),
                score_to_str(self.total),
                score_to_str(self.chinese),
                score_to_str(self.english),
                score_to_str(self.math)
                ]


STUDENT_COL_TITLE = ["姓名", "性别", "课程", "总分", "语文", "英语", "数学"]
