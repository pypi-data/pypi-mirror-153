from dataclasses import dataclass
from enum import Enum
from typing import Optional, Sequence

from derobertis_cv.pltemplates.logo import HasLogo


class OrganizationCharacteristics(str, Enum):
    WARM_WEATHER = 'warm_weather'
    SMALL_TOWN = 'small_town'
    MID_SIZE_CITY = 'mid_size_city'
    LARGE_CITY = 'large_city'
    INTERNATIONAL = 'international'
    WEST_COAST = 'west coast'
    FAMILY_CLOSE = 'family close'
    REMOTE = 'remote'
    MULTIPLE_LOCATIONS = 'multiple locations'
    SPANISH_SPEAKING = 'spanish speaking'
    FRENCH_SPEAKING = 'french speaking'
    NOVA = 'northern virginia'
    SUBURBAN = 'suburban'


@dataclass
class Organization(HasLogo):
    title: str
    location: str
    abbreviation: Optional[str] = None
    logo_url: Optional[str] = None
    logo_svg_text: Optional[str] = None
    logo_base64: Optional[str] = None
    logo_fa_icon_class_str: Optional[str] = None
    address_lines: Optional[Sequence[str]] = None
    city: Optional[str] = None
    country: Optional[str] = None
    characteristics: Sequence[OrganizationCharacteristics] = tuple()

    def __post_init__(self):
        if self.abbreviation is None:
            self.abbreviation = self.title