from copy import deepcopy
from typing import Sequence, Optional, List

from pyexlatex.logic.format.and_join import join_with_commas_and_and_output_list

RESEARCH_INTERESTS = [
    'FinTech',
    'empirical asset pricing',
    'behavioral finance',
    'monetary policy',
    'empirical corporate finance',
    'market microstructure',
]


def get_research_interests(interests: Optional[List[str]] = None):
    if interests is None:
        interests = deepcopy(RESEARCH_INTERESTS)
    interests[0] = interests[0].capitalize()
    joined = join_with_commas_and_and_output_list(interests)
    return joined
