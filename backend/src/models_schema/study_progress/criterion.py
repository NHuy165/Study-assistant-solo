from datetime import datetime

from pydantic import BaseModel, model_validator

from backend.src.exceptions.core import (
    ExceptionRequestValidation_400,
)
from backend.src.models_schema.miscellaneous.enums import (
    CriterionAttribute,
    OperatorType,
    SubjectType,
)
from backend.src.services.study_activity import StudyActivityFormat, StudyActivityType


class Criterion(BaseModel):
    attribute: CriterionAttribute
    value: datetime | bool | int | str | None
    operator: OperatorType

    @model_validator(mode="after")
    def validate_subject_type(self):
        if self.attribute == "subject_type" and self.value is not None:
            try:
                SubjectType(self.value)
            except ValueError:
                raise ExceptionRequestValidation_400(
                    custom_message=f"{self.value} is not a valid value for the attribute subject_type."
                )
        return self

    @model_validator(mode="after")
    def validate_activity_type(self):
        if self.attribute == "activity_type" and self.value is not None:
            try:
                StudyActivityType(self.value)
            except ValueError:
                raise ExceptionRequestValidation_400(
                    custom_message=f"{self.value} is not a valid value for the attribute activity_type."
                )
        return self

    @model_validator(mode="after")
    def validate_activity_format(self):
        if self.attribute == "activity_format" and self.value is not None:
            try:
                StudyActivityFormat(self.value)
            except ValueError:
                raise ExceptionRequestValidation_400(
                    custom_message=f"{self.value} is not a valid value for the attribute activity_format."
                )
        return self

    @model_validator(mode="after")
    def validate_datetime(self):
        if (
            self.attribute
            in (CriterionAttribute.CREATED_AT, CriterionAttribute.SUBMITTED_AT)
            and self.value is not None
        ):
            try:
                parsed_date = datetime.strptime(self.value, "%Y-%m-%d")  # type: ignore
                self.value = parsed_date
            except (TypeError, ValueError):
                raise ExceptionRequestValidation_400(
                    custom_message=f"{self.value} is not a valid value for the attribute {self.attribute}."
                )
        return self

    @model_validator(mode="after")
    def validate_bool_type(self):
        if self.attribute == "is_submitted":
            if self.operator not in (
                "NE",
                "EQ",
                "GROUP_BY",
            ):
                raise ExceptionRequestValidation_400(
                    custom_message="The attribute is_submitted can only work with the operators EQ, NE or GROUP_BY."
                )
            if self.value is not None:
                try:
                    self.value = bool(self.value)
                except ValueError:
                    raise ExceptionRequestValidation_400(
                        custom_message=f"{self.value} is not a valid value for the attribute is_submitted (only True, False, or null allowed)."
                    )
        return self

    @model_validator(mode="after")
    def validate_group_by(self):
        if self.operator == "GROUP_BY" and self.value is not None:
            raise ExceptionRequestValidation_400(
                custom_message="GROUP_BY must strictly go with the value null."
            )
        return self

    @model_validator(mode="after")
    def validate_null_value(self):
        if self.value is None and self.operator not in ("NE", "EQ", "GROUP_BY"):
            raise ExceptionRequestValidation_400(
                custom_message="The value null can only work with the operators EQ or NE."
            )
        return self

    @model_validator(mode="after")
    def validate_interaction_id(self):
        if self.attribute == "interaction_id":
            try:
                self.value = int(self.value)  # type: ignore
            except ValueError:
                raise ExceptionRequestValidation_400(
                    custom_message=f"{self.value} is not a valid value for the attribute interaction_id"
                )
        return self
