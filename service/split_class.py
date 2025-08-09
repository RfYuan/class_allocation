import logging
from collections import defaultdict
from statistics import mean
from typing import List, Tuple

from model.school_class import SchoolClass, MeanClass
from model.student import Student
from model.student_attr import Sex, Score

logger = logging.getLogger(__name__)


def init_class_split(
        students: List[Student],
        number_of_class: int,
) -> List[SchoolClass]:
    result = [SchoolClass() for _ in range(number_of_class)]
    i = 0
    students.sort(key=lambda s: s.total)

    for s in students:
        result[i].students.append(s)
        i += 1
        i %= number_of_class
    return result

def filter_students_with_missing_score(students: List[Student]) -> Tuple[List[Student],List[Student]]:
    # return list(filter(lambda s: s.total != Score.Aplus, students))
    score_missing_students = []
    score_presented_students = []
    for s in students:
        if s.total is not None and s.sex is not None and s.chinese is not None and s.math is not None and s.english is not None:
            score_presented_students.append(s)
        else:
            score_missing_students.append(s)
    return score_missing_students, score_presented_students


def get_medium_class(student_allocations: List[Student]):
    total = [s.total for s in student_allocations]
    score_avg = mean(s.total for s in student_allocations)
    math_avg = mean(s.math for s in student_allocations)
    chinese_avg = mean(s.chinese for s in student_allocations)
    english_avg = mean(s.english for s in student_allocations)
    sex_avg = mean(s.sex for s in student_allocations)

    mean_class = MeanClass()
    mean_class.avg_score = score_avg
    mean_class.avg_math = math_avg
    mean_class.avg_chinese = chinese_avg
    mean_class.avg_english = english_avg
    mean_class.avg_sex = sex_avg
    # setattr(mean_class, "avg_score", score_avg)
    # setattr(mean_class, "avg_math", math_avg)
    # setattr(mean_class, "avg_chinese", chinese_avg)
    # setattr(mean_class, "avg_english", english_avg)
    # setattr(mean_class, "avg_sex", sex_avg)

    return mean_class


def _swap_sex(male_class: SchoolClass, female_class: SchoolClass) -> None:
    # swap one male from male_class with female_class, while keeping the total score the same
    male_dict = get_students_index_group_by_total_score(male_class)
    for score, student_ind in male_dict.items():
        male_dict[score] = list(
            filter(lambda x: male_class.students[x].sex == Sex.Male, student_ind)
        )

    female_dict = get_students_index_group_by_total_score(female_class)
    for score, student_ind in female_dict.items():
        female_dict[score] = list(
            filter(lambda x: female_class.students[x].sex == Sex.Female, student_ind)
        )

    for score in Score:
        a, b = male_dict.get(score, []), female_dict.get(score, [])
        if a and b:
            _swap_student_of_sex(a[0], b[0], female_class, male_class)
            return

    logger.warning(f"have to change the total score of classes {male_class}, {female_class} ")
    for score in Score:
        if score - 1 not in Score:
            continue
        a, b = male_dict.get(score, []), female_dict.get(score - 1, [])
        if a and b:
            _swap_student_of_sex(a[0], b[0], female_class, male_class)
            return
        a, b = male_dict.get(score - 1, []), female_dict.get(score, [])
        if a and b:
            _swap_student_of_sex(a[0], b[0], female_class, male_class)
            return
    raise RuntimeError(f"Could not average out the sex of class {male_class}, class {female_class}")


def _swap_chinese(bad_class: SchoolClass, good_class: SchoolClass) -> bool:
    # swap one male from male_class with female_class, while keeping the total score the same
    bad_dict = get_students_index_and_obj_group_by_total_score(bad_class)
    good_dict = get_students_index_and_obj_group_by_total_score(good_class)
    for score in Score:
        bad_students = bad_dict.get(score, [])
        good_students = good_dict.get(score, [])

        bad_students.sort(key=lambda s: s[1].chinese)
        for bad_student_ind, bad_student in bad_students:
            for good_student_ind, good_student in good_students:

                if bad_student.chinese < good_student.chinese and good_student.sex == bad_student.sex:
                    logger.debug(
                        f"Swapping because chinese, student {bad_student.name} and student {good_student.name}")

                    swap_student(bad_class, good_class, bad_student_ind, good_student_ind)
                    return True
    return False


def _swap_english(bad_class: SchoolClass, good_class: SchoolClass) -> bool:
    # swap one male from male_class with female_class, while keeping the total score the same
    bad_dict = get_students_index_and_obj_group_by_total_score(bad_class)
    good_dict = get_students_index_and_obj_group_by_total_score(good_class)
    for score in Score:
        bad_students = bad_dict.get(score, [])
        good_students = good_dict.get(score, [])

        bad_students.sort(key=lambda s: s[1].english)
        for bad_student_ind, bad_student in bad_students:
            for good_student_ind, good_student in good_students:

                if bad_student.english < good_student.english and good_student.sex == bad_student.sex and abs(
                        good_student.chinese - bad_student.chinese) <1:
                    logger.debug(
                        f"Swapping because english, student {bad_student.name} and student {good_student.name}")

                    swap_student(bad_class, good_class, bad_student_ind, good_student_ind)
                    return True
    return False


def _swap_student_of_sex(a, b, female_class, male_class):
    logger.debug(
        f"Swapping because sex, student {male_class.students[a].name} and student {female_class.students[b].name}")
    swap_student(male_class, female_class, i=a, j=b)
    order_student_by_total_score(male_class)
    order_student_by_total_score(female_class)


def swap_student(a: SchoolClass, b: SchoolClass, i: int, j: int) -> None:
    t1, t2 = a.students.pop(i), b.students.pop(j)
    a.students.append(t2)
    b.students.append(t1)


def order_student_by_total_score(a: SchoolClass):
    a.students.sort(key=lambda x: x.total)


def get_students_index_group_by_total_score(c: SchoolClass) -> dict:
    result = defaultdict(list)
    for i in range(c.student_count):
        student = c.students[i]
        result[student.total].append(i)
    return result


def get_students_index_and_obj_group_by_total_score(c: SchoolClass) -> dict:
    result = defaultdict(list)
    for i in range(c.student_count):
        student = c.students[i]
        result[student.total].append((i, c.students[i]))
    return result


def averaging_out_sex(school_classes: List[SchoolClass], medium_class, tolerant):
    # moving sex rate to avg while keeping the total score the same
    school_classes.sort(key=lambda x: x.avg_sex)
    n = len(school_classes)
    while abs(school_classes[0].avg_sex - school_classes[n - 1].avg_sex) > tolerant:
        _swap_sex(male_class=school_classes[0], female_class=school_classes[n - 1])
        school_classes.sort(key=lambda x: x.avg_sex - medium_class.avg_sex)


def averaging_out_chinese(school_classes: List[SchoolClass], medium_class, tolerant: float):
    # moving sex rate to avg while keeping the total score the same
    school_classes.sort(key=lambda x: x.avg_chinese)
    n = len(school_classes)
    while abs(school_classes[0].avg_chinese - school_classes[n - 1].avg_chinese) > tolerant:
        result = _swap_chinese(bad_class=school_classes[0], good_class=school_classes[n - 1])
        if not result:
            raise RuntimeError(f"Could not average out the chinese of class {school_classes[0]}, "
                               f"class {school_classes[n - 1]}")
        school_classes.sort(key=lambda x: x.avg_chinese - medium_class.avg_chinese)


def averaging_out_english(school_classes: List[SchoolClass], tolerant: float):
    # moving sex rate to avg while keeping the total score the same
    school_classes.sort(key=lambda x: x.avg_english)
    n = len(school_classes)
    while abs(school_classes[0].avg_english - school_classes[n - 1].avg_english) > tolerant:
        result = _swap_english(bad_class=school_classes[0], good_class=school_classes[n - 1])
        if not result:
            raise RuntimeError(f"Could not average out the english of class {school_classes[0]}, "
                               f"class {school_classes[n - 1]}")
        school_classes.sort(key=lambda x: x.avg_english)
