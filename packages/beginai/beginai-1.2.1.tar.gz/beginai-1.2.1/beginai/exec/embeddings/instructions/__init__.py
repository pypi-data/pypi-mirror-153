from .category import instructions_map as category_instructions_map
from .boolean import instructions_map as boolean_instructions_map
from .location import instructions_map as location_instructions_map
from .number import instructions_map as number_instructions_map
from .text import instructions_map as text_instructions_map
from .date import instructions_map as date_instructions_map
from .interaction import instructions_map as interaction_instructions_map

instructions_map = {}

for dict in [category_instructions_map, boolean_instructions_map, location_instructions_map,
    number_instructions_map, text_instructions_map, date_instructions_map, interaction_instructions_map]:

    instructions_map.update(dict)
