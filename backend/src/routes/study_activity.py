from fastapi import APIRouter

from backend.src.core.dependencies import InteractionDep, SessionDep, UserDep
from backend.src.exceptions.core import Responses
from backend.src.models_schema.activity.exercise_item import (
    ExerciseItemOutput,
    ExerciseItemUpdate,
)
from backend.src.models_schema.activity.exercise_item_content import (
    ExerciseItemContentBase,
)
from backend.src.models_schema.activity.study_activity import (
    StudyActivityInput,
    StudyActivityOutput,
    StudyActivityOutputComplete,
    StudyActivityUpdate,
)
from backend.src.services import study_activity

router = APIRouter()

# ----- CREATE ----- #


@router.post(
    "/{interaction_id}/create",
    response_model=StudyActivityOutputComplete,
    responses={
        401: Responses.RESPONSE_401_UNAUTHORIZED,
        404: Responses.RESPONSE_404_NOT_FOUND,
    },
)
async def create_study_activity(
    user: UserDep,
    session: SessionDep,
    interaction: InteractionDep,
    study_activity_input: StudyActivityInput,
):
    """
    Tạo một dạng tài liệu tùy vào các yêu cầu trong request.
    """
    return await study_activity.create_study_activity(
        session,
        interaction,
        study_activity_input,
    )


# ----- READ ----- #


@router.get(
    "/{interaction_id}/",
    response_model=list[StudyActivityOutput],
    responses={
        401: Responses.RESPONSE_401_UNAUTHORIZED,
        404: Responses.RESPONSE_404_NOT_FOUND,
    },
)
async def read_all_study_activity(
    user: UserDep,
    session: SessionDep,
    interaction: InteractionDep,
):
    """
    Đọc thông tin khái quát của tất cả dạng tài liệu đã tạo trong Interaction.
    """
    return await study_activity.read_all_study_activity(
        session,
        interaction,
    )


@router.get(
    "/{study_activity_id}",
    response_model=StudyActivityOutputComplete,
    responses={
        401: Responses.RESPONSE_401_UNAUTHORIZED,
        404: Responses.RESPONSE_404_NOT_FOUND,
    },
)
async def read_study_activity_complete(
    user: UserDep,
    session: SessionDep,
    study_activity_id: int,
):
    """
    Đọc thông tin chi tiết của một tài liệu.
    """
    return await study_activity.read_study_activity_complete(
        user,
        session,
        study_activity_id,
    )


# ----- UPDATE ----- #


@router.patch("/{study_activity_id}", response_model=StudyActivityOutput)
async def update_study_activity(
    user: UserDep,
    session: SessionDep,
    study_activity_id: int,
    study_activity_update: StudyActivityUpdate,
):
    """
    Cập nhật thông tin khái quát của một tài liệu (tên và mô tả).
    """
    return await study_activity.update_study_activity(
        user,
        session,
        study_activity_id,
        study_activity_update,
    )


@router.patch("/{exercise_item_id}", response_model=ExerciseItemOutput)
async def answer_exercise_item(
    user: UserDep,
    session: SessionDep,
    exercise_item_id: int,
    exercise_item_update: ExerciseItemUpdate,
):
    """
    Trả lời MỘT câu hỏi trong một tài liệu dạng Exercise.
    """
    return await study_activity.answer_exercise_item(
        user,
        session,
        exercise_item_id,
        exercise_item_update,
    )


@router.patch("/{study_activity_id}", response_model=ExerciseItemOutput)
async def submit_exercise_activity(
    user: UserDep,
    session: SessionDep,
    study_activity_id: int,
):
    """
    Nộp tài liệu dạng Exercise.
    """
    return await study_activity.submit_exercise_activity(
        user,
        session,
        study_activity_id,
    )


# ----- DELETE ----- #


@router.delete(
    "/{study_activity_id}",
    status_code=204,
    responses={
        401: Responses.RESPONSE_401_UNAUTHORIZED,
        404: Responses.RESPONSE_404_NOT_FOUND,
    },
)
async def delete_study_activity(
    user: UserDep,
    session: SessionDep,
    study_activity_id: int,
):
    """
    Xóa một tài liệu.
    """
    return await study_activity.delete_study_activity(
        user,
        session,
        study_activity_id,
    )
