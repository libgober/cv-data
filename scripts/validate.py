# scripts/validate_cv.py

from pathlib import Path
from typing import Optional, Literal

import yaml
from pydantic import BaseModel, Field, ValidationError


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
    date: Optional[str] = None
    date_start: Optional[str] = None
    date_end: Optional[str] = None
    title: str
    host: str
    role: Optional[str] = None

    def model_post_init(self, __context):
        if self.date is None and (self.date_start is None or self.date_end is None):
            raise ValueError("Talk must have either `date` or both `date_start` and `date_end`.")


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