# scripts/validate_cv.py

from pathlib import Path
from typing import Optional, Literal

from datetime import date as Date
import yaml
from pydantic import BaseModel, Field, ValidationError, model_validator


class EducationItem(BaseModel):
    degree: str
    institution: str
    year: int
    field: Optional[str] = None
    honors: Optional[str] = None
    details: Optional[str] = None


class Affiliation(BaseModel):
    title: str
    dept: Optional[str] = None
    unit: Optional[str] = None


class AppointmentItem(BaseModel):
    date_start: int
    date_end: Optional[int] = None
    ongoing: Optional[bool] = False
    institution: str
    affiliations: list[Affiliation]


class TalkItem(BaseModel):
    date: Optional[Date] = None
    date_start: Optional[Date] = None
    date_end: Optional[Date] = None
    title: str
    host: str
    role: Optional[str] = None

    @model_validator(mode="after")
    def check_date_logic(self):
        has_single = self.date is not None
        has_range = self.date_start is not None or self.date_end is not None

        if not has_single and not has_range:
            raise ValueError("Talk must have either `date` or `date_start`/`date_end`.")

        if has_single and has_range:
            raise ValueError("Talk should not have both `date` and `date_start`/`date_end`.")

        if has_range and (self.date_start is None or self.date_end is None):
            raise ValueError("Talk date range must include both `date_start` and `date_end`.")

        if self.date_start and self.date_end and self.date_end < self.date_start:
            raise ValueError("Talk `date_end` cannot be before `date_start`.")

        return self

class FundingItem(BaseModel):
    date_start: str
    date_end: Optional[str] = None
    ongoing: Optional[bool] = False
    organization: str
    name: Optional[str] = None
    award_number: Optional[str] = None
    amount: Optional[int] = None
    currency: Optional[Literal["USD", "EUR"]] = "USD"
    source: Literal["internal", "external"]


class CVData(BaseModel):
    education: list[EducationItem] = Field(default_factory=list)
    appointments: list[AppointmentItem] = Field(default_factory=list)
    invited_talks: list[TalkItem] = Field(default_factory=list)
    funding: list[FundingItem] = Field(default_factory=list)


def main():
    path = Path("cv.yaml")

    with path.open("r", encoding="utf-8") as f:
        data = yaml.safe_load(f)

    try:
        CVData.model_validate(data)
    except ValidationError as e:
        print("CV data validation failed:\n")
        print(e)
        raise SystemExit(1)

    print("CV data validated successfully.")


if __name__ == "__main__":
    main()