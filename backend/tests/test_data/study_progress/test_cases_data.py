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
    (StudyActivityFormat.MULTIPLE_CHOICE_QUESTIONS, SubjectType.LITERATURE, True, True),
    (
        StudyActivityFormat.MULTIPLE_CHOICE_QUESTIONS,
        SubjectType.LANGUAGES,
        False,
        False,
    ),
    (StudyActivityFormat.OPEN_ENDED, SubjectType.LANGUAGES, False, False),
    (StudyActivityFormat.OPEN_ENDED, SubjectType.LANGUAGES, True, False),
    (StudyActivityFormat.OPEN_ENDED, SubjectType.LANGUAGES, True, True),
    (StudyActivityFormat.OPEN_ENDED, SubjectType.MATHS, True, True),
    (StudyActivityFormat.FLASHCARDS, SubjectType.LITERATURE, True, False),
    (StudyActivityFormat.FLASHCARDS, SubjectType.LITERATURE, False, False),
    (StudyActivityFormat.FLASHCARDS, SubjectType.LANGUAGES, True, False),
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
        4,
        SubjectType.MATHS,
    ),
    (
        4,
        SubjectType.LANGUAGES,
    ),
    (
        3,
        SubjectType.LITERATURE,
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
        6,
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
        value=StudyActivityFormat.FLASHCARDS,
        operator=OperatorType.NE,
    ),
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
        SubjectType.LITERATURE,
    ),
    (
        3,
        StudyActivityType.EXERCISE,
        SubjectType.LANGUAGES,
    ),
    (
        2,
        StudyActivityType.REVIEW,
        SubjectType.LITERATURE,
    ),
    (
        1,
        StudyActivityType.REVIEW,
        SubjectType.LANGUAGES,
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
        SubjectType.LITERATURE,
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
        SubjectType.LANGUAGES,
    ),
]
