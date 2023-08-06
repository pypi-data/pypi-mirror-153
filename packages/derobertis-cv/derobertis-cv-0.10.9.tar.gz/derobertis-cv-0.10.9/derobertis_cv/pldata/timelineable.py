import datetime
from typing import Optional


class Timelineable:
    begin_date: datetime.date
    end_date: Optional[datetime.date] = None
    date_format: str = "%B %Y"

    @property
    def begin_date_str(self) -> str:
        return self.begin_date.strftime(self.date_format)

    @property
    def end_date_str(self) -> str:
        if self.end_date is None:
            return "Present"
        return self.end_date.strftime(self.date_format)

    @property
    def date_str(self) -> str:
        return f"{self.begin_date_str} - {self.end_date_str}"
