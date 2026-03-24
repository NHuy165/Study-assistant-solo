from fastapi import APIRouter, status

from backend.src.core.database import SessionDep
from backend.src.core.dependencies import UserDep
from backend.src.exceptions.core import Responses
from backend.src.models_schema.interaction import (
    InteractionInput,
    InteractionOutput,
    InteractionUpdate,
)
from backend.src.services import interaction

router = APIRouter()

# ----- CREATE ----- #


@router.post(
    "/create",
    response_model=InteractionOutput,
    responses={
        401: Responses.RESPONSE_401_UNAUTHORIZED,
    },
)
async def create_interaction(
    user: UserDep, session: SessionDep, interaction_input: InteractionInput
):
    interaction_output = await interaction.create_interaction(
        user, session, interaction_input
    )
    return interaction_output


# ----- READ ----- #


@router.get(
    "/",
    response_model=list[InteractionOutput],
    responses={401: Responses.RESPONSE_401_UNAUTHORIZED},
)
async def read_all_interactions(user: UserDep, session: SessionDep):
    interaction_output = await interaction.read_all_interactions(user, session)
    return interaction_output


# ----- UPDATE ----- #


@router.patch(
    "/{interaction_id}",
    response_model=InteractionOutput,
    responses={
        401: Responses.RESPONSE_401_UNAUTHORIZED,
        404: Responses.RESPONSE_404_NOT_FOUND,
    },
)
async def update_interaction(
    user: UserDep,
    session: SessionDep,
    interaction_id: int,
    interaction_update: InteractionUpdate,
):
    interaction_output = await interaction.update_interaction(
        user, session, interaction_id, interaction_update
    )
    return interaction_output


# ----- DELETE ----- #


@router.delete(
    "/{interaction_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={
        401: Responses.RESPONSE_401_UNAUTHORIZED,
        404: Responses.RESPONSE_404_NOT_FOUND,
    },
)
async def delete_interaction(user: UserDep, session: SessionDep, interaction_id: int):
    await interaction.delete_interaction(user, session, interaction_id)
