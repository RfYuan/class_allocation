import logging
from typing import List

import file_reader
from model.school_class import SchoolClass, MeanClass
from service import split_class
from service.split_class import init_class_split, get_medium_class, filter_students_with_missing_score

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG, format='%(message)s')

SEX_TOLERANT = 0.08
CHINESE_TOLERANT = 0.3
ENGLISH_TOLERANT = 0.3


def read_all_students():
    students = file_reader.read_from_file()
    hard, medium = file_reader.split_student_by_class_type(students)
    (hard_score_missing_students, hard) = filter_students_with_missing_score(hard)
    print([s.name for s in hard_score_missing_students])

    hard_class_model = get_medium_class(student_allocations=hard)
    hard_classes = init_class_split(students=hard, number_of_class=9)
    logger.info("starting to averaging out sex")
    _avgeraging_out_sex_with_logging(hard_class_model, hard_classes, tolerant=0.07)
    logger.info("starting to averaging out chinese")
    _avgeraging_out_chinese_with_logging(hard_class_model, hard_classes, tolerant=0.2)
    logger.info("starting to averaging out english")
    _avgeraging_out_english_with_logging(hard_class_model, hard_classes, tolerant=0.2)
    logger.info("卓越班\n"+get_classes_info(hard_classes))

    logger.info("Writting to file")
    file_reader.write_to_file(hard_classes, path="卓越班.csv")



    (medium_score_missing_students, medium) = filter_students_with_missing_score(medium)
    print([s.name for s in medium_score_missing_students])
    if medium:
        medium_class_model = get_medium_class(student_allocations=medium)
        medium_classes = init_class_split(students=medium, number_of_class=4)
        logger.info("starting to averaging out sex")
        _avgeraging_out_sex_with_logging(medium_class_model, medium_classes, tolerant=0.08)
        logger.info("starting to averaging out chinese")
        _avgeraging_out_chinese_with_logging(medium_class_model, medium_classes, tolerant=0.2)
        logger.info("starting to averaging out english")
        _avgeraging_out_english_with_logging(medium_class_model, medium_classes, tolerant=0.2)
        logger.info("精进班\n"+get_classes_info(medium_classes))
        logger.info("Writting to file")
        file_reader.write_to_file(medium_classes, path="精进班.csv")


def get_classes_info(classes: List[SchoolClass])->str:
    return f"平均分最高值:{max(c.avg_score for c in classes)}，平均分最低值{min(c.avg_score for c in classes)} \n " \
           f"女生比例最高值:{max(c.avg_sex for c in classes)}，女生比例最低值{min(c.avg_sex for c in classes)} \n " \
           f"数学平均分最高值:{max(c.avg_math for c in classes)}，数学平均分最低值{min(c.avg_math for c in classes)} \n " \
           f"语文平均分最高值:{max(c.avg_chinese for c in classes)}，语文平均分最低值{min(c.avg_chinese for c in classes)} \n " \
           f"英语平均分最高值:{max(c.avg_english for c in classes)}，英语平均分最低值{min(c.avg_english for c in classes)} \n "


def _avgeraging_out_sex_with_logging(hard_class_model: MeanClass, classes: List[SchoolClass],
                                     tolerant=SEX_TOLERANT):
    logger.info(f"Before the splitting, target sex is {hard_class_model.avg_sex} \n "
                f"Classes sex are {', '.join(str(s.avg_sex) for s in classes)}")
    split_class.averaging_out_sex(school_classes=classes, medium_class=hard_class_model, tolerant=tolerant)
    logger.info(f"After the splitting, target sex is {hard_class_model.avg_sex} \n "
                f"Classes sex are {', '.join(str(s.avg_sex) for s in classes)}")


def _avgeraging_out_chinese_with_logging(hard_class_model: MeanClass, classes: List[SchoolClass],
                                         tolerant=CHINESE_TOLERANT):
    logger.info(f"Before the splitting, target chinese is {hard_class_model.avg_chinese} \n "
                f"Classes chinese are {', '.join(str(s.avg_chinese) for s in classes)}")
    split_class.averaging_out_chinese(school_classes=classes, medium_class=hard_class_model, tolerant=tolerant)
    logger.info(f"After the splitting, target chinese is {hard_class_model.avg_chinese} \n "
                f"Classes chinese are {', '.join(str(s.avg_chinese) for s in classes)}")


def _avgeraging_out_english_with_logging(hard_class_model: MeanClass, classes: List[SchoolClass],
                                         tolerant=ENGLISH_TOLERANT):
    logger.info(f"Before the splitting, target english is {hard_class_model.avg_english} \n "
                f"Classes english are {', '.join(str(s.avg_english) for s in classes)}")
    split_class.averaging_out_english(school_classes=classes, tolerant=tolerant)
    logger.info(f"After the splitting, target english is {hard_class_model.avg_english} \n "
                f"Classes english are {', '.join(str(s.avg_english) for s in classes)}")


if __name__ == "__main__":
    read_all_students()
