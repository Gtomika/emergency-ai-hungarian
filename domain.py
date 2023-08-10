import enum
from typing import Union

import json

class EmergencyType(enum.Enum):
    NOT_EMERGENCY = 1
    POLICE = 2
    AMBULANCE = 3
    FIRE_DEPARTMENT = 4
    OTHER = 5
    UNCERTAIN = 6

def emergency_type_to_hungarian(etype: EmergencyType) -> str:
    if etype == EmergencyType.NOT_EMERGENCY:
        return "Nem vészhelyzet"
    elif etype == EmergencyType.POLICE:
        return "Rendőrség"
    elif etype == EmergencyType.FIRE_DEPARTMENT:
        return "Tűzoltóság"
    elif etype == EmergencyType.AMBULANCE:
        return "Mentők"
    elif etype == EmergencyType.OTHER:
        return "Egyéb vészhelyzeti egységek"
    else:
        return "Bizonytalan, továbbítás emberi operátornak"

class EmergencyResponse:

    def __init__(self, emergency_type: EmergencyType, location: Union[str, None], message: str):
        self.emergency_type = emergency_type
        self.message = message
        self.location = location

    def to_detailed_string_hungarian(self) -> str:
        return f'''Hívás típusa: {emergency_type_to_hungarian(self.emergency_type)}.
        Esemény helye: {self.location if self.location is not None else "nem azonosítható"}.
        {self.message}'''


def parse_emergency_response(response_json: str) -> Union[EmergencyResponse, None]:
    try:
        response_dict = json.loads(response_json)
        return EmergencyResponse(
            getattr(EmergencyType, response_dict['type']),
            response_dict['location'] if 'location' in response_dict else None,
            response_dict['message']
        )
    except Exception as e:
        print('The model returned invalid output! Model response follows:')
        print(response_json)
        print(e)
        return None