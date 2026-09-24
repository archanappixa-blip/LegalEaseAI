from pydantic import BaseModel, Field, field_validator


class DocumentRequest(BaseModel):

    document_type: str = Field(
        ...,
        min_length=2,
        max_length=120
    )

    parties: str = Field(
        ...,
        min_length=2,
        max_length=4000
    )

    terms: str = Field(
        ...,
        min_length=2,
        max_length=12000
    )

    effective_date: str = Field(
        ...,
        min_length=2,
        max_length=100
    )

    @field_validator(
        "document_type",
        "parties",
        "terms",
        "effective_date"
    )
    @classmethod
    def validate_text(cls, value: str) -> str:

        value = value.strip()

        if not value:
            raise ValueError(
                "This field cannot be empty."
            )

        return value


class ExportRequest(BaseModel):

    text: str = Field(
        ...,
        min_length=1,
        max_length=100000
    )

    document_type: str = Field(
        default="Legal Document",
        max_length=120
    )

    terms: str = Field(
        default="",
        max_length=12000
    )

    brand_name: str = Field(
        default="LegalEase",
        max_length=100
    )