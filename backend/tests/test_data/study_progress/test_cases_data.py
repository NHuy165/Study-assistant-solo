
from backend.src.models_schema.miscellaneous.enums import (
    AggregateTarget,
    CriterionAttribute,
    OperatorType,
    StudyActivityFormat,
    StudyActivityType,
    SubjectType,
)
from backend.src.models_schema.study_progress.criterion import Criterion

# Data (activity format, subject type, is_deleted, is_submitted)
study_activities = [
    (StudyActivityFormat.MULTIPLE_CHOICE_QUESTIONS, SubjectType.MATHS, False, False),
    (StudyActivityFormat.MULTIPLE_CHOICE_QUESTIONS, SubjectType.MATHS, True, False),
    (StudyActivityFormat.MULTIPLE_CHOICE_QUESTIONS, SubjectType.MATHS, False, True),
    (StudyActivityFormat.MULTIPLE_CHOICE_QUESTIONS, SubjectType.MATHS, True, True),
    (StudyActivityFormat.MULTIPLE_CHOICE_QUESTIONS, SubjectType.ENGLISH, True, True),
    (StudyActivityFormat.MULTIPLE_CHOICE_QUESTIONS, SubjectType.VIETNAMESE, False, False),
    
    (StudyActivityFormat.OPEN_ENDED, SubjectType.VIETNAMESE, False, False),
    (StudyActivityFormat.OPEN_ENDED, SubjectType.VIETNAMESE, True, False),
    (StudyActivityFormat.OPEN_ENDED, SubjectType.VIETNAMESE, True, True),
    (StudyActivityFormat.OPEN_ENDED, SubjectType.MATHS, True, True),
    
    (StudyActivityFormat.FLASHCARDS, SubjectType.ENGLISH, True, False),
    (StudyActivityFormat.FLASHCARDS, SubjectType.ENGLISH, False, False),
    (StudyActivityFormat.FLASHCARDS, SubjectType.VIETNAMESE, True, False),
    
    (StudyActivityFormat.GAP_FILL, SubjectType.ENGLISH, True, False),
    (StudyActivityFormat.GAP_FILL, SubjectType.ENGLISH, False, False),
    (StudyActivityFormat.GAP_FILL, SubjectType.MATHS, False, False),
]

# Test case 1: Counting activities by subject.
target_1 = AggregateTarget.COUNT_ACTIVITY
criteria_1 = [
    Criterion(
        attribute=CriterionAttribute.SUBJECT_TYPE,
        value=None,
        operator=OperatorType.GROUP_BY,
    )
]
validation_1 = [
    (
        5,
        SubjectType.MATHS,
    ),
    (
        4,
        SubjectType.VIETNAMESE,
    ),
    (
        5,
        SubjectType.ENGLISH,
    ),
]

# Test case 2: Counting activity items by activity type.
target_2 = AggregateTarget.COUNT_ITEM
criteria_2 = [
    Criterion(
        attribute=CriterionAttribute.ACTIVITY_TYPE,
        value=None,
        operator=OperatorType.GROUP_BY,
    )
]
validation_2 = [
    (
        16,
        StudyActivityType.EXERCISE,
    ),
    (
        12,
        StudyActivityType.REVIEW,
    ),
]

# Test case 3: Counting activities by activity format, with filters.
target_3 = AggregateTarget.COUNT_ACTIVITY
criteria_3 = [
    Criterion(
        attribute=CriterionAttribute.ACTIVITY_FORMAT,
        value=None,
        operator=OperatorType.GROUP_BY,
    ),
    Criterion(
        attribute=CriterionAttribute.SUBJECT_TYPE,
        value=SubjectType.MATHS,
        operator=OperatorType.NE,
    ),
    Criterion(
        attribute=CriterionAttribute.ACTIVITY_FORMAT,
        value=StudyActivityFormat.GAP_FILL,
        operator=OperatorType.NE,
    )
]
validation_3 = [
    (
        2,
        StudyActivityFormat.MULTIPLE_CHOICE_QUESTIONS,
    ),
    (
        2,
        StudyActivityFormat.OPEN_ENDED,
    ),
    (
        3,
        StudyActivityFormat.FLASHCARDS,
    ),
]

# Test case 4: Counting activities by activity type and subject.
target_4 = AggregateTarget.COUNT_ACTIVITY
criteria_4 = [
    Criterion(
        attribute=CriterionAttribute.ACTIVITY_TYPE,
        value=None,
        operator=OperatorType.GROUP_BY,
    ),
    Criterion(
        attribute=CriterionAttribute.SUBJECT_TYPE,
        value=None,
        operator=OperatorType.GROUP_BY,
    ),
]
validation_4 = [
    (
        4,
        StudyActivityType.EXERCISE,
        SubjectType.MATHS,
    ),
    (
        1,
        StudyActivityType.EXERCISE,
        SubjectType.ENGLISH,
    ),
    (
        3,
        StudyActivityType.EXERCISE,
        SubjectType.VIETNAMESE,
    ),
    (
        1,
        StudyActivityType.REVIEW,
        SubjectType.MATHS,
    ),
    (
        4,
        StudyActivityType.REVIEW,
        SubjectType.ENGLISH,
    ),
    (
        1,
        StudyActivityType.REVIEW,
        SubjectType.VIETNAMESE,
    ),
]

# Test case 5: Counting scores by activity format and subject
target_5 = AggregateTarget.SCORE
criteria_5 = [
    Criterion(
        attribute=CriterionAttribute.ACTIVITY_FORMAT,
        value=None,
        operator=OperatorType.GROUP_BY,
    ),
    Criterion(
        attribute=CriterionAttribute.SUBJECT_TYPE,
        value=None,
        operator=OperatorType.GROUP_BY,
    ),
]
validation_5 = [
    (
        100,
        200,
        StudyActivityFormat.MULTIPLE_CHOICE_QUESTIONS,
        SubjectType.MATHS,
    ),
    (
        50,
        100,
        StudyActivityFormat.MULTIPLE_CHOICE_QUESTIONS,
        SubjectType.ENGLISH,
    ),
    (
        50,
        100,
        StudyActivityFormat.OPEN_ENDED,
        SubjectType.MATHS,
    ),
    (
        50,
        100,
        StudyActivityFormat.OPEN_ENDED,
        SubjectType.VIETNAMESE,
    ),
]